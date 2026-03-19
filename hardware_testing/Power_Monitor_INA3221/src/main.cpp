#include <Arduino.h>  // Required for PlatformIO
#include <Wire.h>
#include <INA3221.h>
#include <Adafruit_INA260.h>
#include <math.h>

// Initialize the sensor with the default I2C address (0x40)
INA3221 ina3221(0x40);
Adafruit_INA260 ina260;

// Use sensor IDs so the same serial format can scale to multiple INA3221 chips.
constexpr uint8_t INA3221_SENSOR_ID = 0;
constexpr uint8_t INA3221_CHANNEL_COUNT = 3;
constexpr uint8_t INA3221_SDA_PIN = 21;
constexpr uint8_t INA3221_SCL_PIN = 22;

constexpr uint8_t INA260_SENSOR_ID = 1;
constexpr uint8_t INA260_CHANNEL_ID = 1;
// Avoid strapping pins (e.g. GPIO12) for attached peripherals to keep upload/boot reliable.
constexpr uint8_t INA260_SDA_PIN = 25;
constexpr uint8_t INA260_SCL_PIN = 26;
constexpr uint8_t INA260_DEFAULT_I2C_ADDRESS = 0x44;  // A1-selected address

bool ina260_ready = false;
uint8_t ina260_i2c_address_in_use = INA260_DEFAULT_I2C_ADDRESS;
const char *ina260_bus_in_use = "Wire1";

float sanitizeReading(float value) {
  if (isnan(value) || isinf(value)) {
    return 0.0f;
  }
  return value;
}

bool i2cDevicePresent(TwoWire &bus, uint8_t address) {
  bus.beginTransmission(address);
  return bus.endTransmission() == 0;
}

bool initIna260AutoAddress() {
  // Use fixed A1-selected address and prefer dedicated secondary bus first.
  if (i2cDevicePresent(Wire1, INA260_DEFAULT_I2C_ADDRESS) &&
      ina260.begin(INA260_DEFAULT_I2C_ADDRESS, &Wire1)) {
    ina260_i2c_address_in_use = INA260_DEFAULT_I2C_ADDRESS;
    ina260_bus_in_use = "Wire1";
    return true;
  }

  if (i2cDevicePresent(Wire, INA260_DEFAULT_I2C_ADDRESS) &&
      ina260.begin(INA260_DEFAULT_I2C_ADDRESS, &Wire)) {
    ina260_i2c_address_in_use = INA260_DEFAULT_I2C_ADDRESS;
    ina260_bus_in_use = "Wire";
    return true;
  }

  return false;
}

void setup() {
  Serial.begin(115200);
  while (!Serial) { delay(10); }
  
  // INA3221 is wired on dedicated ESP32 I2C pins.
  Wire.begin(INA3221_SDA_PIN, INA3221_SCL_PIN);

  // INA260 can run on a separate I2C bus using custom pins.
  // NOTE: If SDA and SCL are the same pin, reads will likely fail.
  Wire1.begin(INA260_SDA_PIN, INA260_SCL_PIN);

  
  // Check if INA3221 is connected.
  if (!ina3221.begin()) {
    Serial.println("Failed to find INA3221 chip. Check wiring!");
    while (1) { delay(10); } // Halt if not found
  } else{
    Serial.println("INA3221 Connected");
  }

  // INA260 is optional: keep firmware running even if missing.
  if (initIna260AutoAddress()) {
    ina260_ready = true;
    Serial.print("INA260 detected on ");
    Serial.print(ina260_bus_in_use);
    Serial.print(" at I2C address 0x");
    Serial.println(ina260_i2c_address_in_use, HEX);
  } else {
    Serial.println("WARN: INA260 not detected on Wire1/Wire at 0x41 (A1). Continuing with INA3221 only.");
  }

  // Set averaging to smooth the data
  // 0 = 1 sample, 1 = 4 samples, 2 = 16 samples, 3 = 64 samples
  ina3221.setAverage(3); 
}

void loop() {
  // Emit one line containing one record per channel:
  // sensor_id,channel_id,voltage,current,power;sensor_id,channel_id,voltage,current,power;...
  bool first_record = true;

  for (uint8_t channel_idx = 0; channel_idx < INA3221_CHANNEL_COUNT; ++channel_idx) {
    float busVoltage = sanitizeReading(ina3221.getBusVoltage(channel_idx));
    float current = sanitizeReading(ina3221.getCurrent(channel_idx));
    float power = busVoltage * current;

    if (!first_record) {
      Serial.print(";");
    }
    first_record = false;

    Serial.print(INA3221_SENSOR_ID);
    Serial.print(",");
    Serial.print(channel_idx + 1);
    Serial.print(",");
    Serial.print(busVoltage, 4);
    Serial.print(",");
    Serial.print(current, 4);
    Serial.print(",");
    Serial.print(power, 4);
  }

  if (ina260_ready) {
    // Adafruit INA260 API returns mV/mA/mW. Convert to SI units for ROS.
    float busVoltage = sanitizeReading(ina260.readBusVoltage() / 1000.0f);
    float current = sanitizeReading(ina260.readCurrent() / 1000.0f);
    float power = sanitizeReading(ina260.readPower() / 1000.0f);

    if (!first_record) {
      Serial.print(";");
    }

    Serial.print(INA260_SENSOR_ID);
    Serial.print(",");
    Serial.print(INA260_CHANNEL_ID);
    Serial.print(",");
    Serial.print(busVoltage, 4);
    Serial.print(",");
    Serial.print(current, 4);
    Serial.print(",");
    Serial.print(power, 4);
  }
  Serial.println();

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