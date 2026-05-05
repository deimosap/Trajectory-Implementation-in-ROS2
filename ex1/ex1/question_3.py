#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf_transformations import euler_from_quaternion

## separate imports
from math import sqrt, atan2, pi


class SimpleMotion(Node):
	def __init__(self):
		super().__init__('simple_motion')
		
		self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
		self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )
		timer_period = 0.1
		
		## create position object
		self.position = None
		## create orientation object
		self.orientation = None
		
		## keep track of a to keep out of bounds
		self.a = None

		## keep gain factors here
		self.Ka = 0.3
		self.Kb = -0.2
		self.Kp = 0.2

		## keep goal values here
		self.xGoal = 5
		self.yGoal = 2.5
		self.thetaGoal = 1.66

		self.timer = self.create_timer(timer_period, self.simple_mov)

		self.get_logger().info('Movement has begun.')
	
	def simple_mov(self):
		msg = Twist()
		
		if self.position == None or self.orientation == None:
			return

		## get current position and orientation for operations (curX, curY, curYaw)
		curX = self.position.x
		curY = self.position.y
		## get orientation as a list of quartenions
		quarts = [self.orientation.x, self.orientation.y, self.orientation.z, self.orientation.w]
		(roll, pitch, curYaw) = euler_from_quaternion(quarts)

		## variables needed for closed loop control (account for limits for a)
		p = sqrt( (self.xGoal-curX)**2 + (self.yGoal-curY)**2 )
		a = max(min(atan2(self.yGoal-curY, self.xGoal-curX) - curYaw, pi/2), -pi/2)
		b = -curYaw -a + self.thetaGoal

		## stop moving if close to the goal
		if p<0.01 and abs(b)<0.1:
			msg.linear.x = 0.0
			msg.angular.z = 0.0
			self.publisher.publish(msg)
			self.get_logger().info(f"Trajectory complete.")
			return


		## get velocities to publish, keep them below limit
		linear = self.Kp * p
		msg.linear.x = max(min(0.18, linear), 0)

		angular = self.Ka * a + self.Kb * b
		msg.angular.z = max(min(0.34906585, angular), -0.34906585)

		self.publisher.publish(msg)
		
		self.get_logger().info(f" Publishing: linear = {msg.linear}, angular = {msg.angular}, position = {self.position}")
	
	## second callback function for subscribing to Odometry
	def odom_callback(self, msg: Odometry):
		self.position = msg.pose.pose.position
		self.orientation = msg.pose.pose.orientation

def main(args=None):
    rclpy.init(args=args)
    node = SimpleMotion()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
