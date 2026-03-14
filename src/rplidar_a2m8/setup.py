from setuptools import find_packages, setup

package_name = 'rplidar_a2m8'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/rplidar.launch.py']),
    ],
    install_requires=['setuptools', 'rplidar-roboticia'],
    zip_safe=True,
    maintainer='rocky',
    maintainer_email='rockyshao22@gmail.com',
    description='ROS 2 interface package for RPLidar A2M8',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'rplidar_interface_node = rplidar_a2m8.rplidar_interface_node:main',
        ],
    },
)
