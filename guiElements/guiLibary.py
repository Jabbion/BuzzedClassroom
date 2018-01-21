from guiElements.main_window import MainWindows
import pygame
BLACK = (0, 0, 0)

# <Settings>
topDownDiffList = 80
fontSizeSelectedList = 80
fontSizeUnselectedList = 50
visibleNumPerPage = 7

def text_box(msg, x, y, width, height, surface, font_size=75, color=BLACK):
    small_text = pygame.font.SysFont("LikhanNormal", font_size)
    text_surf, text_rect = text_objects(msg, small_text, color=color)
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    surface.blit(text_surf, text_rect)

def text_objects(text, font, color=BLACK):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

def text_list(names, selected = None):
    temp_display = MainWindows.get_new_background('images/winner.png')
    for i, name in enumerate(names):
        spalte = i % 5
        zeile = i / 5
        if i == selected:
            text_box("[" + name + "]", (spalte * 300) + 100, (int(zeile) * 50) + 200, 100, 100, temp_display
                     , font_size=50) #old 100
        else:
            text_box(name, (spalte * 300) + 100, (int(zeile) * 50) + 200, 100, 100, temp_display, font_size=25) #old 50

    return temp_display

def top_down_text_list(names, selected = None):
    bHighlight = True
    if selected == None:
        selected = 0
        bHighlight = False

    visibleNames = []
    lenNames = len(names)
    bScrollable = False

    if selected < visibleNumPerPage:
        if lenNames < visibleNumPerPage:
            visibleNames = names[0:lenNames]
        else:
            visibleNames = names[0:visibleNumPerPage]

            if visibleNumPerPage < lenNames:
                bScrollable = True

    elif selected >= visibleNumPerPage:
        if selected < lenNames - 1:
            bScrollable = True

        visibleNames = names[selected - visibleNumPerPage + 1: selected + 1]
        selected = visibleNumPerPage - 1

    temp_display = MainWindows.get_new_background("images/winner.png")
    xMax, yMax = temp_display.get_size()

    for i, name in enumerate(visibleNames):
        if i == selected and bHighlight == True:
            text_box("[ " + name + " ]", xMax / 2 - 40, i * topDownDiffList + 150, 100, 100, temp_display, font_size = fontSizeSelectedList)
        else:
            text_box(name, xMax / 2 - 40, i * topDownDiffList + 150, 100, 100, temp_display, font_size=fontSizeUnselectedList)

    if bScrollable == True:
        text_box("...", xMax / 2 - 40, visibleNumPerPage * topDownDiffList + 150, 100, 100, temp_display, font_size=fontSizeUnselectedList)

    return temp_display
