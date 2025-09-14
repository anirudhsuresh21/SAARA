"""
Module 1: Core Orchestrator & Intent Recognition
Technology: Google Agent Development Kit (ADK), Python

Purpose: Central nervous system of SARAA for NLU, intent recognition, 
entity extraction, agent routing, and response synthesis.
"""

from typing import Dict, List, Optional, Any
import re
from enum import Enum
from dataclasses import dataclass
from google.adk.agents import Agent


class Intent(Enum):
    """Supported intents in SARAA"""
    FIND_COURSE = "find_course"
    SEARCH_LIBRARY = "search_library"
    FIND_EVENTS = "find_events"
    STUDENT_PROFILE = "student_profile"
    ANALYZE_DOCUMENT = "analyze_document"
    GENERAL_QUERY = "general_query"
    MULTI_INTENT = "multi_intent"


@dataclass
class ExtractedEntity:
    """Represents an extracted entity from user query"""
    entity_type: str
    value: str
    confidence: float = 1.0


@dataclass
class ProcessedQuery:
    """Represents a processed user query with intent and entities"""
    original_query: str
    intent: Intent
    entities: List[ExtractedEntity]
    confidence: float
    routing_target: str


class IntentRecognizer:
    """Handles natural language understanding and intent recognition"""
    
    def __init__(self):
        self.course_keywords = [
            'course', 'class', 'subject', 'elective', 'major', 'minor', 
            'prerequisite', 'credit', 'semester', 'schedule', 'professor',
            'grade', 'gpa', 'requirement', 'curriculum', 'degree'
        ]
        
        self.library_keywords = [
            'book', 'library', 'borrow', 'checkout', 'reserve', 'catalog',
            'author', 'isbn', 'journal', 'article', 'research', 'publication',
            'available', 'hold', 'renew', 'due date'
        ]
        
        self.event_keywords = [
            'event', 'meeting', 'club', 'activity', 'workshop', 'seminar',
            'conference', 'sports', 'game', 'concert', 'fair', 'career',
            'networking', 'social', 'cultural', 'academic'
        ]
        
        self.document_keywords = [
            'syllabus', 'pdf', 'document', 'image', 'analyze', 'upload',
            'assignment', 'homework', 'schedule', 'transcript', 'scan',
            'picture', 'photo', 'file', 'attachment'
        ]
        
        self.time_patterns = [
            r'\b(?:morning|afternoon|evening|night)\b',
            r'\b(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
            r'\b(?:today|tomorrow|yesterday|next week|this week)\b',
            r'\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\b',
            r'\b\d{1,2}:\d{2}\s*(?:am|pm)?\b'
        ]
        
        self.constraint_patterns = [
            r'\b(?:not|no|avoid|exclude|except|without)\s+(?:morning|afternoon|evening)\b',
            r'\b(?:before|after|until|by)\s+\d{1,2}:\d{2}\b',
            r'\b(?:minimum|maximum|at least|no more than)\s+\d+\s+(?:credits?|hours?)\b'
        ]

    def extract_entities(self, query: str) -> List[ExtractedEntity]:
        """Extract entities from user query using pattern matching and keyword analysis"""
        entities = []
        query_lower = query.lower()
        
        # Extract time constraints
        for pattern in self.time_patterns:
            matches = re.finditer(pattern, query_lower)
            for match in matches:
                entities.append(ExtractedEntity(
                    entity_type="time",
                    value=match.group(),
                    confidence=0.9
                ))
        
        # Extract constraints
        for pattern in self.constraint_patterns:
            matches = re.finditer(pattern, query_lower)
            for match in matches:
                entities.append(ExtractedEntity(
                    entity_type="constraint",
                    value=match.group(),
                    confidence=0.8
                ))
        
        # Extract subject areas (basic keyword matching)
        subjects = ['ai', 'computer science', 'mathematics', 'physics', 'chemistry', 
                   'biology', 'history', 'english', 'psychology', 'economics']
        
        for subject in subjects:
            if subject in query_lower:
                entities.append(ExtractedEntity(
                    entity_type="subject",
                    value=subject,
                    confidence=0.8
                ))
        
        # Extract course types
        course_types = ['elective', 'required', 'prerequisite', 'major', 'minor']
        for course_type in course_types:
            if course_type in query_lower:
                entities.append(ExtractedEntity(
                    entity_type="course_type",
                    value=course_type,
                    confidence=0.9
                ))
        
        return entities

    def recognize_intent(self, query: str) -> ProcessedQuery:
        """Analyze user query to determine intent and extract entities"""
        query_lower = query.lower()
        entities = self.extract_entities(query)
        
        # Count keyword matches for each category
        course_score = sum(1 for keyword in self.course_keywords if keyword in query_lower)
        library_score = sum(1 for keyword in self.library_keywords if keyword in query_lower)
        event_score = sum(1 for keyword in self.event_keywords if keyword in query_lower)
        document_score = sum(1 for keyword in self.document_keywords if keyword in query_lower)
        
        # Determine if multi-intent
        intent_scores = [course_score, library_score, event_score, document_score]
        active_intents = sum(1 for score in intent_scores if score > 0)
        
        if active_intents > 1:
            return ProcessedQuery(
                original_query=query,
                intent=Intent.MULTI_INTENT,
                entities=entities,
                confidence=0.8,
                routing_target="orchestrator"
            )
        
        # Single intent recognition
        if document_score > 0 and document_score >= max(course_score, library_score, event_score):
            return ProcessedQuery(
                original_query=query,
                intent=Intent.ANALYZE_DOCUMENT,
                entities=entities,
                confidence=min(0.9, document_score / 3.0),
                routing_target="document_analyzer"
            )
        elif course_score > library_score and course_score > event_score:
            return ProcessedQuery(
                original_query=query,
                intent=Intent.FIND_COURSE,
                entities=entities,
                confidence=min(0.9, course_score / 5.0),
                routing_target="course_advisor"
            )
        elif library_score > event_score:
            return ProcessedQuery(
                original_query=query,
                intent=Intent.SEARCH_LIBRARY,
                entities=entities,
                confidence=min(0.9, library_score / 5.0),
                routing_target="library_agent"
            )
        elif event_score > 0:
            return ProcessedQuery(
                original_query=query,
                intent=Intent.FIND_EVENTS,
                entities=entities,
                confidence=min(0.9, event_score / 5.0),
                routing_target="events_agent"
            )
        else:
            return ProcessedQuery(
                original_query=query,
                intent=Intent.GENERAL_QUERY,
                entities=entities,
                confidence=0.5,
                routing_target="general_assistant"
            )


class ResponseSynthesizer:
    """Combines responses from multiple agents into coherent answers"""
    
    def synthesize_response(self, responses: Dict[str, str], original_query: str) -> str:
        """Combine multiple agent responses into a single coherent response"""
        if len(responses) == 1:
            return list(responses.values())[0]
        
        # Multi-agent response synthesis
        synthesized = f"Here's what I found for your query: '{original_query}'\n\n"
        
        if "document_analyzer" in responses:
            synthesized += f"**Document Analysis:**\n{responses['document_analyzer']}\n\n"
            
        if "course_advisor" in responses:
            synthesized += f"**Course Information:**\n{responses['course_advisor']}\n\n"
            
        if "library_agent" in responses:
            synthesized += f"**Library Resources:**\n{responses['library_agent']}\n\n"
            
        if "events_agent" in responses:
            synthesized += f"**Campus Events:**\n{responses['events_agent']}\n\n"
        
        synthesized += "Is there anything specific you'd like me to elaborate on?"
        
        return synthesized


class CoreOrchestrator:
    """Main orchestrator that coordinates all SARAA agents"""
    
    def __init__(self):
        self.intent_recognizer = IntentRecognizer()
        self.response_synthesizer = ResponseSynthesizer()
        self.agents = {}  # Will be populated with agent instances
        
    def register_agent(self, name: str, agent: Agent):
        """Register an agent with the orchestrator"""
        self.agents[name] = agent
        
    def route_query(self, processed_query: ProcessedQuery) -> Dict[str, str]:
        """Route query to appropriate agent(s) and collect responses"""
        responses = {}
        
        if processed_query.intent == Intent.MULTI_INTENT:
            # Route to multiple agents based on keywords
            query = processed_query.original_query.lower()
            
            if any(keyword in query for keyword in self.intent_recognizer.document_keywords):
                if "document_analyzer" in self.agents:
                    responses["document_analyzer"] = self.agents["document_analyzer"].run(
                        processed_query.original_query
                    ).response
            
            if any(keyword in query for keyword in self.intent_recognizer.course_keywords):
                if "course_advisor" in self.agents:
                    responses["course_advisor"] = self.agents["course_advisor"].run(
                        processed_query.original_query
                    ).response
            
            if any(keyword in query for keyword in self.intent_recognizer.library_keywords):
                if "library_agent" in self.agents:
                    responses["library_agent"] = self.agents["library_agent"].run(
                        processed_query.original_query
                    ).response
                    
            if any(keyword in query for keyword in self.intent_recognizer.event_keywords):
                if "events_agent" in self.agents:
                    responses["events_agent"] = self.agents["events_agent"].run(
                        processed_query.original_query
                    ).response
        else:
            # Single agent routing
            target_agent = processed_query.routing_target
            if target_agent in self.agents:
                responses[target_agent] = self.agents[target_agent].run(
                    processed_query.original_query
                ).response
        
        return responses
    
    def process_query(self, user_query: str) -> str:
        """Main entry point for processing user queries"""
        # Step 1: Recognize intent and extract entities
        processed_query = self.intent_recognizer.recognize_intent(user_query)
        
        # Step 2: Route to appropriate agent(s)
        responses = self.route_query(processed_query)
        
        # Step 3: Synthesize responses
        final_response = self.response_synthesizer.synthesize_response(
            responses, user_query
        )
        
        return final_response
