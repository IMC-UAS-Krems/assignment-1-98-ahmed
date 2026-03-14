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
from streaming.sessions import ListeningSession

class User:
    def __init__(self,user_id, name, age):
        self.user_id=user_id
        self.name=name
        self.age=age
        self.sessions=[]
    def add_session(self, session):
        pass
    def total_listening_seconds (self):
        pass
    def total_listening_minutes(self):
        pass
    def unique_tracks_listened(self):
        pass



class FreeUser(User):
    def __init__(self, user_id, name, age):
        super().__init__(user_id, name, age)
        self.max_skips_per_hour=6



class PremiumUser(User):   
    def __init__(self, user_id, name, age):
        super().__init__(user_id, name, age)
        self.subscription_start=self.subscription_start


class FamilyAccountUser(User):
    def __init__(self, user_id, name, age):
        super().__init__(user_id, name, age)
        self.sub_users=[]
    def add_sub_user(self,sub_user):
        pass
    def all_members(self):
        pass

class FamilyMember(User):
    def __init__(self, user_id, name, age):
        super().__init__(user_id, name, age)
        self.parent=FamilyAccountUser(user_id, name, age)
