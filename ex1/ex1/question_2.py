#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


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
		## get start time of node's existance
		self.start_time = self.get_clock().now()
		## create position object
		self.position = None
		self.timer = self.create_timer(timer_period, self.simple_mov)

		self.get_logger().info('Movement has begun.')
	
	def simple_mov(self):
		msg = Twist()
		
		## find out time since Node started
		## turn into nanoseconds and then divide by 1e9 to get value in seconds
		time_elapsed = (self.get_clock().now() - self.start_time).nanoseconds / 1e9

		## 1st trajectory
		if time_elapsed < 1.06277:
			msg.angular.z = (15.055 * time_elapsed) * 0.017453296
		elif time_elapsed < 1.660625:
			msg.angular.z = (16) * 0.017453296
		elif time_elapsed < 2.723395:
			msg.angular.z = (41.0007 - 15.055 * time_elapsed) * 0.017453296
		
		## 2nd trajectory
		elif time_elapsed < 27.568544157:
			msg.linear.x = 0.0057959 * (time_elapsed - 2.723395)
		elif time_elapsed < 41.543544157:
			msg.linear.x = 0.144
		elif time_elapsed < 66.388693314:
			msg.linear.x = 0.005796 * (63.665298314 - (time_elapsed - 2.723395))
		
		## 3rd trajectory
		elif time_elapsed < 67.451463314:
			msg.angular.z = (15.055 * (time_elapsed-66.388693314)) * 0.017453296
		elif time_elapsed < 70.671072974:
			msg.angular.z = (16) * 0.017453296
		elif time_elapsed < 71.733842974:
			msg.angular.z = (80.471228131 - 15.055 * (time_elapsed-66.388693314)) * 0.017453296

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
