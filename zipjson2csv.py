import os
import pandas as pd
import json
from zipfile import ZipFile
import json
import csv

# declaringa a class
class obj:
    
    # constructor
    def __init__(self, dict1):
        self.__dict__.update(dict1)

def dict2obj(dict1):
    
    # using json.loads method and passing json.dumps
    # method and custom object hook as arguments
    return json.loads(json.dumps(dict1), object_hook=obj)

def print_attr(attr):
    try:
        print(attr)
    except:
        print("not found")

# Path to the ZIP file containing JSON files
zip_file_path = 'many_json_files.zip'

# Full path to extract JSON files
exctracted_csv_file = 'destination_folder\\file_name.csv'



# Extract the ZIP file
with ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder)

# List all JSON files in the extracted folder
json_files = [os.path.join(extracted_folder, file) for file in os.listdir(extracted_folder) if file.endswith('.json')]
#print(json_files)

# Initialize an empty list to store JSON data
json_data = []

# Read JSON files and append data to the list
for json_file in json_files:
    with open(json_file, 'rb') as file:
        file_name=file.name
        data = json.load(file)

        if isinstance(data, dict):
            data['ServerName'] = file_name.split("\\")[-1].split(".")[0][:-17]
            #print("data:{}".format(data))
            json_data.append(data)
        else:
            for i in range(len(data)):
                data[i]['ServerName'] = file_name.split("\\")[-1].split(".")[0][:-17]
                #print("data_i:{}".format(data[i]))
                json_data.append(data[i])

    #for i in range(len(json_data)):
     #   print("json_data {}: {}".format(i, json_data[i]))

def print_fail_status(FatalErrorFound, Status):
    if FatalErrorFound:
        if Status=="Unknown":
            return "Fatal Fail Unknown"
        else:
            return "Fatal {}".format(Status)
    else:
        if Status=="Unknown":
            return "Fail Unknown"
        else:
            return "{}".format(Status)

def print_warn_status(Status):
    if Status=="Unknown":
            return "Warn Unknown"
    else:
        return "{}".format(Status)
        
# initializing the dictionary 
csv_columns = ['Server','Application Name','Issue Type','Issues Found','Analysis','Action Item']
with open(exctracted_csv_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(csv_columns)
    for data in json_data:
        obj2 = dict2obj(data)

        failedFound=False
        for i in range(len(obj2.FailedChecks)):
            failedFound=True
            writer.writerow([
                obj2.ServerName,
                obj2.SiteName,
                print_fail_status(obj2.FatalErrorFound, obj2.FailedChecks[i].Status),
                obj2.FailedChecks[i].Description.replace("'", "\'"),
                obj2.FailedChecks[i].Details.replace("'", "\'")[0:1024],
                obj2.FailedChecks[i].Recommendation.replace("'", "\'")
            ])
        if failedFound==False:
            writer.writerow([
                obj2.ServerName,
                obj2.SiteName,
                'Passed Failed Checks',
                'None',
                'None',
                'None'
            ]) 

        warnFound=False
        for i in range(len(obj2.WarningChecks)):
            warnFound=True
            writer.writerow([
                obj2.ServerName,
                obj2.SiteName,
                print_warn_status(obj2.WarningChecks[i].Status),
                obj2.WarningChecks[i].Description.replace("'", "\'"),
                obj2.WarningChecks[i].Details.replace("'", "\'")[0:1024],
                obj2.WarningChecks[i].Recommendation.replace("'", "\'")
            ])
        if warnFound==False:
            writer.writerow([
                obj2.ServerName,
                obj2.SiteName,
                'Passed Warning Checks',
                'None',
                'None',
                'None'
            ])  