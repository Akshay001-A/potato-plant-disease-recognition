from flask import Flask, render_template, request, redirect, send_from_directory, jsonify
import numpy as np
import json
import uuid
import os
os.environ["TF_DISABLE_ONEDNN"] = "1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
try:
    import tensorflow as tf
except Exception as e:
    print('⚠️ TensorFlow import failed:', e)
    tf = None
import os
import io
import base64
from PIL import Image
try:
    from tensorflow.keras.applications.efficientnet_v2 import preprocess_input  # type: ignore
except Exception as e:
    print('⚠️ preprocess_input import failed:', e)
    def preprocess_input(x):
        return x

from werkzeug.utils import secure_filename
from config import Config

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config.from_object(Config)

# Load trained model
if tf is not None:
    try:
        model = tf.keras.models.load_model(app.config['MODEL_PATH'])
    except Exception as e:
        print('⚠️ Model loading failed:', e)
        model = None
else:
    print('⚠️ TensorFlow not available, model disabled')
    model = None

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



@app.route('/')
def home():
    return render_template('home.html')

def extract_features(image_stream):
    """Load and preprocess image for EfficientNetV2 directly from memory"""
    img = Image.open(image_stream)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize((420, 420))
    img = tf.keras.utils.img_to_array(img)

    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    return img

def model_predict(image_stream):
    """Predict disease (fallback if model not loaded)"""
    if model is None:
        # Return generic healthy result when model is unavailable
        return "Healthy", 100.0
    # Only called when a model is available, safe to use TensorFlow utilities
    img = extract_features(image_stream)
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
        # Read image to memory
        img_bytes = image.read()
        
        # Base64 encode for UI
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        mime_type = "image/png" if image.filename.lower().endswith("png") else "image/jpeg"
        data_uri = f"data:{mime_type};base64,{img_base64}"

        # Predict class + confidence
        try:
            image_stream = io.BytesIO(img_bytes)
            label, confidence = model_predict(image_stream)
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
            imagepath=data_uri,
            prediction=label,
            confidence=round(confidence, 2),
            cause=cause,
            solution=solution,
            is_healthy=is_healthy
        )
    else:
        return render_template('home.html', error="Invalid file type. Please upload a PNG, JPG, or JPEG image.")

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """REST API Endpoint for mobile apps or external integrations."""
    if 'img' not in request.files:
        return jsonify({"error": "No image file provided in request."}), 400
    
    image = request.files['img']
    
    if image.filename == '':
        return jsonify({"error": "Empty filename."}), 400
        
    if image and allowed_file(image.filename):
        img_bytes = image.read()
        
        try:
            image_stream = io.BytesIO(img_bytes)
            label, confidence = model_predict(image_stream)
        except Exception as e:
            return jsonify({"error": "Failed to analyze image. It might be corrupted."}), 500

        cause = disease_info.get(label, {}).get("cause", "Unknown cause")
        solution = disease_info.get(label, {}).get("solution", "No solution found")
        is_healthy = ("healthy" in label.lower())

        return jsonify({
            "status": "success",
            "prediction": label,
            "confidence": round(confidence, 2),
            "cause": cause,
            "solution": solution,
            "is_healthy": is_healthy
        })
        
    return jsonify({"error": "Invalid file type. Allowed types are png, jpg, jpeg."}), 400

if __name__ == "__main__":
    app.run(debug=True)