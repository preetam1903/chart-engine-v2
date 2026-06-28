"""
Standard JSON schema for Chart Engine V2
"""


def empty_chart_schema():
    return {
        "chart_metadata": {
            "chart_type": "",
            "title": "",
            "confidence": 0.0
        },

        "axes": {
            "x": {
                "label": "",
                "values": []
            },
            "y": {
                "label": ""
            }
        },

        "series": [],

        "executive_insights": [],

        "business_context": {},

        "relationships": [],

        "raw_extraction": {}
    }
