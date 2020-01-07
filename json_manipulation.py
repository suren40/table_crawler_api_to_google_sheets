#!/usr/bin/env python3
"""
This is the python script used in my lambda function to recieve the json file sent from API-Gateway of AWS and sends 
that data to the google sheets.
--
What is does?
* Receives the json file and send to the google sheets.
---
Modules used:
* gspread
* oauth2client
* json,string


How API is received?

"""


import string
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# It is like gives the access to the google apis for this projectes
SCOPES = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
          "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
# It contains the crendentials for authencation of our file.
# For example I rename it as auth.json
JSON_FILE_FOR_AUTHENTICATION = "auth.json"
# we have to define the function with the parameter event and context. where context carries our configuration of lambda

def handler(event,context):
# event receives our data and loads in our body
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE_FOR_AUTHENTICAION, SCOPES)
    client = gspread.authorize(creds)
    body = json.loads(event['body'])
    print(body)
    start = body['begin']
    sheetID = body['sheet_id']
    if len(sheetID)<=1:
# For defining the defualt sheet_id if it is not given
        sheetID="1A59j3aXKLHkwVx0nj8hMpX8gksnvJ5T2rgZCVNNKxYI"
    
        
    sheet = client.open_by_key(sheetID).sheet1

    row_data = []
    letter = string.ascii_letters[26:]
    
#    print(event)
    
    
    if len(start)<=1:
        start = "A2"
    start_len = str(start)[1:]
        
        
    json_data = body['data']
    #data_read = data.read()
    #json_data = json.loads(data_read)
#    print(json_data)
    end_len = len(json_data)
    print(json)
    column_length = len(json_data[0].keys()) - 1
    end = letter[column_length]+str(end_len+int(start_len))
    for object in json_data:
        for key in object:
            print(f'{key.strip()}')
            row_data.append(object[key].strip())
    range_1 = start+":"+end
    cell_list = sheet.range(range_1)
    for i,cell in enumerate(cell_list):
        try:
            cell.value = row_data[i]
            # TODO: write code...
        except IndexError:
            print("Index error")
    if sheet.update_cells(cell_list):
        return {"message":"Updated correctly"}
    else:
        return {"message":"printed with error"}
        
