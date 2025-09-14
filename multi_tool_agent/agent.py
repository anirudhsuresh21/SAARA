"""
SARAA (Student Academic Resource Assistant Agent)
Main orchestrator integrating all modules for comprehensive student support.
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

# Import SARAA modules
from multi_tool_agent.core.orchestrator import CoreOrchestrator
from multi_tool_agent.core.user_profile import (
    get_user_profile_info, 
    update_user_preferences,
    personalization_engine
)
from multi_tool_agent.tools import event_tools, library_tools
from multi_tool_agent.agents.course_advisor import search_courses_by_query
from multi_tool_agent.agents.document_analyzer import analyze_document, analyze_syllabus_image, analyze_assignment_pdf

# Enhanced tool functions with SARAA integration
def enhanced_library_search(query: str) -> str:
    """Enhanced library search with user context"""
    return library_tools.natural_language_library_search(query)

def enhanced_event_search(query: str) -> str:
    """Enhanced event search with personalization"""
    return event_tools.natural_language_event_search(query)

def enhanced_course_search(query: str) -> str:
    """Enhanced course search with student profile integration"""
    return search_courses_by_query(query)

def get_personalized_recommendations(user_id: str = "student123") -> str:
    """Get personalized recommendations across all domains"""
    # Get user context
    context = personalization_engine.get_personalized_context(user_id)
    if not context:
        return "Please set up your profile first to get personalized recommendations."
    
    recommendations = f"**Personalized Recommendations for {context.get('name', 'you')}**\n\n"
    
    # Course recommendations
    course_recs = personalization_engine.recommend_courses_for_user(user_id)
    if course_recs:
        recommendations += "**📚 Recommended Courses:**\n"
        for course in course_recs[:3]:
            recommendations += f"- {course}\n"
        recommendations += "\n"
    
    # Event recommendations
    event_recs = personalization_engine.get_event_recommendations(user_id)
    if event_recs:
        recommendations += "**🎯 Recommended Events:**\n"
        # Get event details
        for event_id in event_recs[:3]:
            event_details = event_tools.get_event_details(event_id)
            if event_details:
                recommendations += f"- {event_details['title']} ({event_details['date']})\n"
        recommendations += "\n"
    
    # Add interests-based suggestions
    interests = context.get("preferences", {}).get("interests", [])
    if interests:
        recommendations += f"**💡 Based on your interests in {', '.join(interests)}:**\n"
        recommendations += "- Check out the latest research seminars in your field\n"
        recommendations += "- Consider joining relevant student organizations\n"
        recommendations += "- Look for internship opportunities aligned with your goals\n"
    
    return recommendations

# Create specialized agents for each domain

# Document Analysis Agent  
document_analyzer_agent = Agent(
    model="gemini-2.0-flash",
    name="document_analyzer",
    instruction="""You are SARAA's Document Analysis Assistant. You help students with:
    - Analyzing syllabi from images or PDFs to extract key course information
    - Processing assignment documents to provide study suggestions
    - Extracting important dates, requirements, and grading policies
    - Providing personalized academic insights based on document content
    - Connecting document information to library resources and campus services
    
    Use the analyze_document tool for general document analysis.
    Use analyze_syllabus_image for syllabus images.
    Use analyze_assignment_pdf for assignment documents.
    
    Always provide actionable suggestions and connect students to relevant SARAA services.""",
    description="AI-powered document processor for syllabi, assignments, and academic materials",
    tools=[analyze_document, analyze_syllabus_image, analyze_assignment_pdf]
)

# Library Agent
library_agent = Agent(
    model="gemini-2.0-flash",
    name="library_assistant",
    instruction="""You are SARAA's Library Assistant. You help students with:
    - Finding books, journals, and articles in the library catalog
    - Checking availability and location of items
    - Providing detailed directions to find physical items
    - Helping with holds, renewals, and registrations
    
    Use the enhanced_library_search tool for all library-related queries.
    Be helpful, accurate, and provide complete information including locations and call numbers.""",
    description="Virtual librarian available 24/7 for all library needs",
    tools=[enhanced_library_search]
)

# Events Agent
events_agent = Agent(
    model="gemini-2.0-flash",
    name="events_assistant", 
    instruction="""You are SARAA's Events Assistant. You help students with:
    - Finding campus events by category, date, or interests
    - Getting detailed event information including registration links
    - Providing personalized event recommendations
    - Setting up event reminders and notifications
    
    Use the enhanced_event_search tool for all event-related queries.
    Be enthusiastic about campus life and help students get involved.""",
    description="Campus events specialist keeping students engaged",
    tools=[enhanced_event_search]
)

# Course Advisor Agent  
course_advisor_agent = Agent(
    model="gemini-2.0-flash",
    name="course_advisor",
    instruction="""You are SARAA's Course Advisor. You help students with:
    - Finding courses based on interests, requirements, and constraints
    - Checking prerequisites and course availability
    - Providing personalized course recommendations
    - Career-aligned course planning
    
    Use the enhanced_course_search tool for course-related queries.
    Consider student's academic profile, interests, and career goals.""",
    description="Academic advisor for intelligent course recommendations",
    tools=[enhanced_course_search]
)

# Profile Manager Agent
profile_agent = Agent(
    model="gemini-2.0-flash",
    name="profile_manager",
    instruction="""You are SARAA's Profile Manager. You help students with:
    - Viewing and updating their academic profile
    - Managing interests and preferences  
    - Getting personalized recommendations
    - Understanding privacy settings
    
    Use get_user_profile_info to show profile information and 
    update_user_preferences to modify interests/goals.
    Always respect user privacy and explain data usage.""",
    description="Personal profile and preferences manager",
    tools=[get_user_profile_info, update_user_preferences, get_personalized_recommendations]
)

# Convert agents to tools for the main orchestrator
document_analyzer_tool = AgentTool(agent=document_analyzer_agent, skip_summarization=False)
library_tool = AgentTool(agent=library_agent, skip_summarization=False)
events_tool = AgentTool(agent=events_agent, skip_summarization=False)
course_advisor_tool = AgentTool(agent=course_advisor_agent, skip_summarization=False)
profile_tool = AgentTool(agent=profile_agent, skip_summarization=False)

# Main SARAA Orchestrator Agent
saraa_agent = Agent(
    model="gemini-2.0-flash",
    name="SARAA",
    instruction="""You are SARAA (Student Academic Resource Assistant Agent), the main AI assistant for university students.

You are an intelligent orchestrator that understands student queries and routes them to the appropriate specialist:

🏫 **Your Capabilities:**
- **Document Analysis**: Process syllabi, assignments, and academic documents from images/PDFs
- **Course Planning**: Help find courses, check prerequisites, plan academic paths
- **Library Services**: Search catalog, check availability, locate books and resources  
- **Campus Events**: Discover events, get recommendations, find activities
- **Profile Management**: Manage student preferences and get personalized recommendations

🎯 **How to Help Students:**
1. **Understand their intent** - What do they need help with?
2. **Route to the right specialist** - Use the appropriate assistant tool
3. **Provide comprehensive answers** - Combine information when needed

🧑‍💼 **Routing Guide:**
- Document/syllabus/PDF questions → Use 'document_analyzer'
- Library questions → Use 'library_assistant'
- Event/activity questions → Use 'events_assistant'  
- Course/academic questions → Use 'course_advisor'
- Profile/preferences → Use 'profile_manager'

For complex queries involving multiple domains, use multiple assistants and synthesize their responses.

Always be friendly, helpful, and student-focused. Remember you're here to make their university experience better!""",
    description="SARAA - Your intelligent university assistant",
    tools=[document_analyzer_tool, library_tool, events_tool, course_advisor_tool, profile_tool],
)

# Initialize the core orchestrator (for advanced routing if needed)
orchestrator = CoreOrchestrator()
orchestrator.register_agent("document_analyzer", document_analyzer_agent)
orchestrator.register_agent("library_agent", library_agent)
orchestrator.register_agent("events_agent", events_agent) 
orchestrator.register_agent("course_advisor", course_advisor_agent)
orchestrator.register_agent("profile_agent", profile_agent)

# For backwards compatibility, keep the original variable name
root_agent = saraa_agent
