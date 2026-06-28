import json
import base64

from openai import OpenAI


class XAxisAgent:

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
You are an Executive Manufacturing X-Axis Agent.

Your ONLY responsibility is to understand the X Axis.

DO NOT extract any Y values.

DO NOT estimate bar heights.

DO NOT estimate line values.

Return STRICT JSON ONLY.

Extract ONLY the following.

{

    "x_axis":{

        "label":"",

        "rotation":0,

        "categories":[

        ],

        "category_count":0,

        "first_category":"",

        "last_category":"",

        "frequency":"",

        "category_type":"",

        "confidence":0.0

    }

}

Rules

1 Return JSON only.

2 Ignore ALL numerical values on Y axis.

3 Ignore ALL bar heights.

4 Ignore ALL line values.

5 Extract every visible X-axis label.

6 Preserve the exact order.

7 Do not skip labels.

8 Detect the label rotation angle.

9 If labels are weeks return category_type = "Week".

10 If labels are months return category_type = "Month".

11 If labels are dates return category_type = "Date".

12 If labels are text return category_type = "Category".

13 Frequency should be one of:

Weekly
Monthly
Quarterly
Yearly
Category
Unknown

14 Confidence must be between 0 and 1.

15 Return valid JSON only.
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
    # Validate
    ###############################################################

    def validate(
            self,
            result
    ):

        required = [

            "x_axis"

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
