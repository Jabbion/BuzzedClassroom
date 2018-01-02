from guiElements.main_window import MainWindows
from guiElements.guiLibary import text_list, text_box


def player_overview(names : list, selected = None):
    img = text_list(names, selected)
    text_box("Spieler", 800 - 50, 30, 100, 100, img, font_size=100)
    return img
