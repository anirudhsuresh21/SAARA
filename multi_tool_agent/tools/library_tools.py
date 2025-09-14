"""
Module 3: Library Agent Tools
Technology: Python, NLP libraries, integration with Library Management System API

Purpose: Virtual librarian available 24/7 for catalog search, availability checking,
location services, and action execution.
"""

from typing import Optional, Dict, List, Any
from dataclasses import dataclass
from enum import Enum
import re


class BookStatus(Enum):
    """Book availability status"""
    AVAILABLE = "available"
    CHECKED_OUT = "checked_out"
    ON_HOLD = "on_hold"
    IN_REPAIR = "in_repair"
    MISSING = "missing"


@dataclass
class LibraryItem:
    """Represents an item in the library catalog"""
    item_id: str
    title: str
    author: str
    isbn: Optional[str]
    item_type: str  # book, journal, article, dvd, etc.
    location: str
    call_number: str
    status: BookStatus
    due_date: Optional[str]
    hold_count: int = 0
    description: Optional[str] = None
    keywords: List[str] = None


# Enhanced mock database with more comprehensive data
MOCK_LIBRARY_DB = {
    "clean_code": LibraryItem(
        item_id="CC001",
        title="Clean Code: A Handbook of Agile Software Craftsmanship",
        author="Robert C. Martin",
        isbn="9780132350884",
        item_type="book",
        location="Main Library, Floor 3, Aisle 7, Shelf 4",
        call_number="QA76.76.D47 M37 2008",
        status=BookStatus.AVAILABLE,
        due_date=None,
        keywords=["programming", "software engineering", "agile", "clean code"]
    ),
    "design_patterns": LibraryItem(
        item_id="DP001",
        title="Design Patterns: Elements of Reusable Object-Oriented Software",
        author="Gang of Four",
        isbn="9780201633612",
        item_type="book",
        location="Main Library, Floor 3, Aisle 8, Shelf 2",
        call_number="QA76.64 G35 1995",
        status=BookStatus.CHECKED_OUT,
        due_date="2025-09-20",
        keywords=["design patterns", "object-oriented", "programming", "software engineering"]
    ),
    "algorithms": LibraryItem(
        item_id="ALG001",
        title="Introduction to Algorithms",
        author="Thomas H. Cormen",
        isbn="9780262033848",
        item_type="book",
        location="Science Library, Floor 2, Section 3A",
        call_number="QA76.6 C662 2009",
        status=BookStatus.AVAILABLE,
        due_date=None,
        keywords=["algorithms", "computer science", "data structures"]
    ),
    "data_intensive": LibraryItem(
        item_id="DIA001",
        title="Designing Data-Intensive Applications",
        author="Martin Kleppmann",
        isbn="9781449373320",
        item_type="book",
        location="Main Library, Floor 2, Aisle 12, Shelf 3",
        call_number="QA76.9.D3 K54 2017",
        status=BookStatus.ON_HOLD,
        due_date="2025-09-15",
        hold_count=3,
        keywords=["databases", "distributed systems", "big data", "scalability"]
    ),
    "python_crash": LibraryItem(
        item_id="PCC001",
        title="Python Crash Course",
        author="Eric Matthes",
        isbn="9781593279288",
        item_type="book",
        location="Main Library, Floor 1, Programming Section",
        call_number="QA76.73.P98 M38 2019",
        status=BookStatus.AVAILABLE,
        due_date=None,
        keywords=["python", "programming", "beginner", "tutorial"]
    ),
    "ai_modern": LibraryItem(
        item_id="AI001",
        title="Artificial Intelligence: A Modern Approach",
        author="Stuart Russell and Peter Norvig",
        isbn="9780134610993",
        item_type="book",
        location="Science Library, Floor 3, AI Section",
        call_number="Q335 R87 2020",
        status=BookStatus.AVAILABLE,
        due_date=None,
        keywords=["artificial intelligence", "machine learning", "ai", "computer science"]
    )
}


def search_catalog(query: str, search_type: str = "title") -> List[Dict[str, Any]]:
    """
    Search the library catalog by title, author, or keyword
    
    Args:
        query: Search term
        search_type: Type of search ("title", "author", "keyword", "isbn")
    
    Returns:
        List of matching items with their details
    """
    query_lower = query.lower()
    results = []
    
    for key, item in MOCK_LIBRARY_DB.items():
        match_found = False
        
        if search_type == "title" or search_type == "all":
            if query_lower in item.title.lower():
                match_found = True
        
        if search_type == "author" or search_type == "all":
            if query_lower in item.author.lower():
                match_found = True
        
        if search_type == "isbn" or search_type == "all":
            if item.isbn and query_lower in item.isbn.lower():
                match_found = True
        
        if search_type == "keyword" or search_type == "all":
            if item.keywords:
                if any(query_lower in keyword.lower() for keyword in item.keywords):
                    match_found = True
        
        if match_found:
            results.append({
                "item_id": item.item_id,
                "title": item.title,
                "author": item.author,
                "isbn": item.isbn,
                "type": item.item_type,
                "status": item.status.value,
                "location": item.location,
                "call_number": item.call_number,
                "due_date": item.due_date,
                "hold_count": item.hold_count
            })
    
    return results


def check_availability(item_id: str) -> Dict[str, Any]:
    """
    Check real-time availability status of a library item
    
    Args:
        item_id: Library item identifier
    
    Returns:
        Dictionary with availability details
    """
    # Find item by ID
    item = None
    for lib_item in MOCK_LIBRARY_DB.values():
        if lib_item.item_id == item_id:
            item = lib_item
            break
    
    if not item:
        return {"error": "Item not found", "item_id": item_id}
    
    availability_info = {
        "item_id": item.item_id,
        "title": item.title,
        "status": item.status.value,
        "location": item.location,
        "call_number": item.call_number
    }
    
    if item.status == BookStatus.AVAILABLE:
        availability_info["message"] = "Available for checkout"
        availability_info["action_available"] = ["checkout"]
    
    elif item.status == BookStatus.CHECKED_OUT:
        availability_info["due_date"] = item.due_date
        availability_info["message"] = f"Currently checked out, due back on {item.due_date}"
        availability_info["action_available"] = ["place_hold"]
    
    elif item.status == BookStatus.ON_HOLD:
        availability_info["hold_count"] = item.hold_count
        availability_info["due_date"] = item.due_date
        availability_info["message"] = f"On hold for another patron. {item.hold_count} people in queue."
        availability_info["action_available"] = ["place_hold"]
    
    return availability_info


def get_location_details(item_id: str) -> Dict[str, str]:
    """
    Get detailed location information for a physical item
    
    Args:
        item_id: Library item identifier
    
    Returns:
        Dictionary with location details and directions
    """
    item = None
    for lib_item in MOCK_LIBRARY_DB.values():
        if lib_item.item_id == item_id:
            item = lib_item
            break
    
    if not item:
        return {"error": "Item not found"}
    
    location_parts = item.location.split(", ")
    building = location_parts[0] if location_parts else "Unknown"
    
    directions = {
        "item_id": item.item_id,
        "title": item.title,
        "full_location": item.location,
        "call_number": item.call_number,
        "building": building,
        "directions": f"Go to {item.location}. Look for call number {item.call_number}"
    }
    
    # Add building-specific directions
    if "Main Library" in building:
        directions["building_hours"] = "Mon-Thu: 8am-11pm, Fri: 8am-6pm, Sat: 10am-6pm, Sun: 12pm-11pm"
        directions["entrance"] = "Main entrance on University Avenue"
    elif "Science Library" in building:
        directions["building_hours"] = "Mon-Fri: 8am-10pm, Sat: 10am-8pm, Sun: 12pm-10pm"
        directions["entrance"] = "Enter through Science Building, 2nd floor"
    
    return directions


def place_hold(item_id: str, user_id: str) -> Dict[str, str]:
    """
    Place a hold on a library item (mock implementation)
    
    Args:
        item_id: Library item identifier
        user_id: User/student identifier
    
    Returns:
        Status of hold placement
    """
    item = None
    for lib_item in MOCK_LIBRARY_DB.values():
        if lib_item.item_id == item_id:
            item = lib_item
            break
    
    if not item:
        return {"error": "Item not found", "status": "failed"}
    
    if item.status == BookStatus.AVAILABLE:
        return {
            "status": "unnecessary", 
            "message": "Item is currently available for immediate checkout"
        }
    
    # Mock hold placement
    return {
        "status": "success",
        "message": f"Hold placed successfully on '{item.title}'",
        "position_in_queue": item.hold_count + 1,
        "estimated_availability": "Within 2-3 weeks"
    }


def renew_item(item_id: str, user_id: str) -> Dict[str, str]:
    """
    Renew a borrowed item (mock implementation)
    
    Args:
        item_id: Library item identifier  
        user_id: User/student identifier
    
    Returns:
        Status of renewal
    """
    # Mock renewal logic
    return {
        "status": "success",
        "message": f"Item {item_id} renewed successfully",
        "new_due_date": "2025-10-06"
    }


def search_book(title: str) -> Dict[str, Any]:
    """
    Legacy function for backward compatibility
    Enhanced to use the new catalog search
    """
    results = search_catalog(title, "title")
    
    if results:
        item = results[0]  # Return first match
        return {
            "title": item["title"],
            "status": "Found",
            "available": item["status"] == "available",
            "location": item["location"],
            "author": item["author"],
            "call_number": item["call_number"]
        }
    else:
        return {"status": "Not Found", "title": title}


def natural_language_library_search(query: str) -> str:
    """
    Main function for natural language library queries
    Parses user intent and routes to appropriate functions
    """
    query_lower = query.lower()
    
    # Extract book/item title using common patterns
    title_patterns = [
        r"(?:find|search for|look for|do you have)\s+['\"]([^'\"]+)['\"]",
        r"(?:find|search for|look for|do you have)\s+(.+?)(?:\s+by\s+|\s+author|\s*$)",
        r"book\s+['\"]([^'\"]+)['\"]",
        r"book\s+(.+?)(?:\s+by\s+|\s+author|\s*$)",
        r"['\"]([^'\"]+)['\"]",  # Extract quoted titles
        r"^(.+?)\s+by\s+",  # Extract title before "by author"
        r"^(.+?)\s+book\s*$",  # Extract subject before "book"
        r"^([a-zA-Z0-9\s:,\.\-]+?)(?:\s+by\s+|\s+author|\s*$)"  # General title extraction
    ]
    
    extracted_title = None
    for pattern in title_patterns:
        match = re.search(pattern, query_lower)
        if match:
            extracted_title = match.group(1).strip()
            break
    
    # Extract author if mentioned
    author_match = re.search(r"by\s+([a-zA-Z\s\.]+)", query_lower)
    author = author_match.group(1).strip() if author_match else None
    
    # Determine query intent
    if "available" in query_lower or "check" in query_lower:
        # Availability check
        if extracted_title:
            results = search_catalog(extracted_title, "title")
            if results:
                item = results[0]
                availability = check_availability(item["item_id"])
                return f"**{item['title']}** by {item['author']}\n" \
                       f"Status: {availability['message']}\n" \
                       f"Location: {availability['location']}\n" \
                       f"Call Number: {availability['call_number']}"
            else:
                return f"Could not find '{extracted_title}' in the catalog."
    
    elif "location" in query_lower or "where" in query_lower:
        # Location inquiry
        if extracted_title:
            results = search_catalog(extracted_title, "title")
            if results:
                item = results[0]
                location_info = get_location_details(item["item_id"])
                return f"**{location_info['title']}**\n" \
                       f"Location: {location_info['full_location']}\n" \
                       f"Call Number: {location_info['call_number']}\n" \
                       f"Directions: {location_info['directions']}"
    
    elif "hold" in query_lower or "reserve" in query_lower:
        # Hold/reservation request
        if extracted_title:
            results = search_catalog(extracted_title, "title")
            if results:
                item = results[0]
                hold_result = place_hold(item["item_id"], "student123")  # Mock user ID
                return f"Hold request for **{item['title']}**\n" \
                       f"Status: {hold_result['status']}\n" \
                       f"Message: {hold_result['message']}"
    
    else:
        # General search
        search_term = extracted_title if extracted_title else query_lower
        
        # Try different search types
        results = search_catalog(search_term, "all")
        
        if not results:
            return f"No items found matching '{search_term}'. Try different keywords or check spelling."
        
        # Format results
        response = f"Found {len(results)} item(s) matching '{search_term}':\n\n"
        
        for i, item in enumerate(results[:3]):  # Show top 3 results
            response += f"**{i+1}. {item['title']}**\n"
            response += f"   Author: {item['author']}\n"
            response += f"   Status: {item['status'].replace('_', ' ').title()}\n"
            response += f"   Location: {item['location']}\n"
            
            if item['status'] == 'checked_out' and item['due_date']:
                response += f"   Due back: {item['due_date']}\n"
            elif item['status'] == 'on_hold' and item['hold_count'] > 0:
                response += f"   Hold queue: {item['hold_count']} people waiting\n"
            
            response += "\n"
        
        if len(results) > 3:
            response += f"... and {len(results) - 3} more results."
    
    return response