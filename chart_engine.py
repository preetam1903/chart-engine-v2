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
You are an expert chart understanding engine.

Return ONLY valid JSON.

Extract:

- chart_type
- title
- x axis label
- x axis values
- y axis label
- every data series
- confidence (0-1)

Do not explain anything.
Do not wrap JSON inside markdown.
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
