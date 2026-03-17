"""Scan model — represents a single scan/testing session."""
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class Scan(db.Model):
    __tablename__ = "scans"

    id: Mapped[str] = mapped_column(primary_key=True)
    target_url: Mapped[str]
    status: Mapped[str] = mapped_column(default="binding")
    # Agent counts
    user_agents: Mapped[int] = mapped_column(default=5)
    admin_agents: Mapped[int] = mapped_column(default=2)
    attacker_agents: Mapped[int] = mapped_column(default=3)
    # Timestamps
    created_at: Mapped[str] = mapped_column(
        default=lambda: datetime.now(timezone.utc).isoformat()
    )
    completed_at: Mapped[Optional[str]] = mapped_column(default=None)
    duration_seconds: Mapped[Optional[int]] = mapped_column(default=None)
    # LLM report (markdown)
    report_markdown: Mapped[Optional[str]] = mapped_column(Text, default=None)

    # Relationships
    routes = relationship("DiscoveredRoute", backref="scan", cascade="all, delete-orphan")
    agents = relationship("Agent", backref="scan", cascade="all, delete-orphan")
    findings = relationship("Finding", backref="scan", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "target_url": self.target_url,
            "status": self.status,
            "user_agents": self.user_agents,
            "admin_agents": self.admin_agents,
            "attacker_agents": self.attacker_agents,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "duration_seconds": self.duration_seconds,
        }
