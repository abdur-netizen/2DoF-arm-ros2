import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import math
import time

class InverseKinematicsNode(Node):
    def __init__(self):
        super().__init__('inverse_kinematics_node')
        
        # Publisher for the Arm
        self.arm_publisher_ = self.create_publisher(
            JointTrajectory, 
            '/arm_controller/joint_trajectory', 
            10
        )
        
        # Publisher for the Gripper
        self.gripper_publisher_ = self.create_publisher(
            JointTrajectory, 
            '/gripper_controller/joint_trajectory', 
            10
        )
        
        self.L1 = 0.4
        self.L2 = 0.3
        self.Z_offset = 0.05
        
    def calculate_ik(self, target_x, target_z):
        z = target_z - self.Z_offset
        x = target_x
        
        distance = math.sqrt(x**2 + z**2)
        if distance > (self.L1 + self.L2) or distance < abs(self.L1 - self.L2):
            self.get_logger().error(f"Target X:{target_x} Z:{target_z} is UNREACHABLE!")
            return None, None
            
        D = (x**2 + z**2 - self.L1**2 - self.L2**2) / (2 * self.L1 * self.L2)
        theta2 = math.atan2(-math.sqrt(1 - D**2), D)
        theta1 = math.atan2(x, z) - math.atan2(self.L2 * math.sin(theta2), self.L1 + self.L2 * math.cos(theta2))
        
        return theta1, theta2

    def move_to_target(self, target_x, target_z, duration_sec=3):
        theta1, theta2 = self.calculate_ik(target_x, target_z)
        
        if theta1 is None or theta2 is None:
            return 
            
        self.get_logger().info(f"Moving Arm to X={target_x}, Z={target_z}")

        msg = JointTrajectory()
        msg.joint_names = ['joint_1', 'joint_2']
        
        point = JointTrajectoryPoint()
        point.positions = [theta1, theta2]
        point.time_from_start.sec = duration_sec
        point.time_from_start.nanosec = 0
        
        msg.points.append(point)
        self.arm_publisher_.publish(msg)

    def set_gripper(self, state="open"):
        msg = JointTrajectory()
        msg.joint_names = ['left_prong_joint', 'right_prong_joint']
        
        point = JointTrajectoryPoint()
        
        if state == "open":
            self.get_logger().info("Opening Gripper...")
            # 0.0 is the home/open position for both joints
            point.positions = [0.0, 0.0] 
        elif state == "close":
            self.get_logger().info("Closing Gripper...")
            # Left prong moves negative, Right prong moves positive to close inward
            point.positions = [-0.025, 0.025] 
            
        point.time_from_start.sec = 1 # Quick 1-second grab
        point.time_from_start.nanosec = 0
        
        msg.points.append(point)
        self.gripper_publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = InverseKinematicsNode()
    
    time.sleep(1.0) 
    
    print("\n========================================")
    print(" Arm & Gripper Controller Started!")
    print(" 1. Move Arm: Enter X, Z (e.g., 0.5, 0.4)")
    print(" 2. Gripper: Type 'o' to open, 'c' to close")
    print(" 3. Quit: Type 'q'")
    print("========================================\n")
    
    try:
        while rclpy.ok():
            user_input = input("Command > ")
            
            if user_input.lower() == 'q':
                break
            elif user_input.lower() == 'o':
                node.set_gripper("open")
            elif user_input.lower() == 'c':
                node.set_gripper("close")
            else:
                try:
                    x_str, z_str = user_input.split(',')
                    node.move_to_target(float(x_str.strip()), float(z_str.strip()), duration_sec=2)
                except ValueError:
                    print(" -> Error: Use 'o', 'c', or coordinates like '0.5, 0.4'")
            
            # Allow ROS 2 to process the publish event
            rclpy.spin_once(node, timeout_sec=0.1)
                
    except KeyboardInterrupt:
        print("\nNode interrupted.")
        
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
