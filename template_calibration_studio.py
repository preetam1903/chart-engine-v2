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
            st.markdown("### Selected Panel")

            st.success(chart["chart_id"])


# ---------------------------------
# Crop Preview
# ---------------------------------

            st.markdown("### Crop Preview")

            page = Image.open(page_template["page_image"])

            bbox = chart["expected_bbox"]

            crop_image = page.crop((
                bbox["left"],
                bbox["top"],
                bbox["right"],
                bbox["bottom"]
            ))

            st.image(
                crop_image,
                use_container_width=True
            )

            st.markdown("---")


# ---------------------------------
# Panel Information
# ---------------------------------

            bbox = chart["expected_bbox"]

            width = bbox["right"] - bbox["left"]
            height = bbox["bottom"] - bbox["top"]

            st.markdown("### Panel Information")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Width", width)

            with col2:
                st.metric("Height", height)

            st.write(f"**Position:** {chart['position']}")

            st.success("🟢 Ready for Calibration")


            

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
