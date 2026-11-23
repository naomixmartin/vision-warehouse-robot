import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class RobotController(Node):
    def __init__(self):
        super().__init__("robot_controller")

        self.publisher_ = self.create_publisher(Twist, "/model/warehouse_robot/cmd_vel", 10)

        self.start_time = self.get_clock().now()
        self.timer = self.create_timer(0.1, self.control_robot)

    def control_robot(self):
        elapsed = (self.get_clock().now() - self.start_time).nanoseconds / 1e9

        cmd = Twist()

        if elapsed < 3:
            cmd.linear.x = 0.3

        elif elapsed < 5:
            cmd.angular.z = 0.5

        else:
            self.timer.cancel()

        self.publisher_.publish(cmd)


def main(args=None):
    rclpy.init(args=args)

    node = RobotController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()