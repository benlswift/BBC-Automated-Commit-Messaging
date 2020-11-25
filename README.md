# BBC-Automated-Commit-Messaging
A project to automatically post a message to a Slack channel when a change is committed. This project was completed whilst on work experience at the BBC.

## Config Update Message Automation
### Aims
This project aims to post a message to Slack once a team member has pushed a commit. The team member’s name, the commit message and the file(s) committed should be shown in the message.

### Overview
The project is coded in Python 3, using Flask and ngrok. The project code is in config_messager.py. The payload() function within config_messager.py runs when a commit is pushed to GitHub. GitHub sends a POST request containing information of the commit in JSON, this can then be parsed for the necessary information.

## Running the Program
### Flask
Flask is a Python server that is used to run the program.
Within the folder containing config_updater.py type set FLASK_APP=config_messager.py into the command line.
Set up debug mode using set FLASK_ENV=development in the command line
Run Flask using flask run in the command line
See https://flask.palletsprojects.com/en/1.1.x/quickstart/ for further information

## Ngrok
Download ngrok using the steps on https://dashboard.ngrok.com/get-started
Run ngrok and type ngrok http 5000 into the command line.
## GitHub
In the relevant repository in GitHub navigate to settings and webhooks.
Copy the forwarding address in ngrok and paste this into Payload URL in settings. Add /payload onto the end of the address.
Ensure that Push event and Active are checked.
Click Add webhook.
This will send the POST request to the correct address when a commit is pushed.

The program is now set up, when a commit is pushed a message should be sent.

## Code
Payload()
Within the payload() function, once a POST request has been sent the JSON is read into the payload variable. Then the necessary information can be extracted from this JSON, the committer’s name, commit message and the files that have been committed are parsed and stored. A commit can relate to modifying, adding or removing files, so all of these changes are stored to the path variable. In order to split the file path of the committed files a while loop is used. This will loop through each committed file splitting it into the app, version number and platform that the committed file belongs to. Once all of this information has been parsed it is printed.
genMessage()
The genMessage() function is used to randomly generate a message to be posted to Slack. This function reads a yaml file and randomly chooses parts of the message, the commit information (passed as parameters) is then added to this randomised text. The commit_update.yaml file contains multiple variations on the same message, these are stored under headings. The genMessage() function gets a list of possible messages and chooses one at random. A complete message is stitched together and returned by the function.

Examples are below:

postToSlack()
The postToSlack() function takes the complete message and posts it to a slack channel. Firstly the Slack token and the relevant channel must be identified, for this the commit_update.yaml file is again used. Once the token and channel have been identified the message, which is passed as a parameter, can be sent to the Slack channel. The correct token and channel must be in the commit_update.yaml file under the token and channel headings.
