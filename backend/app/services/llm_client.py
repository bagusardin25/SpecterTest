"""LLM Client — OpenAI API integration for report generation."""
import os

from openai import OpenAI

from app.services.sse_manager import sse_manager


def get_client() -> OpenAI:
    """Create OpenAI client from environment config."""
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))


def generate_report(
    scan_id: str,
    target_url: str,
    findings: list[dict],
    agents_summary: list[dict],
    duration_seconds: int,
) -> str:
    """
    Use OpenAI API to generate a narrative security report
    based on findings from the swarm simulation.
    Returns Markdown string.
    """
    sse_manager.publish(scan_id, "report_generating", {"status": "analyzing_findings"})

    # Build structured prompt
    findings_text = ""
    for i, f in enumerate(findings, 1):
        findings_text += f"""
### Finding #{i}
- **Agent**: {f.get('agent_id', 'unknown')}
- **Category**: {f.get('category', 'unknown')}
- **Severity**: {f.get('severity', 'unknown')}
- **Title**: {f.get('title', 'Untitled')}
- **Description**: {f.get('description', '')}
- **Evidence**: {f.get('evidence', '')}
"""

    agents_text = ""
    for a in agents_summary:
        agents_text += f"- {a['id']} ({a['role']}): {a.get('status', 'completed')}\n"

    prompt = f"""You are a senior cybersecurity analyst. Generate a comprehensive security assessment report based on the following swarm intelligence scan results.

## Scan Information
- **Target**: {target_url}
- **Duration**: {duration_seconds} seconds
- **Total Agents**: {len(agents_summary)}
- **Total Findings**: {len(findings)}

## Agent Summary
{agents_text}

## Raw Findings
{findings_text}

---

Generate a professional Markdown report with these sections:

1. **Executive Summary** — High-level overview of the security posture. Mention the most critical issues.

2. **Critical Findings** — Detail each finding with:
   - Clear title and severity badge
   - What was found and how
   - Evidence (HTTP requests/response snippets)
   - Impact assessment
   - Remediation recommendations

3. **Risk Assessment** — Overall risk level (Critical/High/Medium/Low) with justification.

4. **Recommendations** — Prioritized list of actions the development team should take.

Write in a professional but understandable tone. Use Markdown formatting with code blocks for evidence.
If there are no findings, state that the scan completed successfully with no issues detected, but include general security recommendations.
"""

    try:
        client = get_client()
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a senior cybersecurity analyst writing professional security assessment reports."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=4000,
        )

        report = response.choices[0].message.content

    except Exception as e:
        # Fallback: generate a basic report without LLM
        report = _generate_fallback_report(
            target_url, findings, agents_summary, duration_seconds, str(e)
        )

    sse_manager.publish(scan_id, "report_ready", {"scan_id": scan_id})
    return report


def _generate_fallback_report(
    target_url: str,
    findings: list[dict],
    agents_summary: list[dict],
    duration_seconds: int,
    error_msg: str,
) -> str:
    """Generate a basic report when LLM is unavailable."""
    # Categorize findings
    logic_flaws = [f for f in findings if f.get("category") == "logic_flaw"]
    security_issues = [f for f in findings if f.get("category") == "security_issue"]
    perf_issues = [f for f in findings if f.get("category") == "performance_issue"]
    critical = [f for f in findings if f.get("severity") == "critical"]

    report = f"""# 👻 SpecterTest Security Report

> **Note**: This report was generated without LLM analysis due to: {error_msg}

## 1. Executive Summary

Scan target **{target_url}** selama **{duration_seconds} detik** menggunakan **{len(agents_summary)} agen** swarm intelligence.

| Kategori | Jumlah |
|---|---|
| Logic Flaws | {len(logic_flaws)} |
| Security Issues | {len(security_issues)} |
| Performance Issues | {len(perf_issues)} |
| **Total** | **{len(findings)}** |

## 2. Critical Findings
"""

    if not findings:
        report += "\n✅ Tidak ada temuan signifikan. Scan selesai tanpa menemukan vulnerability.\n"
    else:
        for i, f in enumerate(findings, 1):
            severity_badge = f.get("severity", "unknown").upper()
            report += f"""
### [{severity_badge}] {f.get('title', 'Untitled Finding')}

**Agent**: `{f.get('agent_id', 'N/A')}` | **Category**: {f.get('category', 'N/A')}

{f.get('description', 'No description')}

```
{f.get('evidence', 'No evidence recorded')}
```

---
"""

    report += f"""
## 3. Recommendations

1. Perbaiki semua temuan **Critical** dan **High** segera.
2. Implementasikan proper authorization checks pada semua endpoints.
3. Gunakan parameterized queries untuk mencegah SQL Injection.
4. Sanitize semua user input untuk mencegah XSS.
5. Jalankan scan ulang setelah perbaikan.
"""

    return report
