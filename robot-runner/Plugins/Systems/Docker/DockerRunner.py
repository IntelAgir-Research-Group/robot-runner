
import docker
import os
import subprocess
import time

# Used to set Robot Runner Context
#from ConfigValidator.Config.Models.RobotRunnerContext import RobotRunnerContext

containers = ['gazebo', 'nav2', 'rviz']
volumes = ['compose_exp_orchestration','compose_maps','compose_nav2_data','compose_nav2_profiler','compose_packages']
rl4greenros_path = os.getenv('RL4GreenROS_PATH')

compose_file_path = None

class DockerRunner:
    def volume_exists(self, volume_name):
        try:
            subprocess.run(["docker", "volume", "inspect", volume_name], check=True, stdout=subprocess.PIPE)
            return True  # Volume exists
        except subprocess.CalledProcessError:
            return False  # Volume does not exist

    def container_exists(self, container_name):
        try:
            subprocess.run(["docker", "container", "inspect", container_name], check=True, stdout=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            return False

    def remove_containers(self):
        # Removing containers
        for container in containers:
            container_name = container+'_container'
            if self.container_exists(container_name):
                try:
                    subprocess.run(["docker", "rm", "-f", container_name], check=True)
                    print(f"Container '{container_name}' removed successfully.")
                except subprocess.CalledProcessError as e:
                    print(f"Error removing container '{container_name}': {e}")

    def remove_volumes(self):
        # Removing volumes
        for volume in volumes:
            if self.volume_exists(volume):
                try:
                    subprocess.run(["docker", "volume", "rm", volume], check=True)
                    print(f"Volume '{volume}' removed successfully.")
                except subprocess.CalledProcessError as e:
                    print(f"Error removing volume '{volume}': {e}")

    def clean_docker_environment(self):
        self.remove_containers()
        self.remove_volumes()

    def check_compose_file(self):
        global compose_file_path
        compose_file_path = rl4greenros_path+'/docker/compose/compose-ros-humble-navigation-allinone.yml'
        if not os.path.exists(compose_file_path):
            print("docker-compose.yml file not found.")
            return False
        else:
            return True
            
    #def start_gazebo_container(self, context: RobotRunnerContext):
    def start_container(self, container):
        if self.check_compose_file():
            try:
                subprocess.run(["docker-compose", "-f", compose_file_path, "up", "-d", container], check=True)
                print(f"Container for service '{container}' started successfully.")
                print('Wainting for the container to warm up... ')
                time.sleep(30)
                return True
            except subprocess.CalledProcessError as e:
                print(f"Error starting container for service '{container}': {e}")
                return False

#docker_runner = DockerRunner()
#docker_runner.clean_docker_environment()
#docker_runner.start_container("gazebo")
#docker_runner.start_container("nav2")
#docker_runner.start_container("rviz")

