# 🌿 Potato Plant Disease Recognition

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Framework](https://img.shields.io/badge/Framework-Flask-green)
![AI](https://img.shields.io/badge/AI-TensorFlow-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

A **Deep Learning based web application** that detects **potato plant diseases** from leaf images.

Users upload a potato leaf image and the system predicts whether the plant is **Healthy or affected by disease** using a trained TensorFlow model.

---

# 📑 Table of Contents

* Features
* Technologies Used
* Quick Start
* Model Download
* Run the Application
* Application Demo
* Requirements
* Author
* License

---

# 🚀 Features

* Upload potato leaf images
* Deep learning disease detection
* Confidence score for predictions
* Cause and solution for detected disease
* Simple and interactive Flask web interface

---

# 🛠 Technologies Used

* Python
* Flask
* TensorFlow / Keras
* HTML
* CSS
* JavaScript
* NumPy
* Pillow

---

# ⚡ Quick Start

Clone the repository:

```
git clone https://github.com/Akshay001-A/potato-plant-disease-recognition.git
```

Navigate to the project folder:

```
cd potato-plant-disease-recognition
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# 🧠 Model Download

The trained model is **not included in this repository** because it exceeds GitHub's file size limit.

Download the model from Google Drive:

https://drive.google.com/file/d/1jQLlUoyXaTr4wTnRKv-5uydloXUJnDQF/view

After downloading, place the file inside the **models** folder.

Example structure:

```
potato-plant-disease-recognition
│
├── app.py
├── plant_disease.json
├── README.md
├── LICENSE
├── requirements.txt
│
├── models
│   └── plant_disease_recog_model1.keras
│
├── static
├── templates
└── uploadimages
```

---

# ▶️ Run the Application

Start the Flask server:

```
python app.py
```

Open the browser:

```
http://127.0.0.1:5000
```



---

# 📷 Application Demo

### Home Page

![Home Page](images/home.png)

### Disease Prediction Result

![Prediction Result](images/prediction.png)



---

# 📦 Requirements

```
flask
tensorflow
keras
numpy
pillow
gdown
```

Install using:

```
pip install -r requirements.txt
```

---
# 👨‍💻 Authors

- **Akshay R** – [GitHub](https://github.com/Akshay001-A)
- **Charan Kumar R** - [GitHub](https://github.com/CharanKumarR)

---

# 📄 License

This project is licensed under the **MIT License**.

See the LICENSE file for more details.
