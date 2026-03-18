#include <Arduino.h>  // Required for PlatformIO
#include <Wire.h>
#include <INA3221.h>

// Initialize the sensor with the default I2C address (0x40)
INA3221 ina3221(0x40);

void setup() {
  Serial.begin(115200);
  while (!Serial) { delay(10); }
  
  // Explicitly initialize the I2C bus: Wire.begin(SDA, SCL)
  Wire.begin(21, 22);
  
  // Check if the sensor is connected
  if (!ina3221.begin()) {
    Serial.println("Failed to find INA3221 chip. Check wiring!");
    while (1) { delay(10); } // Halt if not found
  }

  // Set averaging to smooth the data
  // 0 = 1 sample, 1 = 4 samples, 2 = 16 samples, 3 = 64 samples
  ina3221.setAverage(3); 
}

void loop() {
  // Read Channel 1 (Index 0)
  float busVoltage = ina3221.getBusVoltage(0);
  float current = ina3221.getCurrent(0); 
  
  // Calculate Power (Watts)
  float power = busVoltage * current;

  // Print as clean CSV for your Ubuntu laptop C++ script to read:
  // Voltage,Current,Power
  Serial.print(busVoltage,4);
  Serial.print(",");
  Serial.print(current,4);
  Serial.print(",");
  Serial.println(power,4);

// // Human-readable formatting
//   Serial.print("Voltage: "); 
//   Serial.print(busVoltage); 
//   Serial.print(" V  |  ");
  
//   Serial.print("Current: "); 
//   Serial.print(current, 4); 
//   Serial.print(" A  |  ");
  
//   Serial.print("Power: "); 
//   Serial.print(power, 4); 
//   Serial.println(" W");

  // 10Hz publish rate (100ms delay)
  delay(100); 
}