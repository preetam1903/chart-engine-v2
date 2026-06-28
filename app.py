import os
import tempfile
import streamlit as st

from chart_engine import ChartEngine

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

    engine = ChartEngine()

    with st.spinner("Understanding Chart..."):

        result = engine.understand_chart(image_path)

    st.subheader("Extracted JSON")

    st.json(result)

    os.remove(image_path)
