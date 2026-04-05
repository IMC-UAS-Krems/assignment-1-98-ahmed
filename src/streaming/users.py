"""
users.py
--------
Implement the class hierarchy for platform users.

Classes to implement:
  - User (base class)
    - FreeUser
    - PremiumUser
    - FamilyAccountUser
    - FamilyMember
"""

class User :
    def __init__(self,user_id, name, age):
        from streaming.sessions import ListeningSession        
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("User ID must be a non-empty string.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string.")
        if not isinstance(age, int) or age < 0:
            raise ValueError("Age must be a non-negative integer.")
        
        self.user_id : str = user_id
        self.name : str = name
        self.age : int = age
        self.sessions : list[ListeningSession] = []

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return (
            self.user_id == other.user_id
            and self.name == other.name
            and self.age == other.age
        )
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}" 
            f"(user_id={self.user_id!r}," 
            f"name={self.name!r}," 
            f"age={self.age!r})"
        )

    def add_session(self, session) :
        from streaming.sessions import ListeningSession
        if not isinstance(session, ListeningSession):
            raise ValueError("Session must be an instance of ListeningSession class.")
        self.sessions.append(session)
    
    def total_listening_seconds (self) -> int:
        return sum(session.duration_listened_seconds for session in self.sessions)
    
    def total_listening_minutes(self) -> float:
        return self.total_listening_seconds() / 60
    
    def unique_tracks_listened(self) -> set[str] :
        return set(session.track.track_id for session in self.sessions)
    

class FreeUser(User) :
    def __init__(self, user_id, name, age):
        super().__init__(user_id, name, age)
        self.max_skips_per_hour = 6
    
    def __repr__(self):
        return (
            f"FreeUser(user_id={self.user_id!r}, name={self.name!r}, "
            f"age={self.age!r}, max_skips_per_hour={self.max_skips_per_hour!r})"
        )


class PremiumUser(User) : 
    def __init__(self, user_id, name, age, subscription_start):
        from datetime import date  
        if not isinstance(subscription_start, date):
            raise ValueError("Subscription start must be a valid date")
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start
    def __repr__(self):
        return (
            f"PremiumUser(user_id={self.user_id!r}, name={self.name!r}, "
            f"age={self.age!r}, subscription_start={self.subscription_start!r})"
        )


class FamilyAccountUser(User) :
    def __init__(self, user_id, name, age):
        super().__init__(user_id, name, age)
        self.sub_users : list[FamilyMember] = []
    
    def add_sub_user(self,sub_user):
        if not isinstance(sub_user, FamilyMember):
            raise ValueError("Sub-user must be an instance of FamilyMember class.")
        if sub_user.parent is not self:
            raise ValueError("Sub-user's parent must be the FamilyAccountUser.")   
        if sub_user in self.sub_users:
            raise ValueError("Sub-user already exists in this family account.")    
        self.sub_users.append(sub_user)
    
    def all_members(self) :
        return [self] + self.sub_users
    
    def __repr__(self):
        return (
            f"FamilyAccountUser(user_id={self.user_id!r}, name={self.name!r}, "
            f"age={self.age!r}, sub_users={len(self.sub_users)!r})"
        )

    
class FamilyMember(User) :
    def __init__(self, user_id, name, age, parent):
        super().__init__(user_id, name, age)
        if not isinstance(parent, FamilyAccountUser):
            raise ValueError("Parent must be an instance of FamilyAccountUser class.")
        self.parent = parent
    def __repr__(self):
        return (
            f"FamilyMember(user_id={self.user_id!r}, name={self.name!r}, "
            f"age={self.age!r}, parent={self.parent.user_id!r})"
        )



