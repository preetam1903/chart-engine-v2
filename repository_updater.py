import os
import json


class RepositoryUpdater:

    def build_repository(
        self,
        chart_id,
        understanding,
        values
    ):

        repository = {

            "chart_id": chart_id,

            "chart_title": understanding.get(
                "chart_title", ""
            ),

            "chart_type": understanding.get(
                "chart_type", ""
            ),

            "chart_subtype": understanding.get(
                "chart_subtype", ""
            ),

            "unit": understanding.get(
                "y_axis", {}
            ).get(
                "unit", ""
            ),

            "y_axis_title": understanding.get(
                "y_axis", {}
            ).get(
                "title", ""
            ),

            "x_axis": understanding.get(
                "x_axis", {}
            ).get(
                "labels", []
            ),

            "legend": understanding.get(
                "legend", []
            ),

            "series": {},

            "summary": understanding.get(
                "summary", ""
            ),

            "confidence": understanding.get(
                "confidence", 0
            )

        }

        x_labels = repository["x_axis"]

        for series in values.get(
            "series",
            []
        ):

            name = series.get(
                "name",
                "Unknown"
            )

            nums = series.get(
                "values",
                []
            )

            mapping = {}

            for i in range(

                min(
                    len(x_labels),
                    len(nums)
                )

            ):

                mapping[
                    x_labels[i]
                ] = nums[i]

            repository["series"][name] = mapping

        return repository

    ##########################################################

    def save_repository(

        self,

        repository,

        output_folder

    ):

        chart_folder = os.path.join(

            output_folder,

            repository["chart_id"]

        )

        os.makedirs(

            chart_folder,

            exist_ok=True

        )

        output_file = os.path.join(

            chart_folder,

            "chart_repository.json"

        )

        with open(

            output_file,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                repository,

                f,

                indent=4,

                ensure_ascii=False

            )

        return output_file
