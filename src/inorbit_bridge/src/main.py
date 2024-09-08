#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String

# Callback function for when a message is received on the /inorbit/custom_command topic
def custom_command_callback(msg: String):
    # Republish the received message to the /cmd_vel topic
    lin_str, ang_str = msg.data.split(':')
    sx, sy, sz = lin_str.split(',')
    sa, sb, sc = ang_str.split(',')
    twist_msg = Twist()
    twist_msg.linear.x  = float(sx)
    twist_msg.linear.y  = float(sy)
    twist_msg.linear.z  = float(sz)
    twist_msg.angular.x = float(sa)
    twist_msg.angular.y = float(sb)
    twist_msg.angular.z = float(sc)
    pub_cmd_vel.publish(twist_msg)
    rospy.loginfo("Republishing to /cmd_vel: %s, %s", lin_str, ang_str)

def listener_and_republisher():
    # Initialize the ROS node
    rospy.init_node('custom_command_republisher', anonymous=True)

    # Create a subscriber for /inorbit/custom_command, subscribing to Twist messages
    rospy.Subscriber('/inorbit/custom_command', String, custom_command_callback)
    rospy.loginfo("Subscriber created.")

    # Create a publisher for /cmd_vel
    global pub_cmd_vel
    pub_cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.loginfo("Publisher created.")

    # Keep the node running
    rospy.spin()

if __name__ == '__main__':
    try:
        listener_and_republisher()
    except rospy.ROSInterruptException:
        pass
