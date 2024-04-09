import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class ImageFlipper(Node):
    def __init__(self):
        super().__init__('image_flipper')
        self.subscription_leftcam = self.create_subscription(
            Image,
            '/ARTcar/left_camera',  # Name of the input image topic
            self.listener_callback_leftcam,
            10)
        self.subscription_leftcam  # Prevent unused variable warning
        
        self.subscription_rightcam = self.create_subscription(
            Image,
            '/ARTcar/right_camera',  # Name of the input image topic
            self.listener_callback_rightcam,
            10)
        self.subscription_rightcam  # Prevent unused variable warning

        self.publisher_leftcam = self.create_publisher(Image, '/ARTcar/left_camera_flipped', 10)
        self.publisher_rightcam = self.create_publisher(Image, '/ARTcar/right_camera_flipped', 10)
        self.bridge = CvBridge()

    def listener_callback_leftcam(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        
        # Flip the image by 180 degrees
        flipped_image = cv2.rotate(cv_image, cv2.ROTATE_180)

        # Convert OpenCV image back to ROS2 image message
        flipped_image_msg = self.bridge.cv2_to_imgmsg(flipped_image, "bgr8")

        # Publish the flipped image
        self.publisher_leftcam.publish(flipped_image_msg)
        self.get_logger().info('LEFT Image has been flipped and published. ---- by AI')
        
    def listener_callback_rightcam(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        
        # Flip the image by 180 degrees
        flipped_image = cv2.rotate(cv_image, cv2.ROTATE_180)

        # Convert OpenCV image back to ROS2 image message
        flipped_image_msg = self.bridge.cv2_to_imgmsg(flipped_image, "bgr8")

        # Publish the flipped image
        self.publisher_rightcam.publish(flipped_image_msg)
        self.get_logger().info('RIGHT Image has been flipped and published. ---- by AI')

def main(args=None):
    rclpy.init(args=args)
    image_flipper = ImageFlipper()
    rclpy.spin(image_flipper)
    image_flipper.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
