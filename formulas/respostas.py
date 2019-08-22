import wiotp.sdk.application as application
import requests, json as jsony

def fahrenheit(Celsius):
	return 9.0 / 5.0 * Celsius + 32


def ITU(umidade_ar, celsius):
	return celsius - 0.55 * (1 - umidade_ar) * (celsius - 14)


def volumeAgua(umidade, volumeTotal):
	return umidade / volumeTotal


def volumeEsfera(raio):
	pi = 3.1415926535897931
	return (4.0 / 3.0) * pi * raio ** 3


def connectToIoT(myConfig):
	global respostaFromIoT
	respostaFromIoT = {"iotData": "dict", "itu": 0, "volumeAgua": 0, "fahrenheit": 0}

	def myEventCallback(event):
		global respostaFromIoT

		respostaFromIoT['iotData'] = event.data['data']
		respostaFromIoT['itu'] = ITU(umidade_ar=respostaFromIoT["iotData"]["umidade_ar"], celsius=respostaFromIoT["iotData"]["temperatura"])
		respostaFromIoT['volumeAgua'] = volumeAgua(respostaFromIoT["iotData"]["umidade_solo"], volumeEsfera(1) / 2)
		respostaFromIoT['fahrenheit'] = fahrenheit(respostaFromIoT["iotData"]["temperatura"])
		print(respostaFromIoT)

	client = application.ApplicationClient(config=myConfig)
	client.connect()
	client.subscribeToDeviceEvents(deviceId="d9")
	client.deviceEventCallback = myEventCallback
	return respostaFromIoT





class WatsonConnect:
	def __init__(self, wml):
		wml_credentials = wml

		# Paste your Watson Machine Learning service apikey here
		# Use the rest of the code sample as written
		apikey = wml_credentials['apikey']

		# Get an IAM token from IBM Cloud
		url = "https://iam.bluemix.net/oidc/token"
		headers = {"Content-Type": "application/x-www-form-urlencoded"}
		data = "apikey=" + apikey + "&grant_type=urn:ibm:params:oauth:grant-type:apikey"
		IBM_cloud_IAM_uid = "bx"
		IBM_cloud_IAM_pwd = "bx"
		response = requests.post(url, headers=headers, data=data, auth=(IBM_cloud_IAM_uid, IBM_cloud_IAM_pwd))
		self.iam_token = response.json()["access_token"]

	def sendImage(self, json, url):
		headers = {
			"Authorization": "Bearer " + self.iam_token,
			"Content-Type" : "application/json"
			}
		resp = requests.post(url=url, json=json, headers=headers)
		return jsony.loads(resp.content.decode('utf-8'))
