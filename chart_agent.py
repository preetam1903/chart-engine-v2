import json
import base64

from openai import OpenAI


class ChartAgent:

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
    # Main Extraction
    ###############################################################

    def extract(
            self,
            image_path
    ):

        image64 = self.encode_image(
            image_path
        )

        prompt = self.build_prompt()

        response = self.client.responses.create(

            model="gpt-4.1",

            input=[

                {

                    "role":"user",

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

        ###############################################################
    # Prompt
    ###############################################################

    def build_prompt(self):

        return """
You are an Executive Manufacturing Chart Structure Agent.

Your ONLY responsibility is to understand the VISUAL STRUCTURE of the chart.

DO NOT extract numerical values.

DO NOT read X-axis labels.

DO NOT identify legend names.

Those are handled by other agents.

Return STRICT JSON ONLY.

Extract ONLY the following.

{

    "chart":{

        "chart_type":"",

        "orientation":"",

        "primary_visual":"",

        "secondary_visual":"",

        "stacked":false,

        "grouped":false,

        "dual_axis":false,

        "left_axis_used":true,

        "right_axis_used":false,

        "bar_series_count":0,

        "line_series_count":0,

        "scatter_series_count":0,

        "area_series_count":0,

        "pie_present":false,

        "render_objects":[

            {

                "object_type":"",

                "colour":"",

                "axis":"left"

            }

        ],

        "estimated_complexity":"",

        "confidence":0.0

    }

}

Rules

1 Return VALID JSON ONLY.

2 Ignore all X-axis labels.

3 Ignore all Y-axis labels.

4 Ignore all numerical values.

5 Ignore chart title.

6 Ignore legend text.

7 Detect chart type only.

8 Detect grouped or stacked bars.

9 Detect line overlays.

10 Detect scatter plots.

11 Detect area charts.

12 Detect pie charts.

13 Detect horizontal or vertical orientation.

14 Detect if two Y axes are being used.

15 Identify each visual object.

Allowed object types:

Bar

Line

Area

Scatter

Pie

Allowed chart types:

Grouped Bar

Stacked Bar

Grouped Bar with Line

Stacked Bar with Line

Line

Scatter

Pie

Area

Combination

Unknown

Estimated complexity should be one of:

Simple

Medium

Complex

Confidence must be between 0 and 1.

Return JSON only.
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
    # Validate Output
    ###############################################################

    def validate(
            self,
            result
    ):

        required = [

            "chart"

        ]

        missing = []

        for field in required:

            if field not in result:

                missing.append(field)

        return {

            "valid": len(missing) == 0,

            "missing_fields": missing

        }

    ###############################################################
    # Pretty Print
    ###############################################################

    def pretty_print(
            self,
            result
    ):

        print(

            json.dumps(

                result,

                indent=4,

                ensure_ascii=False

            )

        )

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
