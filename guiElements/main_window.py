import pygame
import sys
from pygame.locals import *
import socket
from threading import Thread
import signal
import os

class MainWindows():

    gameDisplay = None
    width = 0
    height = 0
    HOST = '127.0.0.1'
    PORT = 1234
    sock = None


    def __init__(self, width, height, fullscreen = False):
        #self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock.connect((self.HOST, self.PORT))
        pygame.init()
        if fullscreen:
            infoObject = pygame.display.Info()
            self.gameDisplay = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
            self.width = infoObject.current_w
            self.height = infoObject.current_h
        else:
            self.gameDisplay = pygame.display.set_mode((width, height))
            self.width = width
            self.height = height
        Thread(target=self.main_loop, args=()).start()

    @staticmethod
    def get_new_background(path):
        pre_display = pygame.Surface((1600, 900))
        pre_display.blit(pygame.image.load(path), (0, 0))
        return pre_display

    def set_image(self, image):
        new_image = pygame.transform.scale(image, (self.width, self.height))
        self.gameDisplay.blit(new_image, (0, 0))

        """
        for x in range(self.width):
            for y in range(self.height):
                pix = new_image.get_at((x,y))
                print(pix)
                #self.pixel(x,y,pix[0], pix[1], pix[2])
        """


    def pixel(self, x, y, r, g, b, a=255):
        if a == 255:
            self.send('PX %d %d %02x%02x%02x\n' % (x, y, r, g, b))
        else:
            self.send('PX %d %d %02x%02x%02x%02x\n' % (x, y, r, g, b, a))

    def send(self, string):
        self.sock.send(string.encode("utf-8"))

    def quit(self):
        os.kill(os.getpid(), signal.SIGUSR1)
        pygame.quit()
        sys.exit()

    def main_loop(self):
        while True:
            pygame.display.update()
            e = pygame.event.get()
            for event in e:
                if event.type == QUIT:
                    os.kill(os.getpid(), signal.SIGUSR1)
                    pygame.quit()
                    sys.exit()
