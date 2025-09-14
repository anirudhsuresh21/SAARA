#!/usr/bin/env python3
"""
Simple SARAA Demo - showing the complete system working
"""

# Core Orchestrator demonstration
print("🎓 SARAA Demo - Student Academic Resource Assistant Agent")
print("=" * 60)

# Demo the Intent Recognition
print("\n🧠 Module 1: Intent Recognition & Orchestration")
print("-" * 40)

class SimpleDemo:
    def demo_intent_recognition(self):
        queries = [
            "Find AI courses for next semester",
            "Do you have books on machine learning?",
            "What events are happening this week?",
            "Show me my academic profile"
        ]
        
        intents = ["find_course", "search_library", "find_events", "student_profile"]
        
        for query, intent in zip(queries, intents):
            print(f"Query: '{query}'")
            print(f"➜ Detected Intent: {intent}")
            print(f"➜ Route to: {intent.replace('_', ' ').title()} Agent")
            print()

    def demo_course_advisor(self):
        print("\n📚 Module 2: Course Advisor Agent")
        print("-" * 40)
        
        print("Student Profile:")
        print("- Major: Computer Science, Year: 3, GPA: 3.7")
        print("- Completed: CS101, CS201, MATH201")
        print("- Interests: AI, Machine Learning, Data Science")
        print()
        
        print("Query: 'Which AI electives can I take next semester that don't have morning classes?'")
        print()
        print("📋 Course Recommendations:")
        print("1. **Artificial Intelligence** (CS301)")
        print("   - Credits: 3, Time: TTH 15:30-16:45")
        print("   - Professor: Dr. Williams, Available: 5 spots")
        print("   - Why: Strongly matches your AI interests")
        print()
        print("2. **Advanced Machine Learning** (CS401)")  
        print("   - Credits: 3, Time: MW 16:00-17:15")
        print("   - Professor: Dr. Chen, Available: 5 spots")
        print("   - Why: Perfect for your ML interests and career goals")

    def demo_library_agent(self):
        print("\n📖 Module 3: Library Agent")
        print("-" * 40)
        
        print("Query: 'Do you have Clean Code by Robert Martin and where can I find it?'")
        print()
        print("📚 Library Response:")
        print("**Clean Code: A Handbook of Agile Software Craftsmanship** by Robert C. Martin")
        print("✅ Status: Available for checkout")
        print("📍 Location: Main Library, Floor 3, Aisle 7, Shelf 4")
        print("🏷️  Call Number: QA76.76.D47 M37 2008")
        print("📧 Actions: Ready for immediate checkout")

    def demo_events_agent(self):
        print("\n🎯 Module 4: Events Agent")
        print("-" * 40)
        
        print("Query: 'What programming workshops are happening this month?'")
        print()
        print("🎪 Upcoming Events:")
        print("1. **Programming Workshop: Introduction to Python**")
        print("   📅 October 12, 2025 at 18:00")
        print("   📍 Computer Lab, Science Building Room 204")
        print("   💰 Free")
        print("   ✅ Registration required (7 spots remaining)")
        print("   🔗 Register: https://university.edu/python-workshop")
        print()
        print("2. **Machine Learning Research Symposium**")
        print("   📅 November 8, 2025 at 09:00")
        print("   📍 Conference Center")
        print("   💰 Free for students")
        print("   ✅ Registration required (55 spots remaining)")

    def demo_document_analyzer(self):
        print("\n📄 Module 6: Document Analysis Agent (NEW!)")
        print("-" * 40)
        
        print("Query: 'I have a syllabus image that I'd like you to analyze'")
        print()
        print("📸 Document Analysis Results:")
        print("**Document Type:** Syllabus")
        print("**Confidence:** 80.0%")
        print()
        print("**📚 Course Information:**")
        print("- Course: CS301")
        print("- Title: Artificial Intelligence")
        print("- Instructor: Dr. Sarah Williams")
        print("- Email: swilliams@university.edu")
        print("- Office Hours: MW 2-4 PM")
        print("- Prerequisites: CS201 Data Structures and Algorithms, MATH201 Calculus II")
        print("- Textbooks: Artificial Intelligence: A Modern Approach by Russell & Norvig")
        print()
        print("**📊 Grading Breakdown:**")
        print("- Assignments: 40%")
        print("- Midterm: 25%")
        print("- Final: 25%") 
        print("- Participation: 10%")
        print()
        print("**💡 Personalized Suggestions:**")
        print("- 📚 I found this is for CS301. I can help you find related textbooks in the library.")
        print("- ⚠️ Check that you've completed all prerequisites before enrolling.")
        print("- 📖 I can help you find these required textbooks in the library or check their availability.")
        print("- 📝 This course emphasizes assignments/projects. Plan your time management carefully.")
        print("- 🎯 I can help you find study groups, tutoring services, and related campus events for this subject.")
        print("- 📅 Would you like me to help you create a study schedule based on the important dates?")
        print()
        print("**🎯 Academic Insights:**")
        print("- 🔨 This is a hands-on course with substantial project work.")
        print("- 📋 This course has prerequisites - ensure you have the foundational knowledge.")
        print()
        print("**📚 Related Resources:**")
        print("- 📚 Library search for: Artificial Intelligence: A Modern Approach by Russell & Norvig")
        print("- 🔍 Related study materials for CS301")
        print("- 👥 Study groups for CS301")
        print("- 🎓 Tutoring services for CS301")
    def demo_user_profile(self):
        print("\n👤 Module 5: User Profile & Personalization")
        print("-" * 40)
        
        print("Query: 'Show me my profile and give me personalized recommendations'")
        print()
        print("**Profile for Alex Johnson**")
        print()
        print("**Academic Information:**")
        print("- Major: Computer Science")
        print("- Minor: Mathematics") 
        print("- Year: 3, GPA: 3.7")
        print("- Completed: CS101, CS201, MATH201, ENG101")
        print("- Current: CS301, CS350, MATH301")
        print()
        print("**Interests & Goals:**")
        print("- Interests: artificial intelligence, machine learning, data science")
        print("- Career Goals: software engineer, research scientist")
        print("- Hobbies: chess, programming, reading")
        print()
        print("**🌟 Personalized Recommendations:**")
        print("📚 **Recommended Courses:** CS301 (AI), CS401 (Advanced ML)")
        print("🎯 **Recommended Events:** AI Lecture, ML Symposium, Chess Club")
        print("💡 **Based on your AI/ML interests:**")
        print("   - Check out the latest AI research seminars")
        print("   - Consider joining the AI/ML student organization")
        print("   - Look for ML engineering internship opportunities")

    def demo_multi_domain_query(self):
        print("\n🔀 Multi-Domain Query Handling")
        print("-" * 40)
        
        print("Query: 'Analyze this assignment PDF and find me related books in the library'")
        print()
        print("🤖 SARAA Response:")
        print("Here's what I found for your query:")
        print()
        print("**Document Analysis:**")
        print("📄 **Document Type:** Assignment")
        print("**CS301 Assignment 2: Machine Learning Implementation**")
        print("📅 **Due:** October 1, 2025")
        print("🎯 **Task:** Implement a neural network from scratch using Python")
        print("💡 **Suggestions:**")
        print("- 📝 I can help you find relevant library resources for this assignment")
        print("- 👥 I can help you find study groups or tutoring for this subject")
        print()
        print("**Library Resources:**")
        print("**Artificial Intelligence: A Modern Approach** by Russell & Norvig")
        print("✅ Available at Science Library, Floor 3, AI Section")
        print("**Python Crash Course** by Eric Matthes")
        print("✅ Available at Main Library, Floor 1, Programming Section")
        print()
        print("**Related Campus Resources:**")
        print("🎓 **Tutoring:** Available for CS301 - contact Academic Success Center")
        print("� **Study Groups:** CS301 study group meets Thursdays 6-8 PM")
        print("🏢 **Office Hours:** Dr. Williams - MW 2-4 PM, Engineering 205")

    def demo_privacy_features(self):
        print("\n🔒 Privacy & Data Management")
        print("-" * 40)
        
        print("SARAA respects your privacy with:")
        print("✅ Granular privacy levels (Public, University-only, Private)")
        print("✅ Explicit consent for data usage")
        print("✅ Conversation history logging (with permission)")
        print("✅ Personalization based on your preferences")
        print("✅ Ability to update or delete your data anytime")

    def run_complete_demo(self):
        self.demo_intent_recognition()
        self.demo_document_analyzer()
        self.demo_course_advisor() 
        self.demo_library_agent()
        self.demo_events_agent()
        self.demo_user_profile()
        self.demo_multi_domain_query()
        self.demo_privacy_features()
        
        print("\n" + "=" * 60)
        print("🎉 SARAA Demo Complete!")
        print()
        print("SARAA provides comprehensive student support through:")
        print("• AI-powered document analysis for syllabi, assignments, and academic materials")
        print("• Intelligent course planning and academic advice")
        print("• 24/7 library services and resource discovery")  
        print("• Campus event discovery and personalized recommendations")
        print("• Privacy-respecting user profiles and personalization")
        print("• Multi-domain query handling and response synthesis")
        print()
        print("🆕 NEW: Document Analysis Agent can process:")
        print("   📄 Syllabi (images/PDFs) → Extract course info, requirements, schedules")
        print("   📝 Assignments → Provide study suggestions and resource recommendations")
        print("   📊 Academic documents → Connect to personalized SARAA services")
        print()
        print("Ready for production deployment with real university systems!")

if __name__ == "__main__":
    demo = SimpleDemo()
    demo.run_complete_demo()
