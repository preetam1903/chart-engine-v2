import os
import tempfile
import streamlit as st


from chart_engine import ChartEngine
from axis_reader import AxisReader
from axis_validator import AxisValidator
import json
from bar_value_extractor import BarValueExtractor

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

    st.image(image_path, use_container_width=True)
    axis = AxisReader()

    crop, ocr = axis.read_x_axis(image_path)

    st.subheader("X Axis Crop")

    st.image(crop, use_container_width=True)

    st.subheader("OCR Output")

    st.code(ocr)
    ocr_json = json.loads(ocr)

    validator = AxisValidator()

    corrected = validator.validate(ocr_json["labels"])

    st.subheader("Validated Labels")

    st.json(corrected)

    engine = ChartEngine()

    with st.spinner("Understanding Chart..."):

        result = engine.understand_chart(image_path)

    st.subheader("Extracted JSON")

    st.json(result)
        
    # -------------------------------
    # Bar Detection
    # -------------------------------

    extractor = BarValueExtractor()

    img, bars = extractor.detect_bars(image_path)
    st.write(f"Bars detected: {len(bars)}")

    st.subheader("Detected Bars")

    debug = img.copy()

    

    for i, bar in enumerate(bars):

        x = bar["x"]
        top = bar["top"]
        bottom = bar["bottom"]

        cv2.line(
            debug,
            (x, top),
            (x, bottom),
            (0, 255, 0),
            2
        )

        cv2.putText(
            debug,
            str(i + 1),
            (x - 4, top - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (0, 0, 255),
            1
        )

    st.image(
        cv2.cvtColor(debug, cv2.COLOR_BGR2RGB),
        use_container_width=True
    )

    st.json(bars)

    

    os.remove(image_path)
