#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


## publish two Twist messages

## one for first movement, a rotation around its own z axis, 12 deg/s

## another for second, a rotation around its own z axis, -8 deg/s
## and linear movement along its x axis, 0.15 m/s 

class SimpleMotion(Node):
	def __init__(self):
		super().__init__('simple_motion')
		
		## storing up to 10 samples with QoS settings
		## not crucial, probably
		## also add subscriber to odometry for finding out position
		self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
		self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

		timer_period = 0.1
		## get start time of node's existance
		self.start_time = self.get_clock().now()
		## create position object
		self.position = None
		self.timer = self.create_timer(timer_period, self.simple_mov)

		self.get_logger().info('Movement has begun.')
	
	#duration for the first 15 seconds
	def simple_mov(self):
		msg = Twist()
		
		## find out time since Node started
		## turn into nanoseconds and then divide by 1e9 to get value in seconds
		time_elapsed = (self.get_clock().now() - self.start_time).nanoseconds / 1e9

		## depending on time, do something different
		if time_elapsed < 15:
			msg.angular.z = 0.2
		elif time_elapsed < 35:
			msg.angular.z = -0.14
			msg.linear.x = 0.15
		else:
			pass
		
		self.publisher.publish(msg)
		
		self.get_logger().info(f" Publishing: linear = {msg.linear}, angular = {msg.angular}, position = {self.position}")
	
	## second callback function for subscribing to Odometry
	def odom_callback(self, msg: Odometry):
		self.position = msg.pose.pose.position

def main(args=None):
    rclpy.init(args=args)
    node = SimpleMotion()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
