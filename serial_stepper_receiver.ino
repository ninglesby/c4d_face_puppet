#include <AccelStepper.h>

#define MotorInterfaceType 1
// simple parse demo
char receivedChars[] = "This is a test, 1234, 45.3" ;
const byte numChars = 32;

char message[numChars] = {0};
int command;
int axis;
long value;
long rate;

char recvChar;
char endMarker = '>';
boolean newData = false;

//Commands
int SET_HOME = 1;
int MOVE_TO = 2;
int MOVE = 3;
int GO_HOME = 4;
int RT_MOVE = 5;
int STOP = 6;


AccelStepper axis_01(MotorInterfaceType, 4,5);
AccelStepper axis_02(MotorInterfaceType, 6,7);
AccelStepper axis_03(MotorInterfaceType, 8,9);
AccelStepper axis_04(MotorInterfaceType, 10,11);
AccelStepper axis_05(MotorInterfaceType, 12,13);
//AXIS
AccelStepper stepper[] = {axis_01,axis_02, axis_03, axis_04, axis_05};
int stepperCount = 5;

void setup() {
 Serial.begin(19200);
 Serial.println("<Arduino is ready>");
 for (int thisStepper = 0; thisStepper < stepperCount; thisStepper++) {
  stepper[thisStepper].setMaxSpeed(16000);
  stepper[thisStepper].setAcceleration(8000);
 }
}


void loop() {
  recvWithStartEndMarkers();
  executeNewCommand();
  runAllSteppers( (command == RT_MOVE) );
  
}

 void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;
 

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

void parseData() {

    // split the data into its parts
    
  char * strtokIndx; // this is used by strtok() as an index
  
  strtokIndx = strtok(receivedChars,",");      // get the first part - the string
  command = atoi( strtokIndx); // copy it to messageFromPC
  
  strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
  axis = atoi(strtokIndx);     // convert this part to an integer
  
  strtokIndx = strtok(NULL, ",");
  value = atol(strtokIndx);     // convert this part to a long

  strtokIndx = strtok(NULL, ",");
  rate = atol(strtokIndx);     // convert this part to a long

}

void executeNewCommand() {
    if (newData == true) {
        parseData();
        //showParsedData();
        if (command == MOVE_TO) {
          moveTo(axis, value);   
        } else if (command == RT_MOVE) {
          rtAnim(axis, value, rate);
        } else if (command == STOP) {
          stop();
        }
        newData = false;
    }
}

void runAllSteppers(bool useRunSpeed) {
  for (int thisStepper = 0; thisStepper < stepperCount; thisStepper++) {
      if (useRunSpeed) {
        stepper[thisStepper].runSpeed();
      } else {
        stepper[thisStepper].run();
      }
 }
}

void stop() {
  for (int thisStepper = 0; thisStepper < stepperCount; thisStepper++) {
    stepper[thisStepper].stop();
  }
 }
void moveTo(int axis, long value) {
  if (axis == 0) {
      Serial.println("I should be executing on all axes");
   } else {
      int newAxis = axis-1;
      stepper[newAxis].moveTo(value);

   }
}


void rtAnim(int axis, long value, long rate) {
  if (axis == 0) {
      Serial.println("I should be executing on all axes");
   } else {
      int newAxis = axis-1;
      stepper[newAxis].moveTo(value);
      stepper[newAxis].setSpeed(rate);

   }
}
void showParsedData() {
 Serial.print("command ");
 Serial.println(command);
 Serial.print("axis ");
 Serial.println(axis);
 Serial.print("value ");
 Serial.println(value);
}
