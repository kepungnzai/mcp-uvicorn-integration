import logging
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

# 1. Initialize your MCP logic
mcp = FastMCP("ProductionToolbox")

# Add a sample tool
@mcp.tool()
def greeting_time(server_id: str) -> str:
    """Returns a greeting hello."""
    return f"Server hello {server_id}."

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

if __name__ == "__main__":
    import uvicorn
    # This creates the "http://127.0.0.1:8000" that the client is looking for
    uvicorn.run(app, host="127.0.0.1", port=8000)