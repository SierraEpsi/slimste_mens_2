import random

class Question:
    def __init__(self, question, answers):
        self.question = question
        self.answer_info = []
        self.score = 0
        for answer in answers:
            self.answer_info.append([answer, False])

    def get_question(self) -> str:
        return self.question

    def get_score(self) -> int:
        return self.score

    def get_answers(self) -> list:
        answers = []
        for answer in self.answer_info:
            answers.append[answer[0]]

    def get_answer_info(self) -> list:
        return self.answer_info

    def is_answered(self):
        for answer in self.answer_info:
            if not answer[1]:
                return False
        return True

    def answer(self, given_answer):
        for answer in self.answer_info:
            if answer[0] == given_answer:
                answer[1] = True


class R2Question(Question):
    def __init__(self, question: str, answers: list):
        super(R2Question, self).__init__(question, answers)
        self.score = 20

    @staticmethod
    def from_str(question_str: str):
        question, answers = question_str[1:-1].split(",")
        answers = answers[1:-1].split("|")
        return R2Question(question, answers)


class R3Question(Question):
    def __init__(self, question: list, answers: list):
        super(R3Question, self).__init__(question, answers)
        self.score = 30
        self.hints = []
        colors = ["green", "orange", "blue"]
        for i, answer in enumerate(self.answer_info):
            self.answer_info[i].append(colors[i])
            for hint in self.question[i]:
                self.hints.append([hint, answer[1], colors[i]])
        self.hints = self.shuffle_hints(self.hints)

    def get_hints(self):
        return self.hints

    def answer(self, given_answer):
        color = None
        for answer in self.answer_info:
            if answer[0] == given_answer:
                answer[1] = True
                color = answer[2]
        for hint in self.hints:
            if hint[2] == color:
                hint[1] = True


    @staticmethod
    def from_str(question_str: str):
        questions_temp, answers = question_str[1:-1].split(",")
        questions_temp = questions_temp[1:-1].split("|")
        answers = answers[1:-1].split("|")
        questions = []
        for question in questions_temp:
            questions.append(question[1:-1].split(";"))
        return R3Question(questions, answers)

    @staticmethod
    def shuffle_hints(hints):
        shuffled_hints = hints.copy()
        random.shuffle(shuffled_hints)
        return shuffled_hints

class R4Question(Question):
    def __init__(self, question: str, answers: list):
        super(R4Question, self).__init__(question, answers)
        self.score = 0

    def answer(self, given_answer):
        super(R4Question, self).answer(given_answer)
        self.score += 10

    @staticmethod
    def from_str(question_str: str):
        question, answers = question_str[1:-1].split(",")
        answers = answers[1:-1].split("|")
        return R4Question(question, answers)

class R5Question(Question):
    def __init__(self, question: str, answers: list):
        super(R5Question, self).__init__(question, answers)
        self.score = -20

    @staticmethod
    def from_str(question_str: str):
        print(question_str)
        question, answers = question_str[1:-1].split(",")
        answers = answers[1:-1].split("|")
        return R5Question(question, answers)

