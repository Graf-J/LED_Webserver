from flask import Flask, request
from flask_cors import CORS
import threading
import time
import LED_Controller
import Request_Controller

# Declare Strip
Strip = None
LedController = LED_Controller.LED_Controller()
RequestController = Request_Controller.Request_Controller()

# Flask Initialisation
app = Flask(__name__)
CORS(app)

# Start Parallel Request Thread, because of some while True Loops
def startThread(jsonObject):
    myThread = threading.Thread(target=RequestController.sortModi, args=(jsonObject, Strip,))
    myThread.start()

# Timer Functions
def timer():
    seconds = 0
    while seconds < 3600:
        time.sleep(1)
        seconds += 1

    jsonObject = {
        'modus': 'selectColor',
        'r': 0,
        'g': 0,
        'b': 0
    }
    
    startThread(jsonObject)

def startTimer():
    myThread = threading.Thread(target=timer)
    myThread.start()
    
# Route
@app.route('/api/modus', methods=['POST'])
def modus():
    startTimer()
    jsonObject = request.json
    startThread(jsonObject)
    
    return 'Successfully'


# Main
if __name__ == '__main__':
    # Initialise LED
    Strip = LedController.initLed()
    startTimer()
    
    app.run(debug=True, port=1254, host='0.0.0.0')
