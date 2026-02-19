"""
Student Profile Manager
Extracts and accumulates student profile information across conversation turns.
Tracks: grade, stream preference, location, interests, constraints.
"""

import re
from typing import Optional


class StudentProfile:
    def __init__(self):
        self.grade: Optional[str] = None
        self.stream: Optional[str] = None
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
            "grade": self.grade,
            "stream": self.stream,
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
        if self.grade:
            parts.append(f"Grade: {self.grade}")
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
        return self.grade is not None and (self.stream is not None or len(self.interests) > 0)


def extract_profile_from_text(text: str, profile: StudentProfile) -> StudentProfile:
    """
    Extract student profile information from conversation text.
    Updates and returns the profile object.
    """
    text_lower = text.lower()

    # Extract grade
    grade_patterns = [
        r'\b(class|grade|std|standard)\s*(\d{1,2})\b',
        r'\b(\d{1,2})(th|st|nd|rd)\s*(class|grade|std|standard)\b',
        r'\bin\s*(class|grade)\s*(\d{1,2})\b'
    ]
    for pattern in grade_patterns:
        match = re.search(pattern, text_lower)
        if match:
            # Get the numeric group
            groups = match.groups()
            for g in groups:
                if g and g.isdigit() and 8 <= int(g) <= 12:
                    profile.grade = g
                    break

    # Extract stream preferences
    stream_keywords = {
        "science": ["science", "pcm", "pcb", "physics", "chemistry", "biology", "math", "maths"],
        "commerce": ["commerce", "accounts", "accountancy", "business", "economics", "ca"],
        "arts": ["arts", "humanities", "history", "geography", "political science", "psychology"],
        "vocational": ["vocational", "iti", "polytechnic", "diploma", "skill", "trade"],
        "agriculture": ["agriculture", "farming", "agri", "horticulture"]
    }
    for stream, keywords in stream_keywords.items():
        if any(kw in text_lower for kw in keywords):
            profile.stream = stream
            break

    # Extract location
    indian_states = [
        "tamil nadu", "tamilnadu", "chennai", "coimbatore", "madurai",
        "andhra pradesh", "telangana", "hyderabad",
        "karnataka", "bangalore", "bengaluru",
        "kerala", "rajasthan", "maharashtra", "mumbai", "pune",
        "uttar pradesh", "delhi", "west bengal", "kolkata",
        "bihar", "gujarat", "ahmedabad", "madhya pradesh",
        "odisha", "assam", "punjab", "haryana"
    ]
    for loc in indian_states:
        if loc in text_lower:
            profile.location = loc.title()
            break

    # Extract interests
    interest_keywords = {
        "coding": ["coding", "programming", "software", "computer", "app", "web"],
        "medicine": ["doctor", "medical", "mbbs", "nurse", "nursing", "hospital", "healthcare"],
        "engineering": ["engineer", "engineering", "mechanical", "electrical", "civil", "it"],
        "art_design": ["design", "art", "drawing", "creative", "fashion"],
        "music": ["music", "singing", "dance", "performing"],
        "sports": ["sports", "cricket", "football", "athlete"],
        "business": ["business", "entrepreneur", "startup", "shop", "sell"],
        "teaching": ["teaching", "teacher", "education", "school"],
        "defence": ["army", "navy", "airforce", "defence", "police", "nda"]
    }
    for interest, keywords in interest_keywords.items():
        if any(kw in text_lower for kw in keywords) and interest not in profile.interests:
            profile.interests.append(interest)

    # Extract gender
    if any(w in text_lower for w in ["i am a girl", "i'm a girl", "female", "she", "daughter"]):
        profile.gender = "female"
    elif any(w in text_lower for w in ["i am a boy", "i'm a boy", "male", "he", "son"]):
        profile.gender = "male"

    # Extract category
    if "sc " in text_lower or "scheduled caste" in text_lower:
        profile.category = "SC"
    elif "st " in text_lower or "scheduled tribe" in text_lower:
        profile.category = "ST"
    elif "obc" in text_lower:
        profile.category = "OBC"

    # Extract financial constraints
    income_keywords = ["low income", "poor", "below poverty", "financial problem",
                       "can't afford", "cannot afford", "no money", "financial constraint"]
    if any(kw in text_lower for kw in income_keywords):
        if "financial constraint" not in profile.constraints:
            profile.constraints.append("financial constraint")

    # Extract other constraints
    if any(w in text_lower for w in ["rural", "village", "remote area"]):
        if "rural location" not in profile.constraints:
            profile.constraints.append("rural location")

    profile.conversation_turns += 1
    return profile
