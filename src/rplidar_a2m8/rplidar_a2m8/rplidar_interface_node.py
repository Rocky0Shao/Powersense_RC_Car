import math
import threading
import time

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

from rplidar import RPLidar


class RplidarInterfaceNode(Node):
    def __init__(self):
        super().__init__('rplidar_interface_node')

        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 115200)
        self.declare_parameter('frame_id', 'laser')
        self.declare_parameter('topic', '/scan')
        self.declare_parameter('scan_mode', 'normal')
        self.declare_parameter('inverted', False)
        self.declare_parameter('reversed', False)
        self.declare_parameter('range_min', 0.15)
        self.declare_parameter('range_max', 12.0)
        self.declare_parameter('min_scan_points', 5)
        self.declare_parameter('max_buf_meas', 500)

        self.port = self.get_parameter('port').value
        self.baudrate = int(self.get_parameter('baudrate').value)
        self.frame_id = self.get_parameter('frame_id').value
        self.topic = self.get_parameter('topic').value
        self.scan_mode = self.get_parameter('scan_mode').value
        self.inverted = bool(self.get_parameter('inverted').value)
        self.reversed = bool(self.get_parameter('reversed').value)
        self.range_min = float(self.get_parameter('range_min').value)
        self.range_max = float(self.get_parameter('range_max').value)
        self.min_scan_points = int(self.get_parameter('min_scan_points').value)
        self.max_buf_meas = int(self.get_parameter('max_buf_meas').value)

        if self.scan_mode != 'normal':
            self.get_logger().warn(
                "scan_mode='%s' requested, but current backend uses normal mode scans." % self.scan_mode
            )

        self.scan_pub = self.create_publisher(LaserScan, self.topic, 10)
        self.stop_event = threading.Event()
        self.scan_thread = None
        self.last_scan_time = None

        self.lidar = RPLidar(self.port, baudrate=self.baudrate)

        self._start_lidar()

    def _start_lidar(self):
        self.get_logger().info('Connecting to RPLidar on %s at %d baud...' % (self.port, self.baudrate))
        try:
            self.lidar.connect()
        except Exception:
            # Some versions connect in constructor and raise if called twice.
            pass

        try:
            info = self.lidar.get_info()
            self.get_logger().info('RPLidar info: %s' % str(info))
        except Exception as exc:
            self.get_logger().warn('Could not read lidar info: %s' % str(exc))

        try:
            self.lidar.start_motor()
        except Exception as exc:
            self.get_logger().warn('Could not start motor explicitly: %s' % str(exc))

        self.scan_thread = threading.Thread(target=self._scan_loop, daemon=True)
        self.scan_thread.start()

    def _scan_loop(self):
        self.get_logger().info('Started scan loop.')
        try:
            for scan in self.lidar.iter_scans(min_len=self.min_scan_points, max_buf_meas=self.max_buf_meas):
                if self.stop_event.is_set():
                    break
                self._publish_scan(scan)
        except Exception as exc:
            if not self.stop_event.is_set():
                self.get_logger().error('Lidar scan loop failed: %s' % str(exc))

    def _publish_scan(self, scan):
        bins = 360
        angle_increment = (2.0 * math.pi) / bins
        ranges = [math.inf] * bins
        intensities = [0.0] * bins

        for quality, angle_deg, distance_mm in scan:
            angle = float(angle_deg)

            if self.inverted:
                angle = (angle + 180.0) % 360.0

            if self.reversed:
                angle = (360.0 - angle) % 360.0

            idx = int(angle) % bins
            distance_m = float(distance_mm) / 1000.0

            if distance_m < self.range_min or distance_m > self.range_max:
                continue

            existing = ranges[idx]
            if math.isinf(existing) or distance_m < existing:
                ranges[idx] = distance_m
                intensities[idx] = float(quality)

        now_ros = self.get_clock().now().to_msg()
        now_sec = time.monotonic()

        if self.last_scan_time is None:
            scan_time = 0.0
        else:
            scan_time = max(0.0, now_sec - self.last_scan_time)

        self.last_scan_time = now_sec

        msg = LaserScan()
        msg.header.stamp = now_ros
        msg.header.frame_id = self.frame_id
        msg.angle_min = 0.0
        msg.angle_max = (2.0 * math.pi) - angle_increment
        msg.angle_increment = angle_increment
        msg.time_increment = scan_time / bins if scan_time > 0.0 else 0.0
        msg.scan_time = scan_time
        msg.range_min = self.range_min
        msg.range_max = self.range_max
        msg.ranges = ranges
        msg.intensities = intensities

        self.scan_pub.publish(msg)

    def _stop_lidar(self):
        self.stop_event.set()

        if self.scan_thread is not None and self.scan_thread.is_alive():
            self.scan_thread.join(timeout=2.0)

        try:
            self.lidar.stop()
        except Exception:
            pass

        try:
            self.lidar.stop_motor()
        except Exception:
            pass

        try:
            self.lidar.disconnect()
        except Exception:
            pass

    def destroy_node(self):
        self.get_logger().info('Stopping RPLidar interface node...')
        self._stop_lidar()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = RplidarInterfaceNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
