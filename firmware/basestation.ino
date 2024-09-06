// System 4 Base Station
#include <SPI.h>
#include <mcp2515.h>

#define BASESTATION

#define TARGET = ARDUINO_NANO_ESP32
// Options: ARDUINO_NANO, ARDUINO_NANO_EVERY, ARDUINO_NANO_ESP32, ARDUINO_NANO_RP2040

#define LCC_ADDRESS = 0x050101018B00

void setup()
{

    Serial.begin(115200);

    mcp2515.reset();
    mcp2515.setBitrate(CAN_125KBPS);
    mcp2515.setNormalMode();

    Serial.println("------- CAN Read ----------");
    Serial.println("ID  DLC   DATA");
}

void loop()
{
    if (mcp2515.readMessage(&canMsg) == MCP2515::ERROR_OK) {
    Serial.print(canMsg.can_id, HEX); // print ID
    Serial.print(" "); 
    Serial.print(canMsg.can_dlc, HEX); // print DLC
    Serial.print(" ");
    
    for (int i = 0; i<canMsg.can_dlc; i++)  {  // print the data
      Serial.print(canMsg.data[i],HEX);
      Serial.print(" ");
    }

    Serial.println();      
  }
}