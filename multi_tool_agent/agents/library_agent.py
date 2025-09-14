from google.adk.agents import Agent
from google.adk.tools import AgentTool
from multi_tool_agent.tools import library_tools


search_book_tool = library_tools.search_book
# Create Tool objects from our Python functions
# search_book_tool = Tool(
#     name="search_book_in_library",
#     description="Searches for a book by its title in the university library catalog to check its availability and location.",
#     func=library_tools.search_book,
# )

# Define the Library Agent
library_agent = Agent(
    name="library_agent",
    model="gemini-2.5-pro",
    instruction="You are a specialized university library assistant. Your sole purpose is to help users find books in the library using the provided tools. Be concise and helpful.",
    tools=[search_book_tool],
)