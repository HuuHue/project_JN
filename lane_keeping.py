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

def region_scan(video):
    height = 540
    polygons = np.array([[(0, height), (960, height), (960, 200), (580, 0), (380, 0), (0, 200) ]])
    mask = np.zeros_like(video)
    cv2.fillPoly(mask, polygons, 255)
    maskd_video = cv2.bitwise_and(video, mask)
    return maskd_video

def dislay_lines(video, lines):
    line_video = np.zeros_like(video)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_video, (x1, y1), (x2, y2), 255, 5)
    return line_video


window_title = "CSI Camera"
video_capture = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
while True:
    ret, frame = video_capture.read()
    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    canny_frame = canny(gray_frame)
    cropped_frame = region_scan(canny_frame)
    lines = cv2.HoughLinesP(cropped_frame, 2, np.pi/180, 150, np.array([]), 40, 5)
    line_frame = dislay_lines(gray_frame, lines)
    combo_frame = cv2.addWeighted(gray_frame, 0.8, line_frame, 1, 0)
    cv2.line(combo_frame, (480, 540), (480, 300), 255, 3)
    cv2.imshow(window_title, combo_frame)
    keyCode = cv2.waitKey(10) & 0xFF       
    if keyCode == 27 or keyCode == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()
    