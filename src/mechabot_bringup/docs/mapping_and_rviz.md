# Small Warehouse Mapping + RViz

## Setup
1. `cd <this-repo>`
2. `source /opt/ros/humble/setup.bash`
3. `rosdep install --from-paths src --ignore-src -r -y`
4. `colcon build --symlink-install`
5. `source install/setup.bash`

## Mapping-only workflow (local GUI)
Single-command option:
- `ros2 launch mechabot_bringup simulated_robot.launch.py enable_slam:=true enable_navigation:=false rviz_config:=$(ros2 pkg prefix --share mechabot_mapping)/rviz/slam.rviz`

Or split terminals:
- T1: `ros2 launch mechabot_description gazebo.launch.py world_name:=small_warehouse`
- T2: `ros2 launch mechabot_controller controller.launch.py`
- T3: `ros2 launch mechabot_controller joystick.launch.py use_sim_time:=true`
- T4: `ros2 launch mechabot_mapping slam.launch.py use_sim_time:=true`
- T5: `rviz2 -d $(ros2 pkg prefix --share mechabot_mapping)/rviz/slam.rviz`

Drive the robot through the warehouse, covering walls, aisles, and loops to capture loop closures. Watch `/map` and `/scan` in RViz as you go.

## Saving the generated map
1. `mkdir -p src/mechabot_mapping/maps/small_warehouse`
2. `ros2 run nav2_map_server map_saver_cli -f src/mechabot_mapping/maps/small_warehouse/map`
3. Confirm `map.yaml` and `map.pgm` exist and `map.yaml` has `resolution`, `origin`, and `image:` pointing to `map.pgm`.

## Localization + navigation after mapping
- `ros2 launch mechabot_localization global_localization.launch.py map_name:=small_warehouse use_sim_time:=true`

## Bringup launch quick reference
`ros2 launch mechabot_bringup simulated_robot.launch.py`
- `use_rviz` defaults to `true` so RViz opens in GUI sessions.
- `enable_slam` defaults to `false` so AMCL localization runs by default; set `enable_slam:=true` for mapping.
- `enable_navigation` defaults to `true`; disable it for mapping-only teleop with `enable_navigation:=false`.
- To disable RViz, pass `use_rviz:=false` when launching.

## Verification checklist
- `ros2 topic list | rg "/scan|/map|/tf|/cmd_vel"`
- `ros2 topic echo /scan --once`
- After moving, `ros2 topic echo /map --once`
- In RViz (fixed frame = `map`): LaserScan is visible on `/scan` and Map updates on `/map`.
- Saved map files exist under `mechabot_mapping/maps/small_warehouse/` and the YAML references the image correctly.
