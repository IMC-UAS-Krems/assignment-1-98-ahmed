"""
artists.py
----------
Implement the Artist class representing musicians and content creators.

Classes to implement:
  - Artist
"""


class Artist:
    def __init__(self,artist_id, name, genre):
        from streaming.tracks import Track

        if not isinstance(artist_id, str) or not artist_id.strip():
            raise ValueError("Artist ID must be a non-empty string.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Artist name must be a non-empty string.")
        if not isinstance(genre, str) or not genre.strip():
            raise ValueError("Genre must be a non-empty string.")
        
        self.artist_id : str = artist_id
        self.name : str = name
        self.genre : str = genre
        self.tracks : list[Track] = []

    def __eq__(self, other):
        if not isinstance(other, Artist):
            return False
        return self.artist_id == other.artist_id

    def __repr__(self):
        return (
            f"Artist(artist_id={self.artist_id!r}, name={self.name!r}, genre={self.genre!r})"
        )


    def add_track(self, track):
        from streaming.tracks import Track
        if not isinstance(track, Track):
            raise ValueError("Track must be an instance of Track class.")
        for existing_track in self.tracks:
            if existing_track.track_id == track.track_id:
                raise ValueError("Track is already associated with this artist.")
        self.tracks.append(track)

    def track_count(self):
        return len(self.tracks)
