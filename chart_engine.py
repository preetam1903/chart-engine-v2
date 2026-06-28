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
You are an Executive Chart Intelligence Engine.

Your job is NOT to describe the chart.

Your job is to DIGITIZE the chart and convert it into structured business data.

Return ONLY valid JSON.

Never return markdown.

Never explain your reasoning.

----------------------------------------------------
DOCUMENT INFORMATION
----------------------------------------------------

Extract if visible:

- report_name
- page_number
- page_title
- section
- sub_section
- business_unit
- plant
- report_date

----------------------------------------------------
CHART INFORMATION
----------------------------------------------------

Extract:

- chart_title
- chart_subtitle
- chart_type

Possible chart types:

grouped_bar
stacked_bar
bar_line_combo
line
area
scatter
pie
waterfall
pareto

Determine:

- orientation
- unit

----------------------------------------------------
AXES
----------------------------------------------------

Extract:

X Axis

- label
- every category

Y Axis

- label
- every tick

----------------------------------------------------
LEGEND
----------------------------------------------------

Extract every legend item.

For every legend return

{
    "name":"",
    "render_type":"bar"
}

render_type can be

bar
line
area

----------------------------------------------------
SERIES
----------------------------------------------------

For every legend entry return

{
    "name":"",
    "render_type":"",
    "values":[]
}

----------------------------------------------------
DATA POINTS
----------------------------------------------------

For every plotted value return

{
    "series":"",
    "category":"",
    "value":0.0,
    "render_type":""
}

----------------------------------------------------
QUALITY
----------------------------------------------------

Return

confidence

----------------------------------------------------

Return EXACTLY this JSON

{

"document":{

"report_name":"",
"page_number":null,
"page_title":"",
"section":"",
"sub_section":"",
"business_unit":"",
"plant":"",
"report_date":""

},

"chart":{

"chart_title":"",
"chart_subtitle":"",
"chart_type":"",
"orientation":"",
"unit":"",
"confidence":0.0

},

"axes":{

"x":{

"label":"",
"values":[]

},

"y":{

"label":"",
"ticks":[]

}

},

"legend":[],

"series":[],

"data_points":[],

"confidence":0.0

}
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
