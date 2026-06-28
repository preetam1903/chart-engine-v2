import os
import json
import fitz

from PIL import Image


class PageTemplateAgent:

    ##############################################################
    # Constructor
    ##############################################################

    def __init__(self):

        pass

    ##############################################################
    # Render PDF Page
    ##############################################################

    def render_page(

            self,

            pdf_path,

            page_number,

            output_folder

    ):

        os.makedirs(

            output_folder,

            exist_ok=True

        )

        document = fitz.open(

            pdf_path

        )

        page = document.load_page(

            page_number

        )

        #
        # High Resolution Rendering
        #

        matrix = fitz.Matrix(

            3,

            3

        )

        pix = page.get_pixmap(

            matrix=matrix,

            alpha=False

        )

        image_path = os.path.join(

            output_folder,

            f"page_{page_number+1}.png"

        )

        pix.save(

            image_path

        )

        document.close()

        return image_path

    ##############################################################
    # Read Page Size
    ##############################################################

    def get_page_size(

            self,

            image_path

    ):

        image = Image.open(

            image_path

        )

        width, height = image.size

        return {

            "page_width": width,

            "page_height": height

        }

        ##############################################################
    # Estimate Page Layout
    ##############################################################

    def estimate_layout(

            self,

            page_info,

            charts_per_page

    ):

        page_width = page_info["page_width"]
        page_height = page_info["page_height"]

        #
        # Executive reports usually have:
        # Header  = ~8%
        # Footer  = ~6%
        #

        header_height = int(

            page_height * 0.08

        )

        footer_height = int(

            page_height * 0.06

        )

        #
        # Usable Area
        #

        usable_top = header_height

        usable_bottom = page_height - footer_height

        usable_height = usable_bottom - usable_top

        ##########################################################
        # Determine Grid
        ##########################################################

        if charts_per_page == 4:

            rows = 1
            columns = 4

        elif charts_per_page == 6:

            rows = 2
            columns = 3

        elif charts_per_page == 8:

            rows = 2
            columns = 4

        elif charts_per_page == 9:

            rows = 3
            columns = 3

        elif charts_per_page == 12:

            rows = 3
            columns = 4

        elif charts_per_page == 16:

            rows = 4
            columns = 4

        else:

            raise Exception(

                f"Unsupported charts_per_page : {charts_per_page}"

            )

        ##########################################################
        # Cell Size
        ##########################################################

        cell_width = page_width / columns

        cell_height = usable_height / rows

        ##########################################################

        return {

            "page_width": page_width,

            "page_height": page_height,

            "header_height": header_height,

            "footer_height": footer_height,

            "usable_top": usable_top,

            "usable_bottom": usable_bottom,

            "usable_height": usable_height,

            "charts_per_page": charts_per_page,

            "rows": rows,

            "columns": columns,

            "cell_width": cell_width,

            "cell_height": cell_height

        }

        ##############################################################
    # Generate Expected Chart Grid
    ##############################################################

    def generate_grid(

            self,

            layout

    ):

        charts = []

        chart_no = 1

        margin_x = 25
        margin_y = 25

        for row in range(layout["rows"]):

            for column in range(layout["columns"]):

                left = int(column * layout["cell_width"]) + margin_x

                top = int(layout["usable_top"] + row * layout["cell_height"]) + margin_y

                right = int((column + 1) * layout["cell_width"]) - margin_x

                bottom = int(layout["usable_top"] + (row + 1) * layout["cell_height"]) - margin_y

                center_x = int((left + right) / 2)

                center_y = int((top + bottom) / 2)

                charts.append(

                    {

                        "chart_id": f"CH{chart_no:03}",

                        "position": f"R{row+1}C{column+1}",

                        "grid": {

                            "row": row + 1,

                            "column": column + 1

                        },

                        "expected_bbox": {

                            "left": left,

                            "top": top,

                            "right": right,

                            "bottom": bottom

                        },

                        "center": {

                            "x": center_x,

                            "y": center_y

                        }

                    }

                )

                chart_no += 1

        return charts

        ##############################################################
    # Save Template JSON
    ##############################################################

    def save_json(

            self,

            result,

            output_file

    ):

        os.makedirs(

            os.path.dirname(output_file),

            exist_ok=True

        )

        with open(

                output_file,

                "w",

                encoding="utf-8"

        ) as f:

            json.dump(

                result,

                f,

                indent=4,

                ensure_ascii=False

            )

        return output_file

    ##############################################################
    # Process Complete Page
    ##############################################################

    def process(

            self,

            pdf_path,

            page_number,

            charts_per_page,

            output_folder

    ):

        ##########################################################
        # Step 1 : Render Page
        ##########################################################

        image_path = self.render_page(

            pdf_path,

            page_number,

            output_folder

        )

        ##########################################################
        # Step 2 : Page Size
        ##########################################################

        page_info = self.get_page_size(

            image_path

        )

        ##########################################################
        # Step 3 : Layout
        ##########################################################

        layout = self.estimate_layout(

            page_info,

            charts_per_page

        )

        ##########################################################
        # Step 4 : Generate Expected Grid
        ##########################################################

        charts = self.generate_grid(

            layout

        )

        ##########################################################
        # Final Object
        ##########################################################

        result = {

            "page_info": page_info,

            "layout": layout,

            "page_image": image_path,

            "charts": charts

        }

        ##########################################################
        # Save JSON
        ##########################################################

        self.save_json(

            result,

            os.path.join(

                output_folder,

                "page_template.json"

            )

        )

        return result
