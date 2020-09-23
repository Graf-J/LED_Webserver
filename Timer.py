import time
import queue
import json

class Timer:
    def __init__(self, Strip, RequestController):
        self.Strip = Strip
        self.RequestController = RequestController
        self.q = queue.Queue()
        self.initQueue()

    def initQueue(self):
        for i in range(3600):
            self.q.put(i)
        self.q.put(None)

    def startTimer(self):
        timeToSleep = 1
        while self.q.get() is not None:
            time.sleep(timeToSleep)

        self.turnOffLed()

    def resetTimer(self):
        with self.q.mutex:
            self.q.queue.clear()
        self.initQueue()

    def turnOffLed(self):
        jsonObject = {
            "modus": "selectColor",
            "r": 0,
            "g": 0,
            "b": 0
        }
        self.RequestController.sortModi(jsonObject, self.Strip)
        
