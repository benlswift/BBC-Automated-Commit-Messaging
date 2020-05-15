from flask import Flask, request
import json
import requests
import os
import yaml
import random
import slack

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello_world():
    return 'Hello World!'

def postToSlack(message):

    with open("commit_update.yaml", 'r') as stream:
        out = yaml.load(stream)
        tokenCode = out['slack']['token']# get the token from the yaml file
        channelCode = out['slack']['channel']# get the channel from the yaml file
        
    client = slack.WebClient(token=tokenCode)

    client.chat_postMessage(
      channel=channelCode, #the channel to send a message to 
      text=message #the message to be sent to Slack
    )
    return "Success"

def genMessage(name, files, commitMsg):
    with open("commit_update.yaml", 'r') as stream:# open and read yaml file
        out = yaml.load(stream)
##        token = out['slack']['token']
##        channel = out['slack']['channel']
        pres = out['slack']['preambles']
        changed = out['slack']['changed']
        commitMessage = out['slack']['commitMessage']
        messageToSend = random.choice(pres) + " " + name + " " + random.choice(changed) + " " + files + " " + random.choice(commitMessage) + " " + commitMsg
        return messageToSend
    
@app.route('/payload', methods=['GET', 'POST'])
def payload():
    if request.method == 'POST':
        payload = request.get_json() #get the whole json -> then split it into necessary info 
        name = payload['commits'][0]['committer']['name'] #get the name of the committer
        path = payload['commits'][0]['modified'] #get the file paths of the committed files
        addedFiles = payload['commits'][0]['added']#files can also be added
        removedFiles = payload['commits'][0]['removed']#or removed
        if len(addedFiles) != 0: #add added/removed files to list of file paths
            path += addedFiles
        if len(removedFiles) != 0:
            path += removedFiles

        message = payload['commits'][0]['message'] #get the commit message

        fileMsg = ""
        numOfFiles = len(path) #get how many files have been committed
        i = 0 #number of file in list
        while numOfFiles >= 1:  #while numFiles > 0 print file path

            file = path[i].split('/') #split the path into components
            if len(path) > 1 and i != 0:#correct grammar when more than one committed file
                fileMsg += " and " + file[4] + " for " + file[1] + " " + file[2] + " version " + file[3]
            else:
                fileMsg += "" + file[4] + " for " + file[1] + " " + file[2] + " version " + file[3]
            
            numOfFiles -= 1 #used as counter
            i += 1
            
        postToSlack(genMessage(name, fileMsg, message))
        return genMessage(name, fileMsg, message)
    
    else:
        return 'Hello'

