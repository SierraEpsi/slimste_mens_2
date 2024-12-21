import random

from SlimsteExceptions import NoMorePLayersException
from UserInterface.ContentWindow import ContentWindow
from UserInterface.ControlWindow import ControlWindow
from UserInterface.LoggerFrame import LoggerFrame
from UserInterface.RoundControlFrame import RoundControlFrame
from Player import Control as PlayerController
from Round import Control as RoundController
from UserInterface.RoundFrame import RoundFrame
from UserInterface.ScoreFrame import ScoreFrame


class Control:

    def __init__(self):
        self.control_window = ControlWindow(self)
        self.content_window = ContentWindow(self.control_window.get_window())
        self.player_control = PlayerController.Control()
        self.round_control = RoundController.Control()
        self.round_control_frame = RoundControlFrame(self.control_window.get_right_frame())
        self.logger = LoggerFrame(self.control_window.get_right_frame())
        self.round_frame = RoundFrame(self.content_window.get_upper_frame())
        self.score_frame = ScoreFrame(self.content_window.get_lower_frame())
        self.control_window.plan_refresh(self)
        self.control_window.start()

    def menu_click(self, command: str):
        self.logger.add_line(f"DEBUG: user clicked on: {command}")
        if command == "Setup":
            self.round_control_frame.create_setup(self)
        elif command == "Debug":
            self.round_control_frame.create_debug(self, self.player_control.get_player_names())
        elif command == "Porte Ouverte":
            self.round_control.r2_start(self.player_control.get_players())
            self.round_control_frame.r2_create_questions(
                self,
                self.round_control.get_round_questions(),
                self.round_control.get_current_player()
            )
        elif command == "Tour de Puzzle":
            self.round_control.r3_start(self.player_control.get_players())
            self.round_control_frame.r3_create_next(self, self.round_control.get_current_player())
        elif command == "Mémoire collective":
            self.round_control.r5_start(self.player_control.get_players())
            self.round_control_frame.r5_create_next(self, self.round_control.get_current_player())
        elif command == "Final":
            self.player_control.initiate_final()
            self.round_control.r6_start(self.player_control.get_final_players())
            self.round_control_frame.r6_create_next(self, self.round_control.get_current_player())
        elif command == "Update":
            self.refresh_score()

    def logger(self, line:str):
        self.logger.add_line(line)

    def setup_players(self, player_names):
        self.logger.add_line(f"DEBUG: setting up following names: {player_names}")
        self.player_control.init_players(player_names)
        self.round_control_frame.refresh()
        self.score_frame.draw_score(self.player_control.get_players())

    def debug_player(self, player_name):
        self.logger.add_line(f"DEBUG: selecting {player_name} for debugging")
        self.round_control_frame.create_debug(
            self,
            self.player_control.get_player_names(),
            self.player_control.get_player(player_name)
        )

    def r2_question(self, question):
        self.round_control.select_question(question)
        answer_info = self.round_control.get_current_answers()
        self.round_frame.r2_draw(answer_info)
        self.round_control_frame.r2_create_answer(self, answer_info)
        self.start_playing(self.round_control.get_current_player())

    def r2_answer(self, answer):
        self.round_control.answer(answer)
        answer_info = self.round_control.get_current_answers()
        self.round_frame.r2_draw(answer_info)
        if self.round_control.is_question_answered():
            self.stop_playing(self.round_control.get_current_player())
            try:
                self.round_control.end_question()
                self.round_control_frame.r2_create_questions(
                    self,
                    self.round_control.get_round_questions(),
                    self.round_control.get_current_player()
                )
            except NoMorePLayersException:
                self.round_control_frame.refresh()
        else:
            self.round_control_frame.r2_create_answer(self, answer_info)

    def r2_pass_question(self):
        self.stop_playing(self.round_control.get_current_player())
        try:
            self.round_control.pass_question()
            self.round_control_frame.r2_create_pass(self, self.round_control.get_current_player())
        except NoMorePLayersException:
            try:
                self.round_control.end_question()
                self.round_control_frame.r2_create_questions(
                    self,
                    self.round_control.get_round_questions(),
                    self.round_control.get_current_player()
                )
            except NoMorePLayersException:
                self.round_control_frame.refresh()
        answer_info = self.round_control.get_current_answers()
        self.round_frame.r2_draw(answer_info)

    def r2_continue(self):
        answer_info = self.round_control.get_current_answers()
        self.round_control_frame.r2_create_answer(self, answer_info)
        self.start_playing(self.round_control.get_current_player())

    def r3_question(self):
        self.round_control.next_question()
        answer_info = self.r3_update_content()
        self.round_control_frame.r3_create_answer(self, answer_info)
        self.start_playing(self.round_control.get_current_player())

    def r3_update_content(self):
        answer_info = self.round_control.get_current_answers()
        hints = self.round_control.get_current_question().get_hints()
        self.round_frame.r3_draw(hints, answer_info)
        return answer_info

    def r3_answer(self, answer):
        self.round_control.answer(answer)
        answer_info = self.r3_update_content()
        if self.round_control.is_question_answered():
            self.stop_playing(self.round_control.get_current_player())
            try:
                self.round_control.end_question()
                self.round_control_frame.r3_create_next(self, self.round_control.get_current_player())
            except NoMorePLayersException:
                self.round_control_frame.refresh()
        else:
            self.round_control_frame.r3_create_answer(self, answer_info)

    def r3_pass_question(self):
        self.stop_playing(self.round_control.get_current_player())
        try:
            self.round_control.pass_question()
            self.round_control_frame.r3_create_pass(self, self.round_control.get_current_player())
        except NoMorePLayersException:
            try:
                self.round_control.end_question()
                self.round_control_frame.r3_create_next(self, self.round_control.get_current_player())
            except NoMorePLayersException:
                self.round_control_frame.refresh()
        answer_info = self.r3_update_content()

    def r3_continue(self):
        answer_info = self.round_control.get_current_answers()
        self.round_control_frame.r3_create_answer(self, answer_info)
        self.start_playing(self.round_control.get_current_player())

    def r5_question(self):
        self.round_control.next_question()
        answer_info = self.round_control.get_current_answers()
        self.round_frame.r5_draw(answer_info)
        self.round_control_frame.r5_create_answer(self, answer_info)
        self.start_playing(self.round_control.get_current_player())

    def r5_answer(self, answer):
        self.round_control.answer(answer)
        answer_info = self.round_control.get_current_answers()
        self.round_frame.r5_draw(answer_info)
        if self.round_control.is_question_answered():
            self.stop_playing(self.round_control.get_current_player())
            try:
                self.round_control.end_question()
                self.round_control_frame.r5_create_next(self, self.round_control.get_current_player())
            except NoMorePLayersException:
                self.round_control_frame.refresh()
        else:
            self.round_control_frame.r5_create_answer(self, answer_info)

    def r5_pass_question(self):
        self.stop_playing(self.round_control.get_current_player())
        try:
            self.round_control.pass_question()
            self.round_control_frame.r5_create_pass(self, self.round_control.get_current_player())
        except NoMorePLayersException:
            try:
                self.round_control.end_question()
                self.round_control_frame.r5_create_next(self, self.round_control.get_current_player())
            except NoMorePLayersException:
                self.round_control_frame.refresh()
        answer_info = self.round_control.get_current_answers()
        self.round_frame.r5_draw(answer_info)

    def r5_continue(self):
        answer_info = self.round_control.get_current_answers()
        self.round_control_frame.r5_create_answer(self, answer_info)
        self.start_playing(self.round_control.get_current_player())

    def r6_question(self):
        self.round_control.next_question()
        answer_info = self.round_control.get_current_answers()
        self.round_frame.r6_draw(answer_info)
        self.round_control_frame.r6_create_answer(self, answer_info)
        self.start_playing(self.round_control.get_current_player())

    def r6_answer(self, answer):
        self.round_control.answer_final(answer)
        answer_info = self.round_control.get_current_answers()
        self.round_frame.r6_draw(answer_info)
        if self.round_control.is_question_answered():
            self.stop_playing(self.round_control.get_current_player())
            try:
                self.round_control.end_question_final()
                self.round_control_frame.r6_create_next(self, self.round_control.get_current_player())
            except NoMorePLayersException:
                self.round_control_frame.refresh()
        else:
            self.round_control_frame.r6_create_answer(self, answer_info)

    def r6_pass_question(self):
        self.stop_playing(self.round_control.get_current_player())
        try:
            self.round_control.pass_question_final()
            self.round_control_frame.r6_create_pass(self, self.round_control.get_current_player())
        except NoMorePLayersException:
            self.round_control.end_question_final()
            self.round_control_frame.r6_create_next(self, self.round_control.get_current_player())
        answer_info = self.round_control.get_current_answers()
        self.round_frame.r6_draw(answer_info)

    def r6_continue(self):
        answer_info = self.round_control.get_current_answers()
        self.round_control_frame.r6_create_answer(self, answer_info)
        self.start_playing(self.round_control.get_current_player())

    def add_time(self, player_name:str, time_added:int):
        self.logger.add_line(f"DEBUG: adding {time_added} to {player_name}")
        self.player_control.add_time(player_name, time_added)

    def start_playing(self, player_name:str):
        self.logger.add_line(f"DEBUG: starting timer for {player_name}")
        self.score_frame.update_current_player(player_name)
        self.player_control.start_playing(player_name)

    def stop_playing(self, player_name:str):
        self.logger.add_line(f"DEBUG: stopping timer for {player_name}")
        self.score_frame.update_current_player(None)
        self.player_control.stop_playing(player_name)

    def refresh_score(self):
        self.score_frame.draw_score(self.player_control.get_players())
        self.control_window.plan_refresh(self)



if __name__ == '__main__':
    Control()
