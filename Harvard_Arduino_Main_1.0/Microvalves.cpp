// Microvalves.cpp

#include "Arduino.h"
#include "Microvalves.h"
#include "Configuration.h"

// ========== Variables ========== //

int microvalve_pins[4] = {
  MICROVALVE_PIN_1, MICROVALVE_PIN_2, MICROVALVE_PIN_3, MICROVALVE_PIN_4};
int sensor_pins[4] = { 
  SENSOR_PIN_1, SENSOR_PIN_2, SENSOR_PIN_3, SENSOR_PIN_4};

unsigned long microvalve_opening_time_internal_mode[4] = {
  DEFAULT_OPENING_TIME_INTERNAL_MODE_MILLIS, 
  DEFAULT_OPENING_TIME_INTERNAL_MODE_MILLIS, 
  DEFAULT_OPENING_TIME_INTERNAL_MODE_MILLIS, 
  DEFAULT_OPENING_TIME_INTERNAL_MODE_MILLIS};

unsigned long microvalve_closing_time_internal_mode[4] = {
  DEFAULT_CLOSING_TIME_INTERNAL_MODE_MILLIS, 
  DEFAULT_CLOSING_TIME_INTERNAL_MODE_MILLIS, 
  DEFAULT_CLOSING_TIME_INTERNAL_MODE_MILLIS, 
  DEFAULT_CLOSING_TIME_INTERNAL_MODE_MILLIS};

unsigned long microvalve_opening_time_external_mode[4] = {
  DEFAULT_OPENING_TIME_EXTERNAL_MODE_MICROS,
  DEFAULT_OPENING_TIME_EXTERNAL_MODE_MICROS,
  DEFAULT_OPENING_TIME_EXTERNAL_MODE_MICROS,
  DEFAULT_OPENING_TIME_EXTERNAL_MODE_MICROS
};

unsigned long microvalve_closing_time_external_mode[4] = {
  DEFAULT_CLOSING_TIME_EXTERNAL_MODE_MICROS,
  DEFAULT_CLOSING_TIME_EXTERNAL_MODE_MICROS,
  DEFAULT_CLOSING_TIME_EXTERNAL_MODE_MICROS,
  DEFAULT_CLOSING_TIME_EXTERNAL_MODE_MICROS
};

// ========== Routines ========== //

boolean microvalve_useMicros[4] = {
  false, false, false, false};

void microvalves_init(){
  for (int i = 0; i<4; i++){
    pinMode(microvalve_pins[i],OUTPUT);
  }
}

void checkForTTL(){
  for(int i = 0; i<4; i++){
    if ((analogRead(sensor_pins[i])>512)){
      digitalWrite(microvalve_pins[i],HIGH);
      delayMicroseconds(750);
      digitalWrite(microvalve_pins[i],LOW);
      delayMicroseconds(3000);
    }
  }
}

void run_microvalve(int valve, unsigned long opening_time, unsigned long closing_time, int num_of_cycles, boolean useMicros){
  Serial.println("Unable to receive or process any additional commands until microvalve process is complete");
  for (int i = 0; i < num_of_cycles; i++){
    digitalWrite(microvalve_pins[valve],HIGH);
    // Determine whether to use delay in micros or millis
    if(useMicros) delayMicroseconds(opening_time);
    else delay(opening_time);

    digitalWrite(microvalve_pins[valve],LOW);
    // Closing time is always in millis
    delay(closing_time);
  }
  Serial.println("Microvalve process complete");
}

void open_microvalve(int valve){
  Serial.print("Opening valve ");Serial.println(valve+1);
  digitalWrite(microvalve_pins[valve],HIGH);
}

void close_microvalve(int valve){
  Serial.print("Closing valve ");Serial.println(valve+1);
  digitalWrite(microvalve_pins[valve],LOW);
}
