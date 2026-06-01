<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:134E5E,50:71B280,100:A8E063&height=260&section=header&text=Potato%20Plant%20Disease%20Recognition&fontSize=38&fontColor=ffffff&animation=fadeIn&fontAlignY=40"/>

# 🌿 Potato Plant Disease Recognition

### 🧠 AI-Powered Deep Learning Based Plant Disease Detection System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/Flask-Web_App-black?style=for-the-badge&logo=flask"/>
  <img src="https://img.shields.io/badge/TensorFlow-Deep_Learning-orange?style=for-the-badge&logo=tensorflow"/>
  <img src="https://img.shields.io/badge/Keras-Neural_Networks-red?style=for-the-badge&logo=keras"/>
  <img src="https://img.shields.io/badge/MongoDB-Atlas_Database-green?style=for-the-badge&logo=mongodb"/>
  <img src="https://img.shields.io/badge/Docker-Containerization-blue?style=for-the-badge&logo=docker"/>
</p>

---

### 🚀 Detect Potato Plant Diseases Using Deep Learning & Image Classification

📷 Upload Leaf Images • 🧠 In-Memory AI Prediction • 🌱 7 Disease Classes Recognition • 📊 Live Metrics & History Dashboard • 💡 Cause & Treatment

</div>

---

# 🌟 Project Overview

**Potato Plant Leaf Disease Recognition** is a production-grade, AI-powered web ecosystem designed to help farmers, agriculturalists, and researchers diagnose plant leaf diseases instantly. By leveraging deep learning models, the system automates leaf health assessment directly from uploaded images.

The system is trained using a **Convolutional Neural Network (CNN)** (EfficientNetV2 based architecture) and supports classification across **7 different health and disease classes**:

*   **Bacteria** (Bacterial infections)
*   **Fungi** (Fungal spot infections)
*   **Healthy** (Optimal plant leaf state)
*   **Nematode** (Parasitic worm damage)
*   **Pest** (Insect or beetle leaf damage)
*   **Phytopthora** (Late Blight pathogen)
*   **Virus** (Viral leaf diseases)

To provide an elite user experience, the system includes:
*   **🔐 Complete Authentication System:** Secured sign-up/sign-in flows with encrypted password hashing.
*   **⚡ Zero-Disk Storage Pipeline:** In-memory, non-disk image classification utilizing `BytesIO` streams.
*   **📁 MongoDB Atlas Integration:** Persistent profiles and chronological leaf diagnosis history records.
*   **🔄 Interactive Logs Sidebar:** Complete with thumbnail grids, modal-based detailed reviews, and CRUD history controls.
*   **📊 Statistics & Analytics Dashboard:** Visual counter cards displaying user statistics and infection trend insights.
*   **🌐 REST API Integration:** Dedicated `/api/predict` endpoint for mobile or external hardware integration.
*   **🐳 Dockerized Container Environment:** Ready-to-go multi-stage container configuration.

---

# ✨ Core Features

### 🌿 1. Deep Learning Image Recognition
*   Drag-and-drop or file selector leaf uploads.
*   In-memory Pillow preprocessor streams (no temp files created on the server's hard drive).
*   Live confidence progress bars featuring contextual color styles based on diagnostics (Green for Healthy, Red for Diseased).

### 💡 2. Live Actionable Diagnostics
*   Instantly maps the predicted class to localized **Cause** and **Recommended Solution** guides.
*   Assists farmers with immediate prevention strategies (e.g. copper-based bactericides, fungicides, nematicides, crop spacing).

### 📁 3. Interactive Chronological Log History
*   **Historical Sidebar Grid:** Displays thumbnail previews, date, time, and predicted labels for past uploads.
*   **Dynamic Detailed Modals:** Click on any past prediction to view a detailed popup with the original image, classification scores, and complete disease information.
*   **History Controls:** Provides tools to delete individual records or clean the entire history stack.

### 🔐 4. Secured Authentication & Profile System
*   Register users with Name, Email, Address, and credentials.
*   Uses `werkzeug.security` secure password hashing rules.
*   Custom profile manager panel to update user info on-the-fly.

### 📊 5. Statistics Dashboard
*   Summarizes diagnostic insights into visually aesthetic metric cards:
    *   **Total Predictions Logged**
    *   **Healthy Leaves Checked**
    *   **Diseased Leaves Diagnosed**
    *   **Most Common Infection Found**
*   Includes trend and recent activity panels.

### 🌐 6. REST API Endpoint
*   Exposes a high-performance POST endpoint at `/api/predict` for external integrations (Mobile apps, drones, IoT hardware).
*   Returns JSON structures with labels, confidence scores, and crop care recommendations.

---

# 🛠 Tech Stack

| Component | Technologies Used |
|---|---|
| **Backend Engine** | Flask, Python, Werkzeug Security, python-dotenv |
| **Deep Learning & AI** | TensorFlow, Keras, EfficientNetV2, NumPy |
| **Image Pipeline** | Pillow (PIL), BytesIO, Base64 URI Encoding |
| **Database** | MongoDB Atlas, PyMongo, BSON ObjectId |
| **Containerization** | Docker, multi-stage debian-slim build |
| **Frontend UI/UX** | HTML5, Modern HSL CSS3, JavaScript, FontAwesome Icons, Poppins Font |

---

# 📸 Application Screenshots

### 🏠 Home Page
Modern image upload interface featuring loading overlays and animated particle backgrounds:
<img src="https://raw.githubusercontent.com/Akshay001-A/potato-plant-disease-recognition/main/static/images/planthome.png" width="100%"/>

---

### 📊 Disease Prediction Result
AI prediction result card displaying the classified label, confidence progress bars, and localized solutions:
<img src="https://raw.githubusercontent.com/Akshay001-A/potato-plant-disease-recognition/main/static/images/prediction.png" width="100%"/>

---

### 🗂 Prediction History Sidebar
Slide-out panel showcasing chronologically ordered past records with thumbnails and quick deletion actions:
<img src="https://raw.githubusercontent.com/Akshay001-A/potato-plant-disease-recognition/main/static/images/history_sidebar.png" width="100%"/>

---

### 📈 Statistics & Analytics Dashboard
Visual summary metrics detailing total diagnoses, healthy leaf logs, diseased leaf logs, and most common infection profiles:
<img src="https://raw.githubusercontent.com/Akshay001-A/potato-plant-disease-recognition/main/static/images/dashboard.png" width="100%"/>

---

### 🔍 History Detail Popup Modal
A clean diagnostic overlay revealing original uploaded plant images, prediction confidences, and precise crop treatment actions:
<img src="https://raw.githubusercontent.com/Akshay001-A/potato-plant-disease-recognition/main/static/images/history_detail.png" width="100%"/>

---

### 👤 Glassmorphism User Profile Manager
A premium profile management screen enabling custom credential updates and secure sign-out flows:
<img src="https://raw.githubusercontent.com/Akshay001-A/potato-plant-disease-recognition/main/static/images/user_profile.png" width="100%"/>

---

# 🧬 Leaf Diagnosis Classes

| Class | Type | Diagnostic Condition | Care Strategy |
|---|---|---|---|
| **Healthy** | ✅ Optimal | Free of pathogens or leaf spots | Maintain irrigation and field hygiene |
| **Bacteria** | ❌ Infection | Pathogenic bacterial leaf damage | Use copper-based bactericides |
| **Fungi** | ❌ Infection | Fungal spot lesions (Alternaria) | Apply chlorothalonil or mancozeb |
| **Nematode** | ❌ Parasitic | Microscopic worm root/vascular damage | Soil sterilization and crop rotation |
| **Pest** | ❌ Infestation | Visual leaf chewing damage (beetles) | Apply neem oil or insecticidal soap |
| **Phytopthora** | ❌ Blight | Late Blight leaf decay | Metalaxyl-based treatments & spacing |
| **Virus** | ❌ Pathogen | Deformed leaves & chlorotic veins | Remove host vector insects like aphids |

---

# ⚡ Quick Start

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Akshay001-A/potato-plant-disease-recognition.git
cd potato-plant-disease-recognition
```

### 2️⃣ Configure Environments
Create a `.env` file in the root directory and add your secret credentials:
```env
SECRET_KEY=your_flask_secret_key_here
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/potato_disease_db
```

### 3️⃣ AI Model Setup
The trained deep learning model is not pushed to the repository due to its large size.
*   **Download Link:** [Google Drive Model Download](https://drive.google.com/file/d/1jQLlUoyXaTr4wTnRKv-5uydloXUJnDQF/view)
*   Place the downloaded `.keras` file in:
    ```text
    models/plant_disease_recog_model1.keras
    ```

---

# 🐳 Running with Docker

This application is fully containerized! You can build and spin up the microservice within seconds.

### 🛠 Build the Docker Image
```bash
docker build -t potato-disease-app .
```

### 🚀 Run the Container
Pass your environment variables or point to your `.env` file to launch:
```bash
docker run -p 5000:5000 --env-file .env potato-disease-app
```
Access the application on: **`http://localhost:5000`**

---

# 📂 Expected Project Structure

```text
potato-plant-disease-recognition/
├── models/
│   └── plant_disease_recog_model1.keras    # Deep Learning Model
├── static/
│   ├── css/
│   │   ├── style.css                      # Base layout styles
│   │   ├── sidebar.css                    # History slider UI
│   │   ├── dashboard.css                  # Stats styling
│   │   ├── profile.css                    # User profile layouts
│   │   ├── signin.css
│   │   └── signup.css
│   └── images/
├── templates/
│   ├── home.html                           # Main app shell
│   ├── sidebar.html                        # Logs sidebar fragment
│   ├── dashboard.html                      # Interactive analytics
│   ├── profile.html                        # Account manager
│   ├── signin.html                         # Login screen
│   └── signup.html                         # Signup screen
├── app.py                                  # Core Flask Application
├── config.py                               # Global Configuration Setup
├── plant_disease.json                      # Disease labels index
├── Dockerfile                              # Multi-stage Container script
├── requirements.txt                        # App dependencies
└── README.md                               # Project documentation
```

---

# 🔍 Internal Pipeline & Workflow

```text
[User Uploads Image] 
         │
         ▼
[BytesIO Memory Stream] ──► (No files saved to host disk)
         │
         ▼
[EfficientNetV2 Preprocessing] (Resized to 420x420, normalized)
         │
         ▼
[Deep Learning Model Prediction] ──► (Keras Classification Inference)
         │
         ▼
[MongoDB Persistence] ──► (Saves prediction log + base64 image data to predictions collection)
         │
         ▼
[Dynamic Render Output] ──► (Displays color-coded results, solutions, and updates sidebar logs)
```

---

# 👨‍💻 Development Team

<div align="center">

# Akshay R 🚀
### AI & Full Stack Developer

<p align="center">
  <a href="https://github.com/Akshay001-A">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github"/>
  </a>
  <a href="https://www.linkedin.com/in/akshayofficial0207">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin"/>
  </a>
  <a href="https://www.instagram.com/akshay_authentic">
    <img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram"/>
  </a>
</p>

---

## 🤝 Contributors

### Charan Kumar R
<a href="https://github.com/Charan-Kumarr">
  <img src="https://img.shields.io/badge/GitHub-Charan--Kumarr-181717?style=for-the-badge&logo=github"/>
</a>

</div>

---

# 📄 License

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.

---

<div align="center">

# ⭐ Thanks for Visiting Our Project ⭐

### 🌱 AI for Smart & Sustainable Agriculture 🌿

<img src="https://readme-typing-svg.herokuapp.com?font=Poppins&size=24&duration=3000&color=6BCB77&center=true&vCenter=true&width=850&lines=Deep+Learning+Based+Plant+Disease+Detection;TensorFlow+%2B+Flask+%2B+MongoDB+Ecosystem;Dockerized+Microservice+Architecture;AI+for+Smart+Agriculture+%F0%9F%8C%BF"/>

</div>
