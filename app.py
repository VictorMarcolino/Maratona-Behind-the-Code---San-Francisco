import io
import json
import os

import numpy as np
from PIL import Image
from flask import Flask, render_template, request, json

from connect import WatsonConnect
from formulas.respostas import connectToIoT

app = Flask(__name__)
app.config.from_object(__name__)
port = int(os.getenv('PORT', 8080))

classes = ['normal', 'praga']
# COLOQUE AQUI SUA URL DO MODELO
model_endpoint_url = "https://eu-gb.ml.cloud.ibm.com/v3/wml_instances/6b701a7c-2988-4118-ba78-87deca634aa6/deployments/e82abb04-8c0a-474f-a7c5-9ffd034f9acc/online"
# COLOQUE AQUI SUAS CREDENCIAIS
wml_credentials = {
	"apikey"                : "cPXyktYqJXBbb2l7Lcr_iO2-rYI2TmnA0L1UIo-q24W5",
	"iam_apikey_description": "Auto-generated for key 3ed26d7a-2839-4f23-ace3-420fe2fecfe9",
	"iam_apikey_name"       : "Credenciais de serviço-1",
	"iam_role_crn"          : "crn:v1:bluemix:public:iam::::serviceRole:Writer",
	"iam_serviceid_crn"     : "crn:v1:bluemix:public:iam-identity::a/01814b0447774fbc983e10bb072893bd::serviceid:ServiceId-95fcb599-b656-48a6-8d19-0b943d5edc2c",
	"instance_id"           : "6b701a7c-2988-4118-ba78-87deca634aa6",
	"url"                   : "https://eu-gb.ml.cloud.ibm.com"
	}
conn = WatsonConnect(wml_credentials)
myConfig = {
	"auth": {
		"key"  : "a-6j2xmi-z5pvdhhtfa",
		"token": "5_-d)L!Lq8pd720slb"
		}
	}
respostaFromIoT = connectToIoT(myConfig)

@app.route("/", methods=['GET'])
def hello():
	error = None
	return render_template('index.html', error=error)


@app.route("/iot", methods=['GET'])
def result():
	print(request)
	# Implemente sua lógica aqui e insira as respostas na variável 'resposta'
	resposta = {
		"iotData"   : "data",
		"itu"       : "data",
		"volumeAgua": "data",
		"fahrenheit": "data"
		}

	response = app.response_class(
			response=json.dumps(respostaFromIoT),
			status=200,
			mimetype='application/json'
			)
	return response


def prepare_image(image):
	image = image.resize(size=(96, 96))
	image = np.array(image, dtype="float") / 255.0
	image = np.expand_dims(image, axis=0)
	image = image.tolist()
	return image

@app.route('/predict', methods=['POST'])
def predict():
	print(request)
	image = request.files["image"].read()
	image = Image.open(io.BytesIO(image))
	image = prepare_image(image)
	model_payload = {"values": image}
	model_result = conn.sendImage(json=model_payload, url=model_endpoint_url)

	resposta = {
		"class": classes[model_result['values'][0][1][0]]
		}
	return resposta

@app.route('/avaliate', methods=['GET'])
def avaliate():
	# NÃO ALTERE
	image = Image.open("teste123.jpg")
	image = prepare_image(image)
	model_payload = {"values": image}
	model_result = conn.sendImage(json=model_payload, url=model_endpoint_url)
	resposta = {
		"class": classes[model_result['values'][0][1][0]]
		}
	return resposta

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port)
