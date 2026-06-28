import os

from PIL import Image


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

            chart,

            output_folder,

            padding_left=20,

            padding_top=50,

            padding_right=20,

            padding_bottom=30

    ):

        width, height = page_image.size

        bbox = chart["expected_bbox"]

        ##########################################################
        # Expand Expected Box
        ##########################################################

        left = max(

            0,

            bbox["left"] - padding_left

        )

        top = max(

            0,

            bbox["top"] - padding_top

        )

        right = min(

            width,

            bbox["right"] + padding_right

        )

        bottom = min(

            height,

            bbox["bottom"] + padding_bottom

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

        return page_template
