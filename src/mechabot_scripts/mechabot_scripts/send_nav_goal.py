import math
import random

import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
from rclpy.node import Node


class NavGoalClient(Node):
    def __init__(self) -> None:
        super().__init__("nav_goal_client")
        self._client = ActionClient(self, NavigateToPose, "navigate_to_pose")

    def send_goal(self, x: float, y: float, yaw: float = 0.0) -> None:
        goal_msg = NavigateToPose.Goal()
        ps = PoseStamped()
        ps.header.frame_id = "map"
        ps.header.stamp = self.get_clock().now().to_msg()
        ps.pose.position.x = float(x)
        ps.pose.position.y = float(y)
        ps.pose.position.z = 0.0

        qz = math.sin(yaw / 2.0)
        qw = math.cos(yaw / 2.0)
        ps.pose.orientation.z = qz
        ps.pose.orientation.w = qw
        goal_msg.pose = ps

        self._client.wait_for_server()
        self.get_logger().info(f"Sending goal: x={x}, y={y}, yaw={yaw}")
        send_goal_future = self._client.send_goal_async(goal_msg)
        rclpy.spin_until_future_complete(self, send_goal_future)
        goal_handle = send_goal_future.result()
        if not goal_handle or not goal_handle.accepted:
            self.get_logger().error("Goal rejected")
            return

        self.get_logger().info("Goal accepted, waiting for result...")
        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        result = result_future.result()
        self.get_logger().info(f"Result status: {result.status}")


def main() -> None:
    rclpy.init()
    node = NavGoalClient()
    try:
        x = random.uniform(0.5, 8.0)
        y = random.uniform(-1.0, 8.0)
        node.send_goal(x, y)
    finally:
        node.destroy_node()
        rclpy.shutdown()

