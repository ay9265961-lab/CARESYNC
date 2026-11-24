
from mcp.server.fastmcp import FastMCP

from backend.mcp_tools import (
    check_medicine_access,
    get_caresync_status
)
from backend.permissions import evaluate_permission

mcp = FastMCP("CARESYNC")


@mcp.tool()
def check_action_permission(action: str) -> dict:
    """Check whether an action is ALLOW, ASK, or BLOCK."""

    decision = evaluate_permission(action)

    return {
        "action": action,
        "decision": decision,
        "message": (
            "Action is allowed."
            if decision == "ALLOW"
            else "Family approval is required."
            if decision == "ASK"
            else "This action is blocked."
        )
    }


@mcp.tool()
def check_medicine_permission(action: str) -> dict:
    """Check permission for a medicine-related action."""

    return check_medicine_access(action)


@mcp.tool()
def caresync_status() -> dict:
    """Get basic CARESYNC service information."""

    return get_caresync_status()


if __name__ == "__main__":
    mcp.run(transport="stdio")
