"""
Module 2: Course Advisor Agent
Technology: Python, Pandas (for data manipulation), integration with Course Catalog DB

Purpose: Provide intelligent and personalized course recommendations
"""

from typing import List, Dict, Optional, Set
from dataclasses import dataclass
from enum import Enum


@dataclass
class Course:
    """Represents a course in the catalog"""
    course_id: str
    title: str
    description: str
    credits: int
    prerequisites: List[str]
    department: str
    level: str  # undergraduate, graduate
    semester_offered: List[str]  # fall, spring, summer
    time_slots: List[str]  # e.g., "MWF 9:00-9:50"
    professor: str
    max_enrollment: int
    current_enrollment: int
    keywords: List[str]  # for interest matching


@dataclass
class StudentProfile:
    """Represents a student's academic profile"""
    student_id: str
    name: str
    major: str
    minor: Optional[str]
    year: int  # 1-4 for undergrad
    gpa: float
    completed_courses: List[str]
    current_courses: List[str]
    interests: List[str]
    career_goals: List[str]
    time_preferences: Dict[str, str]  # e.g., {"no_morning": True}


class CourseDatabase:
    """Mock database for course catalog - in production would connect to SIS"""
    
    def __init__(self):
        # Mock course data
        self.courses = {
            "CS101": Course(
                course_id="CS101",
                title="Introduction to Computer Science",
                description="Fundamentals of programming and computer science",
                credits=3,
                prerequisites=[],
                department="Computer Science",
                level="undergraduate",
                semester_offered=["fall", "spring"],
                time_slots=["MWF 9:00-9:50", "TTH 14:00-15:15"],
                professor="Dr. Smith",
                max_enrollment=50,
                current_enrollment=45,
                keywords=["programming", "fundamentals", "python"]
            ),
            "CS201": Course(
                course_id="CS201",
                title="Data Structures and Algorithms",
                description="Study of fundamental data structures and algorithms",
                credits=4,
                prerequisites=["CS101"],
                department="Computer Science",
                level="undergraduate",
                semester_offered=["fall", "spring"],
                time_slots=["MWF 11:00-11:50", "TTH 9:30-10:45"],
                professor="Dr. Johnson",
                max_enrollment=40,
                current_enrollment=38,
                keywords=["algorithms", "data structures", "programming"]
            ),
            "CS301": Course(
                course_id="CS301",
                title="Artificial Intelligence",
                description="Introduction to AI concepts and techniques",
                credits=3,
                prerequisites=["CS201"],
                department="Computer Science",
                level="undergraduate",
                semester_offered=["spring"],
                time_slots=["TTH 15:30-16:45"],
                professor="Dr. Williams",
                max_enrollment=30,
                current_enrollment=25,
                keywords=["ai", "machine learning", "neural networks"]
            ),
            "CS401": Course(
                course_id="CS401",
                title="Advanced Machine Learning",
                description="Advanced topics in machine learning and deep learning",
                credits=3,
                prerequisites=["CS301"],
                department="Computer Science",
                level="undergraduate",
                semester_offered=["fall"],
                time_slots=["MW 16:00-17:15"],
                professor="Dr. Chen",
                max_enrollment=25,
                current_enrollment=20,
                keywords=["machine learning", "deep learning", "ai", "neural networks"]
            ),
            "MATH201": Course(
                course_id="MATH201",
                title="Calculus II",
                description="Integral calculus and series",
                credits=4,
                prerequisites=["MATH101"],
                department="Mathematics",
                level="undergraduate",
                semester_offered=["fall", "spring"],
                time_slots=["MWF 8:00-8:50", "TTH 13:00-14:15"],
                professor="Dr. Davis",
                max_enrollment=60,
                current_enrollment=55,
                keywords=["calculus", "mathematics", "integration"]
            )
        }
    
    def get_course(self, course_id: str) -> Optional[Course]:
        """Get a course by ID"""
        return self.courses.get(course_id)
    
    def search_courses(self, **kwargs) -> List[Course]:
        """Search courses by various criteria"""
        results = list(self.courses.values())
        
        if 'department' in kwargs:
            results = [c for c in results if c.department.lower() == kwargs['department'].lower()]
        
        if 'level' in kwargs:
            results = [c for c in results if c.level == kwargs['level']]
            
        if 'semester' in kwargs:
            results = [c for c in results if kwargs['semester'] in c.semester_offered]
        
        if 'keywords' in kwargs:
            search_keywords = [k.lower() for k in kwargs['keywords']]
            results = [c for c in results if any(
                any(sk in ck.lower() for ck in c.keywords) for sk in search_keywords
            )]
        
        return results


class PrerequisiteChecker:
    """Handles prerequisite validation logic"""
    
    def __init__(self, course_db: CourseDatabase):
        self.course_db = course_db
    
    def check_prerequisites(self, course_id: str, completed_courses: List[str]) -> bool:
        """Check if student has completed all prerequisites for a course"""
        course = self.course_db.get_course(course_id)
        if not course:
            return False
        
        completed_set = set(completed_courses)
        required_set = set(course.prerequisites)
        
        return required_set.issubset(completed_set)
    
    def get_missing_prerequisites(self, course_id: str, completed_courses: List[str]) -> List[str]:
        """Get list of missing prerequisites for a course"""
        course = self.course_db.get_course(course_id)
        if not course:
            return []
        
        completed_set = set(completed_courses)
        required_set = set(course.prerequisites)
        
        return list(required_set - completed_set)


class ConstraintFilter:
    """Filters courses based on student constraints"""
    
    @staticmethod
    def filter_by_time_constraints(courses: List[Course], constraints: Dict[str, any]) -> List[Course]:
        """Filter courses based on time preferences"""
        filtered = []
        
        for course in courses:
            include_course = True
            
            # Check for morning class avoidance
            if constraints.get('no_morning'):
                for time_slot in course.time_slots:
                    if any(morning_time in time_slot for morning_time in ['8:', '9:', '10:']):
                        include_course = False
                        break
            
            # Check for specific time requirements
            if 'required_times' in constraints:
                required_times = constraints['required_times']
                if not any(req_time in time_slot for time_slot in course.time_slots 
                          for req_time in required_times):
                    include_course = False
            
            if include_course:
                filtered.append(course)
        
        return filtered
    
    @staticmethod
    def filter_by_credits(courses: List[Course], min_credits: int = 0, max_credits: int = 6) -> List[Course]:
        """Filter courses by credit hours"""
        return [c for c in courses if min_credits <= c.credits <= max_credits]
    
    @staticmethod
    def filter_by_enrollment(courses: List[Course], require_availability: bool = True) -> List[Course]:
        """Filter out courses that are full"""
        if not require_availability:
            return courses
        
        return [c for c in courses if c.current_enrollment < c.max_enrollment]


class InterestMatcher:
    """Matches courses to student interests using keyword analysis"""
    
    def __init__(self):
        self.interest_keywords = {
            'data science': ['data', 'statistics', 'machine learning', 'analytics'],
            'cybersecurity': ['security', 'cryptography', 'network', 'privacy'],
            'robotics': ['robotics', 'automation', 'control systems', 'sensors'],
            'web development': ['web', 'frontend', 'backend', 'javascript', 'html'],
            'artificial intelligence': ['ai', 'machine learning', 'neural networks', 'nlp'],
            'software engineering': ['software', 'engineering', 'design patterns', 'testing']
        }
    
    def score_course_interest(self, course: Course, student_interests: List[str]) -> float:
        """Score how well a course matches student interests (0-1 scale)"""
        if not student_interests:
            return 0.5  # neutral score
        
        total_score = 0
        for interest in student_interests:
            interest_lower = interest.lower()
            
            # Direct keyword match in course keywords
            course_keywords_lower = [k.lower() for k in course.keywords]
            if interest_lower in course_keywords_lower:
                total_score += 1.0
                continue
            
            # Check against interest keyword mappings
            related_keywords = self.interest_keywords.get(interest_lower, [interest_lower])
            keyword_matches = sum(1 for keyword in related_keywords 
                                if any(keyword in ck for ck in course_keywords_lower))
            
            if keyword_matches > 0:
                total_score += min(1.0, keyword_matches / len(related_keywords))
        
        return min(1.0, total_score / len(student_interests))


class CareerPathAdvisor:
    """Provides career-aligned course recommendations"""
    
    def __init__(self):
        self.career_paths = {
            'software engineer': ['CS201', 'CS301', 'CS350'],  # Data Structures, AI, Software Engineering
            'data scientist': ['CS301', 'MATH201', 'STAT301'],  # AI, Calculus, Statistics
            'cybersecurity analyst': ['CS201', 'CS400', 'CS450'],  # Data Structures, Security, Network Security
            'research scientist': ['CS301', 'CS401', 'MATH301'],  # AI, Advanced ML, Advanced Math
        }
    
    def recommend_courses_for_career(self, career_goal: str, completed_courses: List[str]) -> List[str]:
        """Recommend courses based on career goals"""
        career_goal_lower = career_goal.lower()
        
        # Find matching career path
        matching_path = None
        for path, courses in self.career_paths.items():
            if career_goal_lower in path or any(word in path for word in career_goal_lower.split()):
                matching_path = courses
                break
        
        if not matching_path:
            return []
        
        # Filter out already completed courses
        completed_set = set(completed_courses)
        return [course for course in matching_path if course not in completed_set]


class CourseAdvisorAgent:
    """Main course advisor agent that combines all components"""
    
    def __init__(self):
        self.course_db = CourseDatabase()
        self.prerequisite_checker = PrerequisiteChecker(self.course_db)
        self.constraint_filter = ConstraintFilter()
        self.interest_matcher = InterestMatcher()
        self.career_advisor = CareerPathAdvisor()
    
    def get_personalized_recommendations(self, 
                                       student_profile: StudentProfile,
                                       semester: str = "spring",
                                       constraints: Optional[Dict] = None) -> List[Dict]:
        """Get personalized course recommendations for a student"""
        
        if constraints is None:
            constraints = {}
        
        # Start with all courses for the semester
        available_courses = self.course_db.search_courses(semester=semester)
        
        # Filter by prerequisites
        eligible_courses = []
        for course in available_courses:
            if self.prerequisite_checker.check_prerequisites(course.course_id, student_profile.completed_courses):
                eligible_courses.append(course)
        
        # Apply constraint filters
        if constraints:
            eligible_courses = self.constraint_filter.filter_by_time_constraints(
                eligible_courses, constraints
            )
            
            if 'min_credits' in constraints or 'max_credits' in constraints:
                min_cred = constraints.get('min_credits', 0)
                max_cred = constraints.get('max_credits', 6)
                eligible_courses = self.constraint_filter.filter_by_credits(
                    eligible_courses, min_cred, max_cred
                )
        
        # Filter by enrollment availability
        eligible_courses = self.constraint_filter.filter_by_enrollment(eligible_courses)
        
        # Score courses by interest match
        recommendations = []
        for course in eligible_courses:
            interest_score = self.interest_matcher.score_course_interest(
                course, student_profile.interests
            )
            
            recommendations.append({
                'course': course,
                'interest_score': interest_score,
                'reason': self._generate_recommendation_reason(course, student_profile, interest_score)
            })
        
        # Sort by interest score (highest first)
        recommendations.sort(key=lambda x: x['interest_score'], reverse=True)
        
        return recommendations[:10]  # Return top 10 recommendations
    
    def get_career_path_courses(self, student_profile: StudentProfile) -> Dict[str, List[str]]:
        """Get course recommendations based on career goals"""
        career_recommendations = {}
        
        for career_goal in student_profile.career_goals:
            recommended_courses = self.career_advisor.recommend_courses_for_career(
                career_goal, student_profile.completed_courses
            )
            career_recommendations[career_goal] = recommended_courses
        
        return career_recommendations
    
    def _generate_recommendation_reason(self, course: Course, profile: StudentProfile, interest_score: float) -> str:
        """Generate explanation for why a course is recommended"""
        reasons = []
        
        if interest_score > 0.7:
            reasons.append(f"Strongly matches your interests in {', '.join(profile.interests)}")
        elif interest_score > 0.4:
            reasons.append(f"Aligns with your interests in {', '.join(profile.interests)}")
        
        if course.department == profile.major:
            reasons.append("Required for your major")
        
        if course.level == "undergraduate" and profile.year >= 3:
            reasons.append("Advanced course suitable for your academic level")
        
        available_spots = course.max_enrollment - course.current_enrollment
        if available_spots <= 5:
            reasons.append(f"Limited availability ({available_spots} spots remaining)")
        
        return "; ".join(reasons) if reasons else "General elective option"


def search_courses_by_query(query: str, student_profile: Optional[StudentProfile] = None) -> str:
    """
    Main function to be used by the agent - searches for courses based on natural language query
    """
    advisor = CourseAdvisorAgent()
    
    # Parse query for key information
    query_lower = query.lower()
    
    # Extract semester if mentioned
    semester = "spring"  # default
    if "fall" in query_lower:
        semester = "fall"
    elif "summer" in query_lower:
        semester = "summer"
    
    # Extract constraints
    constraints = {}
    if "morning" in query_lower and ("no" in query_lower or "not" in query_lower):
        constraints['no_morning'] = True
    
    # Extract subject/department
    department = None
    if "ai" in query_lower or "artificial intelligence" in query_lower:
        keywords = ["ai", "machine learning"]
    elif "computer science" in query_lower or "cs" in query_lower:
        department = "Computer Science"
        keywords = None
    else:
        keywords = None
    
    # Search courses
    search_params = {'semester': semester}
    if department:
        search_params['department'] = department
    if keywords:
        search_params['keywords'] = keywords
    
    courses = advisor.course_db.search_courses(**search_params)
    
    # If student profile is available, get personalized recommendations
    if student_profile:
        recommendations = advisor.get_personalized_recommendations(
            student_profile, semester, constraints
        )
        
        if not recommendations:
            return "No courses found matching your criteria and prerequisites."
        
        response = f"Here are personalized course recommendations for {semester} semester:\n\n"
        for rec in recommendations[:5]:  # Top 5
            course = rec['course']
            response += f"**{course.title}** ({course.course_id})\n"
            response += f"- Credits: {course.credits}\n"
            response += f"- Time: {', '.join(course.time_slots)}\n"
            response += f"- Professor: {course.professor}\n"
            response += f"- Available: {course.max_enrollment - course.current_enrollment} spots\n"
            response += f"- Why recommended: {rec['reason']}\n\n"
    else:
        # Generic search without personalization
        if not courses:
            return "No courses found matching your search criteria."
        
        response = f"Found {len(courses)} courses for {semester} semester:\n\n"
        for course in courses[:5]:  # Top 5
            response += f"**{course.title}** ({course.course_id})\n"
            response += f"- Credits: {course.credits}\n"
            response += f"- Time: {', '.join(course.time_slots)}\n"
            response += f"- Professor: {course.professor}\n"
            response += f"- Description: {course.description}\n\n"
    
    return response
