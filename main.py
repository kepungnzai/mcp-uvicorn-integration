import logging
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

# 1. Initialize your MCP logic
mcp = FastMCP("ProductionToolbox")

# Add a sample tool
@mcp.tool()
def calculate_uptime(server_id: str) -> str:
    """Calculates the uptime for a production server."""
    return f"Server {server_id} has been active for 1,240 hours."

# 2. Create your Production Web App (FastAPI)
app = FastAPI(title="MCP Cloud Gateway")

# --- THE INTEGRATION POINT ---
# This line connects the MCP protocol to the web server.
# It automatically creates endpoints like /sse and /messages.
app.mount("/mcp", mcp.sse_app())
# -----------------------------

@app.get("/health")
def health_check():
    """A standard production health check endpoint."""
    return {"status": "ok", "mcp_enabled": True}

