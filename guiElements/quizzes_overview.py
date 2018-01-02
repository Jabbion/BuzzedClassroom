from guiElements.player_overview import player_overview
from guiElements.guiLibary import text_box, text_list

def quizzes_overview(quiz: list, selected=None):
    img = text_list(quiz, selected)
    text_box("Gewinner", 800 - 50, 30, 100, 100, img, font_size=100)
    return img
