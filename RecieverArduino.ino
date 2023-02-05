#include <SoftwareSerial.h>
#include <stdio.h>
#include <NewPing.h>

// Creates a software serial object named "xbee" using pins 2 and 3
SoftwareSerial xbee(2, 3);

// Define the Echo and Trigger pins for the HC-SR04 Ultrasonic sensor
#define ECHO_PIN 11 
#define TRIG_PIN 12 

// Create an instance of NewPing library using TRIG_PIN and ECHO_PIN
NewPing sonar(TRIG_PIN, ECHO_PIN);

// Declare the distance and voteBack variables
int distance;
int voteBack;

// Declare the pins for forward, backward, left, and right movements
int pin1 = 5; 
int pin2 = 6; 
int pin3 = 9;
int pin4 = 10; 

// Declare the tmp variable
char tmp;

void setup() {
    // Set the TRIG_PIN as an OUTPUT
    pinMode(TRIG_PIN, OUTPUT); 

    // Set the ECHO_PIN as an INPUT
    pinMode(ECHO_PIN, INPUT); 

    // Start the xbee communication at 9600 baud rate
    xbee.begin(9600);

    // Start the serial communication at 9600 baud rate
    Serial.begin(9600);

    // Print a message to indicate that the XBee communication has started
    Serial.println("Starting XBee Communication");

    // Set the pins 5, 6, 9, and 10 as OUTPUTs
    pinMode(5, OUTPUT);
    pinMode(6, OUTPUT);
    pinMode(9, OUTPUT);
    pinMode(10, OUTPUT);

    // Set the speed to 200 (not used in the code)
    speed = 200;
}

void loop() {
    // Wait for 30 milliseconds
    delay(30);

    // Measure the distance using the HC-SR04 ultrasonic sensor
    distance = sonar.ping_cm();

    // If the distance is between 10 and 50 cm and the tmp value is not 'b', then do the following:
    if (distance > 10 && distance < 50 && tmp!='b') {
        // Print a message indicating that the critical distance is less than 50 cm
        Serial.println("Critical distance less than 50");

        // Print "Off"
        Serial.println("Off");

        // Set the forward, left, and right pins to 0
        analogWrite(pin1, 0);
        analogWrite(pin3, 0);
        analogWrite(pin4, 0);

        // Call the "control" function
        control();

    // Otherwise, call the "control" function
    } else {
        control();
    }
}
// Function to control the movement of the motor based on the character received from the Xbee
void control() {
    // Check if there is any data available from the Xbee
    if (xbee.available()) {
        tmp = xbee.read(); // Read the received character

        // Check which character is received and act accordingly
        if (tmp == 'f') {
            voteBack = 0; // Reset the voteBack counter
            Serial.println("forward pin on");
            forward();
        } else if (tmp == 'c') {
            Serial.println("Stopping");
            stop();
        } else if (tmp == 'l') {
            voteBack = 0; // Reset the voteBack counter
            Serial.println("left pin on");
            left();
        } else if (tmp == 'r') {
            voteBack = 0; // Reset the voteBack counter
            Serial.println("right pin on");
            right();
        } else if (tmp == 'b') {
            voteBack++; // Increment the voteBack counter
            // If the voteBack counter reaches 10, move the motor backward
            if (voteBack > 9) {
                Serial.println("backward pin on");
                backward();
                voteBack = 0; // Reset the voteBack counter
            } 
        }
    }
}

// Function to move the motor forward
void forward() {
    Serial.println("Moving forward");
    digitalWrite(pin1, HIGH); // Set pin1 to high to move the motor forward
    digitalWrite(pin2, LOW);
    digitalWrite(pin3, LOW);
    digitalWrite(pin4, LOW);
}

// Function to move the motor backward
void backward() {
    Serial.println("Moving backward");
    digitalWrite(pin2, HIGH); // Set pin2 to high to move the motor backward
    digitalWrite(pin4, LOW);
    digitalWrite(pin3, LOW);
    digitalWrite(pin1, LOW);
}

// Function to move the motor to the left
void left() {
    Serial.println("Moving left");
    digitalWrite(pin3, HIGH); // Set pin3 to high to move the motor to the left
    digitalWrite(pin2, LOW);
    digitalWrite(pin1, LOW);
    digitalWrite(pin4, LOW);
}

// Function to move the motor to the right
void right() {
    Serial.println("Moving right");
    digitalWrite(pin4, HIGH); // Set pin4 to high to move the motor to the right
    digitalWrite(pin2, LOW);
    digitalWrite(pin1, LOW);
    digitalWrite(pin4, LOW);
}

// Function to stop the motor
void stop() {
    Serial.println("Stopping");
    // Set all the pins to low to stop the motor
    analogWrite(pin1, 0);
    analogWrite(pin2, 0);
    analogWrite(pin3, 0);
    analogWrite(pin4, 0);
}
