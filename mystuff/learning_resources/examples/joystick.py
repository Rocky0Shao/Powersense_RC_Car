import evdev
from evdev import InputDevice, categorize, ecodes
import numpy as np
import smbus2
import time
import threading

# I2C configuration
I2C_BUS = 1
I2C_ADDRESS = 0x12
I2C_REGISTER = 0x00

# Data to send (example)
data_to_send = [0, 0, 0, 3, 0, 0, 0, 0, 0, 0]

# Create an SMBus instance
bus = smbus2.SMBus(I2C_BUS)



def send_i2c_message():
    try:
        while True:
            # Sending data as a single block to the STM32
            # This method includes the register address followed by the data to send
            bus.write_i2c_block_data(I2C_ADDRESS, I2C_REGISTER, data_to_send)

            print("Data sent to STM32 successfully.")
            print(f"direct PWM: {data_to_send[7]} PWM: {data_to_send[8]} steer: {data_to_send[2]}")
            
            
            time.sleep(0.1)  # Wait for 100ms before sending the next block


    except KeyboardInterrupt:
        print("Transmission stopped by user.")

    finally:
        bus.close()

def main():
    device = InputDevice("/dev/input/event3")

    # Start the thread for sending I2C messages
    threading.Thread(target=send_i2c_message, daemon=True).start()

    try:
        for event in device.read_loop():
            if event.type == ecodes.EV_KEY:
                print(f"Key event: {event.code} {'pressed' if event.value else 'released'}")
                
            elif event.type == ecodes.EV_ABS:
                # print(f"Absolute axis event: {event.code}, value: {event.value}")
                if event.code == 2:
                    if event.value <= 128:
                        steer = 127 - event.value
                    else:
                        steer = 127+256 - event.value
  
                    data_to_send[2] = steer

                elif event.code == 1:
                    if event.value < 128:
                        pwm = 127 - event.value
                    else:
                        pwm = 127+256 - event.value
                    
                    
                    data_to_send[8] = pwm
                    data_to_send[7] = 1
                    

    except KeyboardInterrupt:
        print("Exiting...")
        
    finally:
         bus.close()

if __name__ == "__main__":
    main()


