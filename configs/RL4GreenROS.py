import os

from EventManager.Models.RobotRunnerEvents import RobotRunnerEvents
from EventManager.EventSubscriptionController import EventSubscriptionController
from ConfigValidator.Config.Models.RunTableModel import RunTableModel
from ConfigValidator.Config.Models.FactorModel import FactorModel
from ConfigValidator.Config.Models.RobotRunnerContext import RobotRunnerContext
from ConfigValidator.Config.Models.OperationType import OperationType

# System Runners
from Plugins.Systems.Docker.DockerRunner import DockerRunner
from Plugins.Systems.RL4GreenROS.RL4GreenROS import RL4GreenROS

# Resource Profilers
#from Plugins.Profilers.DockerCPUProfiler import DockerCPUProfiler
#from Plugins.Profilers.DockerMemProfiler import DockerMemProfiler
#from Plugins.Profilers.DockerPowerProfiler import DockerPowerProfiler
#from Plugins.Profilers.Nav2PerformanceProfiler import Nav2PerformanceProfiler

from typing import Dict, List
from pathlib import Path

rl4greenros_path = os.getenv('RL4GreenROS_PATH')

class RobotRunnerConfig:
    name:                       str             = "rl4greenros_experiment"
    required_ros_version:       int             = 2
    required_ros_distro:        str             = any
    operation_type:             OperationType   = OperationType.AUTO
    time_between_runs_in_ms:    int             = 1000
    results_output_path:        Path             = Path("~/Documents/experiments")
    
    # =================================================USER SPECIFIC UNNECESSARY CONFIG===============================================

    docker_runner: DockerRunner
    rl4greenros: RL4GreenROS

    # Dynamic configurations can be one-time satisfied here before the program takes the config as-is
    # NOTE: Setting some variable based on some criteria
    def __init__(self):
        """Executes immediately after program start, on config load"""
        if not rl4greenros_path:
            print('Please, set the RL4GreenROS path: RL4GreenROS_PATH environment variable.')
            os._exit(0)
        else:
            self.docker_runner = DockerRunner()
            self.rl4greenros = RL4GreenROS()

            EventSubscriptionController.subscribe_to_multiple_events([ 
                (RobotRunnerEvents.BEFORE_EXPERIMENT,   self.before_experiment), 
                (RobotRunnerEvents.BEFORE_RUN,          self.before_run),
                (RobotRunnerEvents.START_RUN,           self.start_run),
                (RobotRunnerEvents.START_MEASUREMENT,   self.start_measurement),
                (RobotRunnerEvents.LAUNCH_MISSION,      self.launch_mission),
                (RobotRunnerEvents.STOP_MEASUREMENT,    self.stop_measurement),
                (RobotRunnerEvents.STOP_RUN,            self.stop_run),
                (RobotRunnerEvents.POPULATE_RUN_DATA,   self.populate_run_data),
                (RobotRunnerEvents.AFTER_EXPERIMENT,    self.after_experiment)
            ])
            
            print("Custom config loaded")

    def create_run_table(self) -> List[Dict]:
        """Create and return the run_table here. A run_table is a List (rows) of tuples (columns), 
        representing each run robot-runner must perform"""
        run_table = RunTableModel(
            factors = [
                FactorModel("round", range(0, 2)),
                FactorModel("configuration", range(1, 3)),
                FactorModel("position_goal", range(1, 3)),
                FactorModel("number_obstacles", range(0, 2))
            ]
            # ,
            # exclude_variations = [
            #     {"example_treatment1"},     # all runs having treatment example_treatment1 will be excluded
            #     {"example_treatment1", "example_treatment2"} # all runs having the combination <treatment1, treatment2> will be excluded
            # ] 
        )
        run_table.create_experiment_run_table()
        return run_table.get_experiment_run_table()

    def before_experiment(self) -> None:
        """Perform any activity required before starting the experiment here"""
        print("before_experiment() called: cleaning the experiment environment")
        self.docker_runner.clean_docker_environment()

    def before_run(self) -> None:
        """Perform any activity required before starting a run, no context is available 
        here as the run is not yet active (BEFORE RUN)"""
        print("before_run() called: setting up the Docker environment")
        self.docker_runner.start_container("gazebo")
        self.docker_runner.start_container("nav2")
        self.docker_runner.start_container("rviz")

        print("Setting robot initial position on Gazebo")
        # set robot initial_position on Gazebo
        

    def start_run(self, context: RobotRunnerContext) -> None:
        """Perform any activity required for starting the run here. 
        Activities before and after starting the run should also be performed here."""
        print("Config.start_run() called!")
        self.rl4greenros.next_configuration(context)
        self.rl4greenros.next_position(context)
        self.rl4greenros.next_obstacle(context)

    def start_measurement(self, context: RobotRunnerContext) -> None:
        """Perform any activity required for starting measurements."""
        print("Config.start_measurement called!")

        # start profilers / echo null to the files

    def launch_mission(self, context: RobotRunnerContext) -> None:
        """Perform any activity interacting with the robotic
        system in question (simulated or real-life) here."""

        print("Config.launch_mission() called!")
        self.rl4greenros.move_to_position(context)

    def stop_measurement(self, context: RobotRunnerContext) -> None:
        """Perform any activity here required for stopping measurements."""
        print("Config.stop_measurement called!")

        # kill profilers / drop files

    def stop_run(self, context: RobotRunnerContext) -> None:
        """Perform any activity required for stopping the run here.
        Activities before and after stopping the run should also be performed here."""
        
        print("Config.stop_run() called!")
        print("Stopping containers...")
        #self.docker_runner.remove_containers()
    
    def populate_run_data(self, context: RobotRunnerContext) -> tuple:
        """Return the run data as a row for the output manager represented as a tuple"""
        return None

    def after_experiment(self) -> None:
        """Perform any activity required after stopping the experiment here"""
        print("after_experiment() called: cleaning the experiment environment")
        self.docker_runner.clean_docker_environment()

    # ===============================================DO NOT ALTER BELOW THIS LINE=================================================
    # NOTE: Do not alter these values
    experiment_path:            Path             = None
