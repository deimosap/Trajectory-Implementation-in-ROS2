from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Start bag recording
        ExecuteProcess(
            cmd=['ros2', 'bag', 'record', '-a', '-o', 'q2Bag'],
            output='screen'
        ),

        # Start your motion script as a ROS 2 node
        Node(
            package='ex2',
            executable='question1',  # Must match the name you installed or defined in setup.py
            name='question1',
            output='screen'
        )
    ])