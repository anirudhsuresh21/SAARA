"""
Module 5: User Profile & Personalization Module
Technology: Python, PostgreSQL/MongoDB database

Purpose: Store user-specific data and preferences, enabling personalized 
experience across all SARAA agents.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import json
from enum import Enum


class NotificationPreference(Enum):
    """Notification delivery preferences"""
    EMAIL = "email"
    SMS = "sms" 
    IN_APP = "in_app"
    NONE = "none"


class PrivacyLevel(Enum):
    """Data privacy levels"""
    PUBLIC = "public"
    UNIVERSITY_ONLY = "university_only"
    PRIVATE = "private"


@dataclass  
class AcademicRecord:
    """Student's academic information"""
    student_id: str
    major: str
    minor: Optional[str] = None
    year: int = 1  # 1-4 for undergrad, 5+ for grad
    gpa: Optional[float] = None
    completed_courses: List[str] = None
    current_courses: List[str] = None
    academic_standing: str = "good"  # good, probation, honors
    graduation_date: Optional[str] = None  # Expected graduation
    
    def __post_init__(self):
        if self.completed_courses is None:
            self.completed_courses = []
        if self.current_courses is None:
            self.current_courses = []


@dataclass
class PersonalPreferences:
    """User's personal preferences and interests"""
    interests: List[str] = None
    career_goals: List[str] = None
    hobbies: List[str] = None
    preferred_learning_style: str = "visual"  # visual, auditory, kinesthetic, reading
    time_preferences: Dict[str, Any] = None
    notification_preferences: Dict[str, NotificationPreference] = None
    
    def __post_init__(self):
        if self.interests is None:
            self.interests = []
        if self.career_goals is None:
            self.career_goals = []
        if self.hobbies is None:
            self.hobbies = []
        if self.time_preferences is None:
            self.time_preferences = {}
        if self.notification_preferences is None:
            self.notification_preferences = {
                "course_reminders": NotificationPreference.IN_APP,
                "event_updates": NotificationPreference.EMAIL,
                "library_notifications": NotificationPreference.EMAIL
            }


@dataclass
class ConversationHistory:
    """Stores conversation context and history"""
    conversation_id: str
    timestamp: str
    user_query: str
    agent_response: str
    intent: str
    entities_extracted: List[Dict[str, Any]] = None
    satisfaction_rating: Optional[int] = None  # 1-5 scale
    
    def __post_init__(self):
        if self.entities_extracted is None:
            self.entities_extracted = []


@dataclass
class UserProfile:
    """Complete user profile combining all aspects"""
    user_id: str
    name: str
    email: str
    phone: Optional[str] = None
    academic_record: Optional[AcademicRecord] = None
    preferences: Optional[PersonalPreferences] = None
    conversation_history: List[ConversationHistory] = None
    created_at: str = None
    updated_at: str = None
    privacy_level: PrivacyLevel = PrivacyLevel.UNIVERSITY_ONLY
    data_consent: bool = False
    
    def __post_init__(self):
        if self.conversation_history is None:
            self.conversation_history = []
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.updated_at is None:
            self.updated_at = datetime.now().isoformat()


class UserProfileDatabase:
    """Mock database for user profiles - in production would use PostgreSQL/MongoDB"""
    
    def __init__(self):
        # Mock user data
        self.users = {
            "student123": UserProfile(
                user_id="student123",
                name="Alex Johnson",
                email="alex.johnson@university.edu",
                phone="+1-555-0123",
                academic_record=AcademicRecord(
                    student_id="student123",
                    major="Computer Science",
                    minor="Mathematics",
                    year=3,
                    gpa=3.7,
                    completed_courses=["CS101", "CS201", "MATH201", "ENG101"],
                    current_courses=["CS301", "CS350", "MATH301"],
                    academic_standing="honors"
                ),
                preferences=PersonalPreferences(
                    interests=["artificial intelligence", "machine learning", "data science"],
                    career_goals=["software engineer", "research scientist"],
                    hobbies=["chess", "programming", "reading"],
                    time_preferences={"no_morning_classes": True, "preferred_study_time": "evening"},
                    notification_preferences={
                        "course_reminders": NotificationPreference.EMAIL,
                        "event_updates": NotificationPreference.IN_APP,
                        "library_notifications": NotificationPreference.EMAIL
                    }
                ),
                privacy_level=PrivacyLevel.UNIVERSITY_ONLY,
                data_consent=True
            ),
            "student456": UserProfile(
                user_id="student456",
                name="Sarah Chen",
                email="sarah.chen@university.edu",
                academic_record=AcademicRecord(
                    student_id="student456",
                    major="Biology",
                    minor="Chemistry",
                    year=2,
                    gpa=3.9,
                    completed_courses=["BIO101", "CHEM101", "MATH101"],
                    current_courses=["BIO201", "CHEM201", "STAT101"]
                ),
                preferences=PersonalPreferences(
                    interests=["medicine", "research", "biotechnology"],
                    career_goals=["physician", "medical researcher"],
                    hobbies=["volleyball", "cooking", "volunteering"]
                ),
                data_consent=True
            )
        }
    
    def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """Retrieve user profile by ID"""
        return self.users.get(user_id)
    
    def create_user_profile(self, profile: UserProfile) -> bool:
        """Create new user profile"""
        if profile.user_id in self.users:
            return False  # User already exists
        
        profile.created_at = datetime.now().isoformat()
        profile.updated_at = profile.created_at
        self.users[profile.user_id] = profile
        return True
    
    def update_user_profile(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """Update existing user profile"""
        if user_id not in self.users:
            return False
        
        profile = self.users[user_id]
        
        # Update basic fields
        for field, value in updates.items():
            if hasattr(profile, field):
                setattr(profile, field, value)
        
        profile.updated_at = datetime.now().isoformat()
        return True
    
    def add_conversation(self, user_id: str, conversation: ConversationHistory) -> bool:
        """Add conversation to user's history"""
        if user_id not in self.users:
            return False
        
        self.users[user_id].conversation_history.append(conversation)
        self.users[user_id].updated_at = datetime.now().isoformat()
        return True
    
    def get_user_context(self, user_id: str) -> Dict[str, Any]:
        """Get user context for personalizing agent responses"""
        profile = self.get_user_profile(user_id)
        if not profile:
            return {}
        
        context = {
            "user_id": user_id,
            "name": profile.name,
            "academic_info": {},
            "preferences": {},
            "recent_conversations": []
        }
        
        # Add academic context
        if profile.academic_record:
            context["academic_info"] = {
                "major": profile.academic_record.major,
                "minor": profile.academic_record.minor,
                "year": profile.academic_record.year,
                "gpa": profile.academic_record.gpa,
                "completed_courses": profile.academic_record.completed_courses,
                "current_courses": profile.academic_record.current_courses
            }
        
        # Add preferences
        if profile.preferences:
            context["preferences"] = {
                "interests": profile.preferences.interests,
                "career_goals": profile.preferences.career_goals,
                "time_preferences": profile.preferences.time_preferences
            }
        
        # Add recent conversation context (last 5 conversations)
        if profile.conversation_history:
            recent_convs = sorted(profile.conversation_history, 
                                key=lambda x: x.timestamp, reverse=True)[:5]
            context["recent_conversations"] = [
                {
                    "query": conv.user_query,
                    "intent": conv.intent,
                    "timestamp": conv.timestamp
                }
                for conv in recent_convs
            ]
        
        return context


class PrivacyManager:
    """Manages user data privacy and consent"""
    
    @staticmethod
    def check_data_consent(user_id: str, db: UserProfileDatabase) -> bool:
        """Check if user has given consent for data usage"""
        profile = db.get_user_profile(user_id)
        return profile.data_consent if profile else False
    
    @staticmethod
    def update_privacy_settings(user_id: str, 
                              privacy_level: PrivacyLevel,
                              data_consent: bool,
                              db: UserProfileDatabase) -> bool:
        """Update user's privacy preferences"""
        return db.update_user_profile(user_id, {
            "privacy_level": privacy_level,
            "data_consent": data_consent
        })
    
    @staticmethod
    def get_filtered_context(context: Dict[str, Any], privacy_level: PrivacyLevel) -> Dict[str, Any]:
        """Filter user context based on privacy level"""
        if privacy_level == PrivacyLevel.PRIVATE:
            # Return minimal context
            return {
                "user_id": context.get("user_id"),
                "preferences": {"interests": context.get("preferences", {}).get("interests", [])}
            }
        elif privacy_level == PrivacyLevel.UNIVERSITY_ONLY:
            # Return academic info but limit personal details
            filtered = context.copy()
            if "recent_conversations" in filtered:
                filtered["recent_conversations"] = []
            return filtered
        else:  # PUBLIC
            return context


class PersonalizationEngine:
    """Provides personalized recommendations and context"""
    
    def __init__(self, db: UserProfileDatabase):
        self.db = db
        self.privacy_manager = PrivacyManager()
    
    def get_personalized_context(self, user_id: str) -> Dict[str, Any]:
        """Get user context respecting privacy settings"""
        profile = self.db.get_user_profile(user_id)
        if not profile or not profile.data_consent:
            return {}
        
        context = self.db.get_user_context(user_id)
        return self.privacy_manager.get_filtered_context(context, profile.privacy_level)
    
    def recommend_courses_for_user(self, user_id: str) -> List[str]:
        """Get course recommendations based on user profile"""
        context = self.get_personalized_context(user_id)
        if not context:
            return []
        
        recommendations = []
        academic_info = context.get("academic_info", {})
        preferences = context.get("preferences", {})
        
        # Basic recommendation logic based on interests and major
        interests = preferences.get("interests", [])
        major = academic_info.get("major", "")
        
        if "artificial intelligence" in interests or "machine learning" in interests:
            recommendations.extend(["CS301", "CS401"])  # AI courses
        
        if "data science" in interests:
            recommendations.extend(["STAT301", "CS350"])  # Data Science courses
        
        if major == "Computer Science":
            recommendations.extend(["CS201", "CS301", "CS350"])
        
        return list(set(recommendations))  # Remove duplicates
    
    def get_event_recommendations(self, user_id: str) -> List[str]:
        """Get event recommendations based on user interests"""
        context = self.get_personalized_context(user_id)
        if not context:
            return []
        
        interests = context.get("preferences", {}).get("interests", [])
        hobbies = context.get("preferences", {}).get("hobbies", [])
        
        event_recommendations = []
        
        # Map interests to event types
        if any(interest in ["ai", "artificial intelligence", "machine learning"] for interest in interests):
            event_recommendations.extend(["EVT002", "EVT007"])  # AI lecture, ML symposium
        
        if "chess" in hobbies:
            event_recommendations.append("EVT006")  # Chess club meeting
        
        if any(interest in ["programming", "coding"] for interest in interests):
            event_recommendations.append("EVT004")  # Python workshop
        
        return event_recommendations
    
    def log_interaction(self, user_id: str, query: str, response: str, intent: str):
        """Log user interaction for improving personalization"""
        if not self.privacy_manager.check_data_consent(user_id, self.db):
            return
        
        conversation = ConversationHistory(
            conversation_id=f"conv_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now().isoformat(),
            user_query=query,
            agent_response=response,
            intent=intent
        )
        
        self.db.add_conversation(user_id, conversation)


# Global instance for use across SARAA
profile_database = UserProfileDatabase()
personalization_engine = PersonalizationEngine(profile_database)


def get_user_profile_info(user_id: str = "student123") -> str:
    """
    Function to be used by agents to get user profile information
    """
    context = personalization_engine.get_personalized_context(user_id)
    
    if not context:
        return "No user profile information available. Please ensure privacy consent is given."
    
    response = f"**Profile for {context.get('name', 'User')}**\n\n"
    
    # Academic information
    academic_info = context.get("academic_info", {})
    if academic_info:
        response += "**Academic Information:**\n"
        response += f"- Major: {academic_info.get('major', 'N/A')}\n"
        if academic_info.get('minor'):
            response += f"- Minor: {academic_info.get('minor')}\n"
        response += f"- Year: {academic_info.get('year', 'N/A')}\n"
        if academic_info.get('gpa'):
            response += f"- GPA: {academic_info.get('gpa')}\n"
        response += f"- Completed Courses: {', '.join(academic_info.get('completed_courses', []))}\n"
        response += f"- Current Courses: {', '.join(academic_info.get('current_courses', []))}\n\n"
    
    # Preferences
    preferences = context.get("preferences", {})
    if preferences:
        response += "**Interests & Goals:**\n"
        if preferences.get('interests'):
            response += f"- Interests: {', '.join(preferences['interests'])}\n"
        if preferences.get('career_goals'):
            response += f"- Career Goals: {', '.join(preferences['career_goals'])}\n"
        if preferences.get('time_preferences'):
            response += f"- Time Preferences: {preferences['time_preferences']}\n"
    
    return response


def update_user_preferences(user_id: str, new_interests: List[str] = None, 
                          new_career_goals: List[str] = None) -> str:
    """
    Function to update user preferences
    """
    profile = profile_database.get_user_profile(user_id)
    if not profile:
        return "User profile not found."
    
    updates = {}
    
    if new_interests:
        if not profile.preferences:
            profile.preferences = PersonalPreferences()
        profile.preferences.interests.extend(new_interests)
        updates['preferences'] = profile.preferences
    
    if new_career_goals:
        if not profile.preferences:
            profile.preferences = PersonalPreferences()
        profile.preferences.career_goals.extend(new_career_goals)
        updates['preferences'] = profile.preferences
    
    if updates:
        success = profile_database.update_user_profile(user_id, updates)
        if success:
            return "User preferences updated successfully!"
        else:
            return "Failed to update preferences."
    
    return "No updates provided."
