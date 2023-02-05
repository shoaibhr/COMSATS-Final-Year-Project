import json
import cv2
import serial
from websocket import create_connection

# Create serial connection to communicate with Xbee
port=''
arduino = serial.Serial(port, 9600)

# Create WebSocket connection to communicate with Cortex API
ws = create_connection("wss://localhost:6868")

# Constants for storing the command and confidence level from Cortex API
command = ""
confLevel = 0.0

# Constants for object detection using computer vision
thres = 0.45  # Threshold for detecting objects
configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'  # Path to the model configuration file
weightsPath = 'frozen_inference_graph.pb'  # Path to the model weights file

person = 1  # Label for person
chair = 62  # Label for chair
desk = 69  # Label for desk
door = 71  # Label for door

# Functions for communicating with Cortex API

def check_connect():
    """
    Check if the connection to Cortex API is established.
    Returns the information of the Cortex API.
    """
    ws.send(json.dumps({
        "id": 1,
        "jsonrpc": "2.0",
        "method": "getCortexInfo"
    }))
    result = ws.recv()
    result = json.loads(result)
    return result


def query_headsets():
    """
    Query the available headsets connected to the Cortex API.
    Returns the information of the available headsets.
    """
    ws.send(json.dumps({
        "id": 1,
        "jsonrpc": "2.0",
        "method": "queryHeadsets"
    }))
    result = ws.recv()
    result = json.loads(result)
    return result


def control_headset():
    """
    Connect to a specific headset.
    Returns the information of the connected headset.
    """
    ws.send(json.dumps({
        "id": 1,
        "jsonrpc": "2.0",
        "method": "controlDevice",
        "params": {
            "command": "connect",
            "headset": "" #add headset ID

        }}))
    result = ws.recv()
    result = json.loads(result)
    return result


def close_connection():
    """
    Close the connection to Cortex API.
    """
    ws.close()


def getUserLogin():
    """
    Get the login information of the user.
    Returns the login information of the user.
    """
    ws.send(json.dumps({
        "id": 1,
        "jsonrpc": "2.0",
        "method": "getUserLogin"
    }))
    result = ws.recv()
    result = json.loads(result)
    return result


def accessright(clientId, clientSecret):
    """
    Request access to the Cortex API using a client ID and client secret.
    """
    # send a JSON-RPC request to the Cortex API with the client ID and secret
    ws.send(json.dumps({
        "id": 1,
        "jsonrpc": "2.0",
        "method": "requestAccess",
        "params": {
            "clientId": clientId,
            "clientSecret": clientSecret
        }
    }))
    # receive the result of the request
    result = ws.recv()
    # parse the result as a JSON object
    result = json.loads(result)
    # return the result
    return result

def authorizeUser(clientId, clientSecret):
    """
    Authorize a user to access their Cortex data.
    """
    # send a JSON-RPC request to the Cortex API with the client ID and secret
    ws.send(json.dumps({
        "id": 1,
        "jsonrpc": "2.0",
        "method": "authorize",
        "params": {
            "clientId": clientId,
            "clientSecret": clientSecret
        }
    }))
    # receive the result of the request
    result = ws.recv()
    # parse the result as a JSON object
    result = json.loads(result)
    # return the result
    return result

def queryHeadset():
    """
    Query available headsets connected to the Cortex API.
    """
    # send a JSON-RPC request to the Cortex API to query available headsets
    ws.send(json.dumps({
        "id": 1,
        "jsonrpc": "2.0",
        "method": "queryHeadsets"
    }))
    # receive the result of the request
    result = ws.recv()
    # parse the result as a JSON object
    result = json.loads(result)
    # return the result
    return result

def openSession(cortexToken, headset):
    """
    Open a new session with the Cortex API.
    """
    # send a JSON-RPC request to the Cortex API to open a new session
    ws.send(json.dumps({
        "id": 1,
        "jsonrpc": "2.0",
        "method": "createSession",
        "params": {
            "cortexToken": cortexToken,
            "headset": headset,
            "status": "open"
        }
    }))
    # receive the result of the request
    result = ws.recv()
    # parse the result as a JSON object
    result = json.loads(result)
    # return the result
    return result

def subscribeData(cortexToken, sessionId):
    global command
    global confLevel

    # Send the "subscribe" command to the WebSocket
    ws.send(json.dumps({
        "id": 1,
        "jsonrpc": "2.0",
        "method": "subscribe",
        "params": {
            "cortexToken": cortexToken,
            "session": sessionId,
            "streams": ["com"]
        }
    }))

    flag = 0
    temp1 = 's'
    temp = 'neutral'

    # Continuously receive data from the WebSocket
    while True:
        result = ws.recv()
        result = json.loads(result)

        # Skip the first received message
        if flag == 0:
            flag = 1
            continue

        # Get the "command" and "confLevel" from the received data
        command = result['com'][0]
        confLevel = result['com'][1]

        # Initialize the "ardCommand" to "neutral"
        ardCommand = 'neutral'

        # Determine the "ardCommand" based on the "command" and "confLevel"
        if command == 'neutral':
            ardCommand = 'neutral'
        elif command == 'push' and confLevel >= 0.50:
            ardCommand = 'push'
        elif command == 'pull' and confLevel >= 0.55:
            ardCommand = 'pull'
        elif command == 'left' and confLevel >= 0.50:
            ardCommand = 'left'
        elif command == 'right' and confLevel >= 0.50:
            ardCommand = 'right'

        # Append a line break character to the "ardCommand"
        ardCommand = command + '\r'

        # Write the "ardCommand" to the Arduino if it's not "neutral"
        if command != 'neutral':
            arduino.write(ardCommand.encode())
            print(ardCommand)

        # Use OpenCV to detect objects in an image
        success, img = cap.read()
        classIds, confs, bbox = net.detect(img, confThreshold=thres)
        if person in classIds:
            print('person detected')
            ardCommand = 'person' + '\r'
            arduino.write(ardCommand.encode())
        if chair in classIds:
            print('chair detected')
            ardCommand = 'person' + '\r' #keeping arduino command same as reciver will stop wheelchair if ardCommand is person
            arduino.write(ardCommand.encode())
        if door in classIds:
            print('door detected')
            ardCommand = 'door' + '\r'
            arduino.write(ardCommand.encode())
        if desk in classIds:
            print('desk detected')
            ardCommand = 'person' + '\r'
            arduino.write(ardCommand.encode())
        if len(classIds) != 0:
            for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
                cv2.putText(img, classNames[classId-1].upper(), (box[0]+10, box[1]+20),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(img, str(round(confidence*100, 2)), (box[0]+200, box[1]+20),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        # Display the image with the label
        cv2.imshow("Output", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    # Define the client ID and client secret for the Cortex API authorization
    myClientId = ""
    myClientSecret = ""
    
    # Define the headset ID
    headset = "INSIGHT-A1D2054C"  # NEW

    # Check the connection status to the Cortex API
    connect = check_connect()

    # Query the available headsets connected to the Cortex API
    headsets = query_headsets()

    # Control the selected headset and get the details
    specific_headset = control_headset()

    # Authorize the user to use the Cortex API
    authorization = authorizeUser(
        clientId=myClientId, clientSecret=myClientSecret)

    # Get the Cortex token for the authorized user
    cortexToken = authorization['result']['cortexToken']

    # Open a session with the selected headset using the Cortex token
    sessionOutput = openSession(cortexToken, headset)

    # Get the session ID
    sessionID = sessionOutput['result']['id']

    # CV Code
    # Initialize the video capture
    cap = cv2.VideoCapture(0)
    cap.set(3, 320)  # Set the width of the frames in the video stream
    cap.set(4, 240)  # Set the height of the frames in the video stream
    cap.set(10, 70)  # Set the brightness of the frames in the video stream

    # Read the class names from the .names file
    classNames = []
    classFile = 'coco.names'
    with open(classFile, 'rt') as f:
        classNames = [line.strip() for line in f]

    # Load the trained DNN model for object detection
    net = cv2.dnn_DetectionModel(weightsPath, configPath)
    net.setInputSize(320, 320)  # Set the input size for the model
    net.setInputScale(1.0 / 127.5)  # Set the input scale for the model
    net.setInputMean((127.5, 127.5, 127.5))  # Set the input mean for the model
    net.setInputSwapRB(True)  # Set the input swap RB for the model

    # Subscribe to the data stream from the selected headset
    subscribeData(cortexToken, sessionID)
