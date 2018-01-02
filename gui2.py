import json
import operator

import pygame
import sys
from pygame.locals import *

from connect import Connection
from guiElements.guiLibary import text_box

img_libary = {}
gameDisplay = None
preDisplay = None
width = 900
height = 450
con = Connection()

def load_image(path):
    global img_libary
    img_libary["background"] = pygame.image.load(path)
    preDisplay.blit(img_libary["background"], (0,0))


def pygame_init():
    global gameDisplay
    global preDisplay
    # set up pygame
    pygame.init()

    gameDisplay = pygame.display.set_mode((width, height))
    preDisplay = pygame.Surface((1600, 900))

def build_quiz(f0,f1,f2,f3,Frage, rightAnswer=None):
    if rightAnswer is not None:

    load_image('images/background.png')
    text_box(f0, 400 - 50, 584 - 50, 100, 100, preDisplay)
    text_box(f1, 400 - 50, 784 - 50, 100, 100, preDisplay)
    text_box(f2, 1200 - 50, 584 - 50, 100, 100, preDisplay)
    text_box(f3, 1200 - 50, 784 - 50, 100, 100, preDisplay)
    text_box(Frage, 800 - 50, 309 - 50, 100, 100, preDisplay)

def name_anzeige(namen, selected = None):
    global preDisplay
    load_image("images/winner.png")
    spalte = 0
    zeile = 0
    pointer = 0
    for name in namen:
        if (zeile > 15):
            print("too many player")
        else:
            if(pointer == selected):
                text_box(name, (spalte * 300) + 100, (zeile * 100) + 200, 100, 100, preDisplay, font_size=100, color=(200, 200, 200))
            else:
                text_box(name, (spalte * 300) + 100, (zeile * 100) + 200, 100, 100, preDisplay, font_size=50)
            spalte += 1
            if (spalte >= 5):
                zeile += 1
                spalte = 0
        pointer += 1


def winner(w0="",w1="",w2=""):
    load_image("images/winner.png")
    text_box(w0, 800 - 50, 300, 100, 100, preDisplay, font_size=200)
    text_box(w1, 400 - 50, 500, 100, 100, preDisplay, font_size=100)
    text_box(w2, 1200 - 50, 600, 100, 100, preDisplay, font_size=75)


def main_loop():
    while True:
        print("[?] hey")
        response = con.readMessage()
        nresponse = ""
        for r in response:
            nresponse = nresponse + chr(r)
        print(nresponse)
        response = nresponse
        response = json.loads(response)
        gameDisplay.fill((255, 255, 255))
        preDisplay.fill((255, 255, 255))
        print(response)
        if(response["windowName"] == "QuizzesOverview"):
            name_anzeige(response["quizzes"],response["selectedQuiz"])
        if(response["windowName"] == "PlayerOverview"):
            name_anzeige(response["players"])
        if(response["windowName"] == "QuestionOverview"):
            antworten = response["answers"]
            build_quiz(antworten[0],antworten[1],antworten[2],antworten[3],response["question"])
        if(response["windowName"] == "WinnerOverview"):
            sorted_dic = sorted(response["playerPoints"].items(), key=operator.itemgetter(1))
            sorted_dic.reverse()
            if(len(sorted_dic) > 2):
                winner(w0=sorted_dic[0][0], w1=sorted_dic[1][0], w2=sorted_dic[2][0])
            elif (len(sorted_dic) > 1):
                winner(w0=sorted_dic[0][0], w1=sorted_dic[1][0])
            elif (len(sorted_dic) > 0):
                winner(w0=sorted_dic[0][0])
        #build_quiz("Antwort 1", "Antwort 2", "Antwort 3", "Antwort 4", "Was ist eine gute Frage?")
        #winner("Peter","Thomas","Atom")
        new_image = pygame.transform.scale(preDisplay, (width, height))
        gameDisplay.blit(new_image, (0, 0))

        pygame.display.update()
        for x in range(height):
            for y in range(width):
                new_image.get_at((x,y))
        e = pygame.event.get()
        for event in e:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


pygame_init()
main_loop()