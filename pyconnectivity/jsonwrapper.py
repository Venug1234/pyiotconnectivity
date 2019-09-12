import json
import iotclient

def convertpayload(data):
	msg = json.dumps(data , indent=4, separators=(", ", " : "))
	print(msg)
	iotclient.sendmessage(msg, "1")


def convertsinglepayload(data):

	msg = json.dumps(data , indent=4, separators=(", ", " : "))
	print(msg)
	iotclient.sendmessage(msg, "1")


def converttoobj(msgstring):
	return json.loads(msgstring)