from .base_scanner import BaseScanner
import cv2
import numpy as np


class BottomToTopScanner(BaseScanner):
    def process_frames(self, frames, width, height, fps, out):
        line_pos = height - 1
        fixed_frames = np.zeros((height, width, 3), dtype=np.uint8)

        for frame_index in range(len(frames)):
            frame = frames[frame_index]
            line_pos = max(line_pos - self.line_speed, 0)

            if line_pos >= 0:
                fixed_frames[line_pos:line_pos + self.line_speed, :] = frame[line_pos:line_pos + self.line_speed, :]

            combined_frame = fixed_frames.copy()
            combined_frame[:line_pos, :] = frame[:line_pos, :]

            frame_with_line = combined_frame.copy()
            cv2.line(frame_with_line, (0, line_pos), (width, line_pos), (255, 0, 0), 2)

            out.write(frame_with_line)
            cv2.imshow('Time Warp Scan', frame_with_line)
            if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
                break

            if line_pos <= 0:
                break
