import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch.actions import TimerAction
from launch_ros.actions import Node


def generate_launch_description():
    warehouse_dir = os.path.expanduser("~/warehouse-reference/tb_worlds")
    world_path = os.path.join(warehouse_dir, "worlds", "warehouse_world.sdf")
    resource_path = os.pathsep.join([os.path.join(warehouse_dir, "models"), os.path.join(warehouse_dir, "worlds"), os.environ.get("GZ_SIM_RESOURCE_PATH", "")])

    ros_gz_dir = get_package_share_directory("ros_gz_sim")
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(ros_gz_dir, "launch", "gz_sim.launch.py")),
        launch_arguments={"gz_args": f"-v 4 --render-engine ogre2 {world_path}"}.items()
    )

    robot = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=["-world", "default", "-file", "/opt/ros/jazzy/share/ros_gz_sim_demos/models/vehicle/model.sdf",
                   "-name", "warehouse_robot", "-x", "0", "-y", "0", "-z", "0.5"],
        output="screen"
    )

    return LaunchDescription([SetEnvironmentVariable("GZ_SIM_RESOURCE_PATH", resource_path), gazebo, TimerAction(period=5.0, actions=[robot])])