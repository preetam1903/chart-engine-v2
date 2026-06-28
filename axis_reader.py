from PIL import Image
import base64
from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


class AxisReader:

    def crop_x_axis(self, image_path):

        img = Image.open(image_path)

        w, h = img.size

        # Bottom 20% of image
        crop = img.crop((0, int(h*0.80), w, h))

        return crop

    def read_x_axis(self, image_path):

        crop = self.crop_x_axis(image_path)

        crop.save("temp_axis.png")

        with open("temp_axis.png","rb") as f:
            image = base64.b64encode(f.read()).decode()

        prompt = """
You are an OCR engine.

Read ONLY the x-axis labels.

Return JSON only.

Example:

{
 "labels":[
   "202352",
   "202401",
   "202402"
 ]
}

Do not guess.
Return labels exactly as seen.
"""

        response = client.responses.create(

            model="gpt-4.1",

            input=[{
                "role":"user",
                "content":[
                    {
                        "type":"input_text",
                        "text":prompt
                    },
                    {
                        "type":"input_image",
                        "image_url":f"data:image/png;base64,{image}"
                    }
                ]
            }]
        )

        return crop, response.output_text
