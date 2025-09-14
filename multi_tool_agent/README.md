# SARAA - Student Academic Resource Assistant Agent

A comprehensive AI assistant system for university students, providing intelligent support across academic planning, library services, campus events, and personalized recommendations.

## 🎓 System Architecture

SARAA consists of 5 integrated modules:

### Module 1: Core Orchestrator & Intent Recognition
- **Technology**: Google Agent Development Kit (ADK), Python
- **Purpose**: Central nervous system for NLU, intent recognition, entity extraction, and agent routing
- **Location**: `core/orchestrator.py`

### Module 2: Course Advisor Agent  
- **Technology**: Python, integration with Course Catalog DB
- **Purpose**: Intelligent course recommendations with prerequisite checking and constraint-based filtering
- **Location**: `agents/course_advisor.py`

### Module 3: Library Agent
- **Technology**: Python, NLP libraries, Library Management System API integration
- **Purpose**: 24/7 virtual librarian for catalog search, availability checking, and location services
- **Location**: `tools/library_tools.py`, `agents/library_agent.py`

### Module 4: Events Agent
- **Technology**: Python, University Calendar/Events DB integration  
- **Purpose**: Event discovery, personalized notifications, and registration assistance
- **Location**: `tools/event_tools.py`, `agents/events_agent.py`

### Module 5: User Profile & Personalization Module
- **Technology**: Python, PostgreSQL/MongoDB database
- **Purpose**: User data storage and personalization engine with privacy management
- **Location**: `core/user_profile.py`

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google API Key for Gemini models

### Installation

1. **Clone/download the project**
```bash
cd multi_tool_agent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
Create a `.env` file with:
```
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

4. **Run the demo**
```bash
python demo.py
```

## 💡 Usage Examples

### Course Planning
```
"Which AI electives can I take next semester that don't have morning classes?"
```

### Library Services  
```
"Do you have 'Clean Code' by Robert Martin and where can I find it?"
```

### Event Discovery
```
"What programming workshops are happening this month?"
```

### Personalized Recommendations
```
"Show me my profile and give me personalized recommendations"
```

### Multi-domain Queries
```
"Find me a book about machine learning and tell me about AI events"
```

## 🏗️ System Features

### ✅ Implemented Features

1. **Intent Recognition & Entity Extraction**
   - Natural language understanding
   - Multi-intent query handling
   - Context-aware routing

2. **Course Advisory System**
   - Prerequisite checking
   - Constraint-based filtering (time, credits, etc.)
   - Interest-based recommendations
   - Career path alignment

3. **Comprehensive Library Services**
   - Catalog search by title, author, ISBN, keywords
   - Real-time availability checking
   - Detailed location information with directions
   - Hold placement and renewal capabilities

4. **Advanced Event Management**
   - Category-based event filtering
   - Keyword search across events
   - Registration link provision
   - Personalized event recommendations

5. **User Profiling & Personalization**
   - Academic record management
   - Interest and preference tracking
   - Conversation history logging
   - Privacy-respecting personalization

6. **Multi-Agent Coordination**
   - Intelligent query routing
   - Response synthesis from multiple agents
   - Context preservation across interactions

## 🔧 Architecture Details

### Agent Hierarchy
```
SARAA (Main Orchestrator)
├── Course Advisor Agent
├── Library Agent  
├── Events Agent
└── Profile Manager Agent
```

### Data Flow
1. User query → Intent Recognition
2. Entity Extraction → Context Building  
3. Agent Routing → Specialized Processing
4. Response Synthesis → User Response
5. Interaction Logging → Profile Updates

### Privacy & Security
- Granular privacy levels (Public, University-only, Private)
- Explicit data consent management
- Filtered context based on privacy settings
- Secure profile data handling

## 📊 Mock Data

The system includes comprehensive mock data for demonstration:

- **Courses**: 5 sample courses with prerequisites, scheduling, and keywords
- **Library Items**: 6 books with availability, location, and detailed metadata  
- **Events**: 7 campus events across all categories with registration info
- **User Profiles**: 2 sample student profiles with academic records and preferences

## 🔮 Production Deployment

### Database Integration
Replace mock databases with:
- **PostgreSQL/MongoDB** for user profiles
- **University SIS API** for course catalog
- **Library Management System API** for catalog data
- **Campus Calendar API** for event information

### Enhanced Features for Production
- Real-time data synchronization
- Advanced ML-based recommendations
- Push notification system
- Mobile app integration
- Analytics dashboard

### Scalability Considerations
- Microservices architecture
- API rate limiting
- Caching for frequently accessed data
- Load balancing for high availability

## 🧪 Testing

Run the demo with various test scenarios:

```bash
python demo.py
```

Choose from:
1. **Demo Queries** - Predefined test cases showcasing all capabilities
2. **Intent Recognition Testing** - Direct testing of the NLU pipeline
3. **Interactive Session** - Free-form conversation with SARAA
4. **Profile Display** - View current user profile data

## 🎯 Key Differentiators

1. **Holistic Student Support** - Covers academic, library, and social aspects
2. **Intelligent Orchestration** - Smart routing and multi-domain query handling
3. **Privacy-First Design** - Granular privacy controls and consent management
4. **Personalization Engine** - Context-aware recommendations across all domains
5. **Extensible Architecture** - Easy to add new agents and capabilities

## 📈 Future Enhancements

- Integration with learning management systems
- Academic performance analytics
- Social networking features for study groups
- Mobile push notifications
- Voice interface support
- Integration with university chatbots and websites

## 🤝 Contributing

This is a demonstration system built for educational purposes. The architecture is designed to be:
- **Modular** - Easy to extend with new agents
- **Scalable** - Ready for production deployment
- **Privacy-Compliant** - Built with data protection in mind

For questions or suggestions, please refer to the comprehensive inline documentation in each module.
