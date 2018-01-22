import requests
import xmltodict
import csv

uuid_list = []
with open("file.csv", "r") as f:
    read = csv.reader(f)
    next(read)
    for line in read:
        uuid_list.append(line[0].replace(":", ""))


form_name = "jor_case"
group_delimeter = ":"

fields = [
    ("SubmissionDate", "@submissionDate"),
    ("meta:instanceID", "@instanceID")
]


def send_to_nest(data):
    r = requests.post('http://localhost:5000/upload', data=data)
    print(r.status_code)

i = 0

for folder in uuid_list:
    with open("data/" + folder+"/submission.xml", "r") as f:
        dictionary = xmltodict.parse(f.read())

        form_data = dictionary[form_name]

        for f in fields:
            form_data[f[0]] = form_data[f[1]]
            del form_data[f[1]]
        for key in list(form_data.keys()):
            if isinstance(form_data[key], dict):
                for inside_key in form_data[key]:
                    form_data[key + group_delimeter + inside_key] = form_data[key][inside_key]
                del form_data[key]
        send_to_nest(form_data)
        i += 1
print(i)
