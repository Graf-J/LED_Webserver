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
        self.timeToQuit = 0 # The time the While(True) Loop needs to finish

    def sortModi(self, jsonObject, Strip):
        self.LedController.stop()

        # Wait some Seconds to close the actual Thread
        if self.modus != 'selectColor' and self.modus != 'pulse':
            time.sleep(self.timeToQuit)
            
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

        elif self.modus == 'wipe':
            speed = jsonObject['speed']
            self.timeToQuit = round(speed/3) + 1
            self.LedController.showWipe(Strip, speed, self.r, self.g, self.b)
            
        elif self.modus == 'rainbow':
            speed = jsonObject['speed']
            self.timeToQuit = (speed + 1) - (speed/6)
            self.LedController.showRainbow(Strip, speed)

        elif self.modus == 'rainbowCircle':
            speed = jsonObject['speed']
            self.timeToQuit = round(speed/4) + 1
            self.LedController.showRainbowCircle(Strip, speed)

        elif self.modus == 'rainbowTheater':
            speed = jsonObject['speed']
            self.timeToQuit = speed - (speed/6) + (1/speed * 90)
            self.LedController.showRainbowTheater(Strip, speed)


            
            
