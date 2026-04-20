"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""

from streaming.users import User
from streaming.tracks import Track
from streaming.albums import Album
from streaming.artists import Artist
from streaming.playlists import Playlist
from streaming.sessions import ListeningSession
from streaming.playlists import CollaborativePlaylist
from datetime import datetime,timedelta

class StreamingPlatform:
    def __init__(self, name : str) -> None:

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Platform name must be a non-empty string.")
        
        self.name : str = name
        self._catalogue  : dict[str, Track] = {}
        self._users : dict[str, User] = {}
        self._artists : dict[str, Artist] = {}
        self._albums : dict[str, Album] = {}
        self._playlists : dict[str, Playlist] = {}
        self._sessions : list[ListeningSession] = []
    
    def __repr__(self) -> str:
        return (
            f"StreamingPlatform(name={self.name!r}, "
            f"tracks={len(self._catalogue)}, "
            f"users={len(self._users)}, "
            f"artists={len(self._artists)}, "
            f"albums={len(self._albums)}, "
            f"playlists={len(self._playlists)}, "
            f"sessions={len(self._sessions)})"   
        )

    def add_track(self, track : Track) -> None:
        if not isinstance(track, Track):
            raise ValueError("Track must be an instance of Track class.")
        if track.track_id in self._catalogue:
            raise ValueError(f"Track with ID {track.track_id} already exists.")
        self._catalogue[track.track_id] = track

    def add_user(self, user : User) -> None:
        
        if not isinstance(user, User):
            raise ValueError("User must be an instance of User class.")
        
        if user.user_id in self._users:
            raise ValueError(f"User with ID {user.user_id} already exists.")
        self._users[user.user_id] = user
   
    def add_artist(self, artist : Artist) -> None:
        if not isinstance(artist, Artist):
            raise ValueError("Artist must be an instance of Artist class.")
        if artist.artist_id in self._artists:
            raise ValueError(f"Artist with ID {artist.artist_id} already exists.")
        self._artists[artist.artist_id] = artist
   
    def add_album(self, album : Album) -> None:
        if not isinstance(album , Album):
            raise ValueError("Album must be an instance of Album class.")
        if album.album_id in self._albums:
            raise ValueError(f"Album with ID {album.album_id} already exists.")
        self._albums[album.album_id] = album
   
    def add_playlist(self, playlist : Playlist) -> None:
        if not isinstance(playlist, Playlist):
            raise ValueError("Playlist must be an instance of Playlist class.")
        if playlist.playlist_id in self._playlists:
            raise ValueError(f"Playlist with ID {playlist.playlist_id} already exists.")
        self._playlists[playlist.playlist_id] = playlist
   
    def record_session(self, session : ListeningSession) -> None:
        if not isinstance(session, ListeningSession):
            raise ValueError("Session must be an instance of ListeningSession class.")
        if session.user.user_id not in self._users:
            raise ValueError(f"User with ID {session.user.user_id} does not exist.")
        if session.track.track_id not in self._catalogue:
            raise ValueError(f"Track with ID {session.track.track_id} does not exist.")
        self._sessions.append(session)
        session.user.add_session(session)

    
    def get_track(self, track_id : str) -> Track | None:
        return self._catalogue.get(track_id)
   
    def get_user(self, user_id : str) -> User | None:
        return self._users.get(user_id)
   

    def get_artist(self, artist_id : str) -> Artist | None:
        return self._artists.get(artist_id)
   
    def get_album(self, album_id : str) -> Album | None:
        return self._albums.get(album_id)
   

    def all_users(self) -> list[User]:
        return list(self._users.values())
   
   
    def all_tracks(self) -> list[Track]:
        return list(self._catalogue.values())
    
#Query methods for analytics:
#Q1
    """
    Q1: Total Cumulative Listening Time
    Method: total_listening_time_minutes(start: datetime, end: datetime) -> float
    Return the total cumulative listening time (in minutes) across all users 
    for a given time period. Sum up the listening duration for all sessions 
    that fall within the specified datetime window (inclusive on both ends). """

    def total_listening_time_minutes(self,start : datetime, end : datetime) -> float:
        if not isinstance(start, datetime) or not isinstance(end, datetime):
            raise ValueError("Start and end must be valid datetime objects.")
        if start > end:
            raise ValueError("Start datetime must be before end datetime.")
        total_seconds : int = 0
        for session in self._sessions:
            if start <= session.timestamp <= end:
                total_seconds += session.duration_listened_seconds
        return total_seconds / 60.0

#Q2
    """
    Q2: Average Unique Tracks per Premium User
    Method: avg_unique_tracks_per_premium_user(days: int = 30) -> float
    Compute the average number of unique tracks listened to per PremiumUser 
    in the last days days (default 30). Only count distinct 
    tracks for sessions within the time window. Return 0.0 if there are no premium users.
    """

    def avg_unique_tracks_per_premium_user(self, days : int = 30) -> float:
        from streaming.users import PremiumUser
        if not isinstance(days, int) or days <= 0:
            raise ValueError("Days must be a positive integer.")
        PremiumUsers : list[PremiumUser] = [user for user in self._users.values() if isinstance(user, PremiumUser)]
        unique_tracks_count : int = 0
        if not PremiumUsers:
            return 0.0
        now = datetime.now()
        for user in PremiumUsers:
            unique_tracks : set[str] = set()
            for session in user.sessions:
                if timedelta(0) <= now - session.timestamp <= timedelta(days=days):
                    unique_tracks.add(session.track.track_id)
            unique_tracks_count += len(unique_tracks)
        avg_unique_tracks_per_premium_user = unique_tracks_count / len(PremiumUsers)
        return avg_unique_tracks_per_premium_user

#Q3

    """
    Q3: Track with Most Distinct Listeners
    Method: track_with_most_distinct_listeners() -> Track | None
    Return the track with the highest number of distinct listeners (not total plays) 
    in the catalogue. Count the number of unique users 
    who have listened to each track and return the one with the most. Return None if no sessions exist.
    """

    def track_with_most_distinct_listeners(self) -> Track | None:
        tracks_and_distinct_listeners : dict[str, set[str]] = {}
        if not self._sessions:
            return None
        for session in self._sessions:
            track=session.track.track_id
            user=session.user.user_id
            if track not in tracks_and_distinct_listeners:
                tracks_and_distinct_listeners[track] = set ()
            tracks_and_distinct_listeners[track].add(user)
        
        most_distinct_listeners : int = 0
        track_with_most_distinct_listeners : Track | None = None
        for track, listeners in tracks_and_distinct_listeners.items():
            if len(listeners) > most_distinct_listeners:
                most_distinct_listeners = len(listeners)
                track_with_most_distinct_listeners = self._catalogue.get(track)
        
        return track_with_most_distinct_listeners
    
#Q4

    """
    Q4: Average Session Duration by User Type 
    Method: avg_session_duration_by_user_type() -> list[tuple[str, float]]
    For each user subtype (e.g., FreeUser, PremiumUser, FamilyAccountUser, FamilyMember), 
    compute the average session duration (in seconds) and 
    return them ranked from longest to shortest. 
    Return as a list of (type_name, average_duration_seconds) tuples.
    """

    def avg_session_duration_by_user_type (self) -> list [ tuple [str, float] ]:

        u : dict[str, list[int]]={}
        result : list[tuple[str, float]] = []
        for session in self._sessions:
            user_type=type(session.user).__name__
            if user_type not in u:
                u[user_type]=[0,0]
            u[user_type][0] += session.duration_listened_seconds
            u[user_type][1] += 1
        
        for user_type in u:
            result.append((user_type, u[user_type][0]/u[user_type][1] if u[user_type][1] > 0 else 0.0))
        result.sort(key=lambda x: x[1], reverse=True)
        return result

#Q5

    """
    Q5: Total Listening Time for Underage Sub-Users
    Method: total_listening_time_underage_sub_users_minutes(age_threshold: int = 18) -> float
    Return the total listening time (in minutes) 
    attributed to tracks associated with FamilyAccountUser sub-accounts 
    where the sub-account holder (i.e., FamilyMember) is under 
    the specified age threshold (default 18, exclusive). 
    For example, with threshold 18, count only family members with age < 18.
    """

    def total_listening_time_underage_sub_users_minutes (self, age_threshold : int = 18) -> float:
        from streaming.users import FamilyMember    

        if not isinstance(age_threshold, int) or age_threshold <= 0:
            raise ValueError("Age threshold must be a positive integer.")
        total_seconds : int = 0
        for session in self._sessions:
            if isinstance(session.user, FamilyMember) and session.user.age < age_threshold:
                total_seconds += session.duration_listened_seconds
        return total_seconds / 60.0

#Q6
    """
    Q6: Top Artists by Listening Time
    Method: top_artists_by_listening_time(n: int = 5) -> list[tuple[Artist, float]]
    Identify the top n artists (default 5) ranked by total cumulative 
    listening time across all their tracks. 
    Only count listening time for tracks where isinstance(track, Song) 
    is true (exclude podcasts and audiobooks). 
    Return as a list of (Artist, total_minutes) tuples, 
    sorted from highest to lowest listening time.
    """

    def top_artists_by_listening_time(self, n: int = 5) -> list[tuple[Artist, float]] : 
        from streaming.tracks import Song
        
        artist_total_listening : dict [str, float] = {}
        artists_list : dict[str, Artist] = {}


        if not isinstance(n, int) or n <= 0:
            raise ValueError("N must be a positive integer.")
        
        for session in self._sessions:
            track=session.track
            if isinstance(track,Song) :
                artist = track.artist
                artist_id = artist.artist_id
                if artist_id not in artist_total_listening:
                    artist_total_listening [artist_id] = 0
                    artists_list[artist_id] = artist
                artist_total_listening [artist_id] += session.duration_listened_seconds
             

        
        result : list[tuple[Artist, float]] =[]

        for art_id, total_sec in artist_total_listening.items():
            result.append((artists_list[art_id], total_sec / 60.0))
        result.sort(key=lambda x: x[1], reverse=True)
        return result[:n]


#Q7

    """
    Q7: User's Top Genre
    Method: user_top_genre(user_id: str) -> tuple[str, float] | None
    Given a user ID, return their most frequently listened-to genre 
    and the percentage of their total listening time it accounts for. 
    Return a (genre, percentage) tuple where percentage is in the range [0, 100], 
    or None if the user doesn't exist or has no listening history.
    """
    
    def user_top_genre(self, user_id: str) -> tuple[str, float] | None :
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("User ID must be a non-empty string.")
        user=self.get_user(user_id)
        genre_totals : dict[str, int] = {}
        if not user or not user.sessions:
            return None
        for session in user.sessions:
            genre : str = session.track.genre
            if genre not in genre_totals:
                genre_totals[genre] = 0
            genre_totals[genre] += session.duration_listened_seconds
        top_genre : tuple[str, float] | None = None
        top_seconds : int = 0
        total = sum(genre_totals.values())
        for gnr, sec in genre_totals.items() :
            if sec > top_seconds :
                top_seconds = sec
                top_genre = (gnr, (top_seconds / total) * 100)
        return top_genre if top_genre else None


#Q8

    """
    Q8: Collaborative Playlists with Many Artists
    Method: collaborative_playlists_with_many_artists(threshold: int = 3) -> list[CollaborativePlaylist]
    Return all CollaborativePlaylist instances that 
    contain tracks from more than threshold (default 3) 
    distinct artists. Only Song tracks count toward the artist count (exclude Podcast and AudiobookTrack which don't have artists). 
    Return playlists in the order they were registered.
    """
    def collaborative_playlists_with_many_artists(self, threshold: int = 3) -> list[CollaborativePlaylist]:
        from streaming.tracks import Song

        if not isinstance(threshold, int) or threshold < 0:
            raise ValueError("Threshold must be a non-negative integer.")
        
        result : list[CollaborativePlaylist] = []

        for play in self._playlists.values():
            if isinstance(play, CollaborativePlaylist):
                unique_artists : set[str] = set()
                for track in play.tracks:
                    if isinstance(track, Song):
                        unique_artists.add(track.artist.artist_id)
                if len(unique_artists) > threshold:
                    result.append(play)
        return result

#Q9 Average number of tracks per playlist
    """
    Q9: Average Tracks per Playlist Type
    Method: avg_tracks_per_playlist_type() -> dict[str, float]
    Compute the average number of tracks per playlist, 
    distinguishing between standard Playlist and CollaborativePlaylist instances.
      Return a dictionary with keys "Playlist" and "CollaborativePlaylist" mapped to their 
      respective averages. Return 0.0 for a type with no instances.
    """

    def avg_tracks_per_playlist_type(self) -> dict[str, float] :

        standard_totals : int = 0
        standard_count : int = 0
        collaborative_totals : int = 0
        collaborative_count : int = 0

        for play in self._playlists.values():
            if isinstance(play, CollaborativePlaylist):
                collaborative_totals += len(play.tracks)
                collaborative_count += 1
            else:
                standard_totals += len(play.tracks)
                standard_count += 1
        avg_standard = standard_totals / standard_count if standard_count > 0 else 0.0
        avg_collaborative = collaborative_totals / collaborative_count if collaborative_count > 0 else 0.0
        return {"Playlist": avg_standard, "CollaborativePlaylist": avg_collaborative }

#Q10
    """
    Q10: Users Who Completed Albums
    Method: users_who_completed_albums() -> list[tuple[User, list[str]]]
    Identify users who have listened to every track on at least one complete 
    Album and return the corresponding album titles. A user "completes" an album 
    if their session history includes at least one listen to each track on that album. 
    Return as a list of (User, [album_title, ...]) tuples in registration order. 
    Albums with no tracks are ignored.
    """

    def users_who_completed_albums(self) -> list[tuple[User, list[str]]] :
        result : list[tuple[User, list[str]]] = []
        for user in self._users.values():
            listened_tracks : set[str] = user.unique_tracks_listened()
            completed_albums : list[str] = []
            for album in self._albums.values():
                if not album.tracks:
                    continue
                album_track_ids : set[str] = album.track_ids()
                if album_track_ids.issubset(listened_tracks):
                    completed_albums.append(album.title)
            if completed_albums:
                result.append((user, completed_albums))
        
        return result




