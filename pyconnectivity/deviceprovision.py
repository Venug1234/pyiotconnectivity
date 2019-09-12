
import json
import hsm_security_client

iothuburi = ""
deviceid = ""
b64EncCert = ""
globalprovuri = ""

def isregistered():
	try:
		f = open("/home/iot/iot_client.json", "r")
		data = json.load(f)
		if(len(data.get("iothub_uri")) == 0):
			return False

		iothuburi = data.get("iothub_uri")
		deviceid = data.get("device_id")
		print("provision URI ", iothuburi)
		print("device id ", deviceid)
		return True

	except:
		print("failed to open iot_client.json file ")
		return False


def readcertfile():
	try:
		f = open("/home/iot/iot_certificate.json")
		data = json.load(f)
		if(len(data.get("certificate")) == 0):
			return False

		b64enccert = data.get("certificate")
		globalprovuri = data.get("global_prov_uri")
		return True
	except:
		print("Error processing certificate file ")
		return False

def read_dps_scope_pswrd():
	dpsscopeid = "jdjfjd"  #TODO


if __name__ == '__main__':
	if isregistered() == True :
		print(" Device is already Provisioned ")
	else:
		if readcertfile() == True:
			Pic6_Prov_Init(globalprovuri , dpsscopeid)


