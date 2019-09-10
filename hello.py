from flask import Flask, request
import json
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello_world():
    return 'Hello World!'

@app.route('/payload', methods=['GET', 'POST'])
def payload():
    if request.method == 'POST':
        payload = request.get_json() #get the whole json
        name = payload['commits'][0]['committer']['name'] #get the name of the committer
        path = payload['commits'][0]['modified'] #get the file paths of the committed files
        #what if more than 1 file?
        numOfFiles = len(path) #get the path of each file in commit
        #find number of files
        #loop through the files
        #create list of file's name & path
        #loop through this list when printing
        i = 0
        while numOfFiles >= 0:
            file = path[i].split('/')
            i = i + 1
            numOfFiles = numOfFiles - 1
        #while numFiles > 0 print file path
        message = payload['commits'][0]['message'] #get the commit message
        nameMsg = "Name: " + name
        fileMsg = "\nFolder: " + file[0] + "\nApp: " + file[1] + "\nOS: " + file[2] + "\nVersion: " + file[3] + "\nFile: " + file[4]
        commitMsg = "\nMessage: " + message
        msg = nameMsg + fileMsg + commitMsg + numOfFiles
        print(msg)
        return msg
    else:
        return 'Hello'

#got json from GitHub on push
#got necessary info (name, file & message)

#TODO:
#work with multiple files
#split file data into components
