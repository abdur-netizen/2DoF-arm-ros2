# 2-DoF Robotic Arm — ROS 2

A ROS 2 workspace containing a simulated 2-degree-of-freedom robotic arm with a two-finger gripper, forward kinematics (FK), inverse kinematics (IK), and Gazebo launch configuration.

## Package

- **Package:** `simple_arm_sim`
- **Robot description:** `arm_ws/src/simple_arm_sim/urdf/arm.urdf`
- **Launch file:** `arm_ws/src/simple_arm_sim/launch/sim.launch.py`
- **Controllers:** `arm_ws/src/simple_arm_sim/config/controllers.yaml`
- **FK node:** `simple_arm_sim/fk_node.py`
- **IK and gripper node:** `simple_arm_sim/ik_node.py`

## Build

From the repository root, source your ROS 2 installation and build the package:

```bash
source /opt/ros/humble/setup.bash
cd arm_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

## Run

Launch the Gazebo simulation:

```bash
ros2 launch simple_arm_sim sim.launch.py
```

Run the forward-kinematics examples in another terminal:

```bash
source /opt/ros/humble/setup.bash
source arm_ws/install/setup.bash
ros2 run simple_arm_sim fk_node
```

Run the interactive inverse-kinematics and gripper controller:

```bash
source /opt/ros/humble/setup.bash
source arm_ws/install/setup.bash
ros2 run simple_arm_sim ik_node
```

The IK node accepts target coordinates as `x, z` (metres), `o` to open the gripper, `c` to close it, and `q` to quit.

> Ensure the required ROS 2, Gazebo Classic, ros2_control, and controller packages are installed for your ROS distribution. The launch and simulation configuration in this repository targets the Gazebo Classic integration.
