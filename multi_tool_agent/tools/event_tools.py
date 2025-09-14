"""
Module 4: Events Agent Tools  
Technology: Python, integration with University Calendar/Events DB

Purpose: Keep university community informed and engaged with event discovery,
personalized notifications, registration links, and reminders.
"""

from typing import Optional, Dict, List, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


class EventCategory(Enum):
    """Event categories"""
    ACADEMIC = "academic"
    SPORTS = "sports"
    CULTURAL = "cultural"
    WORKSHOPS = "workshops"
    CAREER = "career"
    SOCIAL = "social"
    CLUB = "club"
    CONFERENCE = "conference"


@dataclass
class Event:
    """Represents a campus event"""
    event_id: str
    title: str
    description: str
    category: EventCategory
    date: str  # ISO format YYYY-MM-DD
    time: str  # HH:MM format
    end_time: str
    location: str
    department: str
    organizer: str
    registration_required: bool = False
    registration_link: Optional[str] = None
    capacity: Optional[int] = None
    current_registrations: int = 0
    tags: List[str] = None
    cost: str = "Free"


# Enhanced mock events database
MOCK_EVENTS_DB = [
    Event(
        event_id="EVT001",
        title="Fall Semester Career Fair",
        description="Meet with top employers and explore internship and job opportunities across all majors.",
        category=EventCategory.CAREER,
        date="2025-10-15",
        time="10:00",
        end_time="16:00",
        location="Student Union Ballroom",
        department="Career Services",
        organizer="career@university.edu",
        registration_required=True,
        registration_link="https://university.edu/careerfair-registration",
        capacity=500,
        current_registrations=234,
        tags=["career", "networking", "jobs", "internships"],
        cost="Free"
    ),
    Event(
        event_id="EVT002", 
        title="Guest Lecture: AI in Healthcare",
        description="Dr. Sarah Chen from Stanford presents latest developments in medical AI applications.",
        category=EventCategory.ACADEMIC,
        date="2025-10-18",
        time="14:00",
        end_time="15:30",
        location="Engineering Auditorium, Room 101",
        department="Computer Science",
        organizer="Dr. Johnson",
        registration_required=False,
        tags=["ai", "healthcare", "machine learning", "research"],
        cost="Free"
    ),
    Event(
        event_id="EVT003",
        title="Varsity Soccer Match vs. State University",
        description="Support our Wildcats in this crucial conference match!",
        category=EventCategory.SPORTS,
        date="2025-10-20",
        time="19:00",
        end_time="21:00",
        location="University Stadium",
        department="Athletics",
        organizer="athletics@university.edu",
        registration_required=False,
        tags=["soccer", "sports", "wildcats", "conference"],
        cost="$5 students, $10 general"
    ),
    Event(
        event_id="EVT004",
        title="Programming Workshop: Introduction to Python",
        description="Learn Python basics in this hands-on workshop. Perfect for beginners!",
        category=EventCategory.WORKSHOPS,
        date="2025-10-12",
        time="18:00",
        end_time="20:00",
        location="Computer Lab, Science Building Room 204",
        department="Computer Science",
        organizer="Python Club",
        registration_required=True,
        registration_link="https://university.edu/python-workshop",
        capacity=25,
        current_registrations=18,
        tags=["programming", "python", "coding", "workshop", "beginners"],
        cost="Free"
    ),
    Event(
        event_id="EVT005",
        title="International Food Festival",
        description="Taste cuisines from around the world prepared by international student organizations.",
        category=EventCategory.CULTURAL,
        date="2025-10-25",
        time="17:00",
        end_time="21:00",
        location="University Plaza",
        department="International Student Services",
        organizer="International Club",
        registration_required=False,
        tags=["food", "cultural", "international", "festival"],
        cost="$3-8 per dish"
    ),
    Event(
        event_id="EVT006",
        title="Chess Club Weekly Meeting",
        description="All skill levels welcome! Learn strategies, play friendly matches, and prepare for tournaments.",
        category=EventCategory.CLUB,
        date="2025-09-08",  # This week
        time="19:00",
        end_time="21:00",
        location="Student Center Room 305",
        department="Student Activities",
        organizer="Chess Club President",
        registration_required=False,
        tags=["chess", "games", "strategy", "weekly", "club"],
        cost="Free"
    ),
    Event(
        event_id="EVT007",
        title="Machine Learning Research Symposium", 
        description="Graduate students and faculty present cutting-edge ML research.",
        category=EventCategory.CONFERENCE,
        date="2025-11-08",
        time="09:00",
        end_time="17:00",
        location="Conference Center",
        department="Computer Science", 
        organizer="Dr. Williams",
        registration_required=True,
        registration_link="https://university.edu/ml-symposium",
        capacity=200,
        current_registrations=145,
        tags=["machine learning", "research", "symposium", "graduate", "ai"],
        cost="Free for students, $50 professionals"
    )
]


def get_upcoming_events(category: Optional[str] = None, 
                       days_ahead: int = 30,
                       department: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Find upcoming events on campus with enhanced filtering
    
    Args:
        category: Filter by event category
        days_ahead: How many days in the future to search (default 30)
        department: Filter by organizing department
        
    Returns:
        List of event dictionaries
    """
    today = datetime.now().date()
    cutoff_date = today + timedelta(days=days_ahead)
    
    filtered_events = []
    
    for event in MOCK_EVENTS_DB:
        event_date = datetime.strptime(event.date, "%Y-%m-%d").date()
        
        # Skip past events
        if event_date < today:
            continue
            
        # Skip events too far in future
        if event_date > cutoff_date:
            continue
        
        # Apply category filter
        if category and event.category.value.lower() != category.lower():
            continue
            
        # Apply department filter  
        if department and event.department.lower() != department.lower():
            continue
        
        # Convert to dictionary for JSON serialization
        event_dict = {
            "event_id": event.event_id,
            "title": event.title,
            "description": event.description,
            "category": event.category.value,
            "date": event.date,
            "time": event.time,
            "end_time": event.end_time,
            "location": event.location,
            "department": event.department,
            "organizer": event.organizer,
            "registration_required": event.registration_required,
            "registration_link": event.registration_link,
            "capacity": event.capacity,
            "current_registrations": event.current_registrations,
            "tags": event.tags or [],
            "cost": event.cost
        }
        
        filtered_events.append(event_dict)
    
    # Sort by date
    filtered_events.sort(key=lambda x: x["date"])
    
    return filtered_events


def search_events_by_keywords(keywords: List[str], 
                            category: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Search events by keywords in title, description, or tags
    
    Args:
        keywords: List of keywords to search for
        category: Optional category filter
        
    Returns:
        List of matching events
    """
    matching_events = []
    keywords_lower = [k.lower() for k in keywords]
    
    for event in MOCK_EVENTS_DB:
        # Skip past events
        event_date = datetime.strptime(event.date, "%Y-%m-%d").date()
        if event_date < datetime.now().date():
            continue
        
        # Apply category filter
        if category and event.category.value.lower() != category.lower():
            continue
        
        # Check for keyword matches
        searchable_text = (
            event.title.lower() + " " + 
            event.description.lower() + " " + 
            " ".join(event.tags or []).lower()
        )
        
        if any(keyword in searchable_text for keyword in keywords_lower):
            event_dict = {
                "event_id": event.event_id,
                "title": event.title,
                "description": event.description,
                "category": event.category.value,
                "date": event.date,
                "time": event.time,
                "end_time": event.end_time,
                "location": event.location,
                "department": event.department,
                "organizer": event.organizer,
                "registration_required": event.registration_required,
                "registration_link": event.registration_link,
                "capacity": event.capacity,
                "current_registrations": event.current_registrations,
                "tags": event.tags or [],
                "cost": event.cost
            }
            matching_events.append(event_dict)
    
    return matching_events


def get_event_details(event_id: str) -> Optional[Dict[str, Any]]:
    """
    Get detailed information about a specific event
    
    Args:
        event_id: Event identifier
        
    Returns:
        Event details or None if not found
    """
    for event in MOCK_EVENTS_DB:
        if event.event_id == event_id:
            return {
                "event_id": event.event_id,
                "title": event.title,
                "description": event.description,
                "category": event.category.value,
                "date": event.date,
                "time": event.time,
                "end_time": event.end_time,
                "location": event.location,
                "department": event.department,
                "organizer": event.organizer,
                "registration_required": event.registration_required,
                "registration_link": event.registration_link,
                "capacity": event.capacity,
                "current_registrations": event.current_registrations,
                "spots_remaining": (event.capacity - event.current_registrations) if event.capacity else None,
                "tags": event.tags or [],
                "cost": event.cost
            }
    
    return None


def register_for_event(event_id: str, user_id: str) -> Dict[str, str]:
    """
    Register user for an event (mock implementation)
    
    Args:
        event_id: Event identifier
        user_id: User identifier
        
    Returns:
        Registration status
    """
    event = get_event_details(event_id)
    
    if not event:
        return {"status": "error", "message": "Event not found"}
    
    if not event["registration_required"]:
        return {"status": "unnecessary", "message": "This event doesn't require registration"}
    
    if event["capacity"] and event["current_registrations"] >= event["capacity"]:
        return {"status": "full", "message": "Event is at full capacity"}
    
    # Mock registration success
    return {
        "status": "success", 
        "message": f"Successfully registered for '{event['title']}'",
        "confirmation_number": f"REG-{event_id}-{user_id[:8]}"
    }


def set_event_reminder(event_id: str, user_id: str, reminder_time: str) -> Dict[str, str]:
    """
    Set a reminder for an event (mock implementation)
    
    Args:
        event_id: Event identifier
        user_id: User identifier  
        reminder_time: When to remind (e.g., "1 hour before", "1 day before")
        
    Returns:
        Reminder status
    """
    event = get_event_details(event_id)
    
    if not event:
        return {"status": "error", "message": "Event not found"}
    
    return {
        "status": "success",
        "message": f"Reminder set for '{event['title']}' - {reminder_time}",
        "reminder_id": f"REM-{event_id}-{user_id[:8]}"
    }


def natural_language_event_search(query: str) -> str:
    """
    Main function for natural language event queries
    Parses user intent and routes to appropriate functions
    """
    query_lower = query.lower()
    
    # Extract event categories from query
    category_map = {
        "academic": ["academic", "lecture", "seminar", "research"],
        "sports": ["sports", "game", "match", "athletics"],
        "cultural": ["cultural", "festival", "art", "music"],
        "workshops": ["workshop", "training", "tutorial", "class"],
        "career": ["career", "job", "internship", "networking"],
        "social": ["social", "party", "gathering", "mixer"],
        "club": ["club", "meeting", "organization"],
        "conference": ["conference", "symposium", "summit"]
    }
    
    detected_category = None
    for category, keywords in category_map.items():
        if any(keyword in query_lower for keyword in keywords):
            detected_category = category
            break
    
    # Extract time constraints
    days_ahead = 60  # default increased to show more events
    if "today" in query_lower:
        days_ahead = 1
    elif "this week" in query_lower:
        days_ahead = 7  
    elif "next week" in query_lower:
        days_ahead = 14
    elif "this month" in query_lower:
        days_ahead = 30
    
    # Extract specific interests/keywords
    interest_keywords = []
    interests = ["ai", "python", "chess", "soccer", "food", "music", "art", "programming", "machine learning"]
    for interest in interests:
        if interest in query_lower:
            interest_keywords.append(interest)
    
    # Route to appropriate function based on query intent
    if "remind" in query_lower or "reminder" in query_lower:
        return "To set up reminders, please specify which event you're interested in. I can help you find events first, then set reminders."
    
    elif "register" in query_lower or "sign up" in query_lower:
        return "To register for events, please specify which event you're interested in. I can help you find events that require registration."
    
    elif interest_keywords:
        # Search by keywords
        events = search_events_by_keywords(interest_keywords, detected_category)
    else:
        # General event listing
        events = get_upcoming_events(detected_category, days_ahead)
    
    # Format response
    if not events:
        category_text = f" in the {detected_category} category" if detected_category else ""
        return f"No upcoming events found{category_text} matching your criteria."
    
    response = f"Found {len(events)} upcoming event(s)"
    if detected_category:
        response += f" in the {detected_category} category"
    response += ":\n\n"
    
    for event in events[:5]:  # Show top 5 events
        response += f"**{event['title']}**\n"
        response += f"📅 {event['date']} at {event['time']}\n"
        response += f"📍 {event['location']}\n"
        response += f"💰 {event['cost']}\n"
        
        if event['registration_required']:
            spots_left = ""
            if event['capacity']:
                remaining = event['capacity'] - event['current_registrations']
                spots_left = f" ({remaining} spots remaining)"
            response += f"✅ Registration required{spots_left}\n"
            if event['registration_link']:
                response += f"🔗 Register: {event['registration_link']}\n"
        
        response += f"{event['description'][:100]}{'...' if len(event['description']) > 100 else ''}\n\n"
    
    if len(events) > 5:
        response += f"... and {len(events) - 5} more events. Use more specific keywords to narrow results."
    
    return response
