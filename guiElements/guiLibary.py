from guiElements.main_window import MainWindows
import pygame
BLACK = (0, 0, 0)


def text_box(msg, x, y, weidth, height, surface, font_size=75, color=BLACK):
    small_text = pygame.font.SysFont("LikhanNormal", font_size)
    text_surf, text_rect = text_objects(msg, small_text, color=color)
    text_rect.center = ((x + (weidth / 2)), (y + (height / 2)))
    surface.blit(text_surf, text_rect)


def text_objects(text, font, color=BLACK):
    text_surface = font.render(text, True, BLACK)
    return text_surface, text_surface.get_rect()


def text_list(names, selected = None):
    temp_display = MainWindows.get_new_background('images/winner.png')
    for i, name in enumerate(names):
        spalte = i % 4
        zeile = i / 4
        print(str(spalte) + " " + str(zeile))
        if i == selected:
            text_box("[" + name + "]", (spalte * 440) + 100, (int(zeile) * 100) + 200, 100, 100, temp_display
                     , font_size=75, color=(200, 200, 200)) #old 100
        else:
            text_box(name, (spalte * 435) + 100, (int(zeile) * 100) + 200, 100, 100, temp_display, font_size=60) #old 50

    return temp_display
