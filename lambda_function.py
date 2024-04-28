import os
import requests
import zipfile
import shutil
import sys
from GitShade.emerge.main import run 
import yaml
import json
import shutil

def lambda_handler(event, context):
    print(event,context)
    allowedExtension = ['.ts', '.tsx']
    allowedLanguages = ['typescript']
    # Replace these values with your GitHub repository details
    owner = event['queryStringParameters']['owner']
    repo = event['queryStringParameters']['repo']
    root = event['queryStringParameters']['root']
    ref = "master"  # or any other branch/tag/commit ref

    # URL for the zip file
    url = f"https://api.github.com/repos/{owner}/{repo}/zipball"

    # Make a GET request to download the zip file
    response = requests.get(url)
    print(response.status_code, url)
    if response.status_code == 200:
        

        # Set the temporary directory
        temp_dir = "/tmp"
        
        # Create a folder named "my_folder" in the temporary directory
        folder_name = "my_folder"
        folder_path = os.path.join(temp_dir, folder_name)
        
        # Check if the folder already exists, if not, create it
        if not os.path.exists(folder_path):
            print('folder created')
            os.makedirs(folder_path)
        
        # Save the zip file to the newly created folder
        zip_file_path = os.path.join(folder_path, "downloaded_file.zip")
        with open(zip_file_path, "wb") as zip_file:
            zip_file.write(response.content)

        # Extract the contents of the zip file
        extracted_folder_path = os.path.join(folder_path, "extracted")
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_folder_path)
        
        repositoryName = ''
        extracted_files = os.listdir(extracted_folder_path)
        for file_name in extracted_files:
            repositoryName = file_name

        print(repositoryName)
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            # Read content of each file in the zip
            file_contents = {}
            langExtList = {}
            #print(zip_ref.namelist())
            for file_name in zip_ref.namelist():
                with zip_ref.open(file_name) as file:
                    try:
                        file_contents[file_name] = file.read().decode("utf-8")
                        fileNameSplitList = file_name.split('.')
                        if fileNameSplitList.__len__() > 1 and fileNameSplitList[fileNameSplitList.__len__()-1] in allowedLanguages :
                            print(fileNameSplitList[fileNameSplitList.__len__()-1])
                            if fileNameSplitList[fileNameSplitList.__len__()-1] not in langExtList:
                                langExtList[fileNameSplitList[fileNameSplitList.__len__()-1]] = 1
                            else:
                                langExtList[fileNameSplitList[fileNameSplitList.__len__()-1]] = langExtList[fileNameSplitList[fileNameSplitList.__len__()-1]] + 1
                        
                    except Exception as e:
                        print('cannnot decode the file')
            print(langExtList)
            
            ignore_directories = ['node_modules']
            d = {  'project_name':'GitShade',
                    'loglevel':'info',
                    'analyses': 
                        [{ 
                            'analysis_name':'self-check',
                            'source_directory':f'/tmp/my_folder/extracted/{repositoryName}/{root}',
                            'only_permit_languages': allowedLanguages,
                            'only_permit_file_extensions': allowedExtension,
                            'ignore_directories_containing': ignore_directories,
                            'ignore_files_containing': ['.*'],
                            'file_scan': ['number_of_methods'],
                            'export': [{ 'directory' : './emerge/export/emerge'}]
                        }]
                }
                
            with open('/tmp/my_folder/extracted/emerge.yaml', 'w') as yaml_file:
                yaml.dump(d, yaml_file, sort_keys=False)
            os.sync()

        run()
        nodesPath = '/tmp/initNodes.json'
        edgesPath = '/tmp/initEdges.json'
        
        nodes = []
        with open(nodesPath, "r") as file:
            nodes = json.load(file)
        edges = []
        with open(edgesPath, "r") as file:
            edges = json.load(file)
            
        
        extracted_files = os.listdir('/tmp')
        for file_name in extracted_files:
            print(file_name)
        
        
        data = {
            'nodes' : nodes, 
            'edges': edges,
        }
        return {
            "statusCode": 200,
            "body": json.dumps(data)
        }
    else:
        return {
            "statusCode": response.status_code,
            "body": "Failed to download zip file from GitHub."
        }