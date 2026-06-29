from openai import OpenAI
import json
import base64


class ChartUnderstandingAgent:

    def __init__(self, api_key):

        self.client = OpenAI(api_key=api_key)

    def process(self, chart_image):

        prompt = """
You are an expert manufacturing dashboard analyst.

Your job is NOT to extract numerical values.

Your job is only to understand the chart.

Return ONLY valid JSON.

Return ONLY valid JSON.

{
    "chart_title": "",
    "chart_type": "",
    "chart_subtype": "",

    "x_axis": {
        "type": "",
        "labels": []
    },

    "y_axis": {
        "title": "",
        "unit": ""
    },

    "legend": [],

    "series_count": 0,

    "confidence": {

        "chart_title": 0,

        "chart_type": 0,

        "x_axis": 0,

        "y_axis": 0,

        "legend": 0,
    
        "overall": 0

    },

    "reasoning": {

        "chart_title": "",

        "chart_type": "",

        "x_axis": "",

        "y_axis": "",

        "legend": ""

    },

    "observations": []
}
Rules:

1. Do not guess numbers.

2. Detect the chart title.

3. Identify chart type
   Examples:
   - Bar
   - Line
   - Stacked Bar
   - Bar + Line
   - Area
   - Scatter



5. Detect legends.

6. Detect X axis meaning
   Weekly
   Monthly
   Daily
   Shift
   Category

7. Detect Y axis unit.

8. Mention important observations.
9. Estimate confidence between 0 and 100.

10. Explain WHY you selected the chart type.

11. Explain WHY you detected each legend.

12. Never invent labels.

13. If uncertain, write "Unknown".

14. Return JSON only.
Before producing JSON, analyse the chart in this order:

1. Read the chart title.

2. Determine the chart type.

3. Identify every legend.

4. Read every X axis label.

5. Read the Y axis title.

6. Read the Y axis unit.

7. Estimate confidence for every section.

8. Return valid JSON only.


"""

        

        with open(chart_image, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode("utf-8")

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
        text = response.output_text
        print("=" * 80)
        print("CHART UNDERSTANDING")
        print("=" * 80)
        print(text)
        print("=" * 80)

        understanding = json.loads(text)

        understanding["agent"] = "ChartUnderstandingAgent"

        understanding["version"] = "1.0"

        return understanding

        
