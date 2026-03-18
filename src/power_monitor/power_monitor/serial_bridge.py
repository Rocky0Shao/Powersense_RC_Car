import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import serial
import time

class SerialPowerBridge(Node):
    def __init__(self):
        super().__init__('serial_power_bridge')
        
        # Publishers for Voltage, Current, and Power
        self.pub_voltage = self.create_publisher(Float32, '/power/bus_voltage', 10)
        self.pub_current = self.create_publisher(Float32, '/power/current', 10)
        self.pub_power = self.create_publisher(Float32, '/power/watts', 10)

        #custom-defined serial port
        self.serial_port_name = '/dev/esp32' 
        self.baud_rate = 115200

        try:
            self.serial_port = serial.Serial(self.serial_port_name, self.baud_rate, timeout=1.0)
            self.get_logger().info(f"Successfully connected to ESP32 on {self.serial_port_name}")
        except serial.SerialException as e:
            self.get_logger().error(f"Failed to connect to serial port: {e}")
            self.serial_port = None

        # Create a timer to check the serial port much faster than the 10Hz ESP32 loop 
        # so we don't miss data. (100Hz / 0.01s)
        self.timer = self.create_timer(0.01, self.read_serial_data)

    def read_serial_data(self):
        if self.serial_port is not None and self.serial_port.in_waiting > 0:
            try:
                # Read line, decode bytes to string, and strip whitespace/newlines
                line = self.serial_port.readline().decode('utf-8').strip()
                
                # Split the CSV string: "Voltage,Current,Power"
                data = line.split(',')
                
                if len(data) == 3:
                    voltage = float(data[0])
                    current = float(data[1])
                    power = float(data[2])

                    # Publish the data
                    self.pub_voltage.publish(Float32(data=voltage))
                    self.pub_current.publish(Float32(data=current))
                    self.pub_power.publish(Float32(data=power))
                    
                    self.get_logger().debug(f"Published - V:{voltage} I:{current} P:{power}")
                else:
                    self.get_logger().warning(f"Malformed serial data received: {line}")
                    
            except Exception as e:
                self.get_logger().error(f"Error parsing serial data: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = SerialPowerBridge()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node.serial_port is not None:
            node.serial_port.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()