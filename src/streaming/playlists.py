"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""

from streaming.users import User
from streaming.tracks import Track

class Playlist:
    def __init__(self, playlist_id, name, owner) -> None:

        if not isinstance(playlist_id, str) or not playlist_id.strip():
            raise ValueError("Playlist ID must be a non-empty string.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Playlist name must be a non-empty string.")
        if not isinstance(owner, User):
            raise ValueError("Playlist owner must be a valid User.")

        self.playlist_id : str = playlist_id
        self.name : str = name
        self.owner : User = owner
        self.tracks : list[Track] = []
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Playlist):
            return False
        return self.playlist_id == other.playlist_id

    def __repr__(self) -> str:
        return (
            f"Playlist(playlist_id={self.playlist_id!r}, "
            f"name={self.name!r}, "
            f"owner={self.owner!r}, "
            f"tracks={len(self.tracks)})"
        )
    
    def add_track(self, track) -> None:
        if not isinstance(track, Track):
            raise ValueError("Track must be an instance of Track class.")
        for existing_track in self.tracks:
            if existing_track.track_id == track.track_id:
                return
        self.tracks.append(track)

    def remove_track(self, track_id) -> None: 
        if not isinstance(track_id, str) or not track_id.strip():
            raise ValueError("Track ID must be a non-empty string.")
        
        for track in self.tracks:
            if track.track_id == track_id:
                self.tracks.remove(track)
                return

    def total_duration_seconds(self) -> int:
        return sum(track.duration_seconds for track in self.tracks)



class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id, name, owner) -> None:
        super().__init__(playlist_id, name, owner)
        self.contributors : list[User] = [owner]
    
    def __repr__(self) -> str:
        return (
            f"CollaborativePlaylist(playlist_id={self.playlist_id!r}, "
            f"name={self.name!r}, "
            f"owner={self.owner!r}, "
            f"tracks={len(self.tracks)}, "
            f"contributors={len(self.contributors)})"
        )
        
    def add_contributor(self, user) -> None:
        if not isinstance(user, User):
            raise ValueError("Contributor must be a valid User.")
        for contributor in self.contributors:
            if contributor.user_id == user.user_id:
                return
        self.contributors.append(user)

    
    def remove_contributor(self, user) -> None:
        if not isinstance(user, User):
            raise ValueError("Contributor must be a valid User.")
        
        if user.user_id == self.owner.user_id:
            return
                
        for contributor in self.contributors:
            if contributor.user_id == user.user_id:
                self.contributors.remove(contributor)
                return
            
            