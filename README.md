# COMSATS-Final-Year-Project
# Introduction:
This project represents a cutting-edge solution to help individuals with physical challenges by utilizing Brain Computer Interface (BCI) technology. The purpose of the smart wheelchair is to empower those with physical limitations by allowing them to control the movement of the wheelchair solely with their thoughts. This innovative technology offers a new level of independence and freedom for people with disabilities and opens up new possibilities for their daily lives.

# Equipment/Software Used:
* Customised Wheelchair
* Emotiv Insight Headset
* 2 Arduino borads
* 2 Xbee modules
* Emotiv Launcher software
* EmotivBCI software

# Project Repository:
* 'Wheelchair.py': connects to the CortexAPI to get real-time brain signals and detects the desired command. This information is then sent to the Arduino via serial communication. 
* 'SenderArduino.ino':  Receives the data from python script,  and sends it to the receiver Arduino that is connected to the wheelchair.
* 'RecieverArduino.ino': Recieves the command and controls wheelchair movement

# Safety Measures:
For user safety, the wheelchair is equipped with an ultrasound sensor and computer vision technology to detect obstacles in its path.

# Note: 
This README file provides a brief overview of the project and its components. For detailed information, please refer to the code and comments in the repository.
