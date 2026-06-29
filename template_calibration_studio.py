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
        
        

        with open(page_template["grid_preview"], "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode()
        html = f"""
<div style="
width:100%;
height:900px;
border:2px solid green;
position:relative;

background-image:url('data:image/png;base64,{img_base64}');
background-size:contain;
background-repeat:no-repeat;
background-position:center;
">

<div
id="box1"
style="
position:absolute;
left:80px;
top:80px;
width:220px;
height:280px;
border:3px solid green;
background:rgba(0,255,0,0.08);
cursor:move;
user-select:none;
">

CH001

</div>

<div
style="
position:absolute;
left:350px;
top:80px;
width:220px;
height:280px;
border:3px solid green;
background:rgba(0,255,0,0.08);
">

CH002

</div>

<script>

const box=document.getElementById("box1");

let active=false;
let offsetX=0;
let offsetY=0;

box.onmousedown=function(e){

    active=true;

    offsetX=e.offsetX;

    offsetY=e.offsetY;

}

document.onmousemove=function(e){

    if(!active) return;

    box.style.left=(e.pageX-offsetX)+"px";

    box.style.top=(e.pageY-offsetY)+"px";

}

document.onmouseup=function(){

    active=false;

}

</script>

</div>
"""

        components.html(
            html,
            height=520,
            scrolling=False
        )

        return page_template
