// This Arduino code reads data from the serial port, processes it, and sends it to the wheelchair Arduino

String myCmd;
#include <SoftwareSerial.h>
SoftwareSerial xbee(4, 5); // RX and TX pins

void setup() {
  Serial.begin(9600); // Start the serial communication with a baud rate of 9600
  xbee.begin(9600); // Start the serial communication with the xbee with a baud rate of 9600
}

void loop() {
  // Wait until there's data available from the serial port
  while (!Serial.available()) { 
  }
  
  myCmd = Serial.readStringUntil('\r'); // Read the serial data until the carriage return character '\r'

  // Check the value of the command and send the corresponding value to the xbee
  if (myCmd == "neutral") {
    xbee.println('s');
  }
  else if (myCmd == "push") {
    xbee.println('f');
  }
  else if (myCmd == "pull") {
    xbee.println('b');
  }
  else if (myCmd == "left") {
    xbee.println('l');
  }
  else if (myCmd == "person") {
    xbee.println('c');
  }
  else if (myCmd == "right") {
    xbee.println('r');
  }
}
