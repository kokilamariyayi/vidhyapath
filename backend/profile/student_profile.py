"""
Student Profile Manager
Extracts and accumulates student profile information across conversation turns.
Tracks: grade, stream preference, location, interests, constraints.
"""

import re
import json
import os
import logging
from typing import Optional
from groq import Groq

logger = logging.getLogger(__name__)


class StudentProfile:
    def __init__(self):
        self.user_type: Optional[str] = None  # school_student, college_student, parent, job_seeker, professional, entrepreneur
        self.grade: Optional[str] = None
        self.stream: Optional[str] = None
        self.degree: Optional[str] = None
        self.location: Optional[str] = None
        self.interests: list = []
        self.constraints: list = []
        self.gender: Optional[str] = None
        self.category: Optional[str] = None  # SC/ST/OBC/General
        self.family_income: Optional[str] = None
        self.conversation_turns: int = 0
        self.detected_emotions: list = []

    def to_dict(self) -> dict:
        return {
            "user_type": self.user_type,
            "grade": self.grade,
            "stream": self.stream,
            "degree": self.degree,
            "location": self.location,
            "interests": self.interests,
            "constraints": self.constraints,
            "gender": self.gender,
            "category": self.category,
            "family_income": self.family_income,
            "conversation_turns": self.conversation_turns
        }

    def to_context_string(self) -> str:
        """Convert profile to a context string for LLM prompts."""
        parts = []
        if self.user_type:
            parts.append(f"User Type: {self.user_type}")
        if self.grade:
            parts.append(f"Grade: {self.grade}")
        if self.degree:
            parts.append(f"Degree/Qualification: {self.degree}")
        if self.stream:
            parts.append(f"Stream Interest: {self.stream}")
        if self.location:
            parts.append(f"Location: {self.location}")
        if self.interests:
            parts.append(f"Interests: {', '.join(self.interests)}")
        if self.constraints:
            parts.append(f"Constraints/Concerns: {', '.join(self.constraints)}")
        if self.gender:
            parts.append(f"Gender: {self.gender}")
        if self.category:
            parts.append(f"Category: {self.category}")
        if self.family_income:
            parts.append(f"Family Income: {self.family_income}")

        if not parts:
            return "No profile information collected yet."
        return " | ".join(parts)

    def is_complete_enough(self) -> bool:
        """Check if we have enough info to give good recommendations."""
        return (self.grade is not None or self.user_type is not None) and (self.stream is not None or len(self.interests) > 0 or self.degree is not None)


def extract_profile_from_text(text: str, profile: StudentProfile) -> StudentProfile:
    """
    Extract student profile information using AI (Groq).
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        logger.warning("GROQ_API_KEY not found. Skipping AI profile extraction.")
        return profile

    try:
        client = Groq(api_key=api_key)
        
        # System prompt for extraction
        system_prompt = f"""
        Extract student profile details from the following user message. 
        Only update fields that are explicitly mentioned or strongly implied.
        
        Current Profile: {json.dumps(profile.to_dict())}
        
        Fields to extract:
        - user_type: school_student, college_student, parent, job_seeker, professional, entrepreneur
        - grade: e.g., "10", "12" (only if numeric and between 8-12)
        - stream: science, commerce, arts, vocational, agriculture
        - degree: e.g., "B.Tech", "B.Com", "MBBS"
        - location: Indian city or state
        - gender: male, female
        - category: SC, ST, OBC, General
        - family_income: e.g., "low", "high", or specific amount if mentioned
        - interests: list of strings (e.g., ["coding", "medicine"])
        - constraints: list of strings (e.g., ["financial"])

        IMPORTANT: If the user is asking ABOUT a gender (e.g., "schemes for women"), do NOT set their gender to female unless they say "I am a girl" or "As a woman".
        
        Return ONLY a valid JSON object with the keys above. Do not include any explanations.
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0,
            response_format={"type": "json_object"}
        )

        extracted_data = json.loads(response.choices[0].message.content)
        
        # Update profile with extracted data
        if "user_type" in extracted_data: profile.user_type = extracted_data["user_type"]
        if "grade" in extracted_data: profile.grade = str(extracted_data["grade"])
        if "stream" in extracted_data: profile.stream = extracted_data["stream"]
        if "degree" in extracted_data: profile.degree = extracted_data["degree"]
        if "location" in extracted_data: profile.location = extracted_data["location"]
        if "gender" in extracted_data: profile.gender = extracted_data["gender"]
        if "category" in extracted_data: profile.category = extracted_data["category"]
        if "family_income" in extracted_data: profile.family_income = extracted_data["family_income"]
        
        if "interests" in extracted_data:
            for item in extracted_data["interests"]:
                if item not in profile.interests:
                    profile.interests.append(item)
        
        if "constraints" in extracted_data:
            for item in extracted_data["constraints"]:
                if item not in profile.constraints:
                    profile.constraints.append(item)

    except Exception as e:
        logger.error(f"AI Profile extraction failed: {e}")

    profile.conversation_turns += 1
    return profile
