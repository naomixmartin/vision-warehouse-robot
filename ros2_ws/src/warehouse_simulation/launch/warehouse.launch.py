
import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, RegisterEventHandler, SetEnvironmentVariable, LogInfo
from launch.event_handlers import OnProcessExit


def generate_launch_description():
    warehouse_dir = os.path.expanduser("~/warehouse-reference/tb_worlds")
    world_path = os.path.join(warehouse_dir, "worlds", "warehouse_world.sdf")
    robot_path = "/opt/ros/jazzy/share/ros_gz_sim_demos/models/vehicle/model.sdf"

    resource_path = os.pathsep.join([
        os.path.join(warehouse_dir, "models"),
        os.path.join(warehouse_dir, "worlds"),
        os.environ.get("GZ_SIM_RESOURCE_PATH", "")
    ])

    server = ExecuteProcess(
        cmd=["gz", "sim", "-s", "-r", "-v", "4", world_path],
        output="screen"
    )

    spawn_script = (
        "for i in $(seq 1 120); do "
        "if gz service -l | grep -Fxq /world/default/create; then "
        "exec ros2 run ros_gz_sim create "
        f"-world default -file {robot_path} "
        "-name warehouse_robot -x 0 -y 0 -z 0.5; "
        "fi; "
        "sleep 0.5; "
        "done; "
        "echo 'Gazebo create service unavailable' >&2; exit 1"
    )

    robot = ExecuteProcess(
        cmd=["bash", "-c", spawn_script],
        output="screen"
    )

    gui = ExecuteProcess(
        cmd=["gz", "sim", "-g", "--render-engine", "ogre2"],
        output="screen"
    )

    start_gui = RegisterEventHandler(
        OnProcessExit(
            target_action=robot,
            on_exit=lambda event, context: (
                [gui] if event.returncode == 0
                else [LogInfo(msg="Robot spawn failed; GUI not started.")]
            )
        )
    )

    return LaunchDescription([
        SetEnvironmentVariable("GZ_SIM_RESOURCE_PATH", resource_path),
        server,
        robot,
        start_gui
    ])
