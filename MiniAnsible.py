#!/usr/bin/env python3

# Information regarding Servers
from config import *
# User credentials
from credentials import *

# Module to run SSH from python
import paramiko
# Module to save last command used
import pickle

print('Mini Ansible by GeorgeRN')

# Function to Print Menu for server selection


def printServersMenu(servers):
    i = 0
    for server in servers.keys():
        print('\u001B[32m', end='')
        print(i, server)
        i += 1

# Get appropiate credentials for the server


def getCredentials(serverName, genericUser=False):
    credentialsKey = servers[serverName][genericUser+1]
    username = credentials[credentialsKey][0]
    password = credentials[credentialsKey][1]
    return (username, password)

# Executes the provided command in the server


def runCommandInServer(serverName, commandToExecute, genericUser=False):
    credentials = getCredentials(serverName, genericUser)
    ip = servers[serverName][0]
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, 22, username=credentials[0], password=credentials[1])
    stdin, stdout, stderr = ssh.exec_command(commandToExecute)
    # Wait until the completion of the SSH connection
    stderr.channel.recv_exit_status()
    ssh.close()
    del ssh
    return (stdin, stdout, stderr)


# Printing servers menu
printServersMenu(serversMenu)
print('\u001B[0mSelect the number in which servers do you want to execute the command?')
serverSelection = input()

serversMenuKeys = tuple(serversMenu.keys())
groupName = serversMenuKeys[int(serverSelection)]
serversToWork = serversMenu[groupName]

# Load last command from pickle file
with open('save.pk', 'rb') as fi:
    command = pickle.load(fi)

# Read command to run from the user
userEntry = input(
    'Type the command to execute:\nLast command executed: ' + command + '\n')

if(userEntry == ''):
    commandToExecute = command
else:
    commandToExecute = userEntry

# Save comand in a pickle file
with open('save.pk', 'wb') as fi:
    # dump your data into the file
    pickle.dump(commandToExecute, fi)

# Executing comand in servers
print('\nRuning command in: ' + str(serversToWork))
print('\nWorking...\n')

for server in serversToWork:
    fullOutput = runCommandInServer(server, commandToExecute, False)
    stdout = fullOutput[1].readlines()
    # Printing outputs from servers
    print('Server: ' + server)
    # Printing standard output
    print('\u001b[34mStd OUTPUT:\u001b[0m')
    if not stdout:
        print('empty')
    else:
        for line in stdout:
            print(line, end='')
        print('')
        # Printing standard error
        print('\u001b[31mStd ERROR:\u001b[0m')
        stderr = fullOutput[2].readlines()
        if not stderr:
            print('empty')
        else:
            for line in stderr:
                print(line, end='')
        print('')
