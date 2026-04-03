# MechaBot — Warehouse AMR Simulation (ROS 2 + Gazebo Fortress)

Simulation-first Autonomous Mobile Robot (AMR) project for a small warehouse environment using:
- ROS 2 Humble
- Nav2 (planning + control + BT navigator)
- SLAM Toolbox (optional, for mapping)
- Gazebo (Ignition / `gz sim`) with `ros_gz_*` bridge

Note: this repo is simulation-focused (no embedded firmware build included).

## Workspace layout
- `src/mechabot_description`: robot model (URDF/Xacro), Gazebo launch, warehouse world + models
- `src/mechabot_bringup`: one-command simulation bringup
- `src/mechabot_controller`: ros2_control controller spawners + teleop (joystick/keyboard)
- `src/mechabot_mapping`: SLAM + map saving configs
- `src/mechabot_localization`: AMCL + map_server
- `src/mechabot_navigation`: Nav2 servers + behavior tree
- `src/mechabot_scripts`: small helper scripts (optional)

## Prerequisites (native)
- Ubuntu + ROS 2 Humble installed and sourced
- Gazebo Fortress + `ros_gz_*` packages available for Humble

Tip: use a fresh terminal and only source `/opt/ros/humble/setup.bash` before building this workspace.

Install dependencies:
```bash
cd <this-repo>
source /opt/ros/humble/setup.bash
rosdep update
rosdep install --from-paths src --ignore-src -r -y
```

Build:
```bash
colcon build --symlink-install
source install/setup.bash
```

## Run (recommended)
Navigation + localization (default):
```bash
ros2 launch mechabot_bringup simulated_robot.launch.py
```

Mapping (SLAM) mode:
```bash
ros2 launch mechabot_bringup simulated_robot.launch.py \
  enable_slam:=true enable_navigation:=false \
  rviz_config:=$(ros2 pkg prefix --share mechabot_mapping)/rviz/slam.rviz
```

Useful launch args:
- `world_name:=small_warehouse` or `world_name:=empty`
- `use_rviz:=false` (headless / no GUI)
- `enable_teleop:=false` (don’t start joystick + twist_mux)

## Save a map (from SLAM)
```bash
mkdir -p src/mechabot_mapping/maps/small_warehouse
ros2 run nav2_map_server map_saver_cli -f src/mechabot_mapping/maps/small_warehouse/map
```

## Docs
- `src/mechabot_bringup/docs/mapping_and_rviz.md`
- `docs/tf_tree.pdf`

## Notes
- This repo contains third-party 3D assets/models; verify their licenses before publishing or redistributing.

## Docker (optional)
Build:
```bash
docker build -t mechabot-sim:humble .
```

Run (GUI on Linux/X11):
```bash
xhost +local:root
docker run --rm -it \
  --net=host \
  -e DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  --device /dev/dri \
  mechabot-sim:humble
```
