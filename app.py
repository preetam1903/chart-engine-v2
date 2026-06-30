import os
import tempfile
import streamlit as st

st.error("APP VERSION 999")
st.write(__file__)
st.write(os.getcwd())

from pipeline import ChartExtractionPipeline


st.set_page_config(

    page_title="Executive Chart Intelligence",

    layout="wide"

)

st.title(

    "📊 Executive Chart Intelligence Repository"

)

st.markdown("---")

##############################################################
# Sidebar
##############################################################

st.sidebar.header("Configuration")



page_number = st.sidebar.number_input(

    "PDF Page Number",

    min_value=0,

    value=0,

    step=1

)
##############################################################
# Charts Per Page
##############################################################

charts_per_page = st.sidebar.selectbox(

    "Charts Per Page",

    options=[4, 6, 8, 9, 12, 16],

    index=0,

    help="Select the expected number of charts on this page."

)

uploaded_pdf = st.file_uploader(

    "Upload Executive PDF Report",

    type=["pdf"]

)

run_button = st.button(

    "🚀 Build Repository",

    use_container_width=True

)
##############################################################
# Run Pipeline
##############################################################

if run_button:

    if uploaded_pdf is None:

        st.error(

            "Please upload a PDF."

        )

        st.stop()

 

    #
    # Save uploaded PDF
    #

    temp_dir = tempfile.mkdtemp()

    pdf_path = os.path.join(

        temp_dir,

        uploaded_pdf.name

    )

    with open(

            pdf_path,

            "wb"

    ) as f:

        f.write(

            uploaded_pdf.read()

        )

    output_folder = os.path.join(

        temp_dir,

        "repository"

    )

    #
    # Execute Pipeline
    #

    with st.spinner(

            "Running AI Agents..."

    ):

        pipeline = ChartExtractionPipeline(

            st.secrets["OPENAI_API_KEY"]

        )

        results = pipeline.process(

            pdf_path=pdf_path,

            page_number=page_number,
            charts_per_page=charts_per_page,

            output_folder=output_folder

        )

        ##############################################################
# Chart Understanding
##############################################################

        if "understanding" in st.session_state:

            st.markdown("---")
            st.subheader("Chart Understanding")

            st.json(
                st.session_state["understanding"]
            )

        ##############################################################
# Grid Preview
##############################################################

        if "grid_preview" in results:

            st.subheader(

                "Expected Grid Layout"

            )

            st.image(

                results["grid_preview"],

                use_container_width=True

            )

    st.success(

        "Repository Created Successfully."

    )

##############################################################
# Display Executive Chart Repository
##############################################################

    repository = results["repository"]

    st.subheader(

        "Executive Chart Repository"

    )

    st.dataframe(

        repository,

        use_container_width=True,

        hide_index=True

    )

##############################################################
# Download Repository
##############################################################

    csv_path = os.path.join(

        output_folder,

        "chart_inventory.csv"

    )

    with open(

            csv_path,

            "rb"

    ) as f:

        st.download_button(

            "Download Repository CSV",

            data=f,

            file_name="chart_inventory.csv",

            mime="text/csv"

        )

##############################################################
# Chart Details
##############################################################

    st.markdown("---")

    st.subheader(

        "Chart Details"

    )

    for row in results["rows"]:

        with st.expander(

                f'{row["chart_id"]} - {row["chart_title"]}',

                expanded=False

        ):

            chart_folder = os.path.join(

                output_folder,

                row["chart_id"]

            )

            image_path = os.path.join(

                chart_folder,

                "chart.png"

            )

            if os.path.exists(image_path):

                st.image(

                    image_path,

                    use_container_width=True

                )

            col1, col2 = st.columns(2)

            with col1:

                st.write(

                    "### Summary"

                )

                st.write(

                    f'**Position:** {row["position"]}'

                )

                st.write(

                    f'**Chart Type:** {row["chart_type"]}'

                )

                st.write(

                    f'**X Axis:** {row["x_axis"]}'

                )

                st.write(

                    f'**Left Y:** {row["left_y"]}'

                )

                st.write(

                    f'**Right Y:** {row["right_y"]}'

                )

                st.write(

                    f'**Legends:** {row["legends"]}'

                )

            with col2:

                st.write(

                    "### Validation"

                )

                st.metric(

                    "Status",

                    row["status"]

                )

                st.metric(

                    "Confidence",

                    f'{row["confidence"]}%'

                )

                st.write(

                    "**Warnings**"

                )

                st.info(

                    row["warnings"] if row["warnings"] else "None"

                )

                st.write(

                    "**Errors**"

                )

                st.error(

                    row["errors"] if row["errors"] else "None"

                )

                st.write(

                    "**Missing Information**"

                )

                st.warning(

                    row["missing_information"] if row["missing_information"] else "None"

                )

##############################################################
# Footer
##############################################################

    st.markdown("---")

    st.success(

        "Executive Chart Intelligence Repository created successfully."

    )
