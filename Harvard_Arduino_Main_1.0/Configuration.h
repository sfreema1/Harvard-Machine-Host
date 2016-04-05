#ifndef CONFIGURATION_H
#define CONFIGURATION_H

#define BAUDRATE 9600

#define DEBUG_MODE // Uncomment to enable additional feature for debugging purposes

// Serial communication baudrate
#define BAUDRATE 9600
// Maximum length of a command
#define MAX_CMD_SIZE 96
// Pin connected to the digipot slave select pin
#define SS_PIN  10

// Sensor pins are analog input pins to detect Newmark TTL pulses that should trigger pin opening and closing
#define SENSOR_PIN_1 A0
#define SENSOR_PIN_2 A2
#define SENSOR_PIN_3 A4
#define SENSOR_PIN_4 A5
// Microvalve pins are digital output pins to send square pulses to the valve drivers to open microvalves
#define MICROVALVE_PIN_1 2
#define MICROVALVE_PIN_2 5
#define MICROVALVE_PIN_3 6
#define MICROVALVE_PIN_4 9

// Default timing for running microvalves
#define DEFAULT_OPENING_TIME_INTERNAL_MODE_MILLIS 1000 // in milliseconds
#define DEFAULT_CLOSING_TIME_INTERNAL_MODE_MILLIS 1000 // in milliseconds
#define DEFAULT_OPENING_TIME_EXTERNAL_MODE_MICROS 750 // in microseconds
#define DEFAULT_CLOSING_TIME_EXTERNAL_MODE_MICROS 3000 // in microseconds

// Max and min timing for running microvalves
#define MAX_OPENING_TIME_INTERNAL_MODE_MILLIS 10000 // in milliseconds
#define MIN_OPENING_TIME_INTERNAL_MODE_MILLIS 1 // in milliseconds

#define MAX_OPENING_TIME_INTERNAL_MODE_MICROS 1200 // in microseconds
#define MIN_OPENING_TIME_INTERNAL_MODE_MICROS 300 // in microseconds

#define MAX_CLOSING_TIME_INTERNAL_MODE_MILLIS 10000 // in milliseconds
#define MIN_CLOSING_TIME_INTERNAL_MODE_MILLIS 1 // in milliseconds

#define MAX_OPENING_TIME_EXTERNAL_MODE_MICROS 1000 // in microseconds
#define MIN_OPENING_TIME_EXTERNAL_MODE_MICROS 400 // in microseconds

#endif // CONFIGURATION_H
