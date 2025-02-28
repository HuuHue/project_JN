import cv2
import numpy as np

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )
def canny(video):
    blur_video = cv2.blur(video, (5, 5))
    canny_video = cv2.Canny(blur_video, 50, 150)
    return canny_video


window_title = "CSI Camera"
video_capture = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
while True:
    ret, frame = video_capture.read()
    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    canny_frame = canny(gray_frame)
    cv2.imshow(window_title,canny_frame)
    keyCode = cv2.waitKey(10) & 0xFF       
    if keyCode == 27 or keyCode == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()
    