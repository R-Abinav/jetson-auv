import cv2
import depthai as dai

# Create pipeline
pipeline = dai.Pipeline()

# Create a color camera node
color_cam = pipeline.createColorCamera()
#color_cam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)  # 1080p resolution
color_cam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_720_P) #720p resolution
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
    while True:
        # Get the latest frame
        frame = video_queue.get().getCvFrame()

        # Display the frame using OpenCV
        cv2.imshow("OAK-D 30 FPS RGB Feed", frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()