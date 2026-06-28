import json
import base64
from openai import OpenAI


class ChartMetadataAgent:

    def __init__(self, api_key):

        self.client = OpenAI(api_key=api_key)

    def encode_image(self, image_path):

        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def extract_metadata(self, image_path):

        image_b64 = self.encode_image(image_path)

        prompt = """
You are an Executive Manufacturing Chart Metadata Agent.

Your responsibility is to understand EVERYTHING about the chart EXCEPT the numerical values.

DO NOT estimate any values.

Return STRICT JSON ONLY.

Extract the following information.

{
  "page":{

      "page_number":null,

      "position":"",

      "row":null,

      "column":null
  },

  "report":{

      "report_name":"",

      "report_date":"",

      "business_unit":"",

      "plant":""
  },

  "header":{

      "page_title":"",

      "section":"",

      "sub_section":"",

      "chart_title":"",

      "chart_subtitle":""
  },

  "chart":{

      "chart_type":"",

      "orientation":"",

      "dual_axis":false,

      "business_commentary_present":false
  },

  "legend":[

  ],

  "axes":{

      "x_axis":{

          "label":"",

          "rotation":45
      },

      "left_y_axis":{

          "exists":true,

          "label":"",

          "unit":""
      },

      "right_y_axis":{

          "exists":false,

          "label":"",

          "unit":""
      }
  },

  "axis_mapping":[

  ],

  "confidence":0.0

}

Rules

1 Return ONLY JSON.

2 Never estimate numerical values.

3 Never estimate bar heights.

4 Never estimate line values.

5 If information is missing use null.

6 Confidence must be between 0 and 1.

7 If two Y axes exist identify both.

8 Extract legend names exactly as shown.

9 Extract chart title exactly.

10 Return valid JSON only.
"""

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

                            "image_url":f"data:image/png;base64,{image_b64}"
                        }

                    ]

                }

            ]

        )

        text = response.output_text.strip()

        try:

            return json.loads(text)

        except Exception:

            return {

                "error":"Unable to parse JSON",

                "raw_response":text

            }
