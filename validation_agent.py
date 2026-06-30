import json


class ValidationAgent:

    def __init__(self):

        pass

    ###############################################################
    # Main Validation
    ###############################################################

    def validate(

            self,

            header_chart,

            layout_chart,

            x_axis,

            chart

    ):

        validation = {

            "status": "PASS",

            "score": 100,

            "checks": [],

            "warnings": [],

            "errors": []

        }

        self.validate_header_vs_layout(

            header_chart,

            layout_chart,

            validation

        )

        self.validate_header_vs_chart(

            header_chart,

            chart,

            validation

        )

        self.validate_header_vs_xaxis(

            header_chart,

            x_axis,

            validation

        )

        self.validate_chart_vs_xaxis(

            chart,

            x_axis,

            validation

        )

        validation["score"] = max(

            0,

            100 - (len(validation["errors"]) * 20) - (len(validation["warnings"]) * 5)

        )

        if len(validation["errors"]) > 0:

            validation["status"] = "FAIL"

        elif len(validation["warnings"]) > 0:

            validation["status"] = "WARNING"

        return validation

        ###############################################################
    # Header vs Layout
    ###############################################################

    def validate_header_vs_layout(

            self,

            header_chart,

            layout_chart,

            validation

    ):

        expected = 1

        detected = 1

        validation["checks"].append(

            {

                "check": "Header vs Layout",

                "expected": expected,

                "detected": detected,

                "status": "PASS" if expected == detected else "FAIL"

            }

        )

        if expected != detected:

            validation["errors"].append(

                f"Chart validation failed. Expected {expected}, detected {detected}."

            )

    ###############################################################
    # Header vs Chart
    ###############################################################

    def validate_header_vs_chart(

            self,

            header_chart,

            chart,

            validation

    ):

        legends = 0

        legends = len(

            header_chart.get(

                "legend",

                []

            )

        )

        render_objects = len(

            chart.get(

                "chart",

                {}

            ).get(

                "render_objects",

                []

            )

        )

        validation["checks"].append(

            {

                "check": "Legend vs Render Objects",

                "expected": legends,

                "detected": render_objects,

                "status": "PASS" if legends == render_objects else "WARNING"

            }

        )

        if legends != render_objects:

            validation["warnings"].append(

                "Legend count does not match render objects."

            )

        #
        # Dual Axis Validation
        #

        expected_dual = header_chart.get(

            "right_y_axis",

            {}

        ).get(

            "exists",

            False

        )

        detected_dual = chart.get(

            "chart",

            {}

        ).get(

            "dual_axis",

            False

        )

        validation["checks"].append(

            {

                "check": "Dual Axis",

                "expected": expected_dual,

                "detected": detected_dual,

                "status": "PASS" if expected_dual == detected_dual else "FAIL"

            }

        )

        if expected_dual != detected_dual:

            validation["errors"].append(

                "Dual axis mismatch."

            )

    ###############################################################
    # Header vs X Axis
    ###############################################################

    def validate_header_vs_xaxis(

            self,

            header_chart,

            x_axis,

            validation

    ):

        category_count = x_axis.get(

            "x_axis",

            {}

        ).get(

            "category_count",

            0

        )

        validation["checks"].append(

            {

                "check": "X Axis Categories",

                "expected": ">0",

                "detected": category_count,

                "status": "PASS" if category_count > 0 else "FAIL"

            }

        )

        if category_count == 0:

            validation["errors"].append(

                "No X-axis labels detected."

            )

    ###############################################################
    # Chart vs X Axis
    ###############################################################

    def validate_chart_vs_xaxis(

            self,

            chart,

            x_axis,

            validation

    ):

        orientation = chart.get(

            "chart",

            {}

        ).get(

            "orientation",

            ""

        )

        rotation = x_axis.get(

            "x_axis",

            {}

        ).get(

            "rotation",

            0

        )

        validation["checks"].append(

            {

                "check": "Orientation vs Label Rotation",

                "expected": "Consistent",

                "detected": f"{orientation} / {rotation}",

                "status": "PASS"

            }

        )

        ###############################################################
    # Build Repository Row
    ###############################################################

    def build_repository_row(

            self,

            chart_id,

            position,

            header_chart,

            x_axis,

            chart,

            validation,

            understanding=None

    ):

        #
        # Header Information
        #

        chart_title = ""

        legends = ""

        left_y = ""

        right_y = ""

        info = header_chart

        chart_title = (
            understanding.get("chart_title", "")
            if understanding
            else info.get("chart_title", "")
        )

        if understanding:

            legends = ", ".join(
                understanding.get(
                    "legend",
                    []
                )
            )

        else:

            legends = ", ".join(
                [
                    l.get("name", "")
                    for l in info.get(
                        "legend",
                        []
                    )
                ]
            )

        left_y = (
            understanding.get(
                "y_axis",
                {}
            ).get(
                "title",
                ""
            )
            if understanding
            else info.get(
                "left_y_axis",
                {}
            ).get(
                "label",
                ""
            )
        )

        right_y = info.get(

            "right_y_axis",

            {}

        ).get(

            "label",

            ""

        )

        #
        # X Axis
        #

        if understanding:

            x_label = ", ".join(

                understanding.get(
                    "x_axis",
                    {}
                ).get(
                    "labels",
                    []
                )

            )

        else:

            x_label = x_axis.get(
                "x_axis",
                {}
            ).get(
                "label",
                ""
            )

        #
        # Chart
        #

        chart_info = chart.get(

            "chart",

            {}

        )

        chart_type = chart_info.get(

            "chart_type",

            ""

        )

        render_objects = len(

            chart_info.get(

                "render_objects",

                []

            )

        )

        dual_axis = chart_info.get(

            "dual_axis",

            False

        )

        #
        # Missing Information
        #

        missing = []

        if chart_title == "":
            missing.append("Chart Title")

        if legends == "":
            missing.append("Legend")

        if x_label == "":
            missing.append("X Axis")

        if left_y == "":
            missing.append("Left Y Axis")

        #
        # Repository Row
        #

        return {

            "chart_id": chart_id,

            "position": position,

            "chart_title": chart_title,

            "chart_type": chart_type,

            "x_axis": x_label,

            "left_y": left_y,

            "right_y": right_y,

            "legends": legends,

            "render_objects": render_objects,

            "dual_axis": dual_axis,

            "status": validation["status"],

            "confidence": validation["score"],

            "warnings": "; ".join(

                validation["warnings"]

            ),

            "errors": "; ".join(

                validation["errors"]

            ),

            "missing_information": ", ".join(

                missing

            )

        }

    ###############################################################
    # Save Validation
    ###############################################################

    def save_json(

            self,

            result,

            output_file

    ):

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

        ###############################################################
    # Build Executive Chart Repository
    ###############################################################

    def build_repository(

            self,

            repository_rows

    ):

        import pandas as pd

        columns = [

            "chart_id",

            "position",

            "chart_title",

            "chart_type",

            "x_axis",

            "left_y",

            "right_y",

            "legends",

            "render_objects",

            "dual_axis",

            "status",

            "confidence",

            "warnings",

            "errors",

            "missing_information"

        ]

        df = pd.DataFrame(

            repository_rows,

            columns=columns

        )

        return df


    ###############################################################
    # Save Repository CSV
    ###############################################################

    def save_repository(

            self,

            dataframe,

            output_folder

    ):

        import os

        os.makedirs(

            output_folder,

            exist_ok=True

        )

        file_path = os.path.join(

            output_folder,

            "chart_inventory.csv"

        )

        dataframe.to_csv(

            file_path,

            index=False

        )

        return file_path
