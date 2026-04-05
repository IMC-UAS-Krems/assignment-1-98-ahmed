"""
sessions.py
-----------
Implement the ListeningSession class for recording listening events.

Classes to implement:
  - ListeningSession
"""

from streaming.users import User
from streaming.tracks import Track
from datetime import datetime

class ListeningSession:
    
    def __init__(self,session_id, user, track, timestamp, duration_listened_seconds) -> None: 

        if not isinstance(session_id, str) or not session_id.strip():
            raise ValueError("Session ID must be a non-empty string.")
        if not isinstance(user, User):
            raise ValueError("User must be an instance of User class.")
        if not isinstance(track, Track):
            raise ValueError("Track must be an instance of Track class.")
        if not isinstance(timestamp, datetime):
            raise ValueError("Timestamp must be a valid datetime object.")
        if not isinstance(duration_listened_seconds, int) or duration_listened_seconds < 0:
            raise ValueError("Duration listened seconds must be a non-negative integer.")

        self.session_id : str = session_id
        self.user : User = user
        self.track : Track = track
        self.timestamp : datetime = timestamp
        self.duration_listened_seconds : int = duration_listened_seconds
    def __eq__(self, other) -> bool:
        if not isinstance(other, ListeningSession):
            return False
        return self.session_id == other.session_id
    
    def __repr__(self) -> str:
        return (
            f"ListeningSession(session_id={self.session_id!r}, "
            f"user={self.user!r}, "
            f"track={self.track!r}, "
            f"timestamp={self.timestamp!r}, "
            f"duration_listened_seconds={self.duration_listened_seconds})"
        )
    
    def duration_listened_minutes(self) -> float:
        return self.duration_listened_seconds / 60