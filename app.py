print("RUNNING APP FILE:", __file__)
from flask import Flask, render_template, request, redirect, send_from_directory, jsonify, session, flash, url_for
import numpy as np
import json
import uuid
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
import logging

from io import BytesIO




from datetime import datetime

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI')
if not MONGO_URI:
    raise RuntimeError("MONGO_URI not set in .env – please provide your MongoDB Atlas connection string")
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client['potato_disease_db']
users_collection = mongo_db['users']  # Store user credentials
predictions_collection = mongo_db['predictions']  # Store predictions
def save_prediction(label, confidence, cause, solution, is_healthy, image_data_uri):
    """Save prediction details to MongoDB.
    Parameters:
        label (str): Predicted disease label.
        confidence (float): Confidence percentage.
        cause (str): Cause description.
        solution (str): Suggested solution.
        is_healthy (bool): Whether prediction indicates healthy.
        image_data_uri (str): Base64 data URI of the uploaded image.
    """
    try:

     if 'user_id' not in session:
        return
     predictions_collection.insert_one({

        "user_id": session['user_id'],

        "label": label,
        "confidence": confidence,
        "cause": cause,
        "solution": solution,
        "is_healthy": is_healthy,
        "image": image_data_uri,

        "timestamp": datetime.utcnow()
    })

    except Exception as e:
     logging.error(
        'Failed to save prediction to MongoDB: %s',
        e
    )
os.environ["TF_DISABLE_ONEDNN"] = "1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
try:
    import tensorflow as tf
except Exception as e:
    logging.error('TensorFlow import failed: %s', e)
    tf = None
import os
import io
import base64
from PIL import Image
from datetime import datetime
try:
    from tensorflow.keras.applications.efficientnet_v2 import preprocess_input  # type: ignore
except Exception as e:
    print('preprocess_input import failed:', e)
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
        print('Model loading failed:', e)
        model = None
else:
    print('TensorFlow not available, model disabled')
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

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not (email and password):
            flash('Email and password required.', 'error')
            return render_template('signin.html')
        user = users_collection.find_one({'email': email})
        if not user:
            flash('No account with that email.', 'error')
            return render_template('signin.html')
        from werkzeug.security import check_password_hash
        if not check_password_hash(user['password'], password):
            flash('Incorrect password.', 'error')
            return render_template('signin.html')
        # login successful
        session['user_id'] = str(user['_id'])
        session['user_name'] = user.get('name')
        flash('Signed in successfully.', 'success')
        return redirect(url_for('home'))
    return render_template('signin.html')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        address = request.form.get('address')
        if not (name and email and password and address):
            flash('All fields are required.', 'error')
            return render_template('signup.html')
        # Check if user already exists
        if users_collection.find_one({'email': email}):
            flash('Email already registered.', 'error')
            return render_template('signup.html')
        from werkzeug.security import generate_password_hash
        hashed = generate_password_hash(password)
        users_collection.insert_one({
            'name': name,
            'email': email,
            'password': hashed,
            'address': address,
            'created_at': datetime.utcnow()
        })
        flash('Signup successful! Please sign in.', 'success')
        return redirect(url_for('signin'))
    return render_template('signup.html')


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
        session['last_prediction'] = {
    'label': label,
    'confidence': confidence,
    'cause': cause,
    'solution': solution,
    'is_healthy': is_healthy
}
        # Save prediction to MongoDB
        save_prediction(label, confidence, cause, solution, is_healthy, data_uri)

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

from bson import ObjectId

@app.route('/profile')
def profile():

    if 'user_id' not in session:
        return redirect(url_for('signin'))

    user = users_collection.find_one(
        {"_id": ObjectId(session['user_id'])}
    )

    return render_template(
        'profile.html',
        user=user
    )


@app.route('/update_profile', methods=['POST'])
def update_profile():

    if 'user_id' not in session:
        return redirect(url_for('signin'))

    users_collection.update_one(
        {"_id": ObjectId(session['user_id'])},
        {
            "$set": {
                "name": request.form['name'],
                "email": request.form['email'],
                "address": request.form['address']
            }
        }
    )

    session['user_name'] = request.form['name']

    flash('Profile updated successfully!', 'success')

    return redirect(url_for('profile'))


@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('home'))    


@app.route('/history')
def history():

    if 'user_id' not in session:
        return jsonify([])

    records = list(
        predictions_collection.find(
            {
                "user_id": session['user_id']
            }
        ).sort(
            "timestamp",
            -1
        )
    )

    history_data = []

    for item in records:

        history_data.append({
    "_id": str(item["_id"]),
    "label": item.get("label"),
    "confidence": item.get("confidence"),
    "timestamp": item.get("timestamp").strftime("%d %b %Y %H:%M"),
    "image": item.get("image")
})

    return jsonify(history_data)

from bson import ObjectId

@app.route('/history/<prediction_id>')
def history_detail(prediction_id):

    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    record = predictions_collection.find_one({
        "_id": ObjectId(prediction_id),
        "user_id": session['user_id']
    })

    if not record:
        return jsonify({"error": "Not Found"}), 404

    return jsonify({
        "image": record.get("image"),
        "label": record.get("label"),
        "confidence": record.get("confidence"),
        "cause": record.get("cause"),
        "solution": record.get("solution"),
        "timestamp": record.get("timestamp").strftime("%d %b %Y %H:%M")
    })

@app.route('/delete_history/<prediction_id>', methods=['DELETE'])
def delete_history(prediction_id):

    if 'user_id' not in session:
        return jsonify({
            "success": False
        }), 401

    try:

        result = predictions_collection.delete_one({

            "_id": ObjectId(prediction_id),

            "user_id": session['user_id']

        })

        return jsonify({
            "success": result.deleted_count > 0
        })

    except Exception as e:

        print("Delete Error:", e)

        return jsonify({
            "success": False
        }), 500
@app.route('/clear_history', methods=['DELETE'])
def clear_history():

    if 'user_id' not in session:
        return jsonify({
            "success": False
        }), 401

    result = predictions_collection.delete_many({

        "user_id": session['user_id']

    })

    return jsonify({
        "success": True,
        "deleted_count": result.deleted_count
    })

@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect(url_for('signin'))

    user_id = session['user_id']

    total_predictions = predictions_collection.count_documents({
        "user_id": user_id
    })

    healthy_count = predictions_collection.count_documents({
        "user_id": user_id,
        "is_healthy": True
    })

    disease_count = predictions_collection.count_documents({
        "user_id": user_id,
        "is_healthy": False
    })

    pipeline = [
        {
            "$match": {
                "user_id": user_id
            }
        },
        {
            "$group": {
                "_id": "$label",
                "count": {
                    "$sum": 1
                }
            }
        },
        {
            "$sort": {
                "count": -1
            }
        },
        {
            "$limit": 1
        }
    ]

    most_common = list(
        predictions_collection.aggregate(
            pipeline
        )
    )

    most_common_disease = (
        most_common[0]["_id"]
        if most_common
        else "None"
    )

    recent_prediction = predictions_collection.find_one(
        {
            "user_id": user_id
        },
        sort=[("timestamp", -1)]
    )

    return render_template(
        'dashboard.html',

        total_predictions=total_predictions,

        healthy_count=healthy_count,

        disease_count=disease_count,

        most_common_disease=most_common_disease,

        recent_prediction=recent_prediction
    )    
@app.route('/dashboard/trend')
def dashboard_trend():
    if 'user_id' not in session:
        return jsonify([])
    pipeline = [
        {"$match": {"user_id": session['user_id']}},
        {"$group": {"_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}}, "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    raw_data = list(predictions_collection.aggregate(pipeline))
    # Transform to friendly keys
    data = [{"date": item["_id"], "count": item["count"]} for item in raw_data]
    return jsonify(data)




if __name__ == "__main__":
    app.secret_key = os.getenv(
        'SECRET_KEY',
        'potato-plant-secret-key-123'
    )

    app.run(
        debug=True,
        use_reloader=False
    )

