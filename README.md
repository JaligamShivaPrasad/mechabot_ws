# MechaBot — Autonompus Mobile Robot Simulation in Warehouse Environment

Simulation-first Autonomous Mobile Robot (AMR) project for a small warehouse environment using:
- ROS 2 Humble
- Nav2 (planning + control + BT navigator)
- SLAM Toolbox (optional, for mapping)
- Gazebo (Ignition / `gz sim`) with `ros_gz_*` bridge

Note: this repo is simulation-focused (no embedded firmware build included).

<img width="856" height="812" alt="image" src="https://github.com/user-attachments/assets/4e045d34-9f05-4716-b17b-f126da3d3f47" />

## What this repo gives you
- One-command Gazebo + RViz bringup for a differential-drive AMR in a warehouse world
- Navigation stack (Nav2) with configurable localization (AMCL) or mapping (SLAM Toolbox)
- Teleop (keyboard / joystick) and `ros2_control` controller setup
- Robot description (URDF/Xacro) + Gazebo models/worlds


## Quickstart (native)
```bash
cd <this-repo>
source /opt/ros/humble/setup.bash
rosdep update
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
ros2 launch mechabot_bringup simulated_robot.launch.py
```

## Repository layout
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

## Run modes
### Navigation + localization (default)
```bash
ros2 launch mechabot_bringup simulated_robot.launch.py

```
<img width="1684" height="977" alt="Screenshot from 2026-04-03 12-32-25" src="https://github.com/user-attachments/assets/d6eb8efe-948f-4c72-9495-683014a42629" />


### Mapping (SLAM) mode
```bash
ros2 launch mechabot_bringup simulated_robot.launch.py \
  enable_slam:=true enable_navigation:=false \
  rviz_config:=$(ros2 pkg prefix --share mechabot_mapping)/rviz/slam.rviz
```
<img width="1737" height="969" alt="Screenshot from 2026-04-03 12-33-37" src="https://github.com/user-attachments/assets/3ab1c698-2760-4359-83b6-f5bcfb7972a8" />

Useful launch args:
- `world_name:=small_warehouse` or `world_name:=empty`
- `use_rviz:=false` (headless / no GUI)
- `enable_teleop:=false` (don’t start joystick + twist_mux)

## Save a map (from SLAM)
```bash
mkdir -p src/mechabot_mapping/maps/small_warehouse
ros2 run nav2_map_server map_saver_cli -f src/mechabot_mapping/maps/small_warehouse/map
```
<img width="1117" height="750" alt="image" src="https://github.com/user-attachments/assets/173ea31d-243e-46ba-824e-a038832da0c2" />

## TF tree
![TF tree](docs/tf_tree.png)

## Docs
- `src/mechabot_bringup/docs/mapping_and_rviz.md`
- `docs/tf_tree.pdf`
- `docs/tf_tree.png`
- `docs/architecture.svg`

## Notes
- This repo contains third-party 3D assets/models; verify their licenses before publishing or redistributing.
