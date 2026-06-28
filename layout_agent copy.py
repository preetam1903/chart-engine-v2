import os
import fitz
import cv2
import json
import numpy as np
from PIL import Image
from io import BytesIO


class LayoutAgent:

    def __init__(self):

        pass

    ##############################################################
    # Convert PDF Page to Image
    ##############################################################

    def pdf_page_to_image(
            self,
            pdf_path,
            page_number
    ):

        doc = fitz.open(pdf_path)

        page = doc.load_page(page_number)

        pix = page.get_pixmap(matrix=fitz.Matrix(3,3))

        image = Image.open(
            BytesIO(
                pix.tobytes("png")
            )
        )

        return np.array(image)

    ##############################################################
    # Detect Charts
    ##############################################################

    def detect_layout(
            self,
            pdf_path,
            page_number
    ):

        image = self.pdf_page_to_image(
            pdf_path,
            page_number
        )

        layout = self.find_chart_boxes(image)

        return layout
        ##############################################################
    # Find Chart Bounding Boxes
    ##############################################################

    def find_chart_boxes(self, image):

        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        edges = cv2.Canny(
            blur,
            50,
            150
        )

        kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (7, 7)
        )

        edges = cv2.dilate(
            edges,
            kernel,
            iterations=2
        )

        contours, _ = cv2.findContours(
            edges,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        charts = []

        height, width = image.shape[:2]

        chart_no = 1

        for c in contours:

            x, y, w, h = cv2.boundingRect(c)

            area = w * h

            # Ignore tiny objects

            if area < 50000:
                continue

            # Ignore objects touching page border

            if x < 20 or y < 20:
                continue

            if x + w > width - 20:
                continue

            if y + h > height - 20:
                continue

            charts.append({

                "chart_id": f"CH{chart_no:03}",

                "x": int(x),

                "y": int(y),

                "w": int(w),

                "h": int(h)

            })

            chart_no += 1

        charts = sorted(
            charts,
            key=lambda c: (
                c["y"],
                c["x"]
            )
        )

        return self.assign_positions(
            image,
            charts
        )
        ##############################################################
    # Assign Grid Positions
    ##############################################################

    def assign_positions(
            self,
            image,
            charts
    ):

        if len(charts) == 0:

            return {

                "page": None,

                "chart_count": 0,

                "charts": []

            }

        #
        # Sort top to bottom then left to right
        #

        charts = sorted(
            charts,
            key=lambda c: (c["y"], c["x"])
        )

        #
        # Detect rows
        #

        rows = []

        tolerance = 60

        for chart in charts:

            assigned = False

            for row in rows:

                if abs(chart["y"] - row["y"]) < tolerance:

                    row["charts"].append(chart)

                    assigned = True

                    break

            if not assigned:

                rows.append({

                    "y": chart["y"],

                    "charts": [chart]

                })

        #
        # Sort each row by X
        #

        for row in rows:

            row["charts"] = sorted(
                row["charts"],
                key=lambda c: c["x"]
            )

        #
        # Assign R1C1 style positions
        #

        final = []

        for r, row in enumerate(rows):

            for c, chart in enumerate(row["charts"]):

                chart["position"] = f"R{r+1}C{c+1}"

                final.append(chart)

        return {

            "rows": len(rows),

            "chart_count": len(final),

            "charts": final

        }

    ##############################################################
    # Crop Charts
    ##############################################################

    def crop_charts(
            self,
            pdf_path,
            page_number,
            layout,
            output_folder
    ):

        os.makedirs(
            output_folder,
            exist_ok=True
        )

        image = self.pdf_page_to_image(
            pdf_path,
            page_number
        )

        saved = []

        for chart in layout["charts"]:

            x = chart["x"]
            y = chart["y"]
            w = chart["w"]
            h = chart["h"]

            crop = image[
                y:y+h,
                x:x+w
            ]

            file_name = os.path.join(

                output_folder,

                f'{chart["chart_id"]}.png'

            )

            Image.fromarray(crop).save(file_name)

            chart["image"] = file_name

            saved.append(chart)

        layout["charts"] = saved

        return layout

    ##############################################################
    # Save Layout JSON
    ##############################################################

    def save_json(
            self,
            layout,
            output_file
    ):

        with open(
                output_file,
                "w",
                encoding="utf-8"
        ) as f:

            json.dump(
                layout,
                f,
                indent=4,
                ensure_ascii=False
            )

        return output_file
