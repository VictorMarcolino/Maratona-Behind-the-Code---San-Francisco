import numpy as np
import wiotp.sdk.application as application
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
