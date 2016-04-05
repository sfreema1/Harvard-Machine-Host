#ifndef MICROVALVES_H
#define MICROVALVES_H

#include "Arduino.h"
/*
Valve Driver-to-Digital Pin Mapping
 
 V1 = D6 | V2 = D2
 -----------------
 V3 = D9 | V4 = D5
 
 */
// ========== Global Variables ========== //

extern int microvalve_pins[4];
extern int sensor_pins[4];
extern unsigned long microvalve_opening_time_internal_mode[4];
extern unsigned long microvalve_closing_time_internal_mode[4];
extern boolean microvalve_useMicros[4];
extern unsigned long microvalve_opening_time_external_mode[4];
extern unsigned long microvalve_closing_time_external_mode[4];


//=================== Routines =====================//

void microvalves_init();
void checkForTTL();
void run_microvalve(int valve, unsigned long opening_time, unsigned long closing_time, int num_of_cycles, boolean useMicros);
void open_microvalve(int valve);
void close_microvalve(int valve);


#endif // MICROVALVES_H


