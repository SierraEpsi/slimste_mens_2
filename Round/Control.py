from Player.Player import Player
from Player.Control import Control as PlayerControl
from Round.Question import Question, R2Question, R3Question, R4Question, R5Question, R6Question
from SlimsteExceptions import QuestionNotFoundException, QuestionAlreadyAskedException, NoMorePLayersException


class Control:
    def __init__(self):
        self.questions_info = []
        self.current_question: Question = None
        self.players_info = []
        self.current_player: Player = None
        self.other_player: Player = None
        self.r2_questions = self.read_round2()
        self.r3_questions = self.read_round3()
        self.r4_questions = self.read_round4()
        self.r5_questions = self.read_round5()
        self.r6_questions = self.read_round6()

    def get_current_player(self):
        return self.current_player.get_name()

    def start_round(self, players):
        self.current_question = None
        self.players_info = []
        for player in players:
            self.players_info.append([player, False, False])
        self.current_player = self.get_next_player_round()

    def r2_start(self, players):
        self.questions_info = []
        for question in self.r2_questions:
            self.questions_info.append([question, False])
        self.start_round(players)

    def r3_start(self, players):
        self.questions_info = []
        for question in self.r3_questions:
            self.questions_info.append([question, False])
        self.start_round(players)

    def r4_start(self, players):
        self.questions_info = []
        for question in self.r4_questions:
            self.questions_info.append([question, False])
        self.start_round(players)

    def r5_start(self, players):
        self.questions_info = []
        for question in self.r5_questions:
            self.questions_info.append([question, False])
        self.start_round(players)

    def r6_start(self, players):
        self.questions_info = []
        for question in self.r6_questions:
            self.questions_info.append([question, False])
        self.start_round(players)
        for player in self.players_info:
            if player[0].get_name() != self.current_player.get_name():
                self.other_player = player[0]

    def select_question(self, selected_question):
        for player in self.players_info:
            if player[0].get_name() == self.current_player.get_name():
                player[1] = True
                player[2] = True
            else:
                player[2] = False
        for question in self.questions_info:
            if question[0].get_question() == selected_question:
                if question[1]:
                    raise QuestionAlreadyAskedException
                else:
                    question[1] = True
                    self.current_question = question[0]
                    return
        raise QuestionNotFoundException

    def next_question(self):
        for player in self.players_info:
            if player[0].get_name() == self.current_player.get_name():
                player[1] = True
                player[2] = True
            else:
                player[2] = False
        for question in self.questions_info:
            if not question[1]:
                question[1] = True
                self.current_question = question[0]
                return
        raise QuestionNotFoundException

    def end_question(self):
        for answer in self.current_question.get_answer_info():
            answer[1] = True
        self.current_player = self.get_next_player_round()

    def pass_question(self):
        self.current_player = self.get_next_player_question()
        for player in self.players_info:
            if player[0].get_name() == self.current_player.get_name():
                player[2] = True

    def get_round_questions(self) -> list:
        questions = []
        for question in self.questions_info:
            questions.append((question[0].get_question(), question[1]))
        return questions

    def is_question_answered(self) -> bool:
        return self.current_question.is_answered()

    def get_current_answers(self) -> list:
        return self.current_question.get_answer_info()

    def get_current_question(self):
        return self.current_question

    def answer(self, answer):
        self.current_question.answer(answer)
        self.current_player.add_score(self.current_question.get_score())

    def get_next_player_round(self) -> Player:
        still_toplay = []
        for player in self.players_info:
            if not player[1]:
                still_toplay.append(player[0])
        return PlayerControl.get_lowest_score(still_toplay)

    def get_next_player_question(self) -> Player:
        still_toplay = []
        for player in self.players_info:
            if not player[2]:
                still_toplay.append(player[0])
        return PlayerControl.get_lowest_score(still_toplay)

    def answer_final(self, answer):
        self.current_question.answer(answer)
        self.other_player.add_score(self.current_question.get_score())

    def pass_question_final(self):
        self.current_player = self.get_next_player_question()
        for player in self.players_info:
            if player[0].get_name() == self.current_player.get_name():
                player[2] = True
            if player[0].get_name() != self.current_player.get_name():
                self.other_player = player[0]

    def end_question_final(self):
        for answer in self.current_question.get_answer_info():
            answer[1] = True
        if self.current_player.get_score() > self.other_player.get_score():
            temp_player = self.current_player
            self.current_player = self.other_player
            self.other_player = temp_player

    @staticmethod
    def read_round2():
        questions = []
        with open("questions/round_2", "r", encoding="utf-8") as f:
            for line in f.readlines():
                if len(line.strip()) <= 0:
                    break
                questions.append(R2Question.from_str(line.strip()))
        return questions

    @staticmethod
    def read_round3():
        questions = []
        with open("questions/round_3", "r", encoding="utf-8") as f:
            for line in f.readlines():
                if len(line.strip()) <= 0:
                    break
                questions.append(R3Question.from_str(line.strip()))
        return questions

    @staticmethod
    def read_round4():
        questions = []
        with open("questions/round_4", "r", encoding="utf-8") as f:
            for line in f.readlines():
                if len(line.strip()) <= 0:
                    break
                questions.append(R4Question.from_str(line.strip()))
        return questions

    @staticmethod
    def read_round5():
        questions = []
        with open("questions/round_5", "r", encoding="utf-8") as f:
            for line in f.readlines():
                if len(line.strip()) <= 0:
                    break
                questions.append(R5Question.from_str(line.strip()))
        return questions

    @staticmethod
    def read_round6():
        questions = []
        with open("questions/round_6", "r", encoding="utf-8") as f:
            for line in f.readlines():
                if len(line.strip()) <= 0:
                    break
                questions.append(R6Question.from_str(line.strip()))
        return questions
