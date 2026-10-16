
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from pynput import keyboard
class zephturtle(Node):
    def __init__(self):
        super().__init__('zephturtle')

        self.zephturtlecoms=self.create_publisher(
                Twist, '/turtle1/cmd_vel',10
        )
        self.movement=set()
        self.listen=keyboard.Listener(
                on_press=self.press,
                on_release=self.leave,)
        self.listen.start()
        self.timer=self.create_timer(
                0.05, self.callback)
    def press(self,key):
        if key==keyboard.Key.up:
                self.movement.add("up")
        elif key==keyboard.Key.down:
                self.movement.add("down")
        elif key==keyboard.Key.left:
                self.movement.add("left")
        elif key==keyboard.Key.right:
                self.movement.add("right")
    def leave(self,key):
        if key==keyboard.Key.up:
                self.movement.discard("up")
        elif key==keyboard.Key.down:
                self.movement.discard("down")
        elif key==keyboard.Key.right:
                self.movement.discard("right")
        elif key==keyboard.Key.left:
                self.movement.discard("left")
    def callback(self):
        linear_x=0.0
        angular_z=0.0
        if "up" in self.movement:
                linear_x=1.0
        if "down" in self.movement:
                linear_x=-1.0
        if "right" in self.movement:
                angular_z=-2.0
        if "left" in self.movement:
                angular_z=2.0
        txt=Twist()
        txt.linear.x=linear_x
        txt.angular.z=angular_z
        self.zephturtlecoms.publish(txt)
def main(args=None):
        rclpy.init(args=args)
        node=zephturtle()
        try:
                rclpy.spin(node)
        except KeyboardInterrupt:
                pass
        finally:
            node.listen.stop()
            node.destroy_node()
            rclypy.shutdown()
