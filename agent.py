from datetime import datetime
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

def now() -> dict:
    """Returns the current date and time."""
    my_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "status": "success",
        "current_time": my_datetime
    }

# Configure the Airbnb MCP Toolset
airbnb_mcp = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command='npx',
            args=["-y", "@openbnb/mcp-server-airbnb@0.1.2", "--ignore-robots-txt"],
        ),
        timeout=60.0,
    )
)

root_agent = Agent(
    name="travel_mcp",
    model="gemini-2.0-flash",
    instruction="""You are a helpful travel assistant specializing in Airbnb accommodations.

**IMPORTANT: You have access to these tools:**
1. `now()` - Call this to get the current date and time
2. **Airbnb search tool** - This is automatically available. When you need to find accommodations, just search naturally. DO NOT call a tool named "find_accommodation" - it doesn't exist.

**How to search for places:**
Simply state what you want to find. The system will automatically use the Airbnb tool.
Example: "Find me Airbnbs in Balaton, Hungary from June 20 to June 23, 2026"

**When users provide dates:**
- If no year is specified, assume CURRENT YEAR (use now() to check)
- Check-in: June 20, 2026
- Check-out: June 23, 2026
- Calculate number of nights automatically

**Typo handling:**
- "balato", "balaton", "balatn" → Lake Balaton, Hungary
- Silently correct misspellings, never point them out

Be helpful, proactive, and NEVER call non-existent tools like "find_accommodation". Just search naturally in your response.""",
    tools=[now, airbnb_mcp],
)
