#include <MicroView.h>
#include <Wire.h>

/*
 * Count and store the number of detected turns from the attached quadrature encoder.
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

const int encAPin = 3;
const int encBPin = 2;

void setup() {
  pinMode(encAPin, INPUT_PULLUP);
  pinMode(encBPin, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(encAPin), updateEncoderA, CHANGE);

  // start MicroView
  uView.begin();

  // start i2c
  Wire.begin(8);                // join i2c bus with address #8
  Wire.onRequest(requestEvent); // register event
}

int turns = 0;

int nextScreenUpdate = 0;

void loop () {
  int t = millis();
  if (t > nextScreenUpdate) {
    uView.clear(PAGE);          // clear page
    uView.setCursor(0, 0);
    uView.print("\nTurns:" + String(turns));
    uView.display();

    nextScreenUpdate = t + 1000;
  }
}

void updateEncoderA() {
  turns += digitalRead(encAPin) == digitalRead(encBPin) ? 1 : -1;
}

void requestEvent() {
  byte* pInt = (byte*)&turns;
  Wire.write(pInt, sizeof(turns));
  turns = 0;
}
