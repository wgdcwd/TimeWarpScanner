from .base_scanner import BaseScanner
import cv2
import numpy as np


class RightToLeftScanner(BaseScanner):
    def process_frames(self, frames, width, height, fps, out):
        self.line_pos = width - 1
        fixed_frames = np.zeros((height, width, 3), dtype=np.uint8)

        frame_index = 0

        while frame_index < len(frames):
            frame = frames[frame_index]

            if not self.paused:
                self.line_pos = max(self.line_pos - self.line_speed, 0)

            if self.line_pos >= 0:
                fixed_frames[:, self.line_pos:self.line_pos + self.line_speed] = frame[:, self.line_pos:self.line_pos + self.line_speed]

            combined_frame = fixed_frames.copy()
            combined_frame[:, :self.line_pos] = frame[:, :self.line_pos]

            frame_with_line = combined_frame.copy()
            cv2.line(frame_with_line, (self.line_pos, 0), (self.line_pos, height), (255, 0, 0), 2)

            out.write(frame_with_line)
            cv2.imshow('Time Warp Scan', frame_with_line)

            key = cv2.waitKey(int(1000 / fps)) & 0xFF
            if key == 27:  # Esc key
                break
            elif key == ord(' '):  # Spacebar
                self.paused = not self.paused
            elif self.paused:
                self.update_line_position(key, width, height)

            self.update_speed(key)

            if self.line_pos <= 0:
                break

            if not self.paused:
                frame_index += 1

    def update_line_position(self, key, width, height):
        if key == ord('a'):  # 'a' key
            self.line_pos = max(self.line_pos - self.line_speed, 0)
        elif key == ord('d'):  # 'd' key
            self.line_pos = min(self.line_pos + self.line_speed, width - 1)
