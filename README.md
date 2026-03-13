# Powersense_RC_Car: Energy-Efficient Autonomous Navigation Benchmarking

With generous help from Dr. Marco Brocanelli and his lab, I am building a research-oriented framework designed to profile the energy-to-performance trade-offs of autonomous platforms. By integrating high-fidelity sensors (Intel RealSense & RPLidar) with variable computational and network constraints, this project aims to identify the sweet spot for power efficiency in edge robotics.

## 🚀 Project Overview
Modern autonomous systems often struggle with the "Power vs. Perception" paradox. Increasing sensor resolution and CPU frequency improves navigation accuracy but drastically reduces battery life. Conversely, offloading compute-intensive activities to edge servers reduces the computing power cost on the robot, but at the cost of increased network latency.

My goal is to provide a systematic method to measure how different configurations affect a robot's ability to navigate safely while improving energy efficiency for edge-computation.

**Key Variables Tested:**
* **Compute:** CPU frequency scaling (Throttling vs. Performance modes).
* **Network:** Onboard processing vs. Edge-offloading (WiFi/5G latency impact).
* **Sensing:** Lidar point-cloud density and RealSense depth resolution.
* **Optimization:** Quantized vs. Full-precision neural networks for path planning.
* **Model Scaling:** Larger vs. smaller object detection models (e.g., YOLOv8-full vs. YOLOv8-n).

## 🛠 Hardware Stack
| Component | Model | Role |
| :--- | :--- | :--- |
| **Chassis** | RC Chassis | Mobile platform |
| **Vision** | Intel RealSense D455 | Stereo depth & VSLAM |
| **Lidar** | RPLidar A2 | 2D/3D Obstacle detection |
| **Compute** | Jetson Nano | Onboard inference |
| **Power Mon.** | *To be determined* | Real-time power/current sensing |

## 📊 Benchmarking Methodology
We evaluate configurations using the Energy-per-Meter (EpM) metric:

$$EpM = \frac{\int_{0}^{t} P(t) dt}{d}$$

Where $P$ is power in Watts, $t$ is time, and $d$ is total distance traveled.

**Test Matrix:**
* **Baseline:** All sensors active, max CPU clock, local inference.
* **Eco-Mode:** Reduced Lidar frequency, CPU undervolting.
* **Cloud-Hybrid:** Offloading SLAM processing to a local edge server.

## 📂 Repository Structure
```text
├── notes/                   # Research notes and datasheets
└── src/
    └── camera_realsense/    # ROS 2 package for RealSense integration
```

## 📈 Getting Started
*(Instructions for building and running the ROS 2 workspace will be added as the project develops.)*
