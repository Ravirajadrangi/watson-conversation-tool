# Copyright 2017 IBM Corp. All Rights Reserved.
# See LICENSE for details.
#
# Author: Henrik Loeser
#
# Manage workspaces for IBM Watson Conversation service on IBM Bluemix.
# See the README for documentation.
#

import json, argparse
from os.path import join, dirname
from watson_developer_cloud import ConversationV1

# Credentials are read from a file
with open("config.json") as confFile:
     config=json.load(confFile)['credentials']

# Initialize the Conversation client
conversation = ConversationV1(
    username=config['username'],
    password=config['password'],
    version=config['version']
    )


# Define parameters that we want to catch and some basic command help
def getParameters(args=None):
    parser = argparse.ArgumentParser(description='Process my Watson Conversation Commands',prog='wctool')
    parser.add_argument("-l",dest='listWorkspaces', action='store_true', help='list workspaces')
    parser.add_argument("-c",dest='createWorkspace', action='store_true', help='create workspace')
    parser.add_argument("-u",dest='updateWorkspace', action='store_true', help='update workspace')
    parser.add_argument("-d",dest='deleteWorkspace', action='store_true', help='delete workspace')
    parser.add_argument("-g",dest='getWorkspace', action='store_true', help='get details for single workspace')
    parser.add_argument("-full",dest='fullWorkspace', action='store_true', help='get the full workspace')
    parser.add_argument("-id",dest='workspaceID', help='Workspace ID')
    parser.add_argument("-o",dest='outFile', help='output file')
    parser.add_argument("-i",dest='inFile', help='input file')
    parser.add_argument("-name",dest='wsName', help='Workspace Name')
    parser.add_argument("-desc",dest='wsDescription', help='Workspace Description')
    parser.add_argument("-lang",dest='wsLang', help='Workspace Language')


    parms = parser.parse_args()
    return parms

# List available dialogs
def listWorkspaces():
    print(json.dumps(conversation.list_workspaces(), indent=2))

# Get and print a specific workspace by ID
def getPrintWorkspace(workspaceID,exportWS):
    print(json.dumps(conversation.get_workspace(workspace_id=workspaceID,export=exportWS), indent=2))

# Get a specific workspace by ID and export to file
def getSaveWorkspace(workspaceID,outFile):
    ws=conversation.get_workspace(workspace_id=workspaceID,export=True)
    with open(outFile,'w') as jsonFile:
        json.dump(ws, jsonFile, indent=2)
    print "Document saved to " + outFile


# Update a workspace
def updateWorkspace(workspaceID,
                    newName=None,
                    newDescription=None,
                    newLang=None):
    ws=conversation.update_workspace(workspace_id=workspaceID,
                                    name=newName,
                                    description=newDescription,
                                    language=newLang)
    print "Workspace updated - new workspace"
    print(json.dumps(ws, indent=2))

# Create a new workspace
def createWorkspace(newName, newDescription, newLang, inFile):
    with open(inFile) as jsonFile:
        ws=json.load(jsonFile)
    newWorkspace=conversation.create_workspace(name=newName,
                                               description=newDescription,
                                               language=newLang,
                                               intents=ws["intents"],
                                               entities=ws["entities"],
                                               dialog_nodes=ws["dialog_nodes"],
                                               counterexamples=ws["counterexamples"],
                                               metadata=ws['metadata'])
    print(json.dumps(newWorkspace, indent=2))

# Delete a workspaceID
def deleteWorkspace(workspaceID):
    conversation.delete_workspace(workspaceID)
    print "Workspace deleted"

#
# Main program, for now just detect what function to call and invoke it
#
if __name__ == '__main__':
    parms = getParameters()
    print parms
    if (parms.listWorkspaces):
        listWorkspaces()
    if (parms.getWorkspace and parms.workspaceID):
        if (parms.outFile):
            getSaveWorkspace(parms.workspaceID,parms.outFile)
        else:
            getPrintWorkspace(parms.workspaceID,exportWS=parms.fullWorkspace)
    if (parms.updateWorkspace and parms.workspaceID):
        updateWorkspace(parms.workspaceID,
                        parms.wsName,
                        parms.wsDescription,
                        parms.wsLang)
    if (parms.createWorkspace and parms.wsName and parms.wsDescription and parms.wsLang and parms.inFile):
        createWorkspace(newName=parms.wsName,
                        newDescription=parms.wsDescription,
                        newLang=parms.wsLang,
                        inFile=parms.inFile)
    if (parms.deleteWorkspace and parms.workspaceID):
        deleteWorkspace(parms.workspaceID)
