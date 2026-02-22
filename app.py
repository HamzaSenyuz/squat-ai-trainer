from flask import Flask, render_template, request, jsonify
import base64
import cv2
import numpy as np
import math
import os

import mediapipe as mp




app = Flask(__name__)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=0,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

rep_count = 0
squat_stage = "UP"


def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
              np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return angle


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    global rep_count, squat_stage

    data = request.json["image"]
    image_data = base64.b64decode(data.split(",")[1])
    np_arr = np.frombuffer(image_data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    # 🔥 BURADA angle alanını ekledik
    response_data = {
        "reps": rep_count,
        "quality": "",
        "error": False,
        "score": 0,
        "landmarks": [],
        "angle": 0   # ✅ Yeni eklenen alan
    }

    try:
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            for lm in landmarks:
                response_data["landmarks"].append([lm.x, lm.y])

            shoulder = [landmarks[11].x, landmarks[11].y]
            hip = [landmarks[23].x, landmarks[23].y]
            knee = [landmarks[25].x, landmarks[25].y]
            ankle = [landmarks[27].x, landmarks[27].y]

            angle = calculate_angle(hip, knee, ankle)

            # 🔥 Angle'ı frontend'e gönderiyoruz
            response_data["angle"] = int(angle)

            # REP LOGIC
            if angle < 90:
                squat_stage = "DOWN"

            if angle > 160 and squat_stage == "DOWN":
                squat_stage = "UP"
                rep_count += 1

            # DEPTH ANALYSIS
            if 80 < angle < 100:
                response_data["quality"] = "Good Depth"
            elif angle <= 80:
                response_data["quality"] = "Too Deep"
                response_data["error"] = True
            elif 100 <= angle < 140:
                response_data["quality"] = "Half Squat"
                response_data["error"] = True

            # KNEE CHECK
            if knee[0] > ankle[0]:
                response_data["quality"] = "Knee Too Forward"
                response_data["error"] = True

            # TORSO CHECK
            dx = shoulder[0] - hip[0]
            dy = shoulder[1] - hip[1]
            torso_angle = abs(math.degrees(math.atan2(dy, dx)))
            forward_lean = abs(90 - torso_angle)

            if forward_lean > 30:
                response_data["quality"] = "Too Much Forward Lean"
                response_data["error"] = True

            # SCORE SYSTEM
            ideal_angle = 90
            depth_diff = abs(angle - ideal_angle)
            depth_score = max(0, 100 - depth_diff * 2)

            knee_score = 100 if knee[0] <= ankle[0] else 50

            ideal_forward = 15
            forward_diff = abs(forward_lean - ideal_forward)
            torso_score = max(0, 100 - forward_diff * 3)

            final_score = int(
                depth_score * 0.5 +
                knee_score * 0.25 +
                torso_score * 0.25
            )

            response_data["score"] = final_score
            response_data["reps"] = rep_count

    except Exception as e:
        print("Hata:", e)

    return jsonify(response_data)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)