import shutil

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # teleop_twist_keyboard needs an interactive terminal (stdin). When launched from ros2 launch,
    # we open a terminal emulator so keystrokes work.
    terminal_prefix = []
    if shutil.which("xterm"):
        terminal_prefix = ["xterm", "-e"]
    elif shutil.which("x-terminal-emulator"):
        terminal_prefix = ["x-terminal-emulator", "-e"]
    elif shutil.which("gnome-terminal"):
        terminal_prefix = ["gnome-terminal", "--"]
    elif shutil.which("konsole"):
        terminal_prefix = ["konsole", "-e"]
    elif shutil.which("xfce4-terminal"):
        terminal_prefix = ["xfce4-terminal", "-e"]

    use_sim_time_arg = DeclareLaunchArgument(
        name="use_sim_time",
        default_value="true",
        description="Use simulated time",
    )

    keyboard_teleop = Node(
        package="teleop_twist_keyboard",
        executable="teleop_twist_keyboard",
        name="keyboard_teleop",
        output="screen",
        # teleop_twist_keyboard publishes /cmd_vel by default; send it directly to the diff-drive controller
        remappings=[("/cmd_vel", "/wheel_controller/cmd_vel_unstamped")],
        parameters=[{"use_sim_time": LaunchConfiguration("use_sim_time")}],
        prefix=terminal_prefix,
    )

    return LaunchDescription(
        [
            use_sim_time_arg,
            keyboard_teleop,
        ]
    )
