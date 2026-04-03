#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav2_simple_commander.robot_navigator import BasicNavigator
from nav2_simple_commander.robot_navigator import TaskResult
from geometry_msgs.msg import PoseStamped
import tf_transformations
    
class WaypointFollowerNode(Node): 
    def __init__(self):
        super().__init__("waypoint_follower_node") 
        self.nav = BasicNavigator()
        self.run_autonomous_navigation()

    def create_pose_stamped(self, position_x, position_y, rotation_z):
        q_x, q_y, q_z, q_w = tf_transformations.quaternion_from_euler(0.0, 0.0, rotation_z)
        goal_pose = PoseStamped()
        goal_pose.header.frame_id = 'map'
        goal_pose.header.stamp = self.nav.get_clock().now().to_msg()
        goal_pose.pose.position.x = position_x
        goal_pose.pose.position.y = position_y
        goal_pose.pose.position.z = 0.0
        goal_pose.pose.orientation.x = q_x
        goal_pose.pose.orientation.y = q_y
        goal_pose.pose.orientation.z = q_z
        goal_pose.pose.orientation.w = q_w
        return goal_pose
        
    def run_nav_task(self, goal_pose):
        self.nav.goToPose(goal_pose)
        while not self.nav.isTaskComplete():
            feedback = self.nav.getFeedback()
            if feedback is not None:
                print(feedback)
        result = self.nav.getResult()
        print(result)
        return result

    def run_autonomous_navigation(self):
        # Keep Nav2 initial pose aligned with simulation spawn pose.
        initial_pose = self.create_pose_stamped(0.0, 0.0, 0.0)
        self.nav.setInitialPose(initial_pose)

        # Wait for Nav2
        self.nav.waitUntilNav2Active()

        # Two autonomous goals in free-space around the start pose.
        goals = [
            self.create_pose_stamped(2.0, 0.0, 0.0),
            self.create_pose_stamped(0.0, 0.0, 0.0),
        ]
        for goal in goals:
            result = self.run_nav_task(goal)
            if result != TaskResult.SUCCEEDED:
                break
    
    
def main(args=None):
    rclpy.init(args=args)
    node = WaypointFollowerNode() 
    rclpy.spin_once(node)
    rclpy.shutdown()
    
    
if __name__ == "__main__":
    main()
