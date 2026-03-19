import rclpy
from rclpy.node import Node
from custom_msgs.msg import PowerConsumption
import serial
import math
import json
import re

from ament_index_python.packages import get_package_share_directory

class SerialPowerBridge(Node):
    def __init__(self):
        super().__init__('serial_power_bridge')

        # Per-channel publishers are created lazily using keys: (sensor_id, channel_id).
        self.named_channel_publishers = {}

        default_map_path = self._default_sensor_map_path()
        self.declare_parameter('sensor_map_path', default_map_path)
        configured_map_path = self.get_parameter('sensor_map_path').get_parameter_value().string_value
        self.sensor_map = self._load_sensor_map(configured_map_path)

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

    def _default_sensor_map_path(self):
        try:
            return f"{get_package_share_directory('power_monitor')}/config/sensor_map.json"
        except Exception:
            # Fallback when package share path is not available yet.
            return ''

    def _to_topic_token(self, text: str):
        return re.sub(r'[^a-zA-Z0-9_]', '_', text.strip().lower())

    def _load_sensor_map(self, sensor_map_path: str):
        # Map key: (sensor_id, channel_id) -> value with names and metadata.
        mapping = {}

        if not sensor_map_path:
            self.get_logger().warning('No sensor map configured. Publishing numeric topics only.')
            return mapping

        try:
            with open(sensor_map_path, 'r', encoding='utf-8') as f:
                raw = json.load(f)

            for sensor in raw.get('sensors', []):
                sensor_id = int(sensor['sensor_id'])
                sensor_name = sensor.get('name', f'sensor_{sensor_id}')
                sensor_type = sensor.get('type', 'unknown')

                for channel in sensor.get('channels', []):
                    channel_id = int(channel['channel_id'])
                    channel_name = channel.get('name', f'channel_{channel_id}')
                    mapping[(sensor_id, channel_id)] = {
                        'sensor_name': sensor_name,
                        'channel_name': channel_name,
                        'sensor_type': sensor_type,
                    }

            self.get_logger().info(
                f'Loaded sensor map with {len(mapping)} channel entries from {sensor_map_path}'
            )
        except FileNotFoundError:
            self.get_logger().warning(
                f'Sensor map file not found at {sensor_map_path}. Publishing numeric topics only.'
            )
        except Exception as e:
            self.get_logger().warning(
                f'Failed to load sensor map ({sensor_map_path}): {e}. Publishing numeric topics only.'
            )

        return mapping

    def _get_named_channel_publisher(self, sensor_id: int, channel_id: int):
        key = (sensor_id, channel_id)
        map_entry = self.sensor_map.get(key)
        if map_entry is None:
            return None

        if key not in self.named_channel_publishers:
            sensor_name = self._to_topic_token(map_entry['sensor_name'])
            channel_name = self._to_topic_token(map_entry['channel_name'])
            topic_name = f'/power/by_name/{sensor_name}/{channel_name}'
            self.named_channel_publishers[key] = self.create_publisher(PowerConsumption, topic_name, 10)
            self.get_logger().info(f'Created publisher: {topic_name}')

        return self.named_channel_publishers[key]

    def _safe_float(self, value: str):
        try:
            parsed = float(value)
            # Disconnected channels can report NaN/Inf depending on hardware state.
            if not math.isfinite(parsed):
                return 0.0
            return parsed
        except ValueError:
            return 0.0

    def _parse_and_publish_record(self, record: str):
        # Record format: sensor_id,channel_id,voltage,current,power
        fields = record.split(',')
        if len(fields) != 5:
            self.get_logger().warning(f'Malformed record skipped: {record}')
            return

        try:
            sensor_id = int(fields[0])
            channel_id = int(fields[1])
        except ValueError:
            self.get_logger().warning(f'Invalid sensor/channel ids skipped: {record}')
            return

        msg = PowerConsumption()
        msg.sensor_id = sensor_id
        msg.channel_id = channel_id
        msg.voltage = self._safe_float(fields[2])
        msg.current = self._safe_float(fields[3])
        msg.power = self._safe_float(fields[4])

        # Publish only to named topics from sensor_map.json.
        named_publisher = self._get_named_channel_publisher(sensor_id, channel_id)
        if named_publisher is not None:
            named_publisher.publish(msg)
        else:
            self.get_logger().warning(
                f'No sensor_map entry for sensor_id={sensor_id}, channel_id={channel_id}; record skipped.'
            )

    def read_serial_data(self):
        if self.serial_port is not None and self.serial_port.in_waiting > 0:
            try:
                # Read line, decode bytes to string, and strip whitespace/newlines
                line = self.serial_port.readline().decode('utf-8').strip()

                if not line:
                    return

                # Line format supports many channels:
                # sensor_id,channel_id,voltage,current,power;...
                records = [record for record in line.split(';') if record]
                if not records:
                    self.get_logger().warning(f'Malformed serial line received: {line}')
                    return

                for record in records:
                    self._parse_and_publish_record(record)
                    
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