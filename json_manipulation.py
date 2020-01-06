#!/usr/bin/env python3
"""
This is for manipulation of data.

"""
import string
import json

import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
          "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

def handler(event,context):
    creds = ServiceAccountCredentials.from_json_keyfile_name("auth.json", SCOPES)
    client = gspread.authorize(creds)
    body = json.loads(event['body'])
    print(body)
    start = body['begin']
    sheetID = body['sheet_id']
    if len(sheetID)<=1:
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
        
