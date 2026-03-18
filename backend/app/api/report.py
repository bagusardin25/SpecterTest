"""Report API Blueprint — fetch generated reports and findings."""
from flask import Blueprint, jsonify

from app.extensions import db
from app.models.scan import Scan

report_bp = Blueprint("report", __name__)


@report_bp.route("/report/<scan_id>")
def get_report(scan_id):
    """Get the full report for a completed scan."""
    scan = db.session.get(Scan, scan_id)
    if not scan:
        return jsonify({"error": "Scan not found"}), 404

    return jsonify({
        "scan_id": scan_id,
        "status": scan.status,
        "target_url": scan.target_url,
        "duration_seconds": scan.duration_seconds,
        "report_markdown": scan.report_markdown,
        "summary": {
            "logic_flaws": sum(1 for f in scan.findings if f.category == "logic_flaw"),
            "security_issues": sum(1 for f in scan.findings if f.category == "security_issue"),
            "performance_issues": sum(1 for f in scan.findings if f.category == "performance_issue"),
            "total": len(scan.findings),
        },
        "agents": [a.to_dict() for a in scan.agents],
    })


@report_bp.route("/report/<scan_id>/findings")
def get_findings(scan_id):
    """Get all findings for a scan."""
    scan = db.session.get(Scan, scan_id)
    if not scan:
        return jsonify({"error": "Scan not found"}), 404

    return jsonify({
        "scan_id": scan_id,
        "findings": [f.to_dict() for f in scan.findings],
    })