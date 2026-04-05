"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
"""

from typing import Set
from streaming.artists import Artist
from streaming.tracks import AlbumTrack

class Album:
    def __init__(self, album_id, title, artist, release_year):

        if not isinstance(album_id, str) or not album_id.strip():
            raise ValueError("Album ID must be a non-empty string.")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Album title must be a non-empty string.")
        if not isinstance(artist, Artist):
            raise ValueError("Artist must be an instance of Artist class.")
        if not isinstance(release_year, int) or release_year < 0:
            raise ValueError("Release year must be a non-negative integer.")
        
        self.album_id : str =album_id
        self.title : str =title
        self.artist : Artist = artist
        self.release_year : int = release_year
        self.tracks : list[AlbumTrack] = []
    
    def __eq__(self, other):
        if not isinstance(other, Album):
            return False
        return self.album_id == other.album_id
    
    def __repr__(self) -> str:
        return (
            f"Album(album_id={self.album_id!r}, title={self.title!r}, "
            f"artist={self.artist!r}, release_year={self.release_year!r}, "
            f"tracks={len(self.tracks)})"
        )

    def add_track(self, track):
        if not isinstance(track, AlbumTrack):
            raise ValueError("Track must be an instance of AlbumTrack class.")
        for existing_track in self.tracks:
            if existing_track.track_id == track.track_id:
                raise ValueError("Track is already in the album.")
        track.album = self
        self.tracks.append(track)
        self.tracks.sort(key=lambda t: t.track_number)
    
    def track_ids(self) -> Set[str]:
        return {track.track_id for track in self.tracks}
    
    def duration_seconds(self) -> int:
        return sum(track.duration_seconds for track in self.tracks)
