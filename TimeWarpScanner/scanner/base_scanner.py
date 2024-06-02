import cv2
import numpy as np

class BaseScanner:
    def __init__(self, input_path, line_speed=1):
        self.input_path = input_path
        self.line_speed = line_speed
        self.output_data = None

    def convert(self, output_path):
        cap = cv2.VideoCapture(self.input_path)

        if not cap.isOpened():
            print("Error: Could not open video.")
            return

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        frames = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)

        cap.release()

        self.process_frames(frames, width, height, fps, out)

        out.release()
        cv2.destroyAllWindows()

    def process_frames(self, frames, width, height, fps, out):
        raise NotImplementedError("Subclasses should implement this method")

    def get_output_data(self):
        return self.output_data
