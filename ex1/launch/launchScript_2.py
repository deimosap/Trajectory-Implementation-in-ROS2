from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Start bag recording
        ExecuteProcess(
            cmd=['ros2', 'bag', 'record', '-a', '-o', 'q1Bag'],
            output='screen'
        ),

        # Start your motion script as a ROS 2 node
        Node(
            package='ex1',
            executable='question_2',  # Must match the name you installed or defined in setup.py
            name='question_2',
            output='screen'
        )
    ])