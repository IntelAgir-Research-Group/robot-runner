
import os
import subprocess
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory

# Used to set Robot Runner Context
from ConfigValidator.Config.Models.RobotRunnerContext import RobotRunnerContext

def set_initial_position(): # later we can pass the initial position as an argument
    rosbag_folder = os.path.join(
        get_package_share_directory('rl4greenros'),
        'rosbag'
    )

    return LaunchDescription([
        ExecuteProcess(
            cmd=['ros2', 'bag', 'play', '--topics=\"/initialpose\"', rosbag_folder],
            output='screen',
            shell=True
        )
    ])

def move_to_position(context: RobotRunnerContext): # implement the move to position logic
    return