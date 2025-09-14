from google.adk.agents import Agent
from google.adk.tools import AgentTool
from multi_tool_agent.tools import event_tools

get_events_tool = event_tools.get_upcoming_events

# get_events_tool = AgentTool(
#     name="get_upcoming_campus_events",
#     description="Finds upcoming events on campus. Can be filtered by categories like 'career', 'academic', or 'sports'.",
#     func=event_tools.get_upcoming_events,
# )

# Define the Events Agent
events_agent = Agent(
    name="event_agent",
    model="gemini-2.5-pro",
    instruction="You are a specialized campus events assistant. You help students find out what's happening on campus. Use the provided tools to answer questions about events.",
    tools=[get_events_tool],
)