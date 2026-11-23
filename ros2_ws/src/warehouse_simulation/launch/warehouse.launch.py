import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    warehouse_dir = os.path.expanduser("~/warehouse-reference/tb_worlds")
    world_path = os.path.join(warehouse_dir, "worlds", "warehouse_world.sdf")
    resource_path = os.pathsep.join([os.path.join(warehouse_dir, "models"), os.path.join(warehouse_dir, "worlds"), os.environ.get("GZ_SIM_RESOURCE_PATH", "")])

    ros_gz_dir = get_package_share_directory("ros_gz_sim")
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(ros_gz_dir, "launch", "gz_sim.launch.py")),
        launch_arguments={"gz_args": f"-v 4 --render-engine ogre2 {world_path}"}.items()
    )

    return LaunchDescription([SetEnvironmentVariable("GZ_SIM_RESOURCE_PATH", resource_path), gazebo])
