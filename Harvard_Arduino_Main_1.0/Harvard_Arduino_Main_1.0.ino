#include "Microvalves.h"
#include "Configuration.h"
#include "SPI.h"
#include "Pressure_Regulator.h"

/*
//====================== Change Log =============//
 1. Added into digipot_init() function the default function of setting all pressure regulators down to zero to make sure no air is leaking from the start.
 2. Changed order of setup routine so the display_welcome() routine ran after instantiating the serial object.
 3. Changed message when pressure regulator was set.
 4. Added the "terminate the string" line back in. This fixes the inconsistent digit reading of commands
 5. Added in more help options
 6. Moved preprocessor variables to Configuration.h file.
 7. Removed M1 microvalve commands - To be reworked tomorrow.
 8. Modified the microvalves_init() function to use a for loop
 9. Added function and switch case to allow for simple opening and closing of microvalves (M3 code
 
 //====================== Notes on bugs ==========//
 1. If you send a command with extra information at the end, it does not affect the action.
 
 */


// =========== Private Variables ========= //
int serial_count = 0; // Int  for keep track of number of ASCII bytes received
int cmdlen = 0;
char serial_char; // Char to store incoming byte
char cmdbuffer[MAX_CMD_SIZE]; // Char array to store one command to be processed
char *strchr_pointer;
boolean isInternalMode = false;
// ========== Sub-routines ==========//

void display_welcome(){ // Simple routine to greet user upon start-up
  Serial.println("Welcome to the Harvard Yoo Printer. Type 'HELP' for command descriptions.");
}

void display_help(){ // Simple routine to print helpful descriptions about commands
  Serial.println("M90 - Set to external mode");
  Serial.println("M91 - Set to internal mode");
  Serial.println("M0 Rx Ly - Set pressure regulator");
  Serial.println("M1 Vx Ty - Set microvalve external mode opening time in microseconds");
  Serial.println("M2 Vx (P or T)y Cz N# - Set and/or run microvalve in internal mode");
  Serial.println();
}

void display_error(){ // Routine to print an error message
  Serial.print("Error: ");
  Serial.println("Unrecognized command");
}

void set_internal_mode( boolean state){ // Routine to handle seeting the toggling of internal/external mode
  isInternalMode = state;
  if (state) Serial.println("Set to internal mode");
  else Serial.println("Set to external mode");
  Serial.println();
}

boolean code_seen(char code) {
  strchr_pointer = strchr(cmdbuffer, code);
  return (strchr_pointer != NULL);  //Return True if a character was found
}

float code_value() {
  return (strtod(&cmdbuffer[strchr_pointer - cmdbuffer + 1], NULL));
}

long code_value_long() {
  return (strtol(&cmdbuffer[strchr_pointer - cmdbuffer + 1], NULL, 10));
}

void get_commands(){ // Will get any commands in serial and prepare them to be processed

  while (Serial.available() > 0) { // Serial while loop

    serial_char = Serial.read();

    if (serial_char == '\n' || serial_char == '\r' || serial_count >= (MAX_CMD_SIZE - 1)){
      if(!serial_count) return; // return without doing something if empty command
      cmdbuffer[serial_count] = 0; // terminate the string - necessary to prevent carry-ovcer error between commands
#ifdef DEBUG_MODE
      Serial.print("Received command: ");
      Serial.println(cmdbuffer);
#endif // DEBUG_MODE
      // These "commands" will not add to the cmd buffer. They are handled as soon as they are recognized
      if (strcmp(cmdbuffer,"HELP") == 0) display_help();
      else if (strcmp(cmdbuffer,"M90") == 0) set_internal_mode(false);
      else if (strcmp(cmdbuffer,"M91") == 0) set_internal_mode(true);
      // If none of the above "commands" are recognized, then there is a command stored in cmdbuffer that must be process
      // Set flag so that process_commands() will take care of it
      else cmdlen++; // Set flag - a.k.a cmdlen -  to one have process_commands() process the command
      // Reset the serial count - Errors will occur with the reading frame of a command if serial count is not reset
      serial_count = 0;
    }
    // Read the char from serial into the cmd buffer keeping tally of how many have been received
    else cmdbuffer[serial_count++] = serial_char;

  } // End of serial while loop
}

void process_commands(){ // Routine to interpret and execute commmands
  unsigned int valve;
  unsigned int address;
  unsigned int level;
  unsigned long opening_time;
  unsigned long closing_time;
  unsigned int num_of_cycles;
  boolean isMicros;

  if (code_seen('M')){ // Handle M-codes
    Serial.println("M code seen.");
    switch((int)code_value()){

    case 0: // Case 0: Setting pressure regulators
      if (code_seen('R')){ // Look to see which pressure regulator is being called
        address = code_value();
        if (address > 4 || address < 1) { // Check to make sure the pressure regulator being called exists
          display_error();
          return; // Should exit process_command since there is missing or incorrect information
        }
        else if (code_seen('L')){ // Check to see the level to be set for the pressure regulator
          level = code_value();
          if (level > 255 || level < 0) { // Check to make sure the desired level does not exceed bounds
            display_error();
            return; // Should exit process_command since there is missing or incorrect information
          }
          else{ // If it makes it to this point run the function
            Serial.print("Pressure regulator: ");
            Serial.print(address);
            Serial.print(" Level: ");
            Serial.println(level);
            set_pressure(address-1, level);
          }
        }
        else{
          display_error();
          return;
        }
      }
      else{
        display_error();
        return; // Should exit process_commmand() since there is incorrect or missing information
      }

      break; // End of case 0

    case 1: // Case 1: Set microvalves in external mode
      if(code_seen('V')){
        valve = code_value();
        // Check for potential user input errors
        if (valve > 4 || valve < 1){ // User has tried to call a microvalve that doesn't exist
          display_error();
          return; // Should exit process_command() since an invalid command was given
        }
        if (code_seen('P')){
          Serial.println("Error: Unable to set in milliseconds in external mode. Use 'T' for microseconds.");
          return;
        }
        if (code_seen('T')){
          opening_time = code_value_long();
          if(opening_time > MAX_OPENING_TIME_EXTERNAL_MODE_MICROS || opening_time < MIN_OPENING_TIME_EXTERNAL_MODE_MICROS){ // Check whether desired opening time exceeds bounds
            Serial.println("Error: Unable to set external mode opening time. Previous setting will be used if microvalve is run.");
            return;
          }
          else{
            Serial.println("Microvalve opening time set for external mode");
            microvalve_opening_time_external_mode[valve-1] = opening_time;
            Serial.print("Valve: "); 
            Serial.print(valve); 
            Serial.print(" Opening time (us): ");
            Serial.print(microvalve_opening_time_external_mode[valve-1]);
            Serial.print(" Closing time (ms): "); 
            Serial.print(microvalve_closing_time_external_mode[valve-1]);
          }
        }
        return;
      }
      else{ // User has not specified a valve - Cannot complete operation
        display_error();
        return;
      }

      break; // End of case 1





    case 2: // Case 2: Set or run microvalves in internal mode
      if(code_seen('V')){
        valve = code_value();

        // Check for potential user input errors
        if (valve > 4 || valve < 1){ // User has tried to call a microvalve that doesn't exist
          display_error();
          return; // Should exit process_command() since an invalid command was given
        }
        if (code_seen('P') && code_seen('T')){ // User trying to give more information than needed for opening time.
          display_error();
          return; // Should exit since conflicting information given
        }


        // Extract opening time information
        if (code_seen('P')){ // Millisecond opening time input
          opening_time = code_value_long();
          isMicros = false;
          if (opening_time > MAX_OPENING_TIME_INTERNAL_MODE_MILLIS || opening_time < MIN_OPENING_TIME_INTERNAL_MODE_MILLIS){ // Check whether desired opening time exceeds bounds
            Serial.println("Error: Unable to set internal mode opening time. Previous setting will be used if microvalve is run.");
          }
          else{ // If opening time doesn't exceed bounds, set both time and associated boolean
            Serial.println("Microvalve opening time set for internal mode");
            microvalve_opening_time_internal_mode[valve-1] = opening_time;
            microvalve_useMicros[valve-1] = isMicros;
          }

        }
        else if (code_seen('T')){ // Microsecond opening time input
          opening_time = code_value_long();
          isMicros = true;
          if (opening_time > MAX_OPENING_TIME_INTERNAL_MODE_MICROS || opening_time < MIN_OPENING_TIME_INTERNAL_MODE_MICROS){ // Check whether desired opening time exceeds bounds
            Serial.println("Error: Unable to set internal mode opening time. Previous setting will be used if microvalve is run.");
          }
          else{ // If opening time doesn't exceed bounds, set both time and associated boolean
            Serial.println("Microvalve opening time set for internal mode");
            microvalve_opening_time_internal_mode[valve-1] = opening_time;
            microvalve_useMicros[valve-1] = isMicros;
          }
        }


        if (code_seen('C')){ // Millisecond closing time
          closing_time = code_value_long();
          if (closing_time > MAX_CLOSING_TIME_INTERNAL_MODE_MILLIS || closing_time < MIN_CLOSING_TIME_INTERNAL_MODE_MILLIS){
            Serial.println("Error: Unable to set internal mode closing time. Previous setting will be used if microvalve is run.");
          }
          else{
            Serial.println("Microvalve closing time set for internal mode");
            microvalve_closing_time_internal_mode[valve-1] = closing_time;
          }
        }

        if(code_seen('N')){ // Number of cycles to run
          if (isInternalMode){ // Check to make sure not in external mode
            num_of_cycles = code_value();
            Serial.print("Valve: "); 
            Serial.print(valve); 
            Serial.print(" Opening time ");
            if (microvalve_useMicros[valve-1]) Serial.print("(us): "); 
            else Serial.print("(ms): ");
            Serial.print(microvalve_opening_time_internal_mode[valve-1]);
            Serial.print(" Closing time (ms): "); 
            Serial.print(microvalve_closing_time_internal_mode[valve-1]);
            Serial.print(" Run cycles: ");
            Serial.println(num_of_cycles);

            run_microvalve((valve-1), microvalve_opening_time_internal_mode[valve-1], microvalve_closing_time_internal_mode[valve-1], num_of_cycles, microvalve_useMicros[valve-1]);
          }
          else{
            Serial.println("Error: Unable to manually run microvalves in external mode");
          }
        }
        return;
      }
      else{ // User has not specified a valve - Cannot complete operation
        display_error();
        return;
      }

      break; // End of case 2


    case 3: // Purge functionality of microvalves
      Serial.println("Case 3 seen");
      if(code_seen('V')){
        valve = code_value();
        // Check for potential user input errors
        if (valve > 4 || valve < 1){ // User has tried to call a microvalve that doesn't exist
          display_error();
          return; // Should exit process_command() since an invalid command was given
        }
        else if(code_seen('S')){ // Acquire the level for the digitial pin to be set (Should be either 0-OFF or 255-ON)
          level = code_value();
          if( level != 0 && level != 255){ // Make sure the level is the correct input (i.e either 0 or 255 - cannot take any other values and make logical sense)
            Serial.println("Not the correct inputs given");
            display_error();
            return; // Should return since the input was incorrect      
          }
          else{ // If it makes it this far ...
            if(isInternalMode){ // Check to make sure in internal mode
              Serial.print("Valve: ");
              Serial.println(valve);
              Serial.print("Level: ");
              Serial.println(level);
              if (level == 255){
                open_microvalve(valve-1);
              }
              else if(level == 0){
                close_microvalve(valve-1);
              }
              else{
                Serial.println("Error: Unrecognized level input. Aborting...");
                return;
              }
            }
            else{ // Error out since in internal mode
              Serial.println("Error: Cannot perform requested process since in external mode.");
              return;
            }      
          }
        }
        return;
      }
      else{ // The user has not specified a valve - cannot complete operation
        display_error(); 
        return;
      }

      break; // End of case 3





    default: // Default case: Unrecognized M-code
      display_error();
      break;
    }
  }
  else{ // Unrecognized code
    display_error();
  }
}

// =========== Setup & Loop ==========//
void setup(){
  // Instantiate Serial
  Serial.begin(BAUDRATE);
  //Print welcome
  display_welcome();
  // Setup microvalves
  microvalves_init();
  // Setup pressure regulators
  press_reg_init();
}

void loop(){
  // Get any commands from the serial port, reading the entiriety of the command into an array
  get_commands();

  // Process a command if there is one recognized in the cmdbuffer
  if (cmdlen){
    process_commands();
    cmdlen--;
    Serial.println();
  }

  if(isInternalMode == false){
    checkForTTL();
  }
}





































