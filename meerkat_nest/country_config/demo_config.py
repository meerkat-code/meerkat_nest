""" Config for Demo Location """

country_config = {
    "country_name": "Demo",
    "authentication_token": "",
    "tables": [
        "demo_case",
        "demo_alert",
        "demo_register",
        "jor_evaluation",
        "dem_test",
        "rms_test"
    ],
    "scramble_fields": {
        "dem_evaluation": ["simid", "phonenumber"]
    },
    "hash_fields": {
        "demo_case": ["pt1:gender"]
    },
    "patient_id": {
        "demo_case": {
            "field_name": 'pt:pid',
            "validation": "^[1234567890]{10,10}$",
            "translate": True,
            "exclude": [1234567890, 1111111111]
        }
    },
    "rename_fields": {
        "demo_case": {'*meta-instance-id*': 'meta/instanceID',
                      '*meta-submission-date*': 'SubmissionDate',
                      "visit_date": "pt./visit_date",
                      "gender": "pt1./gender",
                      "age": "pt1./age",
                      "visit": "intro./visit"
                      },
        "demo_alert": {'*meta-instance-id*': 'meta/instanceID',
                       '*meta-submission-date*': 'SubmissionDate'},
        "demo_register": {'*meta-instance-id*': 'meta/instanceID',
                          '*meta-submission-date*': 'SubmissionDate'},
        "dem_test": {'*meta-instance-id*': 'meta/instanceID',
                     '*meta-submission-date*': 'SubmissionDate'},
    },
    "rename_forms": {
        "dem_test": "demo_testing"
    },
    "replace_characters": {
        "demo_case":
            [[":", "./"]]
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
        },
    "incremental_conversion":
        {
            "demo_testing":
                {
                    "2": {
                            "newVersion:": "3",
                            "map_fields": [
                                {"name": "cd./malaria_slide",
                                 "new_field": "malaria2./malaria_slide"},
                                {"name": "cd./malaria_rx",
                                 "new_field": "malaria1./malaria_rx"},
                                {"name": "malaria./norx",
                                 "new_field": "malaria2./norx"},
                                {"name": "malaria./ipt",
                                 "new_field": "malaria1./ipt"},
                                {"name": "malaria./ipt_trim1",
                                 "new_field": "malaria1./ipt_trim1"},
                                {"name": "cd./tetanos_vacc_doses",
                                 "new_field": "tetanos_vacc_doses"},
                                {"name": "cd./age_days",
                                 "new_field": "child_age_days"}
                            ],
                            "calculate_fields": [
                                {"name": "malaria./llin_other",
                                 "new_field": "malaria./llin",
                                 "function": ""},
                                {"name": "malaria./llin_routine",
                                 "new_field": "malaria./llin",
                                 "function": ""}
                            ]
                        }
                }
        }
}
