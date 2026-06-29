import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas


class TemplateCalibrationStudio:

    def show(self, page_template):

        st.subheader("🛠 Template Calibration Studio")

        image = Image.open(page_template["page_image"])

        canvas_result = st_canvas(

            fill_color="rgba(0,255,0,0.2)",

            stroke_width=2,

            stroke_color="#00ff00",

            background_image=image,

            update_streamlit=True,

            drawing_mode="rect",

            height=image.height,

            width=image.width,

            key="template_canvas"

        )

        return page_template
