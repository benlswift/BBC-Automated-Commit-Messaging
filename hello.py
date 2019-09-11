from flask import Flask, request
import json
import requests
import os
import slack

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello_world():
    return 'Hello World!'

def postToSlack(message):

    #slack_token = os.environ["xoxb-6084091907-594909232454-0bcWHJKV7duUqklIuklcLo7M"]
    client = slack.WebClient(token="xoxb-6084091907-594909232454-0bcWHJKV7duUqklIuklcLo7M")

    client.chat_postMessage(
      channel="#automationplayground",
      text=message
    )
    
    return "Success"

@app.route('/payload', methods=['GET', 'POST'])
def payload():
    if request.method == 'POST':
        payload = request.get_json() #get the whole json -> then split it into necessary info 
        name = payload['commits'][0]['committer']['name'] #get the name of the committer
        path = payload['commits'][0]['modified'] #get the file paths of the committed files
        addedFiles = payload['commits'][0]['added']#files can also be added
        removedFiles = payload['commits'][0]['removed']#or removed
        if len(addedFiles) != 0:#add added/removed files to list of file paths
            path += addedFiles
        if len(removedFiles) != 0:
            path += removedFiles

        message = payload['commits'][0]['message'] #get the commit message

        commitMsg = " has " + message #write out the commit message

        #what if more than 1 file?
        #find number of files
        #loop through the files
        #create list of file's name & path
        #loop through this list when printing
        
        numOfFiles = len(path) #get how many files have been committed
        i = 0 #number of file in list
        fileMsg = "\n" 
        while numOfFiles >= 1:  #while numFiles > 0 print file path

            file = path[i].split('/') #split the path into components
            fileMsg += "\nOn the " + file[1] + " app on " + file[2] + " version " + file[3] + " file name " + file[4]
            
            numOfFiles -= 1 #used as counter
            i += 1
            
        msg = name + commitMsg + fileMsg #write message to be printed
        print(msg)
        #run the slack function to post to Slack
        #postToSlack(msg)
        return msg
    
    else:
        return 'Hello'

#got json from GitHub on push
#got necessary info (name, file & message)

#TODO:
#work with multiple files
#split file data into components
