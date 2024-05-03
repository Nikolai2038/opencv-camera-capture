#!/usr/bin/env python3

# main.py
import cv2
from tkinter import Tk, Button, Label, messagebox
from PIL import Image, ImageTk


class VideoCapture:
    label = Label(
        width=32,
        height=24,
        bg="blue",
        fg="yellow",
    )

    def __init__(self):
        self.capture = cv2.VideoCapture(0)
        self.video_writer = None
        self.running = False

    def start_capture(self):
        if not self.running:
            self.running = True
            self.video_writer = cv2.VideoWriter('./output/video.avi', cv2.VideoWriter_fourcc(*'XVID'), 30.0, (320, 240))

    def stop_capture(self):
        if self.running:
            self.running = False
            self.video_writer.release()

    def update_preview(self):
        ret, frame = self.capture.read()
        if ret:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.config(image=imgtk)


root = Tk()
vcapture = VideoCapture()
vcapture.label.pack()

start_button = Button(root, text="Start", command=vcapture.start_capture)
start_button.pack(side="left")

stop_button = Button(root, text="Stop", command=vcapture.stop_capture)
stop_button.pack(side="right")

exit_button = Button(root, text="Exit", command=root.destroy)
exit_button.pack(side="bottom")

vcapture.update_preview()
root.mainloop()
