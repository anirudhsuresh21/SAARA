# SARAA Core Module
# Contains the orchestrator and user profile management

from .orchestrator import CoreOrchestrator, IntentRecognizer, ResponseSynthesizer
from .user_profile import (
    UserProfile, 
    AcademicRecord, 
    PersonalPreferences,
    profile_database,
    personalization_engine,
    get_user_profile_info,
    update_user_preferences
)
