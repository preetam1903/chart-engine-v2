import cv2
import numpy as np


class BarValueExtractor:

    def detect_bars(self, image_path):

        img = cv2.imread(image_path)

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Detect blue bars
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([140, 255, 255])

        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        bars = []

        for c in contours:

            x, y, w, h = cv2.boundingRect(c)

            # Ignore tiny objects
            if h < 20:
                continue

            bars.append({
                "x": x,
                "y": y,
                "w": w,
                "h": h
            })

        bars = sorted(bars, key=lambda b: b["x"])

        return img, bars
