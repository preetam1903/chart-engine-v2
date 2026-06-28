import os
import tempfile
import json
import streamlit as st

from chart_engine import ChartEngine
from axis_reader import AxisReader
from axis_validator import AxisValidator
from image_preprocessor import ImagePreprocessor

st.set_page_config(page_title="Chart Engine V2")

st.title("📊 Chart Engine V2")

uploaded = st.file_uploader(
    "Upload Cropped Chart",
    type=["png", "jpg", "jpeg"]
)

if uploaded:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(uploaded.read())
        image_path = tmp.name

    # -------------------------------------------------
    # Original Image
    # -------------------------------------------------

    st.subheader("Original Chart")

    st.image(image_path, width="stretch")

    # -------------------------------------------------
    # X Axis OCR
    # -------------------------------------------------

    axis = AxisReader()

    crop, ocr = axis.read_x_axis(image_path)

    st.subheader("X Axis Crop")

    st.image(crop, width="stretch")

    st.subheader("OCR Output")

    st.code(ocr)

    try:

        ocr_json = json.loads(ocr)

        validator = AxisValidator()

        corrected = validator.validate(ocr_json["labels"])

        st.subheader("Validated Labels")

        st.json(corrected)

    except Exception:

        st.error("OCR JSON could not be parsed.")

    # -------------------------------------------------
    # Image Enhancement
    # -------------------------------------------------

    processor = ImagePreprocessor()

    enhanced_image = processor.enhance(image_path)

    st.subheader("Enhanced Chart")

    st.image(enhanced_image, width="stretch")

    # -------------------------------------------------
    # Chart Digitization
    # -------------------------------------------------

    engine = ChartEngine()

    with st.spinner("Digitizing chart..."):

        result = engine.understand_chart(enhanced_image)

    st.subheader("Extracted JSON")

    st.json(result)

    # -------------------------------------------------

    os.remove(image_path)

    if os.path.exists(enhanced_image):
        os.remove(enhanced_image)
