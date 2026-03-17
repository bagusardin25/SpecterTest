"""Agent Manager — handles agent lifecycle, persona generation, and spawning."""
import json

from app.extensions import db
from app.models.agent import Agent
from app.services.sse_manager import sse_manager

# Behavior profiles for each agent role
BEHAVIOR_PROFILES = {
    "user": {
        "description": "Normal user browsing behavior",
        "patterns": [
            "Navigate to pages",
            "Fill out forms with normal data",
            "Click buttons and links",
            "Browse product/content listings",
            "Submit search queries",
        ],
        "aggressiveness": 0.1,
        "speed_multiplier": 1.0,
    },
    "admin": {
        "description": "Administrator with elevated access",
        "patterns": [
            "Access admin panels and dashboards",
            "CRUD operations on resources",
            "User management actions",
            "Configuration changes",
            "Access API endpoints directly",
        ],
        "aggressiveness": 0.3,
        "speed_multiplier": 0.8,
    },
    "attacker": {
        "description": "Malicious actor attempting to exploit vulnerabilities",
        "patterns": [
            "SQL injection on input fields",
            "XSS payload injection",
            "IDOR — accessing other users' resources",
            "Path traversal attempts",
            "Race condition exploitation",
            "Parameter tampering",
            "Auth bypass attempts",
            "CSRF token manipulation",
        ],
        "aggressiveness": 0.9,
        "speed_multiplier": 1.5,
    },
}


def spawn_agents(
    scan_id: str,
    user_count: int,
    admin_count: int,
    attacker_count: int,
) -> list[Agent]:
    """
    Spawn all agents for a scan session and save to database.
    Returns list of created Agent objects.
    """
    agents = []

    # Helper to create agents of a given role
    def _create_agents(role: str, count: int, prefix: str):
        for i in range(1, count + 1):
            agent_id = f"{prefix}-{str(i).zfill(2)}"
            profile = BEHAVIOR_PROFILES[role]

            agent = Agent(
                id=agent_id,
                scan_id=scan_id,
                role=role,
                status="idle",
                current_action=f"Initializing {role} agent",
                actions_log=json.dumps([{
                    "action": "spawned",
                    "profile": profile["description"],
                    "aggressiveness": profile["aggressiveness"],
                }]),
            )
            db.session.add(agent)
            agents.append(agent)

            # Publish SSE event
            sse_manager.publish(scan_id, "agent_spawned", {
                "agent_id": agent_id,
                "role": role,
                "profile": profile["description"],
            })

    _create_agents("user", user_count, "usr")
    _create_agents("admin", admin_count, "adm")
    _create_agents("attacker", attacker_count, "atk")

    db.session.commit()

    sse_manager.publish(scan_id, "all_agents_spawned", {
        "total": len(agents),
        "users": user_count,
        "admins": admin_count,
        "attackers": attacker_count,
    })

    return agents
