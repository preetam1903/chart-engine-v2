import os

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class GridPreviewAgent:

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
    # Draw Expected Grid
    ##############################################################

    def draw_expected_grid(

            self,

            image,

            page_template

    ):

        draw = ImageDraw.Draw(

            image

        )

        try:

            font = ImageFont.truetype(

                "arial.ttf",

                24

            )

        except:

            font = ImageFont.load_default()

        ##########################################################
        # Draw Every Expected Chart
        ##########################################################

        for chart in page_template["charts"]:

            bbox = chart["expected_bbox"]

            left = bbox["left"]
            top = bbox["top"]
            right = bbox["right"]
            bottom = bbox["bottom"]

            ######################################################
            # Green Rectangle
            ######################################################

            draw.rectangle(

                [

                    (left, top),

                    (right, bottom)

                ],

                outline="green",

                width=4

            )

            ######################################################
            # Chart ID
            ######################################################

            draw.text(

                (

                    left + 8,

                    top + 8

                ),

                chart["chart_id"],

                fill="green",

                font=font

            )

            ######################################################
            # Grid Position
            ######################################################

            draw.text(

                (

                    left + 8,

                    top + 38

                ),

                chart["position"],

                fill="green",

                font=font

            )

            ######################################################
            # Center Point
            ######################################################

            cx = chart["center"]["x"]
            cy = chart["center"]["y"]

            radius = 6

            draw.ellipse(

                [

                    (

                        cx - radius,

                        cy - radius

                    ),

                    (

                        cx + radius,

                        cy + radius

                    )

                ],

                fill="green"

            )

        return image

        ##############################################################
    # Save Preview Image
    ##############################################################

    def save_preview(

            self,

            image,

            output_folder

    ):

        os.makedirs(

            output_folder,

            exist_ok=True

        )

        output_path = os.path.join(

            output_folder,

            "grid_preview.png"

        )

        image.save(

            output_path

        )

        return output_path

    ##############################################################
    # Complete Process
    ##############################################################

    def process(

            self,

            page_template,

            output_folder

    ):

        ##########################################################
        # Load Page Image
        ##########################################################

        image = self.load_page(

            page_template["page_image"]

        )

        ##########################################################
        # Draw Grid
        ##########################################################

        image = self.draw_expected_grid(

            image,

            page_template

        )

        ##########################################################
        # Save
        ##########################################################

        preview_path = self.save_preview(

            image,

            output_folder

        )

        return preview_path
