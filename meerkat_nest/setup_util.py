import requests
import json
from requests.auth import HTTPDigestAuth
import uuid
import os
from xmljson import badgerfish as bf
from lxml.html import Element, tostring


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

aggregate_data = {
    "start": "2017-06-22T14:21:53.490",
    "end": "2017-06-22T14:22:20.175",
    "today": "2017-06-22",
    "deviceid": "1",
    "subscriberid": "123123123123123",
    "simid": "1231231231231231231",
    "phonenumber": "+44123123123",
    "pt./visit_date": "2017-08-24",
    "pt1./gender": "male",
    "pt1./age": 2,
    "icd_code": "A09",
}


def groupify(data):
    new = {}
    for key in data.keys():
        if "./" in key:
            group, field = key.split("./")
            if group not in new:
                new[group] = {}
            new[group][field] = data[key]
        else:
            new[key] = data[key]

    return new


def send_to_nest():
    payload['data'][0]["meta/instanceID"] = str(uuid.uuid4())
    post_response = requests.post('http://localhost:5000/upload',
                                      data=json.dumps(payload),
                                      headers={'Content-Type': 'application/json'})


def send_to_aggregate():
    form_id = "demo_case"
    grouped_json = groupify(aggregate_data)
    grouped_json["@id"] = form_id
    result = bf.etree(grouped_json, root=Element(form_id))
    aggregate_user = "test"
    aggregate_password = "password"
    auth = HTTPDigestAuth(aggregate_user, aggregate_password)
    aggregate_url = "https://democountryserver.emro.info"
    with open("tmp.xml", "w") as f:
        f.write(tostring(result).decode("utf-8"))

    r = requests.post(aggregate_url + "/submission", auth=auth,
                      files={
                          "xml_submission_file":  ("tmp.xml", open("tmp.xml"), "text/xml")
                      })
    print(r)


def setup_forms():
    try:
        file = open("setup_secret.cfg", "r")
        aggregate_url = file.readline()
        aggregate_user = file.readline()
        aggregate_password = file.readline()

        auth = HTTPDigestAuth(aggregate_user, aggregate_password)
        ret = requests.get(aggregate_url + "/formList", auth=auth)

        for f in os.listdir("forms"):
            print(f)
            form_id = f.split(".xml")[0]
            if not "formId={}".format(form_id) in ret.text:
                requests.post(aggregate_url + "/formUpload", auth=auth,
                              files={
                                  "form_def_file": open("forms/" + f)
                              })
    except FileNotFoundError as e:
        print("No configurations found")

for i in range(1, 9000):
    send_to_aggregate()
