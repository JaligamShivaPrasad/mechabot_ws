import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

# Path to SLAM configuration
slam_rviz_config_path = os.path.join(
    get_package_share_directory('mechabot_mapping'),
    'rviz',
    'slam.rviz'
)

# Path to Localization configuration
localization_rviz_config_path = os.path.join(
    get_package_share_directory('mechabot_localization'),
    'rviz',
    'global_localization.rviz'
)

def generate_launch_description():
    use_sim_time = LaunchConfiguration("use_sim_time")
    use_rviz = LaunchConfiguration("use_rviz")
    world_name = LaunchConfiguration("world_name")
    map_name = LaunchConfiguration("map_name")
    enable_slam = LaunchConfiguration("enable_slam")
    enable_navigation = LaunchConfiguration("enable_navigation")
    enable_teleop = LaunchConfiguration("enable_teleop")
    rviz_config = LaunchConfiguration("rviz_config")

    use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true",
        description="Use Gazebo simulation time.",
    )

    use_rviz_arg = DeclareLaunchArgument(
        "use_rviz",
        default_value="true",
        description="Launch RViz2 (set true on desktop environments with working OpenGL setup).",
    )

    world_name_arg = DeclareLaunchArgument(
        "world_name",
        default_value="small_warehouse",
        description="World name (without .world extension) from mechabot_description/worlds.",
    )

    map_name_arg = DeclareLaunchArgument(
        "map_name",
        default_value=LaunchConfiguration("world_name"),
        description="Map name (folder under mechabot_mapping/maps). Typically matches world_name.",
    )

    enable_slam_arg = DeclareLaunchArgument(
        "enable_slam",
        default_value="false",
        description="Enable SLAM Toolbox (disables AMCL localization).",
    )

    enable_navigation_arg = DeclareLaunchArgument(
        "enable_navigation",
        default_value="true",
        description="Start Nav2 navigation stack.",
    )

    enable_teleop_arg = DeclareLaunchArgument(
        "enable_teleop",
        default_value="true",
        description="Start joystick teleop + twist_mux.",
    )

    rviz_config_arg = DeclareLaunchArgument(
        "rviz_config",
        default_value=localization_rviz_config_path,
        description="RViz config file path.",
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("mechabot_description"),
                "launch",
                "gazebo.launch.py"
            )
        ),
        launch_arguments={
            "world_name": world_name
        }.items()
    )

    controller = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("mechabot_controller"),
                "launch",
                "controller.launch.py"
            )
        ),
    )
    
    joystick = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("mechabot_controller"),
                "launch",
                "joystick.launch.py"
            )
        ),
        condition=IfCondition(enable_teleop),
        launch_arguments={
            "use_sim_time": use_sim_time
        }.items()
    )

    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("mechabot_mapping"),
                "launch",
                "slam.launch.py"
            )
        ),
        condition=IfCondition(enable_slam),
        launch_arguments={
            "use_sim_time": use_sim_time
        }.items()
    )

    global_localization = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("mechabot_localization"),
                "launch",
                "global_localization.launch.py"
            )
        ),
        condition=UnlessCondition(enable_slam),
        launch_arguments={
            "use_sim_time": use_sim_time,
            "map_name": map_name,
        }.items(),
    )

    navigation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("mechabot_navigation"),
                "launch",
                "navigation.launch.py"
            ),
        ),
        condition=IfCondition(enable_navigation),
        launch_arguments={
            "use_sim_time": use_sim_time,
        }.items(),
    )

    rviz = Node(
        package='rviz2', 
        executable='rviz2', 
        name='rviz', 
        output='screen',
        condition=IfCondition(use_rviz),
        arguments=['-d', rviz_config]
    )

    return LaunchDescription([
        use_sim_time_arg,
        use_rviz_arg,
        world_name_arg,
        map_name_arg,
        enable_slam_arg,
        enable_navigation_arg,
        enable_teleop_arg,
        rviz_config_arg,
        gazebo,
        controller,
        joystick,
        slam,
        global_localization,
        rviz,
        navigation,
    ])
