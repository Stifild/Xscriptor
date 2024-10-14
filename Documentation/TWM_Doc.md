# Documentation for TellWithMe network
this documentation describes basics of TWM network
## What is TWM?
TellWithMe it`s network based on email protocol. It is crated for communication between computers to control them remotely from main server.
### How it works?
TWM network is based on email protocol. It uses email messages to send commands to computers and get responses from them.
### User track:
1. User send telegram message to main server through telegram bot with command and destination computer.
2. Main server send email message to destination computer with command.
3. Destination computer execute command and send response to main server.
4. Main server send response to user through telegram bot.
## TWM protocol
### Email format
```
From: <Configured email address>
To: <Configured email address>
Subject: <Sender>:<Destination>:<Flag>
Body: <log message>(|||)<Command>
```
#### Description
From and To have to be the same email address. Subject contains information about sender, destination and flag. Body contains log message and command separated by '(|||)'.
##### Flags
* IC - Incoming command
* IR - Incoming response
* FIN - Finish connection
* ERR - Error
* EDCN - Emergency disconnection from the network
* IND - Request for identification
* INF - Information message
* ACK - Acknowledgment
##### Computer identification address
All computers have a unique identification address. It is looks like base IPv4 address, but use only 3 octets. For example: "0.0.1". Network has a reserved address "0.0.0" for main server and "255.255.255" for broadcast messages.
### TWMCD
TWMCD _(TellWithMeComputerDictionary)_ is dictionary that contains all computers connected to the network. It is stored at server in JSON format.
#### Example
```json
{
    "0.0.1": {
        "name": "Computer1",
        "os": "Windows"
    },
    "0.0.2": {
        "name": "Computer2",
        "os": "Linux"
    }
}
```

