
from backend.permissions import evaluate_permission


def check_medicine_access(action: str) -> dict:
    """Check permission before accessing medicine-related features."""

    decision = evaluate_permission(action)

    return {
        "action": action,
        "decision": decision,
        "allowed_to_proceed": decision == "ALLOW",
        "requires_approval": decision == "ASK",
        "blocked": decision == "BLOCK"
    }


def get_caresync_status() -> dict:
    """Return basic CARESYNC service information."""

    return {
        "application": "CARESYNC",
        "status": "operational",
        "permission_system": "ALLOW / ASK / BLOCK"
    }
