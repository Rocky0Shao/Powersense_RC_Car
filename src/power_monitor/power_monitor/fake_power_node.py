import rclpy
from rclpy.node import Node
from custom_msgs.msg import PowerConsumption
import math
import csv
import os


class FakePowerPublisher(Node):
    def __init__(self):
        super().__init__('fake_power_publisher')

        # Parameters
        self.declare_parameter('save_csv', False)
        self.declare_parameter('csv_path', '~/power_data.csv')
        self.declare_parameter('publish_rate', 10.0)

        self.save_csv = self.get_parameter('save_csv').get_parameter_value().bool_value
        csv_path = self.get_parameter('csv_path').get_parameter_value().string_value
        self.csv_path = os.path.expanduser(csv_path)
        self.publish_rate = self.get_parameter('publish_rate').get_parameter_value().double_value

        # Publisher
        self.publisher = self.create_publisher(PowerConsumption, '/power/fake', 10)

        # Time tracking for sin(t) calculation
        self.t = 0.0
        self.dt = 1.0 / self.publish_rate

        # CSV file handling
        self.csv_file = None
        self.csv_writer = None
        if self.save_csv:
            self._init_csv()

        # Timer at configured rate
        self.timer = self.create_timer(self.dt, self.timer_callback)

        self.get_logger().info(
            f'FakePowerPublisher started at {self.publish_rate} Hz, '
            f'CSV saving: {self.save_csv}'
        )
        if self.save_csv:
            self.get_logger().info(f'CSV output: {self.csv_path}')

    def _init_csv(self):
        try:
            self.csv_file = open(self.csv_path, 'w', newline='')
            self.csv_writer = csv.writer(self.csv_file)
            self.csv_writer.writerow(['timestamp', 'voltage', 'current', 'power'])
            self.get_logger().info(f'CSV file created: {self.csv_path}')
        except IOError as e:
            self.get_logger().error(f'Failed to create CSV file: {e}')
            self.save_csv = False

    def timer_callback(self):
        # Generate fake power data: power = sin(t) + 1 (always positive, range 0-2)
        power = math.sin(self.t) + 1.0
        voltage = 12.0  # Nominal voltage
        current = power / voltage

        # Create and publish message
        msg = PowerConsumption()
        msg.sensor_id = 99  # Fake sensor marker
        msg.channel_id = 0
        msg.voltage = voltage
        msg.current = current
        msg.power = power

        self.publisher.publish(msg)

        # Save to CSV if enabled
        if self.save_csv and self.csv_writer:
            self.csv_writer.writerow([f'{self.t:.3f}', f'{voltage:.4f}', f'{current:.6f}', f'{power:.6f}'])
            self.csv_file.flush()

        # Increment time
        self.t += self.dt

    def destroy_node(self):
        if self.csv_file:
            self.csv_file.close()
            self.get_logger().info(f'CSV file closed: {self.csv_path}')
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = FakePowerPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
