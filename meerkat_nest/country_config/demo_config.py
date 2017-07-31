""" Config for Demo Location """

country_config = {
    "country_name": "Demo",
    "tables": [
        "demo_case",
        "demo_alert",
        "demo_register",
        "jor_evaluation",
        "dem_test"
    ],
    "scramble_fields": {
        "demo_case": [],
        "demo_alert": [],
        "demo_register": [],
        "jor_evaluation": [],
        "dem_evaluation": ["simid", "phonenumber"]
    },
    "supported_content":
        {
        "form": {
            "token": "",
            "content": "",
            "formId": "",
            "formVersion": "",
            "data": ""
        },
        "record": {
            "token": "",
            "content": "",
            "formId": "",
            "formVersion": "",
            "data": ""
        }
    }
 }