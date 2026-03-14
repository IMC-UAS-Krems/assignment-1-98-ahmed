"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""

from streaming.users import User


class Playlist:
    def __init__(self, playlist_id, name, playlist_owner):
        self.playlist_id=playlist_id
        self.name=name
        self.playlist_owner=playlist_owner
        self.tracks=[]
    def add_track(self, track):
        pass
    def remove_track(self, track_id): 
        pass
    def total_duration_seconds(self):
        pass

class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id, name, playlist_owner):
        super().__init__(playlist_id, name, playlist_owner)
        self.contributors=[]
    def add_contributor(self, user):
        pass
    def remove_contributor(self, user):
        pass