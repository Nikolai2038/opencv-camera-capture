#!/usr/bin/env python3

import cv2
import numpy as np
from tkinter import Tk, Button, Label, messagebox
from PIL import Image, ImageTk


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

overlay_image = cv2.imread('./input/iknk.jpg')
template_image = cv2.imread('./input/poly.png')

class VideoCapture:
    def __init__(self):
        self.capture = cv2.VideoCapture(0)

        # To fix "global cap_v4l.cpp:1134 tryIoctl VIDEOIO(V4L2:/dev/video0): select() timeout."
        self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

        # width
        self.capture.set(3, 640)
        # height
        self.capture.set(4, 480)
        # brightness
        self.capture.set(10, 100)

        self.video_writer = None
        self.running = False

    def start_capture(self):
        if not self.running:
            self.running = True
            self.video_writer = cv2.VideoWriter('./output/result.avi', cv2.VideoWriter_fourcc(*'XVID'), 30.0, (640, 480))

    def stop_capture(self):
        if self.running:
            self.running = False
            self.video_writer.release()

    def update_preview(self):
        ret, frame = self.capture.read()
        if ret:
            #alpha = cv2.getTrackbarPos('Alpha', 'frame') / 10
            alpha = 0
            frame = add_image(frame, overlay_image, alpha)
            frame = template_matching(frame, template_image)
            #cv2.imshow('frame', frame)

            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.config(image=imgtk)

            if self.running:
                self.video_writer.write(frame)
        root.after(30, self.update_preview)

    def __del__(self):
        self.capture.release()
        self.video_writer.release()
        cv2.destroyAllWindows()

cv2.namedWindow('frame')
cv2.createTrackbar('Alpha', 'frame', 0, 10, lambda x: None)

root = Tk()
vcapture = VideoCapture()
vcapture.label = Label(root)
vcapture.label.pack()

start_button = Button(root, text="Start", command=vcapture.start_capture)
start_button.pack(side="left")

stop_button = Button(root, text="Stop", command=vcapture.stop_capture)
stop_button.pack(side="right")

exit_button = Button(root, text="Exit", command=root.destroy)
exit_button.pack(side="bottom")

# key_pressed = cv2.waitKey(1)
# # Q, ESC or SPACE
# if (key_pressed == ord('q')) or (key_pressed % 256 == 27) or (key_pressed % 256 == 32):
#     exit(0)

vcapture.update_preview()
root.mainloop()

# Release everything if job is finished

#
#
# # 1
# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
#
# # 3
# # cap=cv2.VideoCapture(0, cv2.CAP_V4L)
#
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('./output/result.avi', fourcc, 30.0, (640, 480))
#
#
# cv2.labl
#
#
# while cap.isOpened():
#     ret, frame = cap.read()
#     if ret:
#         alpha = cv2.getTrackbarPos('Alpha', 'frame') / 10
#         frame = add_image(frame, overlay_image, alpha)
#         frame = template_matching(frame, template_image)
#         out.write(frame)
#         cv2.imshow('frame', frame)
#     else:
#         print("Can't receive frame (stream end?). Exiting ...")
#         break
#
