"""
Module 6: Document Analysis Agent
Technology: Python, Google Vision API, PDF processing, OCR capabilities

Purpose: Process images and PDFs (syllabi, assignments, documents) to provide
intelligent academic suggestions and insights.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import base64
import json
from datetime import datetime
import re


class DocumentType(Enum):
    """Types of documents that can be processed"""
    SYLLABUS = "syllabus"
    ASSIGNMENT = "assignment"
    LECTURE_NOTES = "lecture_notes"
    TEXTBOOK_PAGE = "textbook_page"
    SCHEDULE = "schedule"
    TRANSCRIPT = "transcript"
    RESEARCH_PAPER = "research_paper"
    UNKNOWN = "unknown"


@dataclass
class DocumentAnalysis:
    """Results of document analysis"""
    document_type: DocumentType
    confidence: float
    key_information: Dict[str, Any]
    extracted_text: str
    suggestions: List[str]
    academic_insights: List[str]
    related_resources: List[str]


class SyllabusAnalyzer:
    """Specialized analyzer for course syllabi"""
    
    def __init__(self):
        self.syllabus_keywords = [
            'syllabus', 'course', 'instructor', 'prerequisites', 'textbook',
            'grading', 'schedule', 'assignments', 'exam', 'office hours'
        ]
    
    def analyze_syllabus(self, text: str) -> Dict[str, Any]:
        """Extract structured information from syllabus text"""
        text_lower = text.lower()
        
        analysis = {
            'course_info': {},
            'instructor_info': {},
            'requirements': {},
            'schedule': [],
            'grading_policy': {},
            'important_dates': []
        }
        
        # Extract course information
        course_match = re.search(r'([A-Z]{2,4}\s*\d{3}[A-Z]?)', text)
        if course_match:
            analysis['course_info']['course_code'] = course_match.group(1)
        
        title_patterns = [
            r'course title:?\s*(.+?)(?:\n|$)',
            r'title:?\s*(.+?)(?:\n|$)',
            r'^(.+?)(?:\n.*syllabus|syllabus)'
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                analysis['course_info']['title'] = match.group(1).strip()
                break
        
        # Extract instructor information
        instructor_patterns = [
            r'instructor:?\s*(.+?)(?:\n|$)',
            r'professor:?\s*(.+?)(?:\n|$)',
            r'taught by:?\s*(.+?)(?:\n|$)'
        ]
        
        for pattern in instructor_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                analysis['instructor_info']['name'] = match.group(1).strip()
                break
        
        # Extract email
        email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', text)
        if email_match:
            analysis['instructor_info']['email'] = email_match.group(1)
        
        # Extract office hours
        office_hours_match = re.search(r'office hours:?\s*(.+?)(?:\n|$)', text, re.IGNORECASE)
        if office_hours_match:
            analysis['instructor_info']['office_hours'] = office_hours_match.group(1).strip()
        
        # Extract prerequisites
        prereq_patterns = [
            r'prerequisite[s]?:?\s*(.+?)(?:\n|$)',
            r'prereq[s]?:?\s*(.+?)(?:\n|$)',
            r'requirements?:?\s*(.+?)(?:\n|$)'
        ]
        
        for pattern in prereq_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                analysis['requirements']['prerequisites'] = match.group(1).strip()
                break
        
        # Extract textbook information
        textbook_patterns = [
            r'textbook[s]?:?\s*(.+?)(?:\n|$)',
            r'required text[s]?:?\s*(.+?)(?:\n|$)',
            r'book[s]?:?\s*(.+?)(?:\n|$)'
        ]
        
        for pattern in textbook_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                analysis['requirements']['textbooks'] = match.group(1).strip()
                break
        
        # Extract grading policy
        grading_patterns = [
            r'grading:?\s*(.+?)(?:\n\n|\n[A-Z]|\n$)',
            r'grade[s]?:?\s*(.+?)(?:\n\n|\n[A-Z]|\n$)',
            r'evaluation:?\s*(.+?)(?:\n\n|\n[A-Z]|\n$)'
        ]
        
        for pattern in grading_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                analysis['grading_policy']['description'] = match.group(1).strip()
                break
        
        # Look for percentage breakdowns
        percentage_matches = re.findall(r'(\w+)[\s:]*(\d+)%', text)
        if percentage_matches:
            analysis['grading_policy']['breakdown'] = dict(percentage_matches)
        
        return analysis


class DocumentProcessor:
    """Main document processing engine"""
    
    def __init__(self):
        self.syllabus_analyzer = SyllabusAnalyzer()
        
        # Mock OCR and image processing capabilities
        # In production, this would use Google Vision API or similar
        self.supported_formats = ['.pdf', '.jpg', '.jpeg', '.png', '.txt', '.docx']
    
    def detect_document_type(self, text: str) -> DocumentType:
        """Detect the type of document based on content"""
        text_lower = text.lower()
        
        # Syllabus detection
        if any(word in text_lower for word in ['syllabus', 'course outline', 'grading policy']):
            return DocumentType.SYLLABUS
        
        # Assignment detection  
        if any(word in text_lower for word in ['assignment', 'homework', 'due date', 'submit']):
            return DocumentType.ASSIGNMENT
        
        # Schedule detection
        if any(word in text_lower for word in ['schedule', 'calendar', 'weekly', 'dates']):
            return DocumentType.SCHEDULE
        
        # Lecture notes detection
        if any(word in text_lower for word in ['lecture', 'notes', 'chapter', 'topic']):
            return DocumentType.LECTURE_NOTES
        
        # Transcript detection
        if any(word in text_lower for word in ['transcript', 'gpa', 'credits earned', 'degree']):
            return DocumentType.TRANSCRIPT
        
        return DocumentType.UNKNOWN
    
    def mock_extract_text_from_image(self, image_path: str) -> str:
        """Mock OCR functionality - in production would use Google Vision API"""
        # This is a mock implementation
        return f"""
        CS301 - Artificial Intelligence
        Fall 2025 Syllabus
        
        Instructor: Dr. Sarah Williams
        Email: swilliams@university.edu
        Office Hours: MW 2-4 PM
        
        Course Description:
        Introduction to artificial intelligence concepts including search algorithms,
        knowledge representation, machine learning, and neural networks.
        
        Prerequisites: CS201 Data Structures and Algorithms
        
        Textbook: "Artificial Intelligence: A Modern Approach" by Russell & Norvig
        
        Grading Policy:
        Assignments: 40%
        Midterm Exam: 25%
        Final Exam: 25%
        Participation: 10%
        
        Important Dates:
        - Midterm: October 15, 2025
        - Final Project Due: November 20, 2025
        - Final Exam: December 10, 2025
        """
    
    def mock_extract_text_from_pdf(self, pdf_path: str) -> str:
        """Mock PDF text extraction - in production would use PyPDF2 or similar"""
        # This is a mock implementation
        return f"""
        CS350 - Software Engineering
        Spring 2025 Course Syllabus
        
        Instructor: Professor John Davis
        Contact: jdavis@university.edu
        Office: Engineering Building 301
        
        Course Objectives:
        Students will learn software development methodologies, design patterns,
        testing strategies, and project management principles.
        
        Prerequisites: CS201, CS250
        
        Required Materials:
        - "Clean Code" by Robert Martin
        - "Design Patterns" by Gang of Four
        
        Assessment:
        Projects: 50%
        Quizzes: 20%
        Final Project: 20%
        Class Participation: 10%
        
        Weekly Schedule:
        Week 1: Introduction to Software Engineering
        Week 2: Requirements Analysis
        Week 3: Design Patterns
        Week 4: Testing Methodologies
        ...
        """
    
    def generate_suggestions(self, document_type: DocumentType, 
                           analysis: Dict[str, Any], 
                           user_context: Optional[Dict] = None) -> List[str]:
        """Generate intelligent suggestions based on document analysis"""
        suggestions = []
        
        if document_type == DocumentType.SYLLABUS:
            suggestions.extend(self._generate_syllabus_suggestions(analysis, user_context))
        elif document_type == DocumentType.ASSIGNMENT:
            suggestions.extend(self._generate_assignment_suggestions(analysis, user_context))
        elif document_type == DocumentType.SCHEDULE:
            suggestions.extend(self._generate_schedule_suggestions(analysis, user_context))
        elif document_type == DocumentType.TRANSCRIPT:
            suggestions.extend(self._generate_transcript_suggestions(analysis, user_context))
        
        return suggestions
    
    def _generate_syllabus_suggestions(self, analysis: Dict[str, Any], 
                                     user_context: Optional[Dict] = None) -> List[str]:
        """Generate suggestions specific to syllabus documents"""
        suggestions = []
        
        course_info = analysis.get('course_info', {})
        requirements = analysis.get('requirements', {})
        grading_policy = analysis.get('grading_policy', {})
        
        # Course-specific suggestions
        if course_info.get('course_code'):
            suggestions.append(f"📚 I found this is for {course_info['course_code']}. I can help you find related textbooks in the library.")
        
        # Prerequisites suggestions
        if requirements.get('prerequisites'):
            suggestions.append("⚠️ Check that you've completed all prerequisites before enrolling.")
            suggestions.append("💡 I can verify your completed courses against the requirements.")
        
        # Textbook suggestions
        if requirements.get('textbooks'):
            suggestions.append("📖 I can help you find these required textbooks in the library or check their availability.")
        
        # Grading policy insights
        if grading_policy.get('breakdown'):
            total_exams = 0
            total_assignments = 0
            
            for item, percentage in grading_policy['breakdown'].items():
                if 'exam' in item.lower():
                    total_exams += int(percentage)
                elif any(word in item.lower() for word in ['assignment', 'homework', 'project']):
                    total_assignments += int(percentage)
            
            if total_exams > 50:
                suggestions.append("⚡ This course is exam-heavy. Consider forming study groups and scheduling regular review sessions.")
            elif total_assignments > 50:
                suggestions.append("📝 This course emphasizes assignments/projects. Plan your time management carefully.")
        
        # Study suggestions
        suggestions.append("🎯 I can help you find study groups, tutoring services, and related campus events for this subject.")
        suggestions.append("📅 Would you like me to help you create a study schedule based on the important dates?")
        
        return suggestions
    
    def _generate_assignment_suggestions(self, analysis: Dict[str, Any], 
                                       user_context: Optional[Dict] = None) -> List[str]:
        """Generate suggestions for assignment documents"""
        return [
            "📝 I can help you find relevant library resources for this assignment.",
            "⏰ Would you like me to set reminders for the due date?",
            "👥 I can help you find study groups or tutoring for this subject.",
            "📚 I can suggest related courses that might help with this topic."
        ]
    
    def _generate_schedule_suggestions(self, analysis: Dict[str, Any], 
                                     user_context: Optional[Dict] = None) -> List[str]:
        """Generate suggestions for schedule documents"""
        return [
            "📅 I can help you check for time conflicts with other courses.",
            "🎯 I can find events and activities that align with your schedule.",
            "📚 I can suggest optimal study times based on your class schedule.",
            "🏃‍♂️ Would you like suggestions for activities during your free periods?"
        ]
    
    def _generate_transcript_suggestions(self, analysis: Dict[str, Any], 
                                       user_context: Optional[Dict] = None) -> List[str]:
        """Generate suggestions for transcript analysis"""
        return [
            "🎓 I can suggest courses to improve your GPA in specific areas.",
            "📊 I can analyze your academic progress toward degree requirements.",
            "🎯 I can recommend courses based on your strongest subject areas.",
            "💼 I can suggest career paths that align with your completed coursework."
        ]
    
    def process_document(self, file_path: str, document_content: Optional[str] = None, 
                        user_context: Optional[Dict] = None) -> DocumentAnalysis:
        """Main method to process any document"""
        
        # Extract text based on file type or use provided content
        if document_content:
            extracted_text = document_content
        else:
            file_extension = file_path.lower().split('.')[-1]
            
            if file_extension in ['jpg', 'jpeg', 'png']:
                extracted_text = self.mock_extract_text_from_image(file_path)
            elif file_extension == 'pdf':
                extracted_text = self.mock_extract_text_from_pdf(file_path)
            elif file_extension in ['txt', 'docx']:
                # In production, would read actual file
                extracted_text = "Mock text content from document"
            else:
                extracted_text = "Unsupported file format"
        
        # Detect document type
        document_type = self.detect_document_type(extracted_text)
        confidence = 0.8  # Mock confidence score
        
        # Analyze based on document type
        key_information = {}
        if document_type == DocumentType.SYLLABUS:
            key_information = self.syllabus_analyzer.analyze_syllabus(extracted_text)
        
        # Generate suggestions
        suggestions = self.generate_suggestions(document_type, key_information, user_context)
        
        # Generate academic insights
        academic_insights = self._generate_academic_insights(document_type, key_information, user_context)
        
        # Find related resources
        related_resources = self._find_related_resources(document_type, key_information)
        
        return DocumentAnalysis(
            document_type=document_type,
            confidence=confidence,
            key_information=key_information,
            extracted_text=extracted_text,
            suggestions=suggestions,
            academic_insights=academic_insights,
            related_resources=related_resources
        )
    
    def _generate_academic_insights(self, document_type: DocumentType, 
                                  key_info: Dict[str, Any], 
                                  user_context: Optional[Dict] = None) -> List[str]:
        """Generate academic insights based on document analysis"""
        insights = []
        
        if document_type == DocumentType.SYLLABUS:
            course_info = key_info.get('course_info', {})
            grading_policy = key_info.get('grading_policy', {})
            
            # Course difficulty analysis
            if 'breakdown' in grading_policy:
                exam_weight = sum(int(v) for k, v in grading_policy['breakdown'].items() 
                                if 'exam' in k.lower())
                if exam_weight > 60:
                    insights.append("🎯 This appears to be a theory-heavy course with significant exam components.")
                
                project_weight = sum(int(v) for k, v in grading_policy['breakdown'].items() 
                                   if any(word in k.lower() for word in ['project', 'assignment']))
                if project_weight > 50:
                    insights.append("🔨 This is a hands-on course with substantial project work.")
            
            # Prerequisites analysis
            if key_info.get('requirements', {}).get('prerequisites'):
                insights.append("📋 This course has prerequisites - ensure you have the foundational knowledge.")
        
        return insights
    
    def _find_related_resources(self, document_type: DocumentType, key_info: Dict[str, Any]) -> List[str]:
        """Find related library and academic resources"""
        resources = []
        
        if document_type == DocumentType.SYLLABUS:
            textbooks = key_info.get('requirements', {}).get('textbooks', '')
            if textbooks:
                resources.append(f"📚 Library search for: {textbooks}")
            
            course_code = key_info.get('course_info', {}).get('course_code', '')
            if course_code:
                resources.append(f"🔍 Related study materials for {course_code}")
                resources.append(f"👥 Study groups for {course_code}")
                resources.append(f"🎓 Tutoring services for {course_code}")
        
        return resources


# Main function to be used by agents
def analyze_document(file_path: str = None, document_text: str = None, 
                    file_type: str = "auto") -> str:
    """
    Main function for document analysis - to be used by SARAA agents
    
    Args:
        file_path: Path to the document file
        document_text: Direct text content (for demo purposes)
        file_type: Type of file (auto-detect if not specified)
    
    Returns:
        Formatted analysis results
    """
    processor = DocumentProcessor()
    
    # For demo purposes, use sample syllabus if no input provided
    if not file_path and not document_text:
        document_text = """
        CS301 - Artificial Intelligence
        Fall 2025 Syllabus
        
        Instructor: Dr. Sarah Williams
        Email: swilliams@university.edu
        Office Hours: MW 2-4 PM
        
        Course Description:
        Introduction to artificial intelligence concepts including search algorithms,
        knowledge representation, machine learning, and neural networks.
        
        Prerequisites: CS201 Data Structures and Algorithms, MATH201 Calculus II
        
        Textbook: "Artificial Intelligence: A Modern Approach" by Russell & Norvig
        
        Grading Policy:
        Assignments: 40%
        Midterm Exam: 25%
        Final Exam: 25%
        Participation: 10%
        
        Important Dates:
        - Assignment 1 Due: September 15, 2025
        - Midterm: October 15, 2025
        - Final Project Due: November 20, 2025
        - Final Exam: December 10, 2025
        """
    
    # Get user context (mock - in production would come from user profile)
    user_context = {
        "completed_courses": ["CS101", "CS201", "MATH201"],
        "major": "Computer Science",
        "interests": ["artificial intelligence", "machine learning"]
    }
    
    # Process the document
    if file_path:
        analysis = processor.process_document(file_path, user_context=user_context)
    else:
        analysis = processor.process_document("mock.txt", document_text, user_context)
    
    # Format the response
    response = f"📄 **Document Analysis Results**\n\n"
    response += f"**Document Type:** {analysis.document_type.value.replace('_', ' ').title()}\n"
    response += f"**Confidence:** {analysis.confidence:.1%}\n\n"
    
    # Show key information for syllabi
    if analysis.document_type == DocumentType.SYLLABUS and analysis.key_information:
        key_info = analysis.key_information
        
        response += "**📚 Course Information:**\n"
        course_info = key_info.get('course_info', {})
        if course_info.get('course_code'):
            response += f"- Course: {course_info['course_code']}\n"
        if course_info.get('title'):
            response += f"- Title: {course_info['title']}\n"
        
        instructor_info = key_info.get('instructor_info', {})
        if instructor_info.get('name'):
            response += f"- Instructor: {instructor_info['name']}\n"
        if instructor_info.get('email'):
            response += f"- Email: {instructor_info['email']}\n"
        if instructor_info.get('office_hours'):
            response += f"- Office Hours: {instructor_info['office_hours']}\n"
        
        requirements = key_info.get('requirements', {})
        if requirements.get('prerequisites'):
            response += f"- Prerequisites: {requirements['prerequisites']}\n"
        if requirements.get('textbooks'):
            response += f"- Textbooks: {requirements['textbooks']}\n"
        
        grading = key_info.get('grading_policy', {})
        if grading.get('breakdown'):
            response += "\n**📊 Grading Breakdown:**\n"
            for item, percentage in grading['breakdown'].items():
                response += f"- {item.title()}: {percentage}%\n"
        
        response += "\n"
    
    # Show suggestions
    if analysis.suggestions:
        response += "**💡 Personalized Suggestions:**\n"
        for suggestion in analysis.suggestions:
            response += f"- {suggestion}\n"
        response += "\n"
    
    # Show academic insights
    if analysis.academic_insights:
        response += "**🎯 Academic Insights:**\n"
        for insight in analysis.academic_insights:
            response += f"- {insight}\n"
        response += "\n"
    
    # Show related resources
    if analysis.related_resources:
        response += "**📚 Related Resources:**\n"
        for resource in analysis.related_resources:
            response += f"- {resource}\n"
    
    return response


def analyze_syllabus_image(image_description: str) -> str:
    """
    Specialized function for analyzing syllabus images
    For demo purposes, uses text description of image content
    """
    return analyze_document(document_text=image_description)


def analyze_assignment_pdf(pdf_description: str) -> str:
    """
    Specialized function for analyzing assignment PDFs
    For demo purposes, uses text description of PDF content
    """
    assignment_text = f"""
    CS301 Assignment 2: Machine Learning Implementation
    Due: October 1, 2025
    
    Task: Implement a neural network from scratch using Python
    Requirements:
    - Use only NumPy (no ML libraries)
    - Train on provided dataset
    - Achieve 85%+ accuracy
    - Submit code + report
    
    Grading Criteria:
    - Implementation: 60%
    - Performance: 25%  
    - Report: 15%
    
    Resources:
    - Chapter 4 of Russell & Norvig textbook
    - Lecture slides on neural networks
    - Office hours: MW 2-4 PM
    """
    
    return analyze_document(document_text=assignment_text)
