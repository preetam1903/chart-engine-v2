import cv2
import numpy as np


class BarValueExtractor:

    def detect_bars(self, image_path):

        img = cv2.imread(image_path)

        if img is None:
            return None, []

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Blur to remove noise
        gray = cv2.GaussianBlur(gray, (3, 3), 0)

        # Binary image
        _, thresh = cv2.threshold(
            gray,
            220,
            255,
            cv2.THRESH_BINARY_INV
        )

        # Join broken bar edges
        kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (3, 3)
        )

        thresh = cv2.morphologyEx(
            thresh,
            cv2.MORPH_CLOSE,
            kernel,
            iterations=2
        )

        contours, _ = cv2.findContours(
            thresh,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        bars = []

        h_img, w_img = gray.shape

        for cnt in contours:

            x, y, w, h = cv2.boundingRect(cnt)

            # Ignore tiny objects
            if w < 4:
                continue

            if h < 15:
                continue

            # Ignore very wide objects
            if w > 40:
                continue

            # Ignore objects touching image border
            if x <= 2 or y <= 2:
                continue

            if x + w >= w_img - 2:
                continue

            if y + h >= h_img - 2:
                continue

            # Keep only vertical objects
            if h > w:

                bars.append({
                    "x": x,
                    "y": y,
                    "w": w,
                    "h": h
                })

        bars.sort(key=lambda b: b["x"])

        return img, bars
