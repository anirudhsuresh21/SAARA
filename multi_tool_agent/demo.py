"""
SARAA Demo and Test Runner
Demonstrates the capabilities of the complete SARAA system
"""

from multi_tool_agent.agent import saraa_agent, orchestrator
from multi_tool_agent.core.user_profile import profile_database, personalization_engine


def demo_saraa_capabilities():
    """Demonstrate SARAA's multi-domain capabilities"""
    
    print("🎓 Welcome to SARAA - Student Academic Resource Assistant Agent!")
    print("=" * 60)
    
    # Test queries that demonstrate different modules
    test_queries = [
        # Document Analysis Module (NEW!)
        {
            "query": "I have a syllabus image that I'd like you to analyze and give me suggestions",
            "description": "Document analysis with personalized suggestions"
        },
        
        # Course Advisor Module
        {
            "query": "Which AI electives can I take next semester that don't have morning classes?",
            "description": "Course planning with constraints"
        },
        
        # Library Module  
        {
            "query": "Do you have 'Clean Code' by Robert Martin and where can I find it?",
            "description": "Library catalog search and location"
        },
        
        # Events Module
        {
            "query": "What programming workshops are happening this month?",
            "description": "Event discovery with keyword filtering"
        },
        
        # Profile Management
        {
            "query": "Show me my academic profile and give me personalized recommendations",
            "description": "Profile display and personalized suggestions"
        },
        
        # Multi-domain query
        {
            "query": "Analyze this assignment PDF and find me related books in the library",
            "description": "Multi-agent coordination with document analysis"
        }
    ]
    
    for i, test_case in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: {test_case['description']}")
        print(f"Query: \"{test_case['query']}\"")
        print("-" * 50)
        
        try:
            # Use SARAA to process the query
            response = saraa_agent.run(test_case['query'])
            print("SARAA Response:")
            print(response.response)
            
            # Log the interaction
            personalization_engine.log_interaction(
                user_id="student123",
                query=test_case['query'],
                response=response.response,
                intent="demo_test"
            )
            
        except Exception as e:
            print(f"Error processing query: {str(e)}")
        
        print("=" * 60)


def test_orchestrator_direct():
    """Test the orchestrator's intent recognition directly"""
    
    print("\n🧠 Testing Core Orchestrator Intent Recognition")
    print("=" * 60)
    
    test_queries = [
        "Analyze this syllabus image for me",
        "Find courses about data science",
        "What books do you have on artificial intelligence?", 
        "Are there any chess club meetings this week?",
        "Show me my completed courses and GPA",
        "I have a PDF assignment that needs analysis and want to know about coding workshops"
    ]
    
    for query in test_queries:
        print(f"\nQuery: \"{query}\"")
        processed = orchestrator.intent_recognizer.recognize_intent(query)
        print(f"Intent: {processed.intent.value}")
        print(f"Routing Target: {processed.routing_target}")
        print(f"Confidence: {processed.confidence:.2f}")
        
        if processed.entities:
            print("Extracted Entities:")
            for entity in processed.entities:
                print(f"  - {entity.entity_type}: {entity.value} (confidence: {entity.confidence:.2f})")


def interactive_saraa_session():
    """Interactive session with SARAA"""
    
    print("\n💬 Interactive SARAA Session")
    print("Type your questions for SARAA. Type 'quit' to exit.")
    print("=" * 60)
    
    while True:
        try:
            user_input = input("\n🎓 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Thanks for using SARAA! Have a great day!")
                break
            
            if not user_input:
                continue
            
            print("\n🤖 SARAA: ", end="")
            response = saraa_agent.run(user_input)
            print(response.response)
            
            # Log interaction
            personalization_engine.log_interaction(
                user_id="student123",
                query=user_input,
                response=response.response,
                intent="interactive"
            )
            
        except KeyboardInterrupt:
            print("\n\n👋 Thanks for using SARAA! Have a great day!")
            break
        except Exception as e:
            print(f"\n❌ Sorry, I encountered an error: {str(e)}")


def show_user_profile():
    """Display current user profile"""
    print("\n👤 Current User Profile")
    print("=" * 60)
    
    profile = profile_database.get_user_profile("student123")
    if profile:
        print(f"Name: {profile.name}")
        print(f"Email: {profile.email}")
        
        if profile.academic_record:
            print(f"Major: {profile.academic_record.major}")
            print(f"Minor: {profile.academic_record.minor}")
            print(f"Year: {profile.academic_record.year}")
            print(f"GPA: {profile.academic_record.gpa}")
            print(f"Completed Courses: {', '.join(profile.academic_record.completed_courses)}")
        
        if profile.preferences:
            print(f"Interests: {', '.join(profile.preferences.interests)}")
            print(f"Career Goals: {', '.join(profile.preferences.career_goals)}")
        
        print(f"Conversations Logged: {len(profile.conversation_history)}")
    else:
        print("No profile found for student123")


def main_menu():
    """Main menu for SARAA demo"""
    while True:
        print("\n🎓 SARAA Demo Menu")
        print("=" * 40)
        print("1. Run Demo Queries")
        print("2. Test Intent Recognition")
        print("3. Interactive Session")
        print("4. Show User Profile")
        print("5. Exit")
        
        choice = input("\nSelect an option (1-5): ").strip()
        
        if choice == '1':
            demo_saraa_capabilities()
        elif choice == '2':
            test_orchestrator_direct()
        elif choice == '3':
            interactive_saraa_session()
        elif choice == '4':
            show_user_profile()
        elif choice == '5':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1-5.")


if __name__ == "__main__":
    print("🚀 Initializing SARAA (Student Academic Resource Assistant Agent)...")
    print("Loading all modules: Core Orchestrator, Course Advisor, Library Agent, Events Agent, User Profile...")
    print("✅ SARAA is ready!")
    
    main_menu()
