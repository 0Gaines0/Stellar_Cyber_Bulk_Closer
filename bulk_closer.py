import requests
import base64
import json
import os
from urllib.parse import urlunparse
requests.packages.urllib3.disable_warnings()

HOST = ""
TOKEN = ""

new_case_data = {}


def get_investigations_for_case(token, ticket_id):
    headers = {"Authorization": "Bearer " + token}
    url = urlunparse(("https", HOST, f"/connect/api/v1/incidents?ticket_id={ticket_id}", "", "", "" ))
    res = requests.get(url, headers=headers, verify=False)
    return res.json()

def update_alert_to_closed(token, index, id):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json; charset=utf-8"
    }
    data = {'status': 'Closed'}
    url = urlunparse(("https", HOST, f"/connect/api/v1/security_events/{index}/{id}/status", "", "", "" ))
    res = requests.put(url, headers=headers, json=data, verify=False)
    return res.text

def update_case_to_closed(token, id):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json; charset=utf-8",
        "accept" : "application/json"
    }
    data = {'status': 'Resolved'}
    url = urlunparse(("https", HOST, f"/connect/api/v1/cases/{id}", "", "", "" ))
    res = requests.put(url, headers=headers, json=data, verify=False)
    return res.text


for item in new_case_data["output"]:
    ticket_id = item["ticket_id"]
    case_id = item["_id"]
    investigations = get_investigations_for_case(TOKEN, ticket_id)['data']['incidents']
    filtered_list = []
    for invest in investigations:
        if invest["_id"] == case_id:
            filtered_list.append(invest)
    for invest in filtered_list:
        events = invest['event_ids']
        for event in events:
            index = event["_index"]
            event_id = event["_id"]
            update_alert_to_closed(TOKEN, index, event_id)
    update_case_to_closed(TOKEN, case_id)

print("done...")