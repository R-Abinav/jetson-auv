import cv2
import depthai as dai
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

# Initialize the ROS node
rospy.init_node("oakd_publisher", anonymous=True)

# ROS Publisher for Image messages
image_pub = rospy.Publisher("/oakd/image_raw", Image, queue_size=10)

# Bridge to convert OpenCV images to ROS Image messages
bridge = CvBridge()

# Create pipeline
pipeline = dai.Pipeline()

# Create a color camera node
color_cam = pipeline.createColorCamera()
color_cam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_720_P)  # 720p resolution
color_cam.setFps(30)  # Set FPS to 30
color_cam.setBoardSocket(dai.CameraBoardSocket.RGB)
color_cam.setInterleaved(False)  # Non-interleaved format

# Create an output link for the color camera
xout_video = pipeline.createXLinkOut()
xout_video.setStreamName("video")
color_cam.video.link(xout_video.input)

# Connect to the device
with dai.Device(pipeline) as device:
    # Output queue for video frames
    video_queue = device.getOutputQueue(name="video", maxSize=30, blocking=False)

    print("Press 'q' to exit")
    while not rospy.is_shutdown():
        # Get the latest frame
        frame = video_queue.get().getCvFrame()

        # Display the frame using OpenCV
        cv2.imshow("OAK-D 30 FPS RGB Feed", frame)

        # Convert frame to ROS Image message and publish
        ros_image = bridge.cv2_to_imgmsg(frame, encoding="bgr8")
        image_pub.publish(ros_image)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
