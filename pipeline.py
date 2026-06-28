import os

from header_agent import HeaderAgent
#from layout_agent import LayoutAgent
from x_axis_agent import XAxisAgent
from chart_agent import ChartAgent
from validation_agent import ValidationAgent
import shutil
from page_template_agent import PageTemplateAgent

from grid_preview_agent import GridPreviewAgent


class ChartExtractionPipeline:

    ##############################################################
    # Constructor
    ##############################################################

    def __init__(

            self,

            api_key

    ):

        self.header_agent = HeaderAgent(api_key)

        self.page_template_agent = PageTemplateAgent()

        self.grid_preview_agent = GridPreviewAgent()

        self.xaxis_agent = XAxisAgent(api_key)

        self.chart_agent = ChartAgent(api_key)

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

        header = self.header_agent.extract(

            pdf_path,

            page_number

        )

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
