import xlsxwriter
import datetime

from time import sleep

from Database.database import database
from guiElements.question_overview import question_overview
from guiElements.quizzes_overview import quizzes_overview
from guiElements.player_overview import player_overview
from guiElements.main_window import MainWindows
from Controller.controller import key_mapping as keys
from Controller.controller import subscribe
from Controller.controller import unsubscribe
from Controller.controller import main as start_controller
from timerThread import TimerThread

class Main():

    # <Settings>
    timePerQuestion = 10
    timeShowRightAnswer = 2
    # </Settings>

    currentQuiz = 0

    def __init__(self):
        self.jdb = database()

        # Quiz Overview
        self.mainWin = MainWindows(1280, 1024, fullscreen=True)
        self.allQuizzes = self.jdb.getQuizNames()
        self.mainWin.set_image(quizzes_overview(self.allQuizzes, self.currentQuiz))

        # Set Admin
        subscribe(self.handle_get_admin)
        start_controller()

    def handle_get_admin(self, buttonPressed, deviceId):
        if keys[buttonPressed] == "A":
            self.adminId = deviceId
            unsubscribe(self.handle_get_admin)
            subscribe(self.handle_quizzes_overview)

    def handle_quizzes_overview(self, buttonPressed, deviceId):
        if deviceId == self.adminId:
            if keys[buttonPressed] == "C":  # Up
                if self.currentQuiz == 0:
                    self.currentQuiz = len(self.allQuizzes) - 1
                else:
                    self.currentQuiz -= 1

            elif keys[buttonPressed] == "D":    # Down
                if self.currentQuiz == len(self.allQuizzes) - 1:
                    self.currentQuiz = 0
                else:
                    self.currentQuiz += 1

            self.mainWin.set_image(quizzes_overview(self.allQuizzes, self.currentQuiz))

            if keys[buttonPressed] == "A":      # Run Quiz
                if len(self.allQuizzes) - 1 != 0:
                    self.players = []
                    self.playerIds = []
                    self.mainWin.set_image(player_overview(self.players))
                    unsubscribe(self.handle_quizzes_overview)
                    subscribe(self.handle_player_overview)

            elif keys[buttonPressed] == "B":
                pass
                # Exit?


    def handle_player_overview(self, buttonPressed, deviceId):
        if deviceId == self.adminId:
            if keys[buttonPressed] == "A":      # Start Quiz
                self.questions = self.jdb.getQuiz(self.allQuizzes[self.currentQuiz])
                self.curQuestion = 0
                self.clear_player_answers()
                self.quizAnswers = []
                self.timerThread = TimerThread()
                self.timerThread.run(self.timePerQuestion, onEnd=self.next_question)
                self.blockController = False
                self.mainWin.set_image(question_overview(self.questions[self.curQuestion], self.curQuestion + 1, len(self.questions)))
                unsubscribe(self.handle_player_overview)
                subscribe(self.handle_question_overview)

            elif keys[buttonPressed] == "B":    # Back to Quizzes Overview
                self.mainWin.set_image(quizzes_overview(self.allQuizzes, self.currentQuiz))
                unsubscribe(self.handle_player_overview)
                subscribe(self.handle_quizzes_overview)

        elif not deviceId in self.playerIds:    # Add to players
            self.players.append("Player " + str(len(self.players) + 1))
            self.playerIds.append(deviceId)
            self.mainWin.set_image(player_overview(self.players))

    def handle_question_overview(self, buttonPressed, deviceId):
        if deviceId == self.adminId:
            if keys[buttonPressed] == "B":  # Back to Player Overview
                self.mainWin.set_image(player_overview(self.players))
                unsubscribe(self.handle_question_overview)
                subscribe(self.handle_player_overview)
                return

        elif deviceId in self.playerIds and self.blockController == False:
            if self.playerAnswers[self.playerIds.index(deviceId)] == None:      # Set to chosen answer
                self.playerAnswers[self.playerIds.index(deviceId)] = keys[buttonPressed]

        if self.has_everyone_answered():
            self.next_question()

    def next_question(self):
        self.blockController = True
        self.timerThread.enable(False)

        self.quizAnswers.append(self.playerAnswers[:])
        self.clear_player_answers()
        self.mainWin.set_image(
            question_overview(self.questions[self.curQuestion], self.curQuestion + 1, len(self.questions),
                              self.questions[self.curQuestion].rightAnswer))
        sleep(self.timeShowRightAnswer)

        self.curQuestion += 1

        if self.curQuestion != len(self.questions):
            self.mainWin.set_image(
                question_overview(self.questions[self.curQuestion], self.curQuestion + 1, len(self.questions)))
            self.timerThread = TimerThread()
            self.timerThread.run(self.timePerQuestion, onEnd=self.next_question)

        else:
            self.dump_csv()
            self.currentQuiz = 0
            self.mainWin.set_image(quizzes_overview(self.allQuizzes, self.currentQuiz))
            unsubscribe(self.handle_question_overview)
            subscribe(self.handle_quizzes_overview)

        self.blockController = False

    def dump_csv(self):
        workbook = xlsxwriter.Workbook(str(datetime.datetime.now()) + ".xlsx")
        ws = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        corAnswer = workbook.add_format({'bold': True})
        corAnswer.set_bg_color("green")

        # Write top row
        firstRow = ["Questions", "A", "B", "C", "D", "N/A", "Correct Answer"]

        ws.write_row(0, 0, firstRow, bold)

        # Write every question
        for i, answers in enumerate(self.quizAnswers):
            ws.write(i + 1, 0, str(i + 1) + ".) " + self.questions[i].question, bold)

            # Calculate counts
            counts = [0 for x in range(5)]

            for answer in answers:
                num = self.answer_char_to_num(answer)

                if num == None:
                    counts[4] += 1
                else:
                    counts[num] += 1

            for answIndex, count in enumerate(counts):
                if self.questions[i].rightAnswer == answIndex:
                    ws.write(i + 1, 1 + answIndex, count, corAnswer)
                else:
                    ws.write(i + 1, 1 + answIndex, count)

            ws.write(i + 1, 6, self.answer_num_to_char(self.questions[i].rightAnswer))

    def answer_char_to_num(self, char):
        if char != None:
            return ord(char) - 65
        return None

    def answer_num_to_char(self, num):
        return chr(num + 65)

    def has_everyone_answered(self):
        for el in self.playerAnswers:
            if el == None:
                return False
        return True

    def clear_player_answers(self):
        self.playerAnswers = [None for i in range(len(self.players))]

if __name__ == "__main__":
    Main()