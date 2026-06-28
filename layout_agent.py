import os
import json
import base64
import fitz

from PIL import Image
from openai import OpenAI


class LayoutAgent:

    ##############################################################
    # Constructor
    ##############################################################

    def __init__(

            self,

            api_key

    ):

        self.client = OpenAI(

            api_key=api_key

        )

    ##############################################################
    # Convert PDF Page to Image
    ##############################################################

    def render_page(

            self,

            pdf_path,

            page_number,

            output_folder

    ):

        os.makedirs(

            output_folder,

            exist_ok=True

        )

        document = fitz.open(

            pdf_path

        )

        page = document.load_page(

            page_number

        )

        #
        # High Resolution Rendering
        #

        matrix = fitz.Matrix(

            3,

            3

        )

        pix = page.get_pixmap(

            matrix=matrix,

            alpha=False

        )

        image_path = os.path.join(

            output_folder,

            f"page_{page_number+1}.png"

        )

        pix.save(

            image_path

        )

        document.close()

        return image_path
        ##############################################################
    # Detect Chart Layout using GPT Vision
    ##############################################################

    def detect_layout(

            self,

            image_path

    ):

        prompt = """
You are an expert in executive dashboard analysis.

Your task is to detect EVERY chart visible on this page.

For every detected chart return:

1. chart_id
2. position (R1C1, R1C2...)
3. chart_type
4. confidence (0-100)
5. bounding box
    - left
    - top
    - right
    - bottom
6. includes

Rules

1. Ignore page titles.
2. Ignore comments.
3. Ignore tables.
4. Ignore logos.
5. Return ONLY charts.
6. Return ONLY JSON.

A chart MUST include:

• Chart title
• Complete plotting area
• X axis
• Left Y axis
• Right Y axis (if present)
• Legend
• Threshold lines
• Forecast lines
• Trend lines
• Data labels

The bounding box MUST NOT include:

• Adjacent charts
• Page title
• Headers
• Footers
• Tables
• Logos

Return ONLY valid JSON.

Do NOT crop away legends or chart titles.

Do NOT include neighbouring charts.

Return the smallest rectangle containing the complete chart.

8. Return JSON only.

Example

Example

{
    "page_number": 1,
    "chart_count": 4,
    "charts": [
        {
            "chart_id": "CH001",
            "position": "R1C1",

            "chart_type": "Unknown",

            "confidence": 98,

            "bbox": {
                "left": 20,
                "top": 40,
                "right": 400,
                "bottom": 260
            },

            "includes": [
                "title",
                "plot_area",
                "x_axis",
                "left_y_axis",
                "legend"
            ]
        },

        {
            "chart_id": "CH002",
            "position": "R1C2",

            "chart_type": "Unknown",

            "confidence": 97,

            "bbox": {
                "left": 420,
                "top": 40,
                "right": 800,
                "bottom": 260
            },

            "includes": [
                "title",
                "plot_area",
                "x_axis",
                "left_y_axis",
                "right_y_axis",
                "legend"
            ]
        }
    ]
}
"""

        with open(

                image_path,

                "rb"

        ) as f:
            image_base64 = base64.b64encode(
                f.read()
            ).decode(
                "utf-8"
            )


            response = self.client.responses.create(

                model="gpt-4.1",

                input=[

                    {
                        "role": "user",

                        "content": [

                            {
                                "type": "input_text",

                                "text": prompt

                            },

                            {
                                "type": "input_image",

                                "image_url": f"data:image/png;base64,{image_base64}"

                            }

                        ]

                    }

                ]

            )

        result = response.output_text.strip()

        if result.startswith("```json"):
            result = result.replace("```json", "").replace("```", "").strip()

        elif result.startswith("```"):
            result = result.replace("```", "").strip()

        return json.loads(result)
        ##############################################################
    # Crop Charts using Pillow
    ##############################################################

    def crop_charts(

            self,

            image_path,

            layout,

            output_folder

    ):

        os.makedirs(

            output_folder,

            exist_ok=True

        )

        page = Image.open(

            image_path

        )
        page = page.convert("RGB")

        charts = []

        for chart in layout["charts"]:

            bbox = chart["bbox"]

            left = int(bbox["left"])
            top = int(bbox["top"])
            right = int(bbox["right"])
            bottom = int(bbox["bottom"])

            page_width, page_height = page.size

            left = max(0, left)
            top = max(0, top)

            right = min(page_width,right)
            bottom = min(page_height,bottom)

            cropped = page.crop(

                (

                    left,

                    top,

                    right,

                    bottom

                )

            )

            filename = f'{chart["chart_id"]}.png'

            filepath = os.path.join(

                output_folder,

                filename

            )

            cropped.save(

                filepath

            )

            charts.append(

                {

                    "chart_id": chart["chart_id"],

                    "position": chart["position"],

                    "bbox": bbox,

                    "image": filepath

                }

            )

        return {

            "page_number": layout["page_number"],

            "chart_count": len(charts),

            "charts": charts

        }

        ##############################################################
    # Save Layout JSON
    ##############################################################

    def save_json(

            self,

            result,

            output_file

    ):

        os.makedirs(

            os.path.dirname(

                output_file

            ),

            exist_ok=True

        )

        with open(

                output_file,

                "w",

                encoding="utf-8"

        ) as f:

            json.dump(

                result,

                f,

                indent=4,

                ensure_ascii=False

            )

        return output_file

    ##############################################################
    # Process Complete Layout
    ##############################################################

    def process(

            self,

            pdf_path,

            page_number,

            output_folder

    ):

        page_image = self.render_page(

            pdf_path,

            page_number,

            output_folder

        )

        layout = self.detect_layout(

            page_image

        )

        layout = self.crop_charts(

            page_image,

            layout,

            os.path.join(

                output_folder,

                "cropped"

            )

        )

        self.save_json(

            layout,

            os.path.join(

                output_folder,

                "layout.json"

            )

        )

        return layout
