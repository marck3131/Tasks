import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class Talker_Node(Node):
    def __init__(self):
        super().__init__('talker_node')
        self.publisher = self.create_publisher(String, 'jde_task', 10)
        timer_period = 1
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello! ROS2 is fun'
       
        self.publisher.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)

    talker_node = Talker_Node()

    rclpy.spin(talker_node)

    talker_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

