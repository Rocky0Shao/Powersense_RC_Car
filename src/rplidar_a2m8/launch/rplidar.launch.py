from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('port', default_value='/dev/ttyUSB0'),
        DeclareLaunchArgument('baudrate', default_value='115200'),
        DeclareLaunchArgument('frame_id', default_value='laser'),
        DeclareLaunchArgument('scan_mode', default_value='normal'),
        DeclareLaunchArgument('inverted', default_value='false'),
        DeclareLaunchArgument('reversed', default_value='false'),
        DeclareLaunchArgument('topic', default_value='/scan'),
        Node(
            package='rplidar_a2m8',
            executable='rplidar_interface_node',
            name='rplidar_interface_node',
            output='screen',
            parameters=[{
                'port': LaunchConfiguration('port'),
                'baudrate': LaunchConfiguration('baudrate'),
                'frame_id': LaunchConfiguration('frame_id'),
                'scan_mode': LaunchConfiguration('scan_mode'),
                'inverted': LaunchConfiguration('inverted'),
                'reversed': LaunchConfiguration('reversed'),
                'topic': LaunchConfiguration('topic'),
            }],
        ),
    ])
