"""Agent model — represents an individual AI agent in the swarm."""
from typing import Optional

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class Agent(db.Model):
    __tablename__ = "agents"

    id: Mapped[str] = mapped_column(primary_key=True)
    scan_id: Mapped[str] = mapped_column(ForeignKey("scans.id"))
    role: Mapped[str]  # user | admin | attacker
    status: Mapped[str] = mapped_column(default="idle")
    current_action: Mapped[Optional[str]] = mapped_column(default=None)
    actions_log: Mapped[Optional[str]] = mapped_column(Text, default="[]")

    # Relationships
    findings = relationship("Finding", backref="agent", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "scan_id": self.scan_id,
            "role": self.role,
            "status": self.status,
            "action": self.current_action,
        }
