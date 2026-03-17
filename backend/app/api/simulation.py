"""Simulation API Blueprint — SSE streaming and agent status."""
from flask import Blueprint, Response, jsonify

from app.extensions import db
from app.models.scan import Scan
from app.services.sse_manager import sse_manager

simulation_bp = Blueprint("simulation", __name__)


@simulation_bp.route("/simulation/<scan_id>/stream")
def simulation_stream(scan_id):
    """SSE endpoint — streams real-time events for a scan."""
    scan = db.session.get(Scan, scan_id)
    if not scan:
        return jsonify({"error": "Scan not found"}), 404

    return Response(
        sse_manager.stream(scan_id),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@simulation_bp.route("/simulation/<scan_id>/agents")
def simulation_agents(scan_id):
    """Get current status of all agents in a scan."""
    scan = db.session.get(Scan, scan_id)
    if not scan:
        return jsonify({"error": "Scan not found"}), 404

    return jsonify({
        "scan_id": scan_id,
        "agents": [a.to_dict() for a in scan.agents],
    })


@simulation_bp.route("/simulation/<scan_id>/metrics")
def simulation_metrics(scan_id):
    """Get aggregated metrics for a running simulation."""
    scan = db.session.get(Scan, scan_id)
    if not scan:
        return jsonify({"error": "Scan not found"}), 404

    findings = scan.findings
    logic_flaws = sum(1 for f in findings if f.category == "logic_flaw")
    security_issues = sum(1 for f in findings if f.category == "security_issue")
    perf_issues = sum(1 for f in findings if f.category == "performance_issue")

    return jsonify({
        "scan_id": scan_id,
        "status": scan.status,
        "total_agents": len(scan.agents),
        "total_routes": len(scan.routes),
        "findings": {
            "logic_flaws": logic_flaws,
            "security_issues": security_issues,
            "performance_issues": perf_issues,
            "total": len(findings),
        },
    })
