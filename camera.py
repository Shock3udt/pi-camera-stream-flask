#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This scrtipt script..

import cv2
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import numpy as np
import threading

class VideoCamera(object):
    def __init__(self, flip = False):
        self.vs = PiVideoStream().start()
        self.flip = flip
        self.buffer = None
        self.lock = threading.Lock()
        time.sleep(2.0)
    def _thread(self):
        while True:
            frame = self.get()
            with self.lock:
                self.buffer = frame
            time.sleep(.1)

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get(self):
        frame = self.flip_if_needed(self.vs.read())
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
    def get_frame(self):
        frame = None
        with self.lock:
            frame = self.buffer
        return frame