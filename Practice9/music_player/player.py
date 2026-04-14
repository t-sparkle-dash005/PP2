import pygame
import os
from typing import List, Optional


class MusicPlayer:

    def __init__(self, music_dir: str):
        pygame.mixer.init()

        supported = (".wav")
        self.playlist: List[str] = sorted(
            os.path.join(music_dir, f)
            for f in os.listdir(music_dir)
            if f.lower().endswith(supported)
        )

        if not self.playlist:
            raise FileNotFoundError(f"No audio files found in '{music_dir}'")

        self.index:   int  = 0
        self.playing: bool = False

    def play(self) -> None:
        """Load current track and start playback."""
        pygame.mixer.music.load(self.playlist[self.index])
        pygame.mixer.music.play()
        self.playing = True

    def stop(self) -> None:
        pygame.mixer.music.stop()
        self.playing = False

    def next_track(self) -> None:
        self.stop()
        self.index = (self.index + 1) % len(self.playlist)
        self.play()

    def prev_track(self) -> None:
        self.stop()
        self.index = (self.index - 1) % len(self.playlist)
        self.play()

    @property
    def current_name(self) -> str:
        return os.path.basename(self.playlist[self.index])

    @property
    def position_sec(self) -> float:
        return pygame.mixer.music.get_pos() / 1000.0

    @property
    def status(self) -> str:
        return "Playing" if self.playing else "Stopped"