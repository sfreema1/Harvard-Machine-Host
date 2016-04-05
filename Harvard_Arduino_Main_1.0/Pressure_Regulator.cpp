// Pressure_regulator.cpp
#include "Arduino.h"
#include "Configuration.h"
#include "SPI.h"

/*
Testing the pressure regulators for different input values
with M0 RX LY commands
M0 R2 L255 = 7.4 PSI
M0 R2 L254 = 7.3 PSI
M0 R2 L253 = 7.2-7.3 PSI
M0 R2 L252 = 7.2 PSI
M0 R2 L251 = 7.1 PSI
M0 R2 L250 = 7.0-7.1 PSI
M0 R2 L240 = 6.4 PSI
M0 R2 L230 = 5.8 PSI
M0 R2 L220 = 5.3-5.4 PSI
M0 R2 L210 = 4.9-5.0 PSI
M0 R2 L200 = 4.5-4.6 PSI
M0 R2 l190 = 4.2 PSI
M0 R2 L180 = 3.9 PSI
M0 R2 L170 = 3.6 PSI
M0 R2 L160 = 3.4 PSI
M0 R2 L150 = 3.1-3.2 PSI
M0 R2 L100 = 2.1 PSI
M0 R2 L90 = ERROR: The program thinks that I am trying to exceed the scale.
M0 R2 L090 = 1.9 PSI This works, but I shouldn't have to use this work around
M0 R2 L080 = 1.7 PSI
M0 R2 L070 = 1.5 PSI
M0 R2 L060 = 1.3-1.4 PSI
M0 R2 L055 = 1.2-1.3 PSI
M0 R2 L050 = 1.1-1.2 PSI
M0 R2 L025 = 0.6 PSI

When giving the firmware a number with N digits, and then giving it a number with N-1 digits, an error occurs with the strchr functionality.
This was fixed by adding the "terminate the string" line back into the get_command() function.
*/

// ========== Routines ========== // 

void set_pressure(int address, int level) { // Routine to control pressure
  digitalWrite(SS_PIN, LOW);
  SPI.transfer(address);
  SPI.transfer(level);
  digitalWrite(SS_PIN, HIGH);
}

void press_reg_init() {
  SPI.begin();
  // Set slave select (SS) pin of digitpot to output, and preset it HIGH since it is active low
  pinMode(SS_PIN, OUTPUT);
  digitalWrite(SS_PIN, HIGH);
  for (int i = 0; i < 4; i++) {
    set_pressure(i, 0);
  }
}
