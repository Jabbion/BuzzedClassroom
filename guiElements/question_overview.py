from guiElements.main_window import MainWindows
from guiElements.guiLibary import text_box


class Quiz:
    answer0 = ""
    answer1 = ""
    answer2 = ""
    answer3 = ""
    question = ""

    def contentFromJson(self, answers):
        pass
        self.answer0 = answers["answer0"]
        self.answer1 = answers["answer1"]
        self.answer2 = answers["answer2"]
        self.answer3 = answers["answer3"]
        self.question = answers["question"]
        self.rightAnswer = answers["rightAnswer"]


def question_overview(question, questionIndex ="", maxQuestions ="", selected ="", win ="", font_question = 50):
    # hier kann böser Exploit sein!                                         ----------
    if(selected == "3"):
        selected = "2"
    elif selected == "2":
        selected = "3"
    swin = ""
    if win == True:
        swin = "g"
    elif win == False:
        swin = "l"

    temp_display = MainWindows.get_new_background('images/background'+str(selected)+str(swin)+'.png')
    if questionIndex != "" and maxQuestions != "":
        text_box(str(questionIndex) + "/" + str(maxQuestions), 300 - 50, 30, 100, 100, temp_display, font_size=100)
    font = 50
    if(len(question.answer0) > 50):
        font = 50
    text_box(question.answer0, 400 - 50, 584 - 50, 100, 100, temp_display, font_size=font)
    font = 50
    if(len(question.answer0) > 50):
        font = 50
    text_box(question.answer1, 1200 - 50, 584 - 50, 100, 100, temp_display, font_size=font)
    font = 50
    if(len(question.answer0) > 50):
        font = 50
    text_box(question.answer3, 400 - 50, 784 - 50, 100, 100, temp_display, font_size=font)

    font = 50
    if(len(question.answer0) > 50):
        font = 50
    text_box(question.answer2, 1200 - 50, 784 - 50, 100, 100, temp_display, font_size=font)
    text_box(question.question, 800 - 50, 309 - 50, 100, 100, temp_display, font_size=font_question)
    return temp_display
