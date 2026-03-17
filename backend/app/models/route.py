"""DiscoveredRoute model — a route/endpoint found by the crawler."""
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db


class DiscoveredRoute(db.Model):
    __tablename__ = "discovered_routes"

    id: Mapped[int] = mapped_column(primary_key=True)
    scan_id: Mapped[str] = mapped_column(ForeignKey("scans.id"))
    path: Mapped[str]
    method: Mapped[str] = mapped_column(default="GET")
    has_form: Mapped[bool] = mapped_column(default=False)
    has_auth: Mapped[bool] = mapped_column(default=False)
    page_title: Mapped[Optional[str]] = mapped_column(default=None)

    def to_dict(self):
        return {
            "id": self.id,
            "path": self.path,
            "method": self.method,
            "has_form": self.has_form,
            "has_auth": self.has_auth,
            "page_title": self.page_title,
        }
