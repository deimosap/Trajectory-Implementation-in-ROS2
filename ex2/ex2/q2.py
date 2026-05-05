#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState



class RRBotTrajectoryController(Node):
    def __init__(self):
        super().__init__('joint_commander')
        
        ## publish position instructions
        self.publisher = self.create_publisher(
            Float64MultiArray,
            '/forward_position_controller/commands',
            10
        )
        ## get position results
        self.subscriber = self.create_subscription(
            JointState,
            '/joint_states',
            self.velocity_callback,
            10
        )
        ## publish velocity to results (RViz doesn't supply them)
        self.velocity_publisher = self.create_publisher(
            JointState,
            '/joint_velocity_states',
            10
        )

        self.dt = 0.1
        self.q1 = 0.0
        self.q2 = 0.0
        ## despite name, they just keep actual last position of each joint
        self.dq1 = 0.0
        self.dq2 = 0.0
        self.start_time = self.get_clock().now()

        self.timer = self.create_timer(self.dt, self.move_step)


    def move_step(self):

        t = (self.get_clock().now() - self.start_time).nanoseconds / 1e9
        
        ## need to use values that you are publishing
        ## if using actual values as criteria, it breaks
        if abs(abs(self.q1) - 0.87)<0.001 and abs(abs(self.q2) - 1.74)<0.001:
            ## give result
            msg = Float64MultiArray()
            msg.data = [self.q1,self.q2]
            self.publisher.publish(msg)
            self.get_logger().info(f"Trajectory complete.")
            self.timer.cancel()
            return

        ## new position equations
        self.q1 = (0.273066667 * t ** 2 + (-0.00776723) * t ** 3)* 0.017453296
        self.q2 = ((-0.5461333333) * t ** 2 + 0.0155344593 * t ** 3)* 0.017453296
        

        ## publish joint positions
        msg = Float64MultiArray()
        msg.data = [self.q1,self.q2]
        self.publisher.publish(msg)

    
    def velocity_callback(self, msg: JointState):
        omega1 = (msg.position[msg.name.index('joint1')] - self.dq1)/self.dt
        omega2 = (msg.position[msg.name.index('joint2')] - self.dq2)/self.dt
        msg.velocity = [omega1 , omega2]
        self.dq1 = msg.position[msg.name.index('joint1')]
        self.dq2 = msg.position[msg.name.index('joint2')]
        self.velocity_publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    controller = RRBotTrajectoryController()
    rclpy.spin(controller)
    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()