import time
from connect.Connection import Connection
from guiElements.question_overview import question_overview, Quiz
from guiElements.quizzes_overview import quizzes_overview
from guiElements.player_overview import player_overview
from guiElements.winner_overview import winner_overview, Winner
import operator
from guiElements.main_window import MainWindows

import json

class Network(object):

    main = MainWindows(1280, 1024)
    old_question = None
    second_package = True
    conn = None

    def __init__(self):
        self.conn = Connection()

    def response_to_json(self, response):
        nresponse = ""
        for r in response:
            nresponse = nresponse + chr(r)
        return json.loads(nresponse)

    def execute_from_json(self, response):
        img = None
        print(response)
        if response["windowName"] == "QuizzesOverview":
            img = quizzes_overview(response["quizzes"], response["selectedQuiz"])
        if response["windowName"] == "PlayerOverview":
            img = player_overview(response["players"])
        if response["windowName"] == "QuestionOverview":
            q = Quiz()
            q.contentFromJson(response)

            if response["isCorrect"] == True:
                img = question_overview(self.old_question, response["selectedAnswer"], "g", questionIndex=response["currentQuestionNum"], maxQuestions=response["countQuestions"])
                self.main.set_image(img)
                time.sleep(3)

            elif response["isCorrect"] == False:
                img = question_overview(self.old_question, response["selectedAnswer"], "l", questionIndex=response["currentQuestionNum"], maxQuestions=response["countQuestions"])
                self.main.set_image(img)
                time.sleep(3)

            img = question_overview(q, questionIndex=response["currentQuestionNum"], maxQuestions=response["countQuestions"])
            self.old_question = q

        if response["windowName"] == "WinnerOverview":
            sorted_dic = sorted(response["playerPoints"].items(), key=operator.itemgetter(1))
            sorted_dic.reverse()
            win = Winner(response)
            img = winner_overview(win)

        self.main.set_image(img)

    def start_network(self):
        msg = self.conn.readMessage()
        msg = self.response_to_json(msg)
        self.execute_from_json(msg)
