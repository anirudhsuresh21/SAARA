#!/usr/bin/env python3
"""
Simple test script for SARAA components
"""

import sys
import os

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_orchestrator():
    """Test the core orchestrator"""
    try:
        from multi_tool_agent.core.orchestrator import CoreOrchestrator, IntentRecognizer
        print("✅ Core Orchestrator imported successfully")
        
        # Test intent recognition
        recognizer = IntentRecognizer()
        query = "Find AI courses for next semester"
        processed = recognizer.recognize_intent(query)
        print(f"✅ Intent Recognition working: {processed.intent.value}")
        
        return True
    except Exception as e:
        print(f"❌ Core Orchestrator test failed: {e}")
        return False

def test_course_advisor():
    """Test course advisor"""
    try:
        from multi_tool_agent.agents.course_advisor import search_courses_by_query
        print("✅ Course Advisor imported successfully")
        
        result = search_courses_by_query("AI courses")
        print(f"✅ Course search working: {len(result)} chars returned")
        
        return True
    except Exception as e:
        print(f"❌ Course Advisor test failed: {e}")
        return False

def test_library_tools():
    """Test library tools"""
    try:
        from multi_tool_agent.tools.library_tools import search_book, natural_language_library_search
        print("✅ Library Tools imported successfully")
        
        result = search_book("Clean Code")
        print(f"✅ Library search working: {result['status']}")
        
        return True
    except Exception as e:
        print(f"❌ Library Tools test failed: {e}")
        return False

def test_event_tools():
    """Test event tools"""
    try:
        from multi_tool_agent.tools.event_tools import get_upcoming_events, natural_language_event_search
        print("✅ Event Tools imported successfully")
        
        events = get_upcoming_events()
        print(f"✅ Event search working: {len(events)} events found")
        
        return True
    except Exception as e:
        print(f"❌ Event Tools test failed: {e}")
        return False

def test_user_profile():
    """Test user profile system"""
    try:
        from multi_tool_agent.core.user_profile import profile_database, get_user_profile_info
        print("✅ User Profile imported successfully")
        
        profile = profile_database.get_user_profile("student123")
        print(f"✅ User profile working: {profile.name if profile else 'No profile found'}")
        
        return True
    except Exception as e:
        print(f"❌ User Profile test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🎓 SARAA System Tests")
    print("=" * 50)
    
    tests = [
        test_orchestrator,
        test_course_advisor,
        test_library_tools,
        test_event_tools,
        test_user_profile
    ]
    
    results = []
    for test in tests:
        results.append(test())
        print()
    
    passed = sum(results)
    total = len(results)
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All SARAA components are working correctly!")
        return True
    else:
        print("❌ Some components need attention")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
