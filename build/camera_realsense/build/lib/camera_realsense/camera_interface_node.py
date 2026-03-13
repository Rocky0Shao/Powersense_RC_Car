#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import pyrealsense2 as rs
import numpy as np
from sensor_msgs.msg import Image, PointCloud2, PointField
from cv_bridge import CvBridge

class RealsenseInterfaceNode(Node):
    def __init__(self):
        super().__init__('camera_interface_node')
        
        # ROS 2 Publishers
        self.color_pub = self.create_publisher(Image, '/camera/color/image_raw', 10)
        self.pc_pub = self.create_publisher(PointCloud2, '/camera/depth/color/points', 10)
        
        self.bridge = CvBridge()
        
        # RealSense configuration
        self.pipeline = rs.pipeline()
        config = rs.config()
        # Enable Color stream
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        # Enable Depth stream
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        
        self.get_logger().info("Starting RealSense pipeline...")
        try:
            self.pipeline_profile = self.pipeline.start(config)
            self.get_logger().info("RealSense pipeline started successfully.")
        except Exception as e:
            self.get_logger().error(f"Failed to start pipeline: {e}")
            raise e

        # RealSense object to calculate pointcloud
        self.pc = rs.pointcloud()
        
        # Set up a timer to poll for frames at 30Hz
        timer_period = 1.0 / 30.0
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        try:
            # Wait for frames
            frames = self.pipeline.wait_for_frames()
            
            # Align depth to color to ensure pointcloud aligns with the RGB image
            align_to = rs.stream.color
            align = rs.align(align_to)
            aligned_frames = align.process(frames)
            
            color_frame = aligned_frames.get_color_frame()
            depth_frame = aligned_frames.get_depth_frame()
            
            if not color_frame or not depth_frame:
                return

            # Grab timestamp
            now = self.get_clock().now().to_msg()

            # 1. Publish Color Image
            color_image = np.asanyarray(color_frame.get_data())
            img_msg = self.bridge.cv2_to_imgmsg(color_image, encoding="bgr8")
            img_msg.header.stamp = now
            img_msg.header.frame_id = "camera_color_optical_frame"
            self.color_pub.publish(img_msg)
            
            # 2. Publish Aligned PointCloud2
            # Map the pointcloud onto the color image
            self.pc.map_to(color_frame)
            points = self.pc.calculate(depth_frame)
            
            # Convert to numpy arrays
            # The get_vertices() function returns an array of structured vertices
            vtx = np.asanyarray(points.get_vertices())
            verts = np.zeros((len(vtx), 3), dtype=np.float32)
            verts[:, 0] = vtx['f0']
            verts[:, 1] = vtx['f1']
            verts[:, 2] = vtx['f2']
            
            # Create the ROS2 PointCloud2 message
            pc_msg = self.create_pointcloud2_msg(verts, now, "camera_depth_optical_frame")
            self.pc_pub.publish(pc_msg)
            
        except Exception as e:
            self.get_logger().warn(f"Error processing frames: {e}")

    def create_pointcloud2_msg(self, points, stamp, frame_id):
        '''
        Helper function to turn an Nx3 Numpy Float32 Array into a sensor_msgs/PointCloud2 message
        '''
        msg = PointCloud2()
        msg.header.stamp = stamp
        msg.header.frame_id = frame_id
        
        msg.height = 1
        msg.width = points.shape[0]
        msg.fields = [
            PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
            PointField(name='y', offset=4, datatype=PointField.FLOAT32, count=1),
            PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1),
        ]
        msg.is_bigendian = False
        msg.point_step = 12 # 3 floats * 4 bytes
        msg.row_step = msg.point_step * msg.width
        msg.is_dense = False # Could contain invalid points (NaN/Inf)
        
        msg.data = points.tobytes()
        return msg

    def destroy_node(self):
        self.get_logger().info("Stopping RealSense pipeline...")
        self.pipeline.stop()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = RealsenseInterfaceNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
