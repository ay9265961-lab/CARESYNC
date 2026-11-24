
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



def calculate_refill_days(
    stock_count: int,
    units_used_per_day: float
) -> dict:
    """Estimate how many days the recorded stock may last."""

    if stock_count < 0:
        return {"error": "Stock count cannot be negative."}

    if units_used_per_day <= 0:
        return {"error": "Daily usage must be greater than zero."}

    days_remaining = stock_count / units_used_per_day

    return {
        "stock_count": stock_count,
        "estimated_days_remaining": round(days_remaining, 1),
        "message": (
            f"Recorded stock may last approximately "
            f"{round(days_remaining, 1)} days."
        ),
        "note": "Inventory estimate only; follow the prescribed schedule."
    }

