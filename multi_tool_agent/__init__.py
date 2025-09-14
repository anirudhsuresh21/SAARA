"""
SARAA (Student Academic Resource Assistant Agent)
A comprehensive AI assistant system for university students.

This package provides:
- Multi-domain student support (academic, library, events)
- Intelligent intent recognition and agent orchestration  
- Personalized recommendations with privacy controls
- Extensible architecture for university integration
"""

from .agent import saraa_agent, orchestrator
from .core import (
    CoreOrchestrator, 
    profile_database,
    personalization_engine
)

__version__ = "1.0.0"
__author__ = "SARAA Development Team"
