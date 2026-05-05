#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState

class RRBotSimpleMovementController(Node):
    def __init__(self):
        super().__init__('joint_commander')

        self.publisher = self.create_publisher(
            Float64MultiArray,
            '/forward_position_controller/commands',
            10
        )
        self.subscriber = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )
        ## publish velocity to results (RViz doesn't supply them)
        self.velocity_publisher = self.create_publisher(
            JointState,
            '/joint_velocity_states',
            10
        )

        self.target = [-0.610865, 0.872665]
        self.current = [0.0, 0.0]
        self.step_size = 0.05 #Prolly gonna change it 

        self.timer = self.create_timer(0.1, self.move_step)

    def joint_state_callback(self, msg : JointState):
        omega1 = (msg.position[msg.name.index('joint1')] - self.current[0])/0.1
        omega2 = (msg.position[msg.name.index('joint2')] - self.current[1])/0.1
        msg.velocity = [omega1 , omega2]
        ## get current angles of joints
        self.current = [msg.position[msg.name.index('joint1')], msg.position[msg.name.index('joint2')]]
        self.velocity_publisher.publish(msg)
            
    def move_step(self):
        ## give result
        msg = Float64MultiArray()
        msg.data = self.target
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    controller = RRBotSimpleMovementController()
    rclpy.spin(controller)
    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()