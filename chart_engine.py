import base64
import json

from openai import OpenAI
from json_schema import empty_chart_schema

client = OpenAI()


class ChartEngine:

    def __init__(self):
        pass

    def image_to_base64(self, image_path):

        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def understand_chart(self, image_path):

        image = self.image_to_base64(image_path)

        prompt = """
You are an expert chart digitization engine.

Your task is NOT to summarize the chart.

Your task is to DIGITIZE the chart exactly.

Rules:

1. Return ONLY valid JSON.
2. No markdown.
3. No explanation.
4. Measure values using the visible Y-axis scale.
5. Return values rounded to ONE decimal place.
6. Preserve the order exactly as displayed.
7. If uncertain, estimate using the Y-axis gridlines rather than guessing.

Return JSON in EXACTLY this format:

{
    "chart_type":"",
    "title":"",
    "x_axis":{
        "label":"",
        "values":[]
    },
    "y_axis":{
        "label":"",
        "ticks":[]
    },
    "series":[
        {
            "name":"",
            "values":[]
        }
    ],
    "bars":[
        {
            "series":"",
            "x":"",
            "value":0.0
        }
    ],
    "confidence":0.0
}

Requirements:

- Read EVERY X-axis label.
- Read EVERY Y-axis tick.
- Detect EVERY legend entry.
- Digitize EVERY bar.
- Calculate the numerical value of EVERY bar using the Y-axis.
- Do NOT skip bars.
- Do NOT merge series.
- If there are two bars for one category, return two entries.

Accuracy is more important than speed.
"""

        response = client.responses.create(
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
                            "image_url": f"data:image/png;base64,{image}"
                        }
                    ]
                }
            ]
        )

        text = response.output_text.strip()

        try:
            return json.loads(text)

        except Exception:

            schema = empty_chart_schema()
            schema["raw_extraction"] = {
                "response": text
            }

            return schema
