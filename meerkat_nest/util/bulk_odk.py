import requests
import xmltodict
import time
from threading import Thread
from queue import Queue

# Recommended use:  copy this script inside the nest container, because /upload
# hasn't been opened to the outside.

username = "username"
password = "password"
aggregate_url = "https://aggurl.info"
form_id = "form_id"
nest_url = "http://localhost:5000/upload"

auth = requests.auth.HTTPDigestAuth(username, password)
num_threads = 100

def get_odk_submission(aggregate_url: str,
                       auth: requests.auth.HTTPDigestAuth,
                       form_id: str, uuid: str) -> dict:
    form_id_string = f'{form_id}[@version=null and @uiVersion=null]/{form_id}[@key={uuid}]'
    submission = requests.get(aggregate_url + "/view/downloadSubmission",
                              params={"formId": form_id_string}, auth=auth)
    if submission.status_code == 200:
        submission = xmltodict.parse(submission.text)["submission"]["data"][form_id]
        return fix_odk_data(submission)
    return None


def fix_odk_data(form_submission: dict) -> dict:
    return_submission = {}
    for key, value in form_submission.items():
        if key not in ["orx:meta"]:
            new_key = key.replace("@", "")
            return_submission[new_key] = value
    return return_submission

def fix_groups(sub, delim=":"):
    new_sub = {}
    for key, value in sub.items():
        if isinstance(value, dict):
            for inner_key, inner_value in value.items():
                new_sub[key + delim + inner_key] = inner_value
        elif key == "instanceID":
            new_sub["*meta-instance-id*"] = value
            new_sub["meta:instanceID"] = value
        elif key == "submissionDate":
            new_sub["*meta-submission-date*"] = value
        elif key == "isComplete":
            new_sub["*meta-is-complete*"] = value
        elif key == "markedAsCompleteDate":
            new_sub["*meta-date-marked-as-complete*"] = value
        else:
            new_sub[key] = value
    return new_sub


def submitt_to_nest(sub):
    data = {
        "formId": sub["id"],
        "data": [sub],
        "content": "record",
        "formVersion": None,
        "token": ""
        }
    requests.post(nest_url, json=data)

def crawl(q):
    while not q.empty():
        index, individual_submission = q.get()
        try: 
            sub = get_odk_submission(aggregate_url,
                                     auth,
                                     form_id,
                                     individual_submission)
            submitt_to_nest(fix_groups(sub))
        except Exception as e:
            raise e
        q.task_done()


q = Queue(maxsize=0)

## To pull everything from ODK and push to nest:
# cursor = None # Starting cursor
# for i in range(10):
#     params = {"formId": form_id,
#               "numEntries": 3000}
#     if cursor is not None:
#         params["cursor"] = cursor
#     submissions = [] 
#     with open("uuids.txt") as f:
#         submissions = [ s.strip() for s in f.readlines()]
#     requests.get(aggregate_url + "/view/submissionList",
#                                params=params, auth=auth)
#     try:     
#         submissions_dict = xmltodict.parse(submissions.text)["idChunk"]
#     except:
#         time.sleep(60)
#         next;

#     print(submissions_dict["resumptionCursor"])
#     cursor = submissions_dict["resumptionCursor"]
#     for i, individual_submission in enumerate(submissions_dict["idList"]["id"]):
#         q.put((i, individual_submission))
#     for i in range(num_threads):
#         worker = Thread(target=crawl, args=(q,))
#         worker.setDaemon(True)
#         worker.start()
#     q.join()
#     if cursor is None:
#         break
    

## To read from a file with uuids
filename = "uuids.txt"
with open(filename) as f:
    submissions = [s.strip() for s in f.readlines()]
for i, individual_submission in enumerate(submissions):
    q.put((i, individual_submission))
for i in range(num_threads):
    worker = Thread(target=crawl, args=(q,))
    worker.setDaemon(True)
    worker.start()
q.join()

