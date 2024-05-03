#!/usr/bin/env python3

import cv2
import numpy as np


def add_image(frame, overlay, alpha):
    overlay_resized = cv2.resize(overlay, (frame.shape[1], frame.shape[0]))
    return cv2.addWeighted(overlay_resized, alpha, frame, 1 - alpha, 0)


def template_matching(frame, template):
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    w, h = template_gray.shape[::-1]
    res = cv2.matchTemplate(frame_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)

    return frame


# 1
cap = cv2.VideoCapture(0)
# To fix "global cap_v4l.cpp:1134 tryIoctl VIDEOIO(V4L2:/dev/video0): select() timeout."
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

# 3
# cap=cv2.VideoCapture(0, cv2.CAP_V4L)
cap.set(3,640)#width
cap.set(4,480)#height
cap.set(10,100)#brightness

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('./output/result.avi', fourcc, 30.0, (640, 480))

cv2.namedWindow('frame')
cv2.createTrackbar('Alpha', 'frame', 0, 10, lambda x: None)

overlay_image = cv2.imread('./input/iknk.jpg')
template_image = cv2.imread('./input/poly.png')

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        alpha = cv2.getTrackbarPos('Alpha', 'frame') / 10
        frame = add_image(frame, overlay_image, alpha)
        frame = template_matching(frame, template_image)
        out.write(frame)
        cv2.imshow('frame', frame)
    else:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    key_pressed = cv2.waitKey(1)
    if key_pressed == ord('q'):
        break
    # ESC pressed
    elif key_pressed % 256 == 27:
        print("Escape hit, closing...")
        break
    # SPACE pressed
    elif key_pressed % 256 == 32:
        img_name = "./output/opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()

#
# import numpy as np
# import cv2
#
# video_capture = cv2.VideoCapture(0)
#
# while(True):
#     # Capture frame-by-frame
#     ret, frame = video_capture.read()
#
#     # Our operations on the frame comes here
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#     # Display the resulting frame
#     cv2.imshow('frame',gray)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # When everything's done, release the capture
# video_capture.release()
# cv2.destroyAllWindows()
#
#
# import cv2
#
# cam = cv2.VideoCapture(0)
# cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
#
# cv2.namedWindow("test")
#
# img_counter = 0
#
# while True:
#     ret, frame = cam.read()
#     if not ret:
#         print("failed to grab frame")
#         break
#     cv2.imshow("test", frame)
#
#     k = cv2.waitKey(1)
#     # ESC pressed
#     if k % 256 == 27:
#         print("Escape hit, closing...")
#         break
#     # SPACE pressed
#     elif k % 256 == 32:
#         img_name = "./output/opencv_frame_{}.png".format(img_counter)
#         cv2.imwrite(img_name, frame)
#         print("{} written!".format(img_name))
#         img_counter += 1
#
# cam.release()
#
# cv2.destroyAllWindows()
