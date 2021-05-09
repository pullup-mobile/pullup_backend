import pyrebase
import cv2
import numpy as np
from picamera import PiCamera
from time import sleep
import time
from datetime import datetime

camera = PiCamera()

config = {
    "apiKey": "AIzaSyB8aLUNV7U6SCxXEZelvbKWN8hXmrwL5MQ",
    "authDomain": "pullup-5edde.firebaseapp.com",
    "databaseURL": "https://pullup-5edde-default-rtdb.firebaseio.com",
    "projectId": "pullup-5edde",
    "storageBucket": "pullup-5edde.appspot.com",
    "messagingSenderId": "443552526831",
    "appId": "1:443552526831:web:896e3bf4195852f4b4461a",
    "measurementId": "G-Y99W2G7087"
}


firebase = pyrebase.initialize_app(config)

db = firebase.database()



while True:

    sleep(1)
    camera.capture('/tmp/picture.jpg')
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Image captured at: " + str(current_time))
    
#camera.stop_preview()

    net = cv2.dnn.readNet("/home/pi/pull_up/yolov3.weights", "/home/pi/pull_up/yolov3.cfg")
    classes = []
    with open("/home/pi/pull_up/coco_1.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Loading image
    img = cv2.imread("/tmp/picture.jpg")
    img = cv2.resize(img, None, fx=0.7, fy=0.7)
    height, width, channels = img.shape

# Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

# Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
            # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

            # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
#print(indexes)
#num= len(indexes)


    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
    car_num = 0
    motor_num=0
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            if label == "car" :
                car_num = car_num +1
                
            if  label == "motorbike":
                motor_num = motor_num +1


            
    print("cars: "+ str(car_num))
    print("motor:"+ str(motor_num))
    print("total:")
    print(car_num + motor_num)
    
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    data = {"available_spots": 20 - car_num - motor_num}
    db.child("North_Garage_Floor_1").child("Section_A").set(data)
    print("data added to real time database")