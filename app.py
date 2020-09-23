from flask import Flask, request
from flask_cors import CORS
import threading
import time
import LED_Controller
import Request_Controller
import Timer

timerThread = None
LedController = LED_Controller.LED_Controller()
RequestController = Request_Controller.Request_Controller()

# Flask Initialisation
app = Flask(__name__)
CORS(app)

# Start Parallel Request Thread, because of some while True Loops
def sendRequest(jsonObject):
    myThread = threading.Thread(target=RequestController.sortModi, args=(jsonObject, Strip,))
    myThread.start()

# Start Parallel Timer Thread
def startTimer():
    global timerThread
    timerThread = threading.Thread(target=MyTimer.startTimer)
    timerThread.start()
    
# Route
@app.route('/api/modus', methods=['POST'])
def modus():
    # Timer
    if timerThread is None:
        startTimer()
    elif timerThread.is_alive():
        MyTimer.resetTimer()
    else:
        MyTimer.initQueue()
        startTimer()
        
    jsonObject = request.json
    sendRequest(jsonObject)
    
    return 'Successfully'

# Main
if __name__ == '__main__':
    Strip = LedController.initLed()
    MyTimer = Timer.Timer(Strip, RequestController)
    
    app.run(debug=True, port=1254, host='0.0.0.0')
