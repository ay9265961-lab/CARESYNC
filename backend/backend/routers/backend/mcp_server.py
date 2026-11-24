
from mcp.server.fastmcp import FastMCP

from backend.permissions import evaluate_permission

# Create CARESYNC MCP server
mcp = FastMCP("CARESYNC")


@mcp.tool()
def check_action_permission(action: str) -> dict:
    """
    Check whether a requested action is ALLOW, ASK, or BLOCK.

    This tool only checks permission. It does not execute the action.
    """
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


if __name__ == "__main__":
    mcp.run(transport="stdio")
