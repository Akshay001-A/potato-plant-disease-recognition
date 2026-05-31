import os

class Config:
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'potato-plant-secret-key-123'
    
    # Upload Settings
    UPLOAD_FOLDER = 'uploadimages'
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # Limits uploads to 2 MB to prevent abuse
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    
    # Model & Data Paths
    MODEL_PATH = 'models/plant_disease_recog_model1.keras'
    CLASS_NAMES_PATH = 'plant_disease.json'
