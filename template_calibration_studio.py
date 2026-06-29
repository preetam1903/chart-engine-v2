import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import base64
import json
import os


class TemplateCalibrationStudio:

    def __init__(self):

        self.selected_chart = None

    ##############################################################
    # Main Screen
    ##############################################################

    def show(
            self,
            page_template
    ):

        st.markdown("# 🛠 Template Calibration Studio")

        ##############################################################
        # Chart Selector
        ##############################################################

        chart_ids = [

            c["chart_id"]

            for c in page_template["charts"]

        ]

        selected_chart = st.selectbox(

            "Select Chart",

            chart_ids,

            index=0

        )

        chart = next(

            c

            for c in page_template["charts"]

            if c["chart_id"] == selected_chart

        )

        self.selected_chart = chart

        ##############################################################
        # Layout
        ##############################################################

        left, right = st.columns([3,2])

        ##############################################################
        # LEFT PANEL
        ##############################################################

        with left:

            st.subheader("PDF Page")

            st.info(
                "Move the green boxes if required."
            )

        ##############################################################
        # RIGHT PANEL
        ##############################################################

        with right:

            st.subheader("Selected Chart")

            st.success(

                f"{chart['chart_id']}   |   {chart['position']}"

            )

            ##########################################################
            # Crop Preview
            ##########################################################

            page = Image.open(

                page_template["page_image"]

            )

            bbox = chart["expected_bbox"]

            crop = page.crop(

                (

                    bbox["left"],

                    bbox["top"],

                    bbox["right"],

                    bbox["bottom"]

                )

            )

            st.image(

                crop,

                use_container_width=True

            )

            ##########################################################
            # Panel Details
            ##########################################################

            st.markdown("---")

            width = bbox["right"] - bbox["left"]

            height = bbox["bottom"] - bbox["top"]

            c1, c2 = st.columns(2)

            with c1:

                st.metric(

                    "Width",

                    width

                )

            with c2:

                st.metric(

                    "Height",

                    height

                )

            st.write(

                f"Position : {chart['position']}"

            )

            st.success(

                "Ready"
            )

            ##########################################################
            # PROCESS BUTTON
            ##########################################################

            st.markdown("---")

            process = st.button(

                "🚀 Process Selected Chart",

                use_container_width=True,

                type="primary"

            )

            if process:

                st.success(

                    "Processing Started..."
                )

                st.info(

                    "Chart Understanding"
                )

                st.info(

                    "X Axis Validation"
                )

                st.info(

                    "Y Value Extraction"
                )

                st.info(

                    "Repository Update"
                )

                st.info(

                    "Executive Intelligence"
                )

                ######################################################
                # Save Crop
                ######################################################

                temp_folder = os.path.join(

                    os.path.dirname(

                        page_template["page_image"]

                    ),

                    "selected_chart"

                )

                os.makedirs(

                    temp_folder,

                    exist_ok=True

                )

                crop_path = os.path.join(

                    temp_folder,

                    f"{chart['chart_id']}.png"

                )

                crop.save(

                    crop_path

                )

                st.success(

                    f"Saved : {crop_path}"

                )

                ######################################################
                # Store for App
                ######################################################

                st.session_state["selected_chart"] = chart

                st.session_state["selected_chart_path"] = crop_path

                st.session_state["run_ai"] = True

        ##############################################################
        # PART 2 STARTS HERE
        ##############################################################
                ##############################################################
        # Navigation
        ##############################################################

        st.markdown("---")

        c1, c2, c3 = st.columns([1,2,1])

        with c1:
            st.button("⬅ Previous")

        with c2:
            st.button(
                "✅ Approve Layout",
                use_container_width=True
            )

        with c3:
            st.button("Next ➡")

        st.markdown("---")

        st.subheader("Calibration Canvas")

        ##############################################################
        # Load Background Image
        ##############################################################

        with open(page_template["page_image"], "rb") as f:
            img_base64 = base64.b64encode(
                f.read()
            ).decode()

        ##############################################################
        # Display Size
        ##############################################################

        DISPLAY_WIDTH = 1500
        DISPLAY_HEIGHT = 1060

        ##############################################################
        # Original PDF Size
        ##############################################################

        PAGE_WIDTH = page_template["layout"]["page_width"]
        PAGE_HEIGHT = page_template["layout"]["page_height"]

        scale_x = DISPLAY_WIDTH / PAGE_WIDTH
        scale_y = DISPLAY_HEIGHT / PAGE_HEIGHT

        ##############################################################
        # Build HTML Boxes
        ##############################################################

        html_boxes = ""

        for c in page_template["charts"]:

            bbox = c["expected_bbox"]

            left = int(bbox["left"] * scale_x)
            top = int(bbox["top"] * scale_y)

            width = int(
                (bbox["right"] - bbox["left"]) * scale_x
            )

            height = int(
                (bbox["bottom"] - bbox["top"]) * scale_y
            )

            color = "#ff6600" if c["chart_id"] == selected_chart else "#00aa00"

            html_boxes += f"""
            <div class='chartBox'
                style='
                position:absolute;
                left:{left}px;
                top:{top}px;
                width:{width}px;
                height:{height}px;
                border:3px solid {color};
                background:rgba(0,255,0,0.08);
                resize:both;
                overflow:auto;
                cursor:move;
                box-sizing:border-box;'>

                <div style='
                    background:{color};
                    color:white;
                    padding:4px;
                    font-size:12px;
                    font-weight:bold;'>

                    {c["chart_id"]}

                </div>

            </div>
            """

        ##############################################################
        # HTML
        ##############################################################

        html = f"""
        <html>

        <body>

        <div style='
            width:{DISPLAY_WIDTH}px;
            height:{DISPLAY_HEIGHT}px;
            position:relative;
            border:2px solid green;
            background-image:url("data:image/png;base64,{img_base64}");
            background-size:{DISPLAY_WIDTH}px {DISPLAY_HEIGHT}px;
            overflow:hidden;'>

            {html_boxes}

        </div>

        </body>

        </html>
        """

        components.html(

            html,

            height=1100,

            scrolling=True

        )

        ##############################################################
        # Return
        ##############################################################

        return page_template

                
