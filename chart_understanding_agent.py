import json
import base64

from openai import OpenAI


class ChartUnderstandingAgent:

    def __init__(self, api_key):

        self.client = OpenAI(api_key=api_key)

    ###############################################################
    # Encode Image
    ###############################################################

    def encode_image(
            self,
            image_path
    ):

        with open(image_path, "rb") as f:

            return base64.b64encode(
                f.read()
            ).decode("utf-8")

    ###############################################################
    # Main Process
    ###############################################################

    def process(
            self,
            image_path
    ):

        image64 = self.encode_image(
            image_path
        )

        prompt = self.build_prompt()

        response = self.client.responses.create(

            model="gpt-4.1-mini",

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

                            "image_url": f"data:image/png;base64,{image64}"

                        }

                    ]

                }

            ]

        )

        text = response.output_text.strip()

        print("=" * 80)
        print("CHART UNDERSTANDING")
        print("=" * 80)
        print(text)
        print("=" * 80)

        understanding = self.clean_json(text)

        understanding["agent"] = "ChartUnderstandingAgent"
        understanding["version"] = "1.0"

        return understanding

    ###############################################################
    # Prompt
    ###############################################################

    def build_prompt(self):

        return """
You are an Executive Manufacturing Intelligence Agent.

Analyse this chart completely.

Return ONLY valid JSON.

{
    "chart_title":"",
    "chart_type":"",
    "chart_subtype":"",

    "x_axis":{
        "type":"",
        "labels":[]
    },

    "y_axis":{
        "title":"",
        "unit":""
    },

    "legend":[],

    "series_count":0,

    "summary":"",

    "confidence":0.0
}

Rules

1. Detect chart title.

2. Detect chart type.

3. Detect chart subtype.

4. Detect X axis type.

5. Read every visible X axis label.

6. Detect Y axis title.

7. Detect Y axis unit.

8. Detect legend names.

9. Count total data series.

10. Write a two-line executive summary.

11. Confidence must be between 0 and 1.

12. Return STRICT JSON ONLY.

Do NOT wrap JSON inside markdown.
"""

    ###############################################################
    # Clean JSON
    ###############################################################

    def clean_json(
            self,
            text
    ):

        try:

            text = text.replace(
                "```json",
                ""
            )

            text = text.replace(
                "```",
                ""
            )

            text = text.strip()

            return json.loads(text)

        except Exception:

            return {

                "status": "ERROR",

                "message": "Unable to parse model response",

                "raw_response": text

            }

    ###############################################################
    # Save JSON
    ###############################################################

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
