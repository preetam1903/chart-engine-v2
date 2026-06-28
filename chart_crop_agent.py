import os

from PIL import Image
import json
import streamlit as st



class ChartCropAgent:

    ##############################################################
    # Constructor
    ##############################################################

    def __init__(self):

        pass

    ##############################################################
    # Load Page Image
    ##############################################################

    def load_page(

            self,

            image_path

    ):

        image = Image.open(

            image_path

        )

        image = image.convert(

            "RGB"

        )

        return image

        ##############################################################
    # Crop One Chart
    ##############################################################

    def crop_chart(

            self,

            page_image,
            page_template,

            chart,

            output_folder,

            left_ratio=0.12,

            top_ratio=0.15,

            right_ratio=0.12,

            bottom_ratio=0.3

    ):

        width, height = page_image.size

        layout = page_template["layout"]

        grid = chart["grid"]

        row = grid["row"]
        column = grid["column"]

        cell_width = layout["cell_width"]
        cell_height = layout["cell_height"]

        usable_top = layout["usable_top"]

        left = int((column - 1) * cell_width)
        top = int(usable_top + (row - 1) * cell_height)

        right = int(left + cell_width)
        bottom = int(top + cell_height)

        bbox = {
            "left": left,
            "top": top,
            "right": right,
            "bottom": bottom
        }

       ##########################################################
# Calculate Dynamic Padding
##########################################################

        left = bbox["left"]
        top = bbox["top"]
        right = bbox["right"]
        bottom = bbox["bottom"]

##########################################################
# Expand Expected Box
##########################################################

        left = max(
            0,
            bbox["left"] - left_padding
        )

        top = max(
            0,
            bbox["top"] - top_padding
        )

        right = min(
            width,
            bbox["right"] + right_padding
        )

        bottom = min(
            height,
            bbox["bottom"] + bottom_padding
        )

        ##########################################################
        # Crop
        ##########################################################

        cropped = page_image.crop(

            (

                left,

                top,

                right,

                bottom

            )

        )

        ##########################################################
        # Save
        ##########################################################

        crop_folder = os.path.join(

            output_folder,

            "cropped_charts"

        )
        crop_folder = os.path.join(

            output_folder,

            "grid_cell_crops"

        )

        os.makedirs(

            crop_folder,

            exist_ok=True

        )

        image_path = os.path.join(

            crop_folder,

            f'{chart["chart_id"]}.png'

        )

        cropped.save(

            image_path

        )

        ##########################################################
        # Update Chart Metadata
        ##########################################################

        chart["image"] = image_path

        chart["refined_bbox"] = {

            "left": left,

            "top": top,

            "right": right,

            "bottom": bottom

        }

        chart["crop_width"] = right - left

        chart["crop_height"] = bottom - top

        chart["crop_metadata"] = {

            "left_padding": left_padding,
            "right_padding": right_padding,
            "top_padding": top_padding,
            "bottom_padding": bottom_padding,
            "method": "dynamic_percentage_v1"

        }

        return chart

        ##############################################################
    # Process All Charts
    ##############################################################

    def process(

            self,

            page_template,

            output_folder

    ):

        ##########################################################
        # Load Page
        ##########################################################

        page_image = self.load_page(

            page_template["page_image"]

        )

        ##########################################################
        # Crop Every Chart
        ##########################################################

        updated_charts = []

        for chart in page_template["charts"]:

            updated_chart = self.crop_chart(

                page_image=page_image,
                page_template=page_template,

                chart=chart,

                output_folder=output_folder

            )

            updated_charts.append(

                updated_chart

            )

        ##########################################################
        # Update Template
        ##########################################################

        page_template["charts"] = updated_charts

        st.subheader("Page Template")

        st.json(page_template)
        return page_template
