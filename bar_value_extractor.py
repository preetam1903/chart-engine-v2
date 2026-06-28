import cv2
import numpy as np


class BarValueExtractor:

    def detect_bars(self, image_path):

        img = cv2.imread(image_path)

        if img is None:
            return None, []

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Invert image
        _, binary = cv2.threshold(
            gray,
            210,
            255,
            cv2.THRESH_BINARY_INV
        )

        h, w = binary.shape

        # Ignore top legend
        binary = binary[40:h-35, :]

        projection = np.sum(binary > 0, axis=0)

        bars = []

        inside = False
        start = 0

        for x in range(len(projection)):

            if projection[x] > 15 and not inside:
                start = x
                inside = True

            elif projection[x] <= 15 and inside:

                end = x

                width = end - start

                if 4 <= width <= 25:

                    center = (start + end) // 2

                    column = binary[:, center]

                    pixels = np.where(column > 0)[0]

                    if len(pixels):

                        top = pixels[0]
                        bottom = pixels[-1]

                        bars.append({

                            "x": center,

                            "top": int(top),

                            "bottom": int(bottom),

                            "height": int(bottom-top)

                        })

                inside = False

        debug = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

        for i, bar in enumerate(bars):

            cv2.line(
                debug,
                (bar["x"], bar["top"]),
                (bar["x"], bar["bottom"]),
                (0,255,0),
                2
            )

            cv2.putText(
                debug,
                str(i+1),
                (bar["x"]-4, bar["top"]-5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (0,0,255),
                1
            )

        return debug, bars
