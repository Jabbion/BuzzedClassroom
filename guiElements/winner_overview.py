from guiElements.main_window import MainWindows
from guiElements.guiLibary import text_box
import operator

class Winner:
    first_place = ""
    second_place = ""
    third_place = ""

    def __init__(self, json):
        sorted_dic = sorted(json["playerPoints"].items(), key=operator.itemgetter(1))
        sorted_dic.reverse()
        if(len(sorted_dic) > 0):
            self.first_place = sorted_dic[0][0]
        if(len(sorted_dic) > 1):
            self.second_place = sorted_dic[1][0]
        if(len(sorted_dic) > 2):
            self.third_place = sorted_dic[2][0]


def winner_overview(winner):
    pre_display = MainWindows.get_new_background('images/winner.png')
    text_box("Gewinner", 800 - 50, 30, 100, 100, pre_display, font_size=100)
    text_box(winner.first_place, 800 - 50, 300, 100, 100, pre_display, font_size=200)
    text_box(winner.second_place, 400 - 50, 500, 100, 100, pre_display, font_size=100)
    text_box(winner.third_place, 1200 - 50, 600, 100, 100, pre_display, font_size=75)
    return pre_display
