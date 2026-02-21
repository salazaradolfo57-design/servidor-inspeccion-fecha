from flask import Flask, request
import cv2
import numpy as np
import pytesseract
import re

app = Flask(__name__)

def contiene_fecha(texto):
    patrones = [
        r"\b\d{2}/\d{2}/\d{4}\b",
        r"\b\d{2}-\d{2}-\d{4}\b",
        r"\b\d{4}-\d{2}-\d{2}\b"
    ]
    for p in patrones:
        if re.search(p, texto):
            return True
    return False

@app.route('/upload', methods=['POST'])
def upload():
    img_bytes = request.data
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    texto = pytesseract.image_to_string(gray)

    if contiene_fecha(texto):
        return "OK"
    else:
        return "RECHAZO"

app.run(host="0.0.0.0", port=5000)
