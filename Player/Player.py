from SlimsteExceptions import AlreadyPlayingException, NotPlayingException
import time

class Player:

    def __init__(self, name: str):
        self.name = name
        self.score = 60
        self.playing = False
        self.play_start = None

    def get_score(self) -> int:
        if not self.is_playing():
            return self.score
        current_time = time.time()
        time_playing = int(current_time - self.play_start)
        return self.score - time_playing

    def get_name(self) -> str:
        return self.name

    def add_score(self, to_add):
        self.score += to_add

    def is_playing(self) -> bool:
        return self.playing

    def start_playing(self):
        if self.is_playing():
            raise(AlreadyPlayingException())
        else:
            self.play_start = time.time()
            self.playing = True

    def stop_playing(self):
        if not self.is_playing():
            raise(NotPlayingException())
        else:
            current_time = time.time()
            time_playing = int(current_time - self.play_start)
            self.add_score(-time_playing)
            self.playing = False
