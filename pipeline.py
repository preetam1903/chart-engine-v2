import os
import json
import streamlit as st

from header_agent import HeaderAgent
#from layout_agent import LayoutAgent
from x_axis_agent import XAxisAgent
from chart_agent import ChartAgent
from validation_agent import ValidationAgent
import shutil
from page_template_agent import PageTemplateAgent

from grid_preview_agent import GridPreviewAgent
from chart_crop_agent import ChartCropAgent
from template_calibration_studio import TemplateCalibrationStudio
from chart_understanding_agent import ChartUnderstandingAgent


class ChartExtractionPipeline:

    ##############################################################
    # Constructor
    ##############################################################

    def __init__(

            self,

            api_key

    ):

        self.header_agent = HeaderAgent(api_key)
        self.template_calibration = TemplateCalibrationStudio()

        self.page_template_agent = PageTemplateAgent()

        self.grid_preview_agent = GridPreviewAgent()
        self.chart_crop_agent = ChartCropAgent()

        self.xaxis_agent = XAxisAgent(api_key)

        self.chart_agent = ChartAgent(api_key)
        self.chart_understanding_agent = ChartUnderstandingAgent(
            api_key
        )

        self.validation_agent = ValidationAgent()

    ##############################################################
    # Main Process
    ##############################################################

    def process(

            self,

            pdf_path,

            page_number,
            charts_per_page,

            output_folder

    ):

        os.makedirs(

            output_folder,

            exist_ok=True

        )

        repository_rows = []

        #
        # STEP 1
        # Header Agent
        #
        header = {"charts": []}

        #header = self.header_agent.extract(

            #pdf_path,

            #page_number

        #)

 ##############################################################
# STEP 2
# Page Template Agent
##############################################################

        page_template = self.page_template_agent.process(

            pdf_path=pdf_path,

            page_number=page_number,

            charts_per_page=charts_per_page,

            output_folder=output_folder

        )

        

##############################################################
# STEP 3.1
# Grid Preview
##############################################################

        preview_image = self.grid_preview_agent.process(
            page_template,
            output_folder
        )
        page_template["grid_preview"] = preview_image
        
        st.warning("Reached Calibration Studio")

        # TEMPORARY FOR DEMO

        if not st.session_state.get("calibration_done", False):
            page_template = self.template_calibration.show(page_template)

            if st.session_state.get("run_ai", False):

                st.session_state["run_ai"] = False

                chart_image = st.session_state["selected_chart_path"]

                st.success(f"Processing {chart_image}")

                understanding = self.chart_understanding_agent.process(chart_image)
                values = self.chart_understanding_agent.extract_series_values(
                    chart_image
                )

                st.subheader("Extracted Numerical Values")

                st.json(values)
                st.session_state["understanding"] = understanding

                st.json(understanding)

                st.stop()
        else:
            st.success("Calibration Completed")


        st.success("Calibration Completed (Demo Mode)")
        
        if st.session_state.get("run_ai", False):

            st.session_state["run_ai"] = False

            chart_image = st.session_state["selected_chart_path"]

            st.success("Processing CH001")

            understanding = self.chart_understanding_agent.process(
                chart_image
            )

            st.json(understanding)

            st.stop()
        

##############################################################
# STEP 4
# Crop Charts
##############################################################

        page_template = self.chart_crop_agent.process(

            page_template,

            output_folder

        )

        ##############################################################
# STEP 4.1
# Process CH001
##############################################################

        chart_image = page_template["charts"][0]["image"]

        print("=" * 80)
        print("STARTING CHART UNDERSTANDING")
        print(chart_image)
        print("=" * 80)

        try:

            understanding = self.chart_understanding_agent.process(
                chart_image
            )

            print("SUCCESS")

        except Exception as e:

            print("FAILED")
            print(type(e))
            print(e)

            raise

        page_template["charts"][0]["understanding"] = understanding

        

        print("=" * 80)
        print("CH001 UNDERSTANDING")
        print("=" * 80)
        print(json.dumps(understanding, indent=4))
        print("=" * 80)


        
                ##############################################################
        # STEP 3
        # Process Every Cropped Chart
        ##############################################################

        charts = page_template["charts"]

        for i, layout_chart in enumerate(charts):

            image_path = layout_chart["image"]

            #
            # Header information for this chart
            #

            header_chart = {}

            if (

                "charts" in header

                and

                i < len(header["charts"])

            ):

                header_chart = header["charts"][i]

            ##########################################################
            # X Axis Agent
            ##########################################################

            x_axis = self.xaxis_agent.extract(

                image_path

            )

            ##########################################################
            # Chart Agent
            ##########################################################

            chart = self.chart_agent.extract(

                image_path

            )

            ##########################################################
            # Validation
            ##########################################################

            validation = self.validation_agent.validate(

                header_chart,

                layout_chart,

                x_axis,

                chart

            )

            ##########################################################
            # Repository Row
            ##########################################################

            row = self.validation_agent.build_repository_row(

                chart_id=layout_chart["chart_id"],

                position=layout_chart["position"],

                header_chart=header_chart,

                x_axis=x_axis,

                chart=chart,

                validation=validation

            )

            repository_rows.append(row)
                ##############################################################
        # STEP 4
        # Save Individual JSON Files
        ##############################################################

            chart_folder = os.path.join(

                output_folder,

                layout_chart["chart_id"]

            )

            os.makedirs(

                chart_folder,

                exist_ok=True

            )
            

            shutil.copy(

                image_path,

                os.path.join(

                    chart_folder,

                    "chart.png"

                )

            )

            self.xaxis_agent.save_json(

                x_axis,

                os.path.join(

                    chart_folder,

                    "x_axis.json"

                )

            )

            self.chart_agent.save_json(

                chart,

                os.path.join(

                    chart_folder,

                    "chart.json"

                )

            )

            self.validation_agent.save_json(

                validation,

                os.path.join(

                    chart_folder,

                    "validation.json"

                )

            )

        ##############################################################
        # STEP 5
        # Save Header & Layout
        ##############################################################

        self.header_agent.save_json(

            header,

            os.path.join(

                output_folder,

                "header.json"

            )

        )

       

        ##############################################################
        # STEP 6
        # Build Executive Chart Repository
        ##############################################################

        repository = self.validation_agent.build_repository(

            repository_rows

        )

        ##############################################################
        # STEP 7
        # Save Repository CSV
        ##############################################################

        self.validation_agent.save_repository(

            repository,

            output_folder

        )

        ##############################################################
        # STEP 8
        # Return Everything
        ##############################################################

        return {

            "header": header,

            "page_template": page_template,

            "grid_preview": preview_image,

            "repository": repository,

            "rows": repository_rows

        }
