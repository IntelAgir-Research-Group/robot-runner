import os

# Used to set Robot Runner Context
from ConfigValidator.Config.Models.RobotRunnerContext import RobotRunnerContext

initial_position = '0.73,1.13';

position_goals = [(1, '-2.50,1.5'), (2, '-2.50,-1.25'),
                    (3, '-0.35,-0.80'), (4, '1.50,-1.00'),
                    (5, '2.50,0.50'), (6, '0.6,0.50')]

configuration_prefix = 'local_costmap_config_'

rl4greenros_path = os.getenv('RL4GreenROS_PATH')

class RL4GreenROS:
    def next_configuration(self, context: RobotRunnerContext):
        variation = context.run_variation

        # Getting Configuration
        configuration_number = variation['configuration']
        print(f"Loading configuration '{configuration_number}'...")
        configuration_file = rl4greenros_path+'config/gen_configs/'+configuration_prefix+str(configuration_number)+'.yaml'

        # Load Configuration

    def next_position(self, context: RobotRunnerContext):
        variation = context.run_variation

        # Getting next position
        next_position = variation['position_goal']
        print(f"Setting next position to '{next_position}'...")

        # 2D initial position
        initial_position = next_position - 1
        print(f"Setting initial position to '{initial_position}'...")

        # Move to the next position (ROS Package)

    def next_obstacle(self, context: RobotRunnerContext):

        variation = context.run_variation

        # number obstacles
        number_obstacles = variation['number_obstacles']

        if number_obstacles > 0:
            print(f"Adding '{number_obstacles}' obstacles.")
        else:
            print("No obstacles!")

    def move_to_position(self, context: RobotRunnerContext):
        print("Moving")
        # Navigate from A to B given the state and configuration (via ROS Package)
