#include <Wire.h>

/*
 * Count and store the number of detected turns from the 2 attached quadrature encoders.
 * A turn is counted when the encoder A signal rises or falls and the direction of turn
 * is given by the encoder B signal's current state. 
 * 
 * A \ B | HIGH | LOW
 * RISE  |  ->  |  <- 
 * FALL  |  <-  |  ->
 * (or generally if both signals equal = forward turn, not equal = reverse)
 * 
 * Note this does mean that each RISE + FALL will denote 2 turns though really only
 * one sweep of the sensors has occured. This helps as when the measured rotation changes  
 * direction midway through the single turn will be undone.
 * 
 * The turn count is reset when sent in response to a i2c read request.
 */

const int enc1APin = 2;
const int enc1BPin = 5;

const int enc2APin = 3;
const int enc2BPin = 6;

int enc1Turns = 0;
int enc2Turns = 0;

void setup() {
  pinMode(enc1APin, INPUT_PULLUP);
  pinMode(enc1BPin, INPUT_PULLUP);
  pinMode(enc2APin, INPUT_PULLUP);
  pinMode(enc2BPin, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(enc1APin), updateEncoder1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(enc2APin), updateEncoder2, CHANGE);
  
  // start i2c
  Wire.begin(8);                // join i2c bus with address #8
  Wire.onRequest(requestEvent); // register event
}

void loop () {
}

void updateEncoder1() {
  enc1Turns += digitalRead(enc1APin) == digitalRead(enc1BPin) ? 1 : -1;
}

void updateEncoder2() {
  enc2Turns += digitalRead(enc2APin) == digitalRead(enc2BPin) ? 1 : -1;
}

void requestEvent() {
  byte* pInt = (byte*)&enc1Turns;
  Wire.write(pInt, sizeof(enc1Turns));
  enc1Turns = 0;

  pInt = (byte*)&enc2Turns;
  Wire.write(pInt, sizeof(enc2Turns));
  enc2Turns = 0;
}
