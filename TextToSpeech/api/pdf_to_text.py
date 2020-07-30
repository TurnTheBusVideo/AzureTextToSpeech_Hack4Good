from pdf2image import convert_from_path, convert_from_bytes
from pathlib import Path
from PIL import Image
import tempfile
import os
import pytesseract
import time
from datetime import datetime
from flask import Flask, request, Response, send_file
from werkzeug.utils import secure_filename
from __init__ import webapp

uploads_dir = os.path.join(webapp.instance_path, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)

@webapp.route('/pdf-to-text', methods=['POST'])
def pdf_to_text():    
    try:
        pdf_file = request.files.get('pdf')
        if pdf_file == None:
            return 'Missing pdf input in request body!'
        
        upload_path = os.path.join(uploads_dir, secure_filename(pdf_file.filename))
        pdf_file.save(upload_path)
        
        images = convert_from_path(upload_path)
        def image_to_text():
            all_text = ""     
            for img in images:
                text = pytesseract.image_to_string(img, lang='hin')
                yield text + "\n"    
        return Response(image_to_text())
    except Exception as e:
	    return str(e)

@webapp.route('/get-digant-text', methods=['GET'])
def get_digant_text():    
    try:
        with open('Digant.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        return text
    except Exception as e:
	    return str(e)

@webapp.route('/get-digant-audio', methods=['GET'])
def get_digant_audio():
	try:
		return send_file('digant_audio.zip', mimetype='application/zip', as_attachment=True)
	except Exception as e:
	    return str(e)