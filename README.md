# 🏋️ Squat AI Trainer

AI-powered real-time squat form analyzer built with Flask and Computer Vision.

This web application detects body landmarks using pose estimation and evaluates squat form quality in real time.

---

## 🚀 Features

- 📷 Real-time webcam integration
- 🦵 Knee angle calculation
- 🔢 Automatic rep counting
- 📊 Form score evaluation
- 🎯 Visual landmark skeleton overlay
- ⚡ Live feedback system

---

## 🧠 How It Works

1. The webcam stream is captured in the browser.
2. Each frame is sent to the Flask backend.
3. Pose landmarks are extracted using a pose detection model.
4. Knee angle is calculated using joint coordinates.
5. Squat depth and posture quality are evaluated.
6. Score and feedback are returned to the frontend.
7. Landmarks are drawn over the video in real-time.

---

## 🛠 Technologies Used

- Python
- Flask
- MediaPipe (Pose Estimation)
- OpenCV
- JavaScript
- HTML / CSS

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/squat-ai-trainer.git
cd squat-ai-trainer

Create virtual environment:
python -m venv venv

Activate:
Windows:
venv\Scripts\activate
Mac/Linux:
source venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Run the application:
python app.py

Open in browser:
http://127.0.0.1:5000

👨‍💻 Author:

Hamza Şenyüz
Computer Engineering Student
