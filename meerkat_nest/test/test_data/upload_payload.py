"""
Meerkat Nest Test Data

Payload for testing the Meerkat Nest Upload function
"""
upload_payload = {
    "content": "record", 
    "formId": "dem_test",
    "formVersion": "2",
    "token": "",
    "data": [
        {
            "*meta-instance-id*": "uuid:75099745-d218-4129-8b27-de3520c1281a",
            "*meta-model-version*": "",
            "*meta-ui-version*": "",
            "*meta-submission-date*": "2017-06-23T15:51:33.415Z",
            "*meta-is-complete*": True,
            "*meta-date-marked-as-complete*": "2017-06-23T15:51:33.415Z",
            "start": "2017-06-22T14:21:53.490Z",
            "end": "2017-06-22T14:22:20.175Z",
            "today": "2017-06-22",
            "deviceid": "123123123123123",
            "subscriberid": "123123123123123",
            "simid": "1231231231231231231",
            "phonenumber": "+44123123123",
            "instanceID": "uuid:75099745-d218-4129-8b27-de3520c1281a",
            "cd./malaria_slide": "malaria_slide",
            "cd./malaria_rx": "malaria_rx"
        }
    ]
}

processed_upload_payload = {
    "token": "",
    "content": "record",
    "formId": "dem_test",
    "formVersion": "3",
    "data": [
        {
            "meta/instanceID": "uuid:75099745-d218-4129-8b27-de3520c1281a",
            "*meta-model-version*": "",
            "*meta-ui-version*": "",
            "SubmissionDate": "2017-06-23T15:51:33.415Z",
            "*meta-is-complete*": True,
            "*meta-date-marked-as-complete*": "2017-06-23T15:51:33.415Z",
            "start": "2017-06-22T14:21:53.490Z",
            "end": "2017-06-22T14:22:20.175Z",
            "today": "2017-06-22",
            "deviceid": "355828065518701",
            "subscriberid": "234200404200842",
            "simid": "",
            "phonenumber": "+",
            "instanceID": "uuid:75099745-d218-4129-8b27-de3520c1281a",
            "malaria2./malaria_slide": "malaria_slide",
            "malaria1./malaria_rx": "malaria_rx"
        }
    ]
}