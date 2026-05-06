# Trajectory Implementation in ROS2

As part of a robotics university class that required specific trajectories to be designed and simulated, these simulation tests for Turtlebot 3 Burger and RRBot were completed using ROS2, and then compared to the trajectories initially designed.

Through careful examination of how these differ, one is able to better judge what parameters and, as a result, trajectories should be designed for a specific robot. Since, even when within the device's limits, as defined by the manufacturer, some trajectories might not always be possible in a real-life scenario.

The math that lead up to the design of the trajectories is omitted, possibly to be added later (TODO).

## Setup Guide

### For running scripts within these packages

- .bashrc had these added to it:

```
# ros related here
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash

export TURTLEBOT3_MODEL=burger

stat /usr/share/gazebo/setup.sh &> /dev/null
if [ $? -eq 0 ]; then
	source /usr/share/gazebo/setup.sh
fi
```

- After second package was created, compilation done with: `colcon build --merge-install`

- If running scripts from ex1, also call: `source ~/ros2_ws/install/local_setup.bash`

- If running scripts from ex2, call: `. /opt/ros/${ROS_DISTRO}/setup.bash`

### Commands for running scripts through launch scripts:

Normal commands work just fine too, but these also output a **bag** in ROS workspace (named q1Bag or q2Bag depending on it being part 1 or 2). Remember to delete bag folder before every execution.

**Exercise 1:**

- Question 1: `ros2 launch ex1 launchScript.py`

- Question 2: `ros2 launch ex1 launchScript_2.py`

- Question 3: `ros2 launch ex1 launchScript_3.py`

**Exercise 2:**

- Question 1: `ros2 launch ex2 launch.py`

- Question 2: `ros2 launch ex2 launch2.py`


## Exercise 1 (ex1 - Turtlebot)

### Question 1

Here, the only request was to publish Twist messages to allow for movement. Still, this is a chance to mention, that, while in a real-life environment, this would absolutely not work as intended (instantly high linear and/or rotational velocity is not feasible), the simulation allows this.

### Question 2

After designing three separate trajectories that, one by one:

1.  Describes the rotation of the robot, so that it is oriented towards its final position (in the X-Y plane)
2.  Describes the translation of the robot to its final position
3.  Describes the rotation of the robot towards a different orientation

They were implemented in a simulation environment, with the results being as such:

**Trajectory 1:**

Intended rotation | Actual rotation
:------------------------------:|:-----------------------------:
<img src="https://github.com/deimosap/Trajectory-Implementation-in-ROS2/blob/main/images/1_ex1_question2_rotation_traj_1.png" width="400"/> | <img src="https://github.com/deimosap/Trajectory-Implementation-in-ROS2/blob/main/images/3_ex1_question2_rotation_traj_1.png" width="400"/>

Intended angular velocity | Actual angular velocity
:------------------------------:|:-----------------------------:
<img src="https://github.com/deimosap/Trajectory-Implementation-in-ROS2/blob/main/images/2_ex1_question2_angular_traj_1.png" width="400"/> | <img src="https://github.com/deimosap/Trajectory-Implementation-in-ROS2/blob/main/images/4_ex1_question2_angular_traj_1.png" width="400"/>


While when comparing the robot's yaw (from ```/pose/position``` provided by topic ```/odom```) to rotation, they seem to align (maximum value is off 0.22 degrees), the angular velocity plot taken from the bag is evidently not as clean as expected, likely due to the fact that the robot is being given a different value for it after a set interval, which might cause irregularities (among them, a short correction in the end, not found in the original trajectory). Here that interval is 0.1 seconds, but even when shorter, similar plots appear.

**Trajectory 2:**

Intended translation in XY | Actual translation in XY
:------------------------------:|:-----------------------------:
<img src="https://github.com/deimosap/Trajectory-Implementation-in-ROS2/blob/main/images/5_ex1_question2_position_traj_2.png" width="400"/> | <img src="https://github.com/deimosap/Trajectory-Implementation-in-ROS2/blob/main/images/8_ex1_question2_position_traj_2.png" width="400"/>

Intended linear velocity | Actual linear velocity
:------------------------------:|:-----------------------------:
<img src="https://github.com/deimosap/Trajectory-Implementation-in-ROS2/blob/main/images/7_ex1_question2_velocity_traj_2.png" width="400"/> | <img src="https://github.com/deimosap/Trajectory-Implementation-in-ROS2/blob/main/images/10_ex1_question2_velocity_traj_2.png" width="400"/>

These seem mostly accurate, other than a slight deviation in the final position (by a centimeter at most), possibly caused by unexpected behaviors, like the fact that during both the first and third trajectories, the robot did move slightly in the X-Y plane, while only being programmed to rotate. It is evident with a closer look on the linear velocity plot, and specifically, its section corresponding to the first trajectory:

![alt text](https://github.com/deimosap/Trajectory-Implementation-in-ROS2/blob/main/images/11_ex1_question2_velocity_traj_2_bonus.png "Unintentional linear velocity")

**Trajectory 3:**

Intended rotation | Actual rotation
:------------------------------:|:-----------------------------:
<img src="https://github.com/deimosap/Trajectory-Implementation-in-ROS2/blob/main/images/12_ex1_question2_rotation_traj_3.png" width="400"/> | <img src="https://github.com/deimosap/Trajectory-Implementation-in-ROS2/blob/main/images/14_ex1_question2_rotation_traj_3.png" width="400"/>

Intended angular velocity | Actual angular velocity
:------------------------------:|:-----------------------------:
<img src="https://github.com/deimosap/Trajectory-Implementation-in-ROS2/blob/main/images/13_ex1_question2_angular_traj_3.png" width="400"/> | <img src="https://github.com/deimosap/Trajectory-Implementation-in-ROS2/blob/main/images/15_ex1_question2_angular_traj_3.png" width="400"/>

Finally, similar observations to the first trajectory were made.

### Question 3

For this part of the exercise, an **automatic control** algorithm was implemented, to test a method that uses feedback, with the same starting and final position/orientation. The parameters were chosen conservatively, but without causing massive delays until stabilization. The resulting plots are given below, with the only peculiar detail being that because ```cmd_vel/angular/z``` doesn't start at 0, the value read from ```/odom/twist/twist/angular/z``` has to immediately spike from 0, which would likely cause issues in real-life testing. Something similar appears in the linear velocity plots.

Angular velocity | Linear velocity
:------------------------------:|:-----------------------------:
<img src="https://github.com/deimosap/Trajectory-Implementation-in-ROS2/blob/main/images/16_ex1_question3_angular.png" width="400"/> | <img src="https://github.com/deimosap/Trajectory-Implementation-in-ROS2/blob/main/images/17_ex1_question3_linear.png" width="400"/>

The other plots look normal.

Rotation | Position
:------------------------------:|:-----------------------------:
<img src="https://github.com/deimosap/Trajectory-Implementation-in-ROS2/blob/main/images/19_ex1_question3_rotation.png" width="400"/> | <img src="https://github.com/deimosap/Trajectory-Implementation-in-ROS2/blob/main/images/18_ex1_question3_position.png" width="400"/>

## Exercise 2

### Question 1

Not especially worth mentioning, just setting a final orientation for the joints. Would cause instability in a real-life scenario.

### Question 2

After designing a trajectory for each joint, so that each one of them ends up in a specific orientation, a comparison between the intended final result and simulated final result follows:

**Trajectory of bottom joint:**

Intended rotation | Actual rotation
:------------------------------:|:-----------------------------:
<img src="https://github.com/deimosap/Trajectory-Implementation-in-ROS2/blob/main/images/20_ex2_question2_rotation_1.png" width="400"/> | <img src="https://github.com/deimosap/Trajectory-Implementation-in-ROS2/blob/main/images/22_ex2_question2_rotation_1.png" width="400"/>

Intended angular velocity | Actual angular velocity
:------------------------------:|:-----------------------------:
<img src="https://github.com/deimosap/Trajectory-Implementation-in-ROS2/blob/main/images/21_ex2_question2_angular_1.png" width="400"/> | <img src="https://github.com/deimosap/Trajectory-Implementation-in-ROS2/blob/main/images/23_ex2_question2_angular_1.png" width="400"/>

**Trajectory of top joint:**

Intended rotation | Actual rotation
:------------------------------:|:-----------------------------:
<img src="https://github.com/deimosap/Trajectory-Implementation-in-ROS2/blob/main/images/24_ex2_question2_rotation_2.png" width="400"/> | <img src="https://github.com/deimosap/Trajectory-Implementation-in-ROS2/blob/main/images/26_ex2_question2_rotation_2.png" width="400"/>

Intended angular velocity | Actual angular velocity
:------------------------------:|:-----------------------------:
<img src="https://github.com/deimosap/Trajectory-Implementation-in-ROS2/blob/main/images/25_ex2_question2_angular_2.png" width="400"/> | <img src="https://github.com/deimosap/Trajectory-Implementation-in-ROS2/blob/main/images/27_ex2_question2_angular_2.png" width="400"/>

Both the rate at which each joint develops angular velocity and the maximum velocity don't seem to correspond with the intended results. Fixes weren't found using a different clock for the value of time in the calculations of the trajectory, or limiting the execution time to the intended value. It's possible that the cause for this behavior is the controller used for assigning commands to each joint, which could limit the angular velocity they are allowed to reach, hence, leading to an inaccurate representation of each trajectory.

However, it would still be more stable than the methodology of Question 1.

## Environment related and general notes

These tests were done on Ubuntu 22.04, using ROS2's Humble distribution.

For all Turtlebot tests, Gazebo was used to set up a simulation environment, while for all RRBot tests, RViz was used.

For the RRBot tests, RViz itself **doesn't** provide the joints' velocities using ```JointStates/velocities```, and as a result, for these to become available in the rosBag exported, they are calculated using the actual positions, received from a JointStates message, which is re-published once more as a different topic.

PlotJuggler was used for exporting graphs, using each rosBag from the tests.
