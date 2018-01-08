from time import sleep
from threading import Thread

class TimerThread():
    bEnabled = True

    def run(self, time, onBegin=None, onEnd=None):
        Thread(target=self.threaded, args=(time, onBegin, onEnd)).start()

    def threaded(self, time, onBegin, onEnd):
        if onBegin != None and self.bEnabled == True:
            onBegin()

        sleep(time)

        if onEnd != None and self.bEnabled == True:
            onEnd()

    def enable(self, bEnable):
        self.bEnabled = bEnable