from .base_scanner import BaseScanner
import cv2
import numpy as np


class TopToBottomScanner(BaseScanner):
    def process_frames(self, frames, width, height, fps, out):
        self.line_pos = 0
        fixed_frames = np.zeros((height, width, 3), dtype=np.uint8)

        frame_index = 0

        while frame_index < len(frames):
            frame = frames[frame_index]
            if not self.paused:
                self.line_pos = min(self.line_pos + self.line_speed, height - 1)

            if self.line_pos < height:
                fixed_frames[self.line_pos - self.line_speed:self.line_pos, :] = frame[self.line_pos - self.line_speed:self.line_pos, :]

            combined_frame = fixed_frames.copy()
            combined_frame[self.line_pos:, :] = frame[self.line_pos:, :]

            frame_with_line = combined_frame.copy()
            cv2.line(frame_with_line, (0, self.line_pos), (width, self.line_pos), (255, 0, 0), 2)

            out.write(frame_with_line)
            cv2.imshow('Time Warp Scan', frame_with_line)

            key = cv2.waitKey(int(1000 / fps)) & 0xFF
            if key == 27:  # Esc key
                break
            elif key == ord(' '):  # Spacebar
                self.paused = not self.paused
            elif self.paused:
                self.update_line_position(key, width, height)

            if self.line_pos >= height - 1:
                break

            if not self.paused:
                frame_index += 1

    def update_line_position(self, key, width, height):
        if key == ord('w'):  # 'w' key
            self.line_pos = max(self.line_pos - self.line_speed, 0)
        elif key == ord('s'):  # 's' key
            self.line_pos = min(self.line_pos + self.line_speed, height - 1)
