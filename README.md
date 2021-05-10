# pullup_backend
Cross-platform mobile application that displays parking lot vacancy using deep learning data.

Part of: https://github.com/pullup-mobile.

## Prerequisites
1. Raspberry Pi with compatible camera attachment
2. Python IDE 3.9+

## Backend Installation and Setup
1. Install your preffered Python IDE, please make sure it is version 3.9 or above to avoid any complications
2. In your Raspberry Pi Terminal run the following commands:
```
sudo pip3 install pyrebase
sudo pip3 install opencv-python
sudo apt-get install python-picamera
sudo pip3 install numpy
sudo pip3 install datetime
```
Next, make sure your camera port is turned on for the Raspberry Pi by doing the following:

4. In your terminal enter 'sudo raspi-config'
5. Navigate to Interfacing Options and select it
6. Navigate to Camera and set it to Enable
7. Select Finish



After this setup, you will be able to run the (Will insert name here when I change it).py file
