import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import base64


class TemplateCalibrationStudio:

    def show(self, page_template):

        st.markdown("## 🛠 Template Calibration Studio")

        top_left, top_right = st.columns([3, 2])

        ###################################################
        # LEFT
        ###################################################

        with top_left:

            st.markdown("### PDF Page")

            st.info("Interactive calibration canvas is shown below.")

        ###################################################
        # RIGHT
        ###################################################

        with top_right:

            st.markdown("### Selected Panel")

            selected = st.selectbox(

                "Choose Chart",

                [c["chart_id"] for c in page_template["charts"]]

            )

            chart = next(

                c for c in page_template["charts"]

                if c["chart_id"] == selected

            )
            st.markdown("### Selected Panel")

            st.success(

                f"{chart['chart_id']}   |   {chart['position']}"

            )

            st.markdown("### AI Understanding")

            st.info("Chart Title : Detecting...")

            st.info("Chart Type : Detecting...")

            st.info("Business Area : Detecting...")

            st.info("Confidence : 98%")


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

        st.markdown("---")
        st.subheader("🧪 Calibration Canvas Prototype")
        
        

        ##############################################################
# Load Original PDF Page
##############################################################

        with open(page_template["page_image"], "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode()


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


##############################################################
# Scale
##############################################################

        scale_x = DISPLAY_WIDTH / PAGE_WIDTH
        scale_y = DISPLAY_HEIGHT / PAGE_HEIGHT


##############################################################
# Draw Boxes
##############################################################

        html_boxes = ""

        for chart in page_template["charts"]:

            bbox = chart["expected_bbox"]

            left = int(bbox["left"] * scale_x)
            top = int(bbox["top"] * scale_y)

            width = int((bbox["right"] - bbox["left"]) * scale_x)
            height = int((bbox["bottom"] - bbox["top"]) * scale_y)

            html_boxes += f"""
            <div
            class="chartBox"
            id="{chart['chart_id']}"
            style="
            position:absolute;
            left:{left}px;
            top:{top}px;
            width:{width}px;
            height:{height}px;
            border:3px solid #00aa00;
            background:rgba(0,255,0,0.08);
            box-sizing:border-box;
            cursor:move;
            user-select:none;
            ">

            <div style="
            background:#00aa00;
            color:white;
            padding:4px;
            font-family:Arial;
            font-size:12px;
            font-weight:bold;
            ">

            {chart['chart_id']}

            </div>

            </div>
            """

        html = """
        <div style="
        width:1500px;
        height:1060px;
        border:2px solid green;
        position:relative;

        background-image:url('data:image/png;base64,IMAGE_PLACEHOLDER');
        background-size:1500px 1060px;
        background-repeat:no-repeat;
        background-position:center;
        ">

        BOXES_HERE

        <script>

        let activeBox = null;
        let offsetX = 0;
        let offsetY = 0;

        document.querySelectorAll(".chartBox").forEach(function(box){

            box.addEventListener("mousedown", function(e){

                activeBox = box;

                offsetX = e.offsetX;
                offsetY = e.offsetY;

            });

        });

        document.addEventListener("mousemove", function(e){

            if(activeBox == null)
                return;

            const parent = activeBox.parentElement.getBoundingClientRect();

            let newLeft = e.clientX - parent.left - offsetX;
            let newTop = e.clientY - parent.top - offsetY;

            newLeft = Math.max(0, newLeft);
            newTop = Math.max(0, newTop);

            activeBox.style.left = newLeft + "px";
            activeBox.style.top = newTop + "px";

        });

        document.addEventListener("mouseup", function(){

            activeBox = null;

        });

        </script>

        </div>
        """

        html = html.replace(
            "IMAGE_PLACEHOLDER",
            img_base64
        )

        html = html.replace(
            "BOXES_HERE",
            html_boxes
        )

        components.html(
            html,
            height=1100,
            scrolling=False
        )

        return page_template
