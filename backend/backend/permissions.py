
from typing import Any


# Actions that can proceed without additional approval
ALLOWED_ACTIONS = {
    "medicine.list",
    "medicine.stock.view",
    "appointment.list",
    "appointment.create",
    "reminder.create",
    "essentials.list",
    "essentials.add",
    "bill.reminder.create",
    "assistant.navigate",
    "family.activity.view",
}


# Actions that require approval from an authorized family member
APPROVAL_REQUIRED_ACTIONS = {
    "medicine.record.add",
    "medicine.stock.update",
    "appointment.delete",
    "report.access",
    "report.share",
    "purchase.request",
    "permission.change",
}


# Actions that are always prohibited
BLOCKED_ACTIONS = {
    "medical.diagnosis",
    "medicine.dosage.change",
    "medicine.prescription.create",
    "report.access.bypass",
    "authentication.bypass",
    "authorization.bypass",
    "purchase.execute",
    "payment.execute",
}


def evaluate_permission(action: str) -> dict[str, Any]:
    """
    Evaluate an action using CARESYNC's permission rules.

    Returns:
        A dictionary containing the decision and its reason.
    """

    if not isinstance(action, str) or not action.strip():
        return {
            "decision": "BLOCK",
            "reason": "Invalid or empty action."
        }

    action = action.strip().lower()

    if action in BLOCKED_ACTIONS:
        return {
            "decision": "BLOCK",
            "reason": "This action is prohibited by CARESYNC policy."
        }

    if action in APPROVAL_REQUIRED_ACTIONS:
        return {
            "decision": "ASK",
            "reason": "Approval from an authorized family member is required."
        }

    if action in ALLOWED_ACTIONS:
        return {
            "decision": "ALLOW",
            "reason": "This action is permitted by CARESYNC policy."
        }

    # Unknown actions are blocked by default.
    return {
        "decision": "BLOCK",
        "reason": "This action is not recognized or authorized."
    }
