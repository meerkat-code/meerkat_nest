import requests
import json
import uuid

payload = {
    "token": "", 
    "content": "record", 
    "formId": "demo_case",
    "formVersion": "", 
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
            "SubmissionDate": "2017-08-24T16:22:20.175",
            "today": "2017-06-22",
            "deviceid": "1",
            "subscriberid": "123123123123123",
            "simid": "1231231231231231231",
            "phonenumber": "+44123123123",
                "pt./visit_date": "2017-08-24",
                "pt./gender": "male",
                "icd_code": "A09",
            "meta/instanceID": "uuid:75099745-d218-4129-8b27-de3520c1281a"
        }
    ]
}


def send_to_nest():

        payload['data'][0]["meta/instanceID"] = str(uuid.uuid4())
        post_response = requests.post('http://localhost:5000/upload',
                                      data=json.dumps(payload),
                                      headers={'Content-Type': 'application/json'})

send_to_nest()
