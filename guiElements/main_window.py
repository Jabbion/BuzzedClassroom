import pygame
import sys
from pygame.locals import *
import socket

class MainWindows():

    gameDisplay = None
    width = 0
    height = 0
    HOST = '127.0.0.1'
    PORT = 1234
    sock = None


    def __init__(self, width, height):
        #self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock.connect((self.HOST, self.PORT))
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height

    @staticmethod
    def get_new_background(path):
        pre_display = pygame.Surface((1600, 900))
        pre_display.blit(pygame.image.load(path), (0, 0))
        return pre_display

    def set_image(self, image):
        new_image = pygame.transform.scale(image, (self.width, self.height))
        self.gameDisplay.blit(new_image, (0, 0))
        pygame.display.update()

        """
        for x in range(self.width):
            for y in range(self.height):
                pix = new_image.get_at((x,y))
                print(pix)
                #self.pixel(x,y,pix[0], pix[1], pix[2])
        """

        e = pygame.event.get()
        for event in e:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def pixel(self, x, y, r, g, b, a=255):
        if a == 255:
            self.send('PX %d %d %02x%02x%02x\n' % (x, y, r, g, b))
        else:
            self.send('PX %d %d %02x%02x%02x%02x\n' % (x, y, r, g, b, a))

    def send(self, string):
        self.sock.send(string.encode("utf-8"))


