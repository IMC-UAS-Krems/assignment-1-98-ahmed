"""
tracks.py
---------
Implement the class hierarchy for all playable content on the platform.

Classes to implement:
  - Track (abstract base class)
    - Song
      - SingleRelease
      - AlbumTrack
    - Podcast
      - InterviewEpisode
      - NarrativeEpisode
    - AudiobookTrack
"""

from datetime import date
from abc import ABC

#abstract base class for all tracks
class Track(ABC):
    def __init__(self,track_id, title, duration_seconds, genre):
        
        if not isinstance(track_id, str) or not track_id.strip():
            raise ValueError("Track ID must be a non-empty string.")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Track title must be a non-empty string.")
        if not isinstance(duration_seconds, int) or duration_seconds < 0:
            raise ValueError("Duration must be a non-negative integer.")
        if not isinstance(genre, str) or not genre.strip():
            raise ValueError("Genre must be a non-empty string.")
        
        self.track_id : str = track_id
        self.title : str = title
        self.duration_seconds : int = duration_seconds
        self.genre : str = genre
    
    def __eq__(self, other):
        if not isinstance(other, Track):
            return False
        return self.track_id == other.track_id
    
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"track_id={self.track_id!r}, "
            f"title={self.title!r}, "
            f"duration_seconds={self.duration_seconds!r}, "
            f"genre={self.genre!r})"
            )
    
    def duration_minutes(self) -> float:
        return self.duration_seconds / 60
        #pass

class AudiobookTrack(Track):
    def __init__(self, track_id, title, duration_seconds, genre, author, narrator):
        
        if not isinstance(author, str) or not author.strip():
            raise ValueError("Author must be a non-empty string.")
        if not isinstance(narrator, str) or not narrator.strip():
            raise ValueError("Narrator must be a non-empty string.")

        super().__init__(track_id, title, duration_seconds, genre)
        self.author : str = author
        self.narrator : str = narrator
    
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"track_id={self.track_id!r}, "
            f"title={self.title!r}, "
            f"duration_seconds={self.duration_seconds!r}, "
            f"genre={self.genre!r}, "
            f"author={self.author!r}, "
            f"narrator={self.narrator!r})"
            )

class Podcast(Track):
    def __init__(self, track_id, title, duration_seconds, genre, host, description=""):
        
        if not isinstance(host, str) or not host.strip():
            raise ValueError("Host must be a non-empty string.")
        if not isinstance(description, str):
            raise ValueError("Description must be a string.")
        
        super().__init__(track_id, title, duration_seconds, genre)
        self.host : str = host
        self.description : str = description

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"track_id={self.track_id!r}, "
            f"title={self.title!r}, "
            f"duration_seconds={self.duration_seconds!r}, "
            f"genre={self.genre!r}, "
            f"host={self.host!r}, "
            f"description={self.description!r})"
        )
   

class InterviewEpisode(Podcast):
    def __init__(self, track_id, title, duration_seconds, genre, host, guest, description=""):
        if not isinstance(guest, str) or not guest.strip():
            raise ValueError("Guest must be a non-empty string.")
        
        super().__init__(track_id, title, duration_seconds, genre, host, description)
        self.guest : str = guest
    
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"track_id={self.track_id!r}, "
            f"title={self.title!r}, "
            f"duration_seconds={self.duration_seconds!r}, "
            f"genre={self.genre!r}, "
            f"host={self.host!r}, "
            f"description={self.description!r}, "
            f"guest={self.guest!r})"
        )
    

class NarrativeEpisode(Podcast):
    def __init__(self, track_id, title, duration_seconds, genre, host, season, episode_number, description=""):
        
        if not isinstance(season, int) or season < 0:
            raise ValueError("Season must be a non-negative integer.")
        if not isinstance(episode_number, int) or episode_number < 0:
            raise ValueError("Episode number must be a non-negative integer.")
        
        super().__init__(track_id, title, duration_seconds, genre, host, description)
        self.season : int = season
        self.episode_number : int = episode_number
    
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"track_id={self.track_id!r}, "
            f"title={self.title!r}, "
            f"duration_seconds={self.duration_seconds!r}, "
            f"genre={self.genre!r}, "
            f"host={self.host!r}, "
            f"description={self.description!r}, "
            f"season={self.season!r}, "
            f"episode_number={self.episode_number!r})"
        )


class Song(Track):
    def __init__(self, track_id, title, duration_seconds, genre, artist):
        
        from streaming.artists import Artist
        if not isinstance(artist, Artist):
            raise ValueError("Artist must be an instance of Artist class.")
        super().__init__(track_id, title, duration_seconds, genre)
        self.artist = artist
    
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"track_id={self.track_id!r}, "
            f"title={self.title!r}, "
            f"duration_seconds={self.duration_seconds!r}, "
            f"genre={self.genre!r}, "
            f"artist={self.artist!r})"
        )
   
class SingleRelease(Song):
    def __init__(self, track_id, title, duration_seconds, genre, artist, release_date):
        if not isinstance(release_date, date):
            raise ValueError("Release date must be a valid date.")
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.release_date = release_date
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"track_id={self.track_id!r}, "
            f"title={self.title!r}, "
            f"duration_seconds={self.duration_seconds!r}, "
            f"genre={self.genre!r}, "
            f"artist={self.artist!r}, "
            f"release_date={self.release_date!r})"
        )
 

class AlbumTrack(Song):
    def __init__(self, track_id, title, duration_seconds, genre, artist, track_number, album = None):
        from streaming.albums import Album
        if album is not None and not isinstance(album, Album):
            raise ValueError("Album must be an instance of Album class.")
        if not isinstance(track_number, int) or track_number <= 0:
            raise ValueError("Track number must be a positive integer.")
        
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.track_number : int = track_number
        self.album : Album | None = album 
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"track_id={self.track_id!r}, "
            f"title={self.title!r}, "
            f"duration_seconds={self.duration_seconds!r}, "
            f"genre={self.genre!r}, "
            f"artist={self.artist!r}, "
            f"track_number={self.track_number!r}, "
            f"album={self.album!r})"
        )
 
  