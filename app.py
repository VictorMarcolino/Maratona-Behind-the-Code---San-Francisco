import io
import json
import os

import numpy as np
from PIL import Image
from flask import Flask, render_template, request, json


from formulas.respostas import connectToIoT, WatsonConnect

app = Flask(__name__)
app.config.from_object(__name__)
port = int(os.getenv('PORT', 8080))




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
	response = app.response_class(response=json.dumps(resposta), status=200, mimetype='application/json')
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
	model_result = modelo(image)
	resposta = {
		"class": model_result
		}
	return resposta


@app.route('/avaliate', methods=['GET'])
def avaliate():
	image = Image.open("teste123.jpg")
	image = prepare_image(image)
	model_result = modelo(image)
	resposta = {
		"class": model_result
		}
	return resposta


def modelo(image):
	# Defina aqui a conexão com o modelo
	model_payload = {"values": image}
	return "Algo"


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port)
