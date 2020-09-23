import LED_Controller
import time

class Request_Controller:
    def __init__(self):
        self.r = 255
        self.g = 255
        self.b = 255
        self.brightness = 255
        self.modus = 'selectColor'
        self.LedController = LED_Controller.LED_Controller()

    def sortModi(self, jsonObject, Strip):
        # Stop Actual Led Modus
        self.LedController.stop()
            
        self.modus = jsonObject['modus']
        
        if self.modus == 'selectColor':
            r = int(jsonObject['r'])
            g = int(jsonObject['g'])
            b = int(jsonObject['b'])
            newColors = self.LedController.changeBrightness(Strip, self.brightness, r, g, b)
            self.r = newColors[0]
            self.g = newColors[1]
            self.b = newColors[2]
            
        elif self.modus == 'pulse':
            self.brightness = jsonObject['brightness']
            newColors = self.LedController.changeBrightness(Strip, self.brightness, self.r, self.g, self.b)
            self.r = newColors[0]
            self.g = newColors[1]
            self.b = newColors[2]

        elif self.modus == 'random':
            speed = jsonObject['speed']
            self.LedController.showRandom(Strip, speed, self.r, self.g, self.b)

        elif self.modus == 'rainbow':
            speed = jsonObject['speed']
            self.LedController.showRainbow(Strip, speed)
        
        elif self.modus == 'wipe':
            speed = jsonObject['speed']
            self.LedController.showWipe(Strip, speed, self.r, self.g, self.b)
            



            
            
