from flask import Flask, jsonify, request, Response, send_file, send_from_directory
from capturePhoto import *
from flask_cors import CORS
import os
import datetime
import requests
import cv2
import json
import pickle
import base64

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


UPLOAD_FOLDER = 'photos/'
app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/<greyScale>', methods=['POST'])
def index(greyScale):
	if greyScale=='false':
		capture1, date_time, photo_type =capture(False)
	else:
		capture1, date_time, photo_type =capture(True)
	addr = 'http://127.0.0.1:8000/app/save_image'
	fin = open(capture1, 'rb')
	fin_read = fin.read()
	files = {'image': open(capture1, 'rb')}
	data_obj = {"date":datetime.datetime.today(), "grayscale":photo_type}
	filename1 = capture1
	response = requests.post(addr, files=files, data=data_obj)
	if response.status_code==200:
		return jsonify({'message':'Image saved'})
	return json({'message':'Image cannot saved'})

if __name__ == 'app':
	app.run(host='127.0.0.1', port=5000, debug=True)

