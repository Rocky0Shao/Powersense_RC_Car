import smbus2
import time

# I2C configuration
I2C_BUS = 1       # I2C bus number (1 is usually the default on the Jetson Nano)
I2C_ADDRESS = 0x12  # The I2C address of the STM32 device (match this with your STM32 setup)
I2C_REGISTER = 0x00  # Register address to write to (if applicable, depending on your STM32 code)

# Data to send (example)
# data_to_send = [0, 0, 0]
data_to_send = [100, 0, 50, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0xe8, 0x01, 0x22, 0x01, 0x72, 0x01, 0xcc, 0x00, 0x00]

# Create an SMBus instance
bus = smbus2.SMBus(I2C_BUS)

try:
    while True:
        # Sending data as a single block to the STM32
        # This method includes the register address followed by the data to send
        bus.write_i2c_block_data(I2C_ADDRESS, I2C_REGISTER, data_to_send)

        print("Data sent to STM32 successfully.")
        
        time.sleep(0.1)  # Wait for 100ms before sending the next block
        
        
        data_received = bus.read_i2c_block_data(I2C_ADDRESS, 0x00, 20)

        # Convert the received data to a string of hex values for easy reading
        data_as_hex = ['{:02x}'.format(byte) for byte in data_received]
        print_string = ' '.join(data_as_hex)

        print("Data received from STM32:", print_string)

except KeyboardInterrupt:
    print("Transmission stopped by user.")

finally:
    bus.close()

