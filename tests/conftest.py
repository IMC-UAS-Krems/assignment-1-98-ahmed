"""
conftest.py
-----------
Shared pytest fixtures used by both the public and private test suites.
"""

import pytest
from datetime import date, datetime, timedelta

from streaming.platform import StreamingPlatform
from streaming.artists import Artist
from streaming.albums import Album
from streaming.tracks import (
    AlbumTrack,
    SingleRelease,
    InterviewEpisode,
    NarrativeEpisode,
    AudiobookTrack,
)
from streaming.users import FreeUser, PremiumUser, FamilyAccountUser, FamilyMember
from streaming.sessions import ListeningSession
from streaming.playlists import Playlist, CollaborativePlaylist


# ---------------------------------------------------------------------------
# Helper - timestamps relative to the real current time so that the
# "last 30 days" window in Q2 always contains RECENT sessions.
# ---------------------------------------------------------------------------
FIXED_NOW = datetime.now().replace(microsecond=0)
RECENT = FIXED_NOW - timedelta(days=10)   # well within 30-day window
OLD    = FIXED_NOW - timedelta(days=60)   # outside 30-day window


def add_session(platform: StreamingPlatform, session_id: str, user, track, timestamp: datetime) -> None:
    session = ListeningSession(
        session_id,
        user,
        track,
        timestamp,
        track.duration_seconds
    )
    platform.record_session(session)

@pytest.fixture
def platform() -> StreamingPlatform:
    """Return a fully populated StreamingPlatform instance."""
    platform = StreamingPlatform("TestStream")

    # ------------------------------------------------------------------
    # Artists
    # ------------------------------------------------------------------
    pixels  = Artist("a1", "Pixels",    genre="pop")
    waves = Artist("a2", "Waves", genre="synthwave")
    echoes = Artist("a3", "Echoes", genre="indie")
    
    platform.add_artist(pixels)
    platform.add_artist(waves)
    platform.add_artist(echoes)

    # ------------------------------------------------------------------
    # Albums & AlbumTracks
    # ------------------------------------------------------------------
    dd = Album("alb1", "Digital Dreams", artist=pixels, release_year=2022)
    t1 = AlbumTrack("t1", "Pixel Rain",      180, "pop",  pixels, track_number=1)
    t2 = AlbumTrack("t2", "Grid Horizon",    210, "pop",  pixels, track_number=2)
    t3 = AlbumTrack("t3", "Vector Fields",   195, "pop",  pixels, track_number=3)
    for track in (t1, t2, t3):
        dd.add_track(track)
        platform.add_track(track)
        pixels.add_track(track)
    platform.add_album(dd)
    # ------------------------------------------------------------------
    # Album2
    # ------------------------------------------------------------------
    alb2 = Album("alb2", "Neon Nights", artist=waves, release_year=2021)
    t4 = AlbumTrack("t4", "Synthwave Dreams", 240, "synthwave", waves, track_number=1)
    t5 = AlbumTrack("t5", "Cyber Pulse",      220, "synthwave", waves, track_number=2)
    for track in (t4, t5):
        alb2.add_track(track)
        platform.add_track(track)
        waves.add_track(track)
    platform.add_album(alb2)
    # ------------------------------------------------------------------
    #Album3
    # ------------------------------------------------------------------
    alb3 = Album("alb3", "Echoes of Time", artist=echoes, release_year=2020)
    t6 = AlbumTrack("t6", "Timeless", 200, "indie", echoes, track_number=1)
    alb3.add_track(t6)
    platform.add_track(t6)
    echoes.add_track(t6)
    platform.add_album(alb3)
    # ------------------------------------------------------------------
    # Audiobook
    ab = AudiobookTrack("ab1", "AI Basics", 600, "education", "John Writer", "Nina Voice")
    platform.add_track(ab)



    # ------------------------------------------------------------------
    # Users
    # ------------------------------------------------------------------
    alice = FreeUser("u1", "Alice",   age=30)
    bob   = PremiumUser("u2", "Bob",   age=25, subscription_start=date(2023, 1, 1))
    charlie = PremiumUser("u3", "Charlie", age=40, subscription_start=date(2022, 6, 1))
    diana = FamilyAccountUser("u4", "Diana", age=35)
    evan = FamilyMember("u5", "Evan", age=10, parent=diana)
    fay = FamilyMember("u6", "Fay", age=8, parent=diana)
    elena = FamilyMember("u7", "Elena", age=5, parent=diana)
    
    diana.add_sub_user(evan)
    diana.add_sub_user(fay)
    diana.add_sub_user(elena)

    for user in (alice, bob, charlie, diana, evan, fay, elena):
        platform.add_user(user)
    
    # ------------------------------------------------------------------
    #playlists
    p1 = Playlist("p1", "Alice's Favorites", owner=alice)
    p1.add_track(t1)
    p1.add_track(t4)
    platform.add_playlist(p1)

    cp1 = CollaborativePlaylist("cp1", "Bob's Collab", owner=bob)
    cp1.add_contributor(charlie)
    cp1.add_track(t1)
    cp1.add_track(t4)
    cp1.add_track(t6)
    cp1.add_track(ab)
    platform.add_playlist(cp1)
    
    cp2 = CollaborativePlaylist("cp2", "Pixels Only", owner=charlie)
    cp2.add_contributor(bob)
    cp2.add_track(t1)
    cp2.add_track(t2)
    platform.add_playlist(cp2)
    # ------------------------------------------------------------------
    # Listening Sessions
    # ------------------------------------------------------------------
    add_session(platform, "s1", bob, t1, RECENT)
    add_session(platform, "s2", bob, t2, RECENT + timedelta(hours=1))
    add_session(platform, "s3", bob, t3, OLD)
    add_session(platform, "s4", bob, t6, RECENT + timedelta(hours=2))

    add_session(platform, "s5", charlie, t1, RECENT + timedelta(hours=3))
    add_session(platform, "s6", charlie, t4, RECENT + timedelta(hours=4))

    add_session(platform, "s7", alice, t1, RECENT + timedelta(hours=5))

    add_session(platform, "s8", diana, t5, RECENT + timedelta(hours=6))

    add_session(platform, "s9", evan, t1, RECENT + timedelta(hours=7))
    add_session(platform, "s10", evan, t2, RECENT + timedelta(hours=8))
    add_session(platform, "s11", evan, ab, RECENT + timedelta(hours=9))

    add_session(platform, "s12", fay, t3, RECENT + timedelta(hours=10))

    return platform





@pytest.fixture
def fixed_now() -> datetime:
    """Expose the shared FIXED_NOW constant to tests."""
    return FIXED_NOW


@pytest.fixture
def recent_ts() -> datetime:
    return RECENT


@pytest.fixture
def old_ts() -> datetime:
    return OLD
