from rpi_ws281x import *
import random
import time

class LED_Controller():
    def __init__(self):
        self.LED_COUNT      = 196     # Number of LED pixels. Were 30 orginally
        self.LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
        self.LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
        self.LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
        self.LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
        self.LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
        
        self.isRandomRunning = False
        self.isRainbowRunning = False
        self.isWipeRunning = False
    

    # Init LED
    def initLed(self):
        Strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
        Strip.begin()

        return Strip

    # Display on LED-Strip
    def showLED(self, Strip, color):
        for i in range(Strip.numPixels()):
            Strip.setPixelColor(i, color)
            Strip.show()

    # Select a Color
    def selectColor(self, Strip, r, g, b):
        color = Color(r, g, b)
        self.showLED(Strip, color)

    # Brightness
    def changeBrightness(self, Strip, brightness, r, g, b):
        if r != 0:
            if r == 255:
                r = brightness
            else:
                r = round(brightness/2)

        if g != 0:
            if g == 255:
                g = brightness
            else:
                g = round(brightness/2)

        if b != 0:
            if b == 255:
                b = brightness
            else:
                b = round(brightness/2)

        self.selectColor(Strip, r, g, b)

        return [r, g, b]

    # Random
    def showRandom(self, Strip, wait_ms, r, g, b):
        self.isRandomRunning = True
        isCleared = False
        while self.isRandomRunning:
            ledList = []
            for i in range(Strip.numPixels()):
                ledList.append(i)
            random.shuffle(ledList)
            
            if isCleared:
                color = Color(r, g, b)
            else:
                color = Color(0, 0, 0)
                
            while len(ledList) > 0 and self.isRandomRunning:
                selectedPixel = ledList.pop()
                Strip.setPixelColor(selectedPixel, color)
                Strip.show()
                time.sleep(wait_ms/1000.0)

            isCleared = not isCleared
                
    # Rainbow helper Function
    def wheel(self, pos):
        # Generate rainbow colors across 0-255 positions
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    # Standard Rainbow
    def showRainbow(self, Strip, wait_ms):
        # Draw rainbow that fades across all pixels at once
        self.isRainbowRunning = True
        while self.isRainbowRunning:
            for j in range(256):
                if self.isRainbowRunning == True:
                    for i in range(Strip.numPixels()):
                        if self.isRainbowRunning == True:
                            Strip.setPixelColor(i, self.wheel((i+j) & 255))
                Strip.show()
                time.sleep(wait_ms/1000.0)

    # Wipe helper Function
    def wipe(self, Strip, wait_ms, color):
        for i in range(Strip.numPixels()):
            if self.isWipeRunning:
                Strip.setPixelColor(i, color)
                Strip.show()
                time.sleep(wait_ms/1000.0)

    # Wipe
    def showWipe(self, Strip, wait_ms, r, g, b):
        isCleared = False
        color = Color(r, g, b)
        if r == 0 and g == 0 and b == 0:
            color = Color(255, 255, 255)
            isCleared = True
            
        clearColor = Color(0, 0, 0)
        self.isWipeRunning = True
        while self.isWipeRunning:
            if isCleared:
                self.wipe(Strip, wait_ms, color)
                isCleared = False
            else:
                self.wipe(Strip, wait_ms, clearColor)
                isCleared = True

    def stop(self):
        self.isRandomRunning = False
        self.isRainbowRunning = False
        self.isWipeRunning = False
