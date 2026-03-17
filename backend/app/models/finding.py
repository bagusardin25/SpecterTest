"""Finding model — a vulnerability or issue discovered during simulation."""
from typing import Optional

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db


class Finding(db.Model):
    __tablename__ = "findings"

    id: Mapped[int] = mapped_column(primary_key=True)
    scan_id: Mapped[str] = mapped_column(ForeignKey("scans.id"))
    agent_id: Mapped[str] = mapped_column(ForeignKey("agents.id"))
    category: Mapped[str]  # logic_flaw | security_issue | performance_issue
    severity: Mapped[str]  # critical | high | medium | low
    title: Mapped[str]
    description: Mapped[Optional[str]] = mapped_column(Text, default=None)
    evidence: Mapped[Optional[str]] = mapped_column(Text, default=None)
    remediation: Mapped[Optional[str]] = mapped_column(Text, default=None)

    def to_dict(self):
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "category": self.category,
            "severity": self.severity,
            "title": self.title,
            "description": self.description,
            "evidence": self.evidence,
            "remediation": self.remediation,
        }
