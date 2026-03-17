"""Scan API Blueprint — handles target binding and scan orchestration."""
import uuid
import threading
from datetime import datetime, timezone

from flask import Blueprint, request, jsonify

from app.extensions import db
from app.models.scan import Scan
from app.models.route import DiscoveredRoute
from app.models.finding import Finding
from app.services.crawler import run_crawler
from app.services.agent_manager import spawn_agents
from app.services.swarm_engine import run_simulation
from app.services.llm_client import generate_report
from app.services.sse_manager import sse_manager

scan_bp = Blueprint("scan", __name__)


def _run_scan_pipeline(app, scan_id: str, target_url: str, user_count: int, admin_count: int, attacker_count: int):
    """
    Background thread: runs the full scan pipeline
    (crawl → spawn → simulate → report).
    """
    import time
    start_time = time.time()

    with app.app_context():
        scan = db.session.get(Scan, scan_id)
        if not scan:
            return

        try:
            # ─── Phase 1: Binding (Crawl) ───
            scan.status = "binding"
            db.session.commit()

            routes_data = run_crawler(target_url, scan_id)

            # Save routes to DB
            for r in routes_data:
                route = DiscoveredRoute(
                    scan_id=scan_id,
                    path=r["path"],
                    method=r.get("method", "GET"),
                    has_form=r.get("has_form", False),
                    has_auth=r.get("has_auth", False),
                    page_title=r.get("page_title"),
                )
                db.session.add(route)
            db.session.commit()

            # ─── Phase 2: Spawning ───
            scan.status = "spawning"
            db.session.commit()

            agents = spawn_agents(scan_id, user_count, admin_count, attacker_count)
            agents_data = [a.to_dict() for a in agents]

            # ─── Phase 3: Execution ───
            scan.status = "executing"
            db.session.commit()

            findings_data = run_simulation(target_url, scan_id, agents_data, routes_data)

            # Save findings to DB
            for f in findings_data:
                finding = Finding(
                    scan_id=scan_id,
                    agent_id=f["agent_id"],
                    category=f.get("category", "logic_flaw"),
                    severity=f.get("severity", "medium"),
                    title=f.get("title", "Untitled"),
                    description=f.get("description"),
                    evidence=f.get("evidence"),
                )
                db.session.add(finding)
            db.session.commit()

            # Update agent status
            for agent in agents:
                agent.status = "completed"
                agent.current_action = "Simulation finished"
            db.session.commit()

            # ─── Phase 4: Report ───
            scan.status = "reporting"
            db.session.commit()

            elapsed = int(time.time() - start_time)
            report_md = generate_report(
                scan_id=scan_id,
                target_url=target_url,
                findings=findings_data,
                agents_summary=agents_data,
                duration_seconds=elapsed,
            )

            scan.report_markdown = report_md
            scan.status = "completed"
            scan.completed_at = datetime.now(timezone.utc).isoformat()
            scan.duration_seconds = elapsed
            db.session.commit()

        except Exception as e:
            scan.status = "error"
            db.session.commit()
            sse_manager.publish(scan_id, "scan_error", {"error": str(e)[:500]})


@scan_bp.route("/scan", methods=["POST"])
def create_scan():
    """Start a new scan — triggers the full pipeline in a background thread."""
    data = request.get_json()

    if not data or not data.get("target_url"):
        return jsonify({"error": "target_url is required"}), 400

    scan_id = str(uuid.uuid4())[:8]
    target_url = data["target_url"]
    user_count = int(data.get("user_agents", 5))
    admin_count = int(data.get("admin_agents", 2))
    attacker_count = int(data.get("attacker_agents", 3))

    # Create scan record
    scan = Scan(
        id=scan_id,
        target_url=target_url,
        user_agents=user_count,
        admin_agents=admin_count,
        attacker_agents=attacker_count,
    )
    db.session.add(scan)
    db.session.commit()

    # Run pipeline in background thread
    from flask import current_app
    app = current_app._get_current_object()
    thread = threading.Thread(
        target=_run_scan_pipeline,
        args=(app, scan_id, target_url, user_count, admin_count, attacker_count),
        daemon=True,
    )
    thread.start()

    return jsonify({"scan_id": scan_id, "status": "binding"}), 201


@scan_bp.route("/scan/<scan_id>", methods=["GET"])
def get_scan(scan_id):
    """Get scan details including discovered routes."""
    scan = db.session.get(Scan, scan_id)
    if not scan:
        return jsonify({"error": "Scan not found"}), 404

    return jsonify({
        **scan.to_dict(),
        "routes": [r.to_dict() for r in scan.routes],
        "agents_count": len(scan.agents),
        "findings_count": len(scan.findings),
    })


@scan_bp.route("/scan/<scan_id>", methods=["DELETE"])
def abort_scan(scan_id):
    """Abort a running scan."""
    scan = db.session.get(Scan, scan_id)
    if not scan:
        return jsonify({"error": "Scan not found"}), 404

    scan.status = "aborted"
    db.session.commit()

    sse_manager.publish(scan_id, "scan_aborted", {"scan_id": scan_id})
    return jsonify({"status": "aborted"})
