import cv2 as cv
import numpy as np

class VideoTransf():
    """Simple class to apply some transformation on a video file"""
    video_path = None 
    video_cap = None # Video Capture object

    def __init__(self, path):
        self.video_path = path
        try:
            self.video_cap = cv.VideoCapture(filename)
        except Exception as ex:
            print(f'An Error occurred while opening the video file:\n{ex}')

        print(path)


    def release(self):
        self.video_cap.release()
        
