import xlsxwriter
import argparse
import datetime
import os


from time import sleep

from Database.database import database
from guiElements.question_overview import question_overview, Quiz
from guiElements.quizzes_overview import quizzes_overview
from guiElements.player_overview import player_overview
from guiElements.main_window import MainWindows
from Controller.controller import subscribe
from Controller.controller import unsubscribe
from Controller.controller import main as start_controller
from Controller.controller import set_block as blockIds
from timerThread import TimerThread

class Main():

    # <Settings>
    timePerQuestion = 10
    timeShowRightAnswer = 2
    timeQuizPreview = 5
    defXlsxFolder = "Gespielte Quiz"
    defWinWidth = 1600
    defWinHeight = 900
    # </Settings>

    currentQuiz = 0

    def __init__(self):
        # Parse args
        parser = argparse.ArgumentParser()
        parser.add_argument("-f", "--fullscreen", help="Run window in fullscreen mode", action="store_true")
        parser.add_argument("-r", "--resolution", help="Set screen resolution (e.g. '1600x900')", type=str)
        parser.add_argument("-d", "--directory", help="Set output directory for xlsx files", type=str, default=self.defXlsxFolder)

        self.args = parser.parse_args()

        if self.args.resolution != None:
            try:
                resArr = self.args.resolution.split('x')
                self.defWinWidth = int(resArr[0])
                self.defWinHeight = int(resArr[1])
            except:
                print("[!] Please specify a correct resolution (e.g. '1600x900')")
                exit(1)

        self.jdb = database()

        # Prepare Quiz Preview
        self.quizPreviewQuestion = Quiz()
        self.quizPreviewQuestion.question = "-= Unnamed =-"
        self.quizPreviewQuestion.answer0 = "A"
        self.quizPreviewQuestion.answer1 = "B"
        self.quizPreviewQuestion.answer2 = "C"
        self.quizPreviewQuestion.answer3 = "D"
        self.quizPreviewQuestion.rightAnswer = 42

        # Quiz Overview
        self.mainWin = MainWindows(self.defWinWidth, self.defWinHeight, fullscreen=self.args.fullscreen)
        self.allQuizzes = self.jdb.getQuizNames()
        self.mainWin.set_image(quizzes_overview(self.allQuizzes, self.currentQuiz))

        # Set Admin
        subscribe(self.handle_get_admin)
        start_controller()

    def handle_get_admin(self, buttonPressed, deviceId):
        if buttonPressed == "A":
            self.adminId = deviceId
            unsubscribe(self.handle_get_admin)
            subscribe(self.handle_quizzes_overview)

    def handle_quizzes_overview(self, buttonPressed, deviceId):
        if deviceId == self.adminId:
            if buttonPressed == "C":  # Up
                if self.currentQuiz == 0:
                    self.currentQuiz = len(self.allQuizzes) - 1
                else:
                    self.currentQuiz -= 1

            elif buttonPressed == "D":    # Down
                if self.currentQuiz == len(self.allQuizzes) - 1:
                    self.currentQuiz = 0
                else:
                    self.currentQuiz += 1

            self.mainWin.set_image(quizzes_overview(self.allQuizzes, self.currentQuiz))

            if buttonPressed == "A":      # Run Quiz
                if len(self.allQuizzes) - 1 != 0:
                    blockIds()
                    self.players = []
                    self.playerIds = []
                    self.mainWin.set_image(player_overview(self.players))
                    unsubscribe(self.handle_quizzes_overview)
                    subscribe(self.handle_player_overview)

            elif buttonPressed == "B":
                self.mainWin.quit()

    def handle_player_overview(self, buttonPressed, deviceId):
        if deviceId == self.adminId:
            if buttonPressed == "A":      # Start Quiz
                self.show_quiz_preview()

                self.questions = self.jdb.getQuiz(self.allQuizzes[self.currentQuiz])
                self.curQuestion = 0
                self.clear_player_answers()
                self.quizAnswers = []
                self.timerThread = TimerThread()
                self.timerThread.run(self.timePerQuestion, onEnd=self.next_question)
                blockIds()
                self.mainWin.set_image(question_overview(self.questions[self.curQuestion], self.curQuestion + 1, len(self.questions)))
                unsubscribe(self.handle_player_overview)
                subscribe(self.handle_question_overview)

            elif buttonPressed == "B":    # Back to Quizzes Overview
                self.mainWin.set_image(quizzes_overview(self.allQuizzes, self.currentQuiz))
                unsubscribe(self.handle_player_overview)
                subscribe(self.handle_quizzes_overview)

        elif not deviceId in self.playerIds:    # Add to players
            self.players.append("Player " + str(len(self.players) + 1))
            self.playerIds.append(deviceId)
            self.mainWin.set_image(player_overview(self.players))

    def handle_question_overview(self, buttonPressed, deviceId):
        if deviceId == self.adminId:
            if buttonPressed == "B":  # Back to Player Overview
                blockIds()
                self.mainWin.set_image(player_overview(self.players))
                unsubscribe(self.handle_question_overview)
                subscribe(self.handle_player_overview)
                return

        elif deviceId in self.playerIds:
            if self.playerAnswers[self.playerIds.index(deviceId)] == None:      # Set to chosen answer
                self.playerAnswers[self.playerIds.index(deviceId)] = buttonPressed

        if self.has_everyone_answered():
            self.next_question()

    def show_quiz_preview(self):
        blockIds(self.playerIds + [self.adminId])
        self.quizPreviewQuestion.question = self.allQuizzes[self.currentQuiz]
        self.mainWin.set_image(question_overview(self.quizPreviewQuestion, font_question=150))
        sleep(self.timeQuizPreview)
        blockIds()

    def next_question(self):
        blockIds(self.playerIds + [self.adminId])
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

        blockIds()

    def dump_csv(self):
        if not os.path.exists():
            os.makedirs(self.args.directory)
        path = self.args.directory + "/" + str(datetime.datetime.now()) + ".xlsx"
        workbook = xlsxwriter.Workbook(path)
        ws = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        corAnswer = workbook.add_format({'bold': True})
        corAnswer.set_bg_color("green")

        # Write top row
        firstRow = ["Questions", "A", "B", "C", "D", "N/A", "", "Answers:", "A", "B", "C", "D"]

        ws.write_row(0, 0, firstRow, bold)

        # Set line length
        ws.set_column('A:A', 40)
        ws.set_column('B:F', 3)
        ws.set_column('H:H', 13)
        ws.set_column('I:L', 30)

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

            # Empty column
            ws.write(i + 1, 7, "")

            # Answers
            ws.write(i + 1, 8, self.questions[i].answer0)
            ws.write(i + 1, 9, self.questions[i].answer1)
            ws.write(i + 1, 10, self.questions[i].answer2)
            ws.write(i + 1, 11, self.questions[i].answer3)
        workbook.close()
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
