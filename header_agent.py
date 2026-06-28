import json
import base64
import fitz
from io import BytesIO
from PIL import Image
from openai import OpenAI


class HeaderAgent:

    def __init__(self, api_key):

        self.client = OpenAI(api_key=api_key)

    ####################################################################
    # Convert PDF page to image
    ####################################################################

    def pdf_page_to_image(self, pdf_path, page_number):

        doc = fitz.open(pdf_path)

        page = doc.load_page(page_number)

        pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))

        img = Image.open(BytesIO(pix.tobytes("png")))

        return img

    ####################################################################
    # Convert image to base64
    ####################################################################

    def image_to_base64(self, image):

        buffer = BytesIO()

        image.save(buffer, format="PNG")

        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    ####################################################################
    # Main Extraction Function
    ####################################################################

    def extract(
            self,
            pdf_path,
            page_number
    ):

        image = self.pdf_page_to_image(
            pdf_path,
            page_number
        )

        image64 = self.image_to_base64(image)

        prompt = self.build_prompt()

        response = self.client.responses.create(

            model="gpt-4.1",

            input=[

                {
                    "role": "user",

                    "content":[

                        {
                            "type":"input_text",

                            "text":prompt
                        },

                        {
                            "type":"input_image",

                            "image_url":f"data:image/png;base64,{image64}"
                        }

                    ]

                }

            ]

        )

        text = response.output_text.strip()

        return self.clean_json(text)
        ####################################################################
    # Prompt
    ####################################################################

    def build_prompt(self):

        return """
You are an Executive Manufacturing Report Header Agent.

Your ONLY responsibility is to understand the page and identify all NON-NUMERICAL metadata.

DO NOT estimate any values.

DO NOT calculate bar heights.

DO NOT read line values.

DO NOT estimate percentages.

Return STRICT JSON.

Extract ONLY the following.

{

    "page":{

        "page_number":null,

        "page_title":"",

        "section":"",

        "sub_section":""

    },

    "report":{

        "report_name":"",

        "business_unit":"",

        "plant":"",

        "report_date":""

    },

    "charts":[

        {

            "chart_number":1,

            "chart_title":"",

            "chart_subtitle":"",

            "legend":[

                {

                    "name":"",

                    "colour":""

                }

            ],

            "left_y_axis":{

                "exists":true,

                "label":"",

                "unit":""

            },

            "right_y_axis":{

                "exists":false,

                "label":"",

                "unit":""

            },

            "business_commentary_present":false

        }

    ],

    "confidence":0.0

}

Rules

1 Return JSON only.

2 Never estimate numerical values.

3 Return one chart object for every chart visible on the page.

4 Extract chart titles exactly.

5 Extract legend names exactly.

6 If there are two Y axes identify both.

7 If information is unavailable return null.

8 Confidence must be between 0 and 1.

9 Ignore all numerical bar values.

10 Ignore line values.

11 Ignore X-axis labels.

12 Ignore Y-axis tick values.
"""
        ####################################################################
    # Clean JSON
    ####################################################################

    def clean_json(self, text):

        try:

            text = text.replace("```json", "")

            text = text.replace("```", "")

            text = text.strip()

            return json.loads(text)

        except Exception:

            return {

                "status": "ERROR",

                "message": "Unable to parse model response",

                "raw_response": text

            }

    ####################################################################
    # Pretty Print (Optional)
    ####################################################################

    def pretty_print(self, data):

        print(json.dumps(data, indent=4))

    ####################################################################
    # Validate Output Structure
    ####################################################################

    def validate(self, result):

        required = [

            "page",
            "report",
            "charts",
            "confidence"

        ]

        missing = []

        for field in required:

            if field not in result:

                missing.append(field)

        return {

            "valid": len(missing) == 0,

            "missing_fields": missing

        }

    ####################################################################
    # Save JSON
    ####################################################################

    def save_json(
            self,
            result,
            output_file
    ):

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
