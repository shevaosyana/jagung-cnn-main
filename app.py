# app.py
from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from pathlib import Path

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

# Pastikan folder upload ada
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def analyze_leaf_health(image_path):
    """
    Fungsi sederhana untuk menganalisis kesehatan daun berdasarkan warna
    """
    # Baca gambar
    img = cv2.imread(image_path)
    
    # Konversi ke HSV untuk analisis warna yang lebih baik
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Definisikan range warna untuk daun sehat (hijau)
    lower_green = np.array([35, 20, 20])
    upper_green = np.array([85, 255, 255])
    
    # Buat mask untuk area hijau
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Hitung persentase area hijau
    total_pixels = img.shape[0] * img.shape[1]
    green_pixels = cv2.countNonZero(green_mask)
    green_percentage = (green_pixels / total_pixels) * 100
    
    # Analisis sederhana berdasarkan persentase hijau
    if green_percentage > 60:
        return {
            'condition': 'Healthy',
            'confidence': green_percentage / 100,
            'details': 'Daun terlihat sehat dengan dominasi warna hijau'
        }
    elif green_percentage > 40:
        return {
            'condition': 'Minor Disease',
            'confidence': (100 - green_percentage) / 100,
            'details': 'Terdapat tanda-tanda penyakit ringan'
        }
    else:
        return {
            'condition': 'Severe Disease',
            'confidence': (100 - green_percentage) / 100,
            'details': 'Terindikasi penyakit serius'
        }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Analisis gambar
        result = analyze_leaf_health(file_path)
        
        return jsonify({
            'class': result['condition'],
            'confidence': result['confidence'],
            'details': result['details'],
            'image_path': f'/static/uploads/{filename}'
        })

if __name__ == '__main__':
    app.run(debug=True)