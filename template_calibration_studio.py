import streamlit as st
from PIL import Image


class TemplateCalibrationStudio:

    def show(self, page_template):

        st.markdown("## 🛠 Template Calibration Studio")

        top_left, top_right = st.columns([3, 2])

        ###################################################
        # LEFT
        ###################################################

        with top_left:

            st.markdown("### PDF Page")

            image = Image.open(page_template["grid_preview"])

            st.image(
                image,
                use_container_width=True
            )

        ###################################################
        # RIGHT
        ###################################################

        with top_right:

            st.markdown("### Selected Panel")

            selected = st.selectbox(

                "Choose Panel",

                [c["chart_id"] for c in page_template["charts"]]

            )

            chart = next(

                c for c in page_template["charts"]

                if c["chart_id"] == selected

            )

            st.markdown("### Coordinates")

            st.json(chart["expected_bbox"])

            st.markdown("---")

            st.info("Crop Preview Coming Next")

        ###################################################
        # Bottom
        ###################################################

        st.markdown("---")

        left, middle, right = st.columns([1,2,1])

        with left:

            st.button("⬅ Previous")

        with middle:

            st.button(
                "✅ Approve Layout",
                use_container_width=True
            )

        with right:

            st.button("Next ➡")

        return page_template
