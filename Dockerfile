FROM osrf/ros:humble-desktop-full

SHELL ["/bin/bash", "-lc"]
ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=humble
ENV ROS_WS=/root/mechabot_ws

WORKDIR /root

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    python3-colcon-common-extensions \
    python3-rosdep \
  && rm -rf /var/lib/apt/lists/*

WORKDIR ${ROS_WS}
COPY . ${ROS_WS}

# rosdep (safe to rerun)
RUN rosdep init 2>/dev/null || true && rosdep update

# Install dependencies for this workspace
RUN source /opt/ros/${ROS_DISTRO}/setup.bash && \
    rosdep install --from-paths src --ignore-src -r -y

# Build
RUN source /opt/ros/${ROS_DISTRO}/setup.bash && \
    colcon build --symlink-install

# Auto-source
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> /root/.bashrc && \
    echo "source ${ROS_WS}/install/setup.bash" >> /root/.bashrc

CMD ["bash"]

