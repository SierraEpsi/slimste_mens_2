from SlimsteExceptions import NoMorePLayersForQuestionException, NotPlayingException, NoMorePLayersException
from Player.Player import Player


class Control:

    def __init__(self):
        self.players = []
        self.final_players = []
        self.in_final = False

    def init_players(self, players: list):
        for player_name in players:
            self.players.append(Player(player_name))

    def get_players(self) -> list:
        if self.in_final:
            return self.final_players
        else:
            return self.players

    def get_player_names(self) -> list:
        player_names = []
        for player in self.get_players():
            player_names.append(player.get_name())
        return player_names

    def get_player(self, player_name: str) -> Player:
        for player in self.players:
            if player.get_name() == player_name:
                return player

    def get_final_players(self):
        return self.final_players

    @staticmethod
    def get_lowest_score(players: list) -> Player:
        lowest_score = 9999
        lowest_player = -1
        if len(players) <= 0:
            raise NoMorePLayersException
        else:
            for i, player in enumerate(players):
                if player.get_score() < lowest_score:
                    lowest_score = player.get_score()
                    lowest_player = i
        return players[lowest_player]

    def initiate_final(self):
        players = sorted(self.players, key=lambda player: player.get_score())
        self.final_players = players[-2:]
        self.in_final = True

    def add_time(self, player_name:str, time_added:int):
        player = self.get_player(player_name)
        player.add_score(time_added)

    def start_playing(self, player_name:str):
        player = self.get_player(player_name)
        player.start_playing()

    def stop_playing(self, player_name:str):
        player = self.get_player(player_name)
        player.stop_playing()

