from flask import Flask, render_template, request, redirect, send_from_directory
import numpy as np
import json
import uuid
import tensorflow as tf
import os
from tensorflow.keras.applications.efficientnet_v2 import preprocess_input  # type: ignore

from werkzeug.utils import secure_filename
from config import Config

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config.from_object(Config)

# Load trained model
model = tf.keras.models.load_model(app.config['MODEL_PATH'])

# Load class names
with open(app.config['CLASS_NAMES_PATH'], "r") as file:
    class_names = json.load(file)

# ---------------------- GAP 2: CAUSE & SOLUTION ----------------------
disease_info = {
    "Bacteria": {
        "cause": "Caused by bacterial pathogens infecting potato leaves.",
        "solution": "Remove infected leaves, improve drainage, and apply copper-based bactericides."
    },
    "Fungi": {
        "cause": "Caused by Alternaria or other fungal infections.",
        "solution": "Use fungicides such as chlorothalonil or mancozeb."
    },
    "Healthy": {
        "cause": "No signs of disease or infection detected.",
        "solution": "Maintain proper watering, spacing, and field hygiene."
    },
    "Nematode": {
        "cause": "Caused by parasitic nematodes damaging the roots.",
        "solution": "Use nematicides, crop rotation, and sterilized soil."
    },
    "Pest": {
        "cause": "Damage caused by insects like beetles or leaf miners.",
        "solution": "Use neem oil, insecticidal soap, or biological pest control."
    },
    "Phytopthora": {
        "cause": "Caused by Phytophthora infestans (late blight pathogen).",
        "solution": "Apply metalaxyl-based fungicides and increase plant spacing."
    },
    "Virus": {
        "cause": "Caused by viral infections spread by aphids or whiteflies.",
        "solution": "Remove infected plants, use certified seeds, and control insect vectors."
    }
}
# ---------------------------------------------------------------------

@app.route('/uploadimages/<path:filename>')
def uploaded_images(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def home():
    return render_template('home.html')

def extract_features(image_path):
    """Load and preprocess image for EfficientNetV2"""
    img = tf.keras.utils.load_img(image_path, target_size=(420, 420))
    img = tf.keras.utils.img_to_array(img)

    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    return img

def model_predict(image_path):
    """Predict disease"""
    img = extract_features(image_path)
    predictions = model.predict(img)[0]

    index = np.argmax(predictions)
    predicted_label = class_names[index]
    confidence = float(predictions[index] * 100)

    return predicted_label, confidence

@app.route('/upload/', methods=['POST'])
def uploadimage():
    if 'img' not in request.files:
        return redirect('/')
    
    image = request.files['img']
    
    if image.filename == '':
        return redirect('/')
        
    if image and allowed_file(image.filename):
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        filename = secure_filename(image.filename)
        temp_name = f"{app.config['UPLOAD_FOLDER']}/temp_{uuid.uuid4().hex}_{filename}"
        image.save(temp_name)

        # Predict class + confidence
        try:
            label, confidence = model_predict(temp_name)
        except Exception as e:
            # Safely catch any TensorFlow/Keras or Image processing errors
            return render_template('home.html', error="Failed to analyze image. The image might be corrupted or unreadable.")

        # Get cause & solution (GAP 2)
        cause = disease_info.get(label, {}).get("cause", "Unknown cause")
        solution = disease_info.get(label, {}).get("solution", "No solution found")
        is_healthy = ("healthy" in label.lower())

        return render_template(
            'home.html',
            result=True,
            imagepath='/' + temp_name,
            prediction=label,
            confidence=round(confidence, 2),
            cause=cause,
            solution=solution,
            is_healthy=is_healthy
        )
    else:
        return render_template('home.html', error="Invalid file type. Please upload a PNG, JPG, or JPEG image.")

if __name__ == "__main__":
    app.run(debug=True)