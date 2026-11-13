import rclpy
from rclpy.node import Node
import math

class ForwardKinematicsNode(Node):
    def __init__(self):
        super().__init__('forward_kinematics_node')
        self.get_logger().info("Forward Kinematics Calculator Started.")
        
        # Link lengths matching our URDF model
        self.L1 = 0.4         # Bicep length
        self.L2 = 0.3         # Forearm length
        self.Z_offset = 0.05  # Height of Joint 1 from the ground
        
    def calculate_fk(self, theta1, theta2):
        # Calculate Elbow Position (X, Z)
        elbow_x = self.L1 * math.sin(theta1)
        elbow_z = self.Z_offset + self.L1 * math.cos(theta1)
        
        # Calculate End-Effector Tip Position (X, Z)
        tip_x = elbow_x + self.L2 * math.sin(theta1 + theta2)
        tip_z = elbow_z + self.L2 * math.cos(theta1 + theta2)
        
        self.get_logger().info(f"Input Angles -> Joint 1: {math.degrees(theta1):.0f}°, Joint 2: {math.degrees(theta2):.0f}°")
        self.get_logger().info(f"Tip Position -> X: {tip_x:.3f}m, Z: {tip_z:.3f}m \n")
        return tip_x, tip_z

def main(args=None):
    rclpy.init(args=args)
    node = ForwardKinematicsNode()
    
    # Test 1: Arm pointing straight up
    node.calculate_fk(math.radians(0), math.radians(0))
    
    # Test 2: Bicep horizontal (90 deg), forearm straight out
    node.calculate_fk(math.radians(90), math.radians(0))
    
    # Test 3: Bicep horizontal (90 deg), forearm pointing straight down (-90 deg)
    node.calculate_fk(math.radians(90), math.radians(-90))
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
