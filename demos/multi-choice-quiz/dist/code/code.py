import pytch

"""Multi-choice quiz

The questions with their answers are stored as a list in the variable
"all_questions_info".

Each question is stored as its own list, containing the following
items:

    question_info[0] = question text
    question_info[1] = first answer choice
    question_info[2] = second answer choice
    question_info[3] = third answer choice
    question_info[4] = number of correct answer

The "number of correct answer" uses the Python standard of counting
from zero, so

    question_info[4] == 0

means the first answer is correct,

    question_info[4] == 1

means the second answer is correct, and

    question_info[4] == 2

means the third answer is correct.
"""

all_questions_info = [
    [
        "What is the capital of Ireland?",
        "Dublin",
        "Cork",
        "Galway",
        0,
    ],
    [
        "How many centimetres are there in one metre?",
        "10",
        "100",
        "1000",
        1,
    ],
    [
        "What year was the Anglo-Irish Treaty signed?",
        "1921",
        "1922",
        "1923",
        0,
    ],
]

n_questions = len(all_questions_info)

clicked = False
score = 0
answer = None


class Narrator(pytch.Sprite):
    Costumes = ["button-question.png"]

    @pytch.when_green_flag_clicked
    def play_quiz(self):
        global clicked, score, answer

        self.say_for_seconds("Let's begin", 2)

        question_index = 0
        while question_index < n_questions:
            question_info = all_questions_info[question_index]
            question = question_info[0]
            ans_A = "A: " + question_info[1]
            ans_B = "B: " + question_info[2]
            ans_C = "C: " + question_info[3]
            text = question + "\n" + ans_A + "\n" + ans_B + "\n" + ans_C
            self.say(text)

            clicked = False
            while not clicked:
                pass

            if answer == question_info[4]:
                self.say_for_seconds("Correct!", 1)
                score += 1
            else:
                self.say_for_seconds("Sorry, that's not correct", 1)

            question_index += 1

        self.say(f"You got {score} right out of {n_questions}")


class AnswerA(pytch.Sprite):
    Costumes = ["button-ans-A.png"]

    @pytch.when_green_flag_clicked
    def setup(self):
        self.go_to_xy(-140, -120)

    @pytch.when_this_sprite_clicked
    def notify_answered(self):
        global answer, clicked
        answer = 0
        clicked = True


class AnswerB(pytch.Sprite):
    Costumes = ["button-ans-B.png"]

    @pytch.when_green_flag_clicked
    def setup(self):
        self.go_to_xy(0, -120)

    @pytch.when_this_sprite_clicked
    def notify_answered(self):
        global answer, clicked
        answer = 1
        clicked = True


class AnswerC(pytch.Sprite):
    Costumes = ["button-ans-C.png"]

    @pytch.when_green_flag_clicked
    def setup(self):
        self.go_to_xy(140, -120)

    @pytch.when_this_sprite_clicked
    def notify_answered(self):
        global answer, clicked
        answer = 2
        clicked = True
