import smbus2

# I2C configuration
I2C_BUS = 1       # I2C bus number, typically 1 on devices like the Raspberry Pi and Jetson Nano
I2C_ADDRESS = 0x12  # The I2C address of the slave device
I2C_REGISTER = 0x8  # Register address from which to start reading
NUMBER_OF_BYTES = 2  # Number of bytes to read

data_to_send = [NUMBER_OF_BYTES]
# Create an SMBus instance
bus = smbus2.SMBus(I2C_BUS)

try:
    # Read a block of data from the specified register
    data_received = bus.read_i2c_block_data(I2C_ADDRESS, I2C_REGISTER, NUMBER_OF_BYTES)

    # Convert the received data to a string of hex values for easy reading
    data_as_hex = ['{:02x}'.format(byte) for byte in data_received]
    print_string = ' '.join(data_as_hex)

    print("Data received from STM32:", print_string)

except Exception as e:
    print(f"Failed to read data from STM32: {e}")

finally:
    bus.close()

