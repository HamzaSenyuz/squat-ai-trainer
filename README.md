# AI Form Analyzer

> Real-time exercise form analysis powered by computer vision and pose estimation.

Live demo → [ai-form-analyzer on Render](https://squat-ai-trainer.onrender.com)

---

## Overview

AI Form Analyzer is a browser-based fitness application that uses **MediaPipe Pose** to detect body landmarks in real time via webcam, calculates joint angles using vector mathematics, and evaluates exercise form quality frame by frame — with no backend processing required for the CV pipeline.

The project was built as a computer engineering AI course project, demonstrating applied computer vision, real-time signal processing, and rule-based biomechanical analysis.

---

## Features

| Feature | Description |
|---|---|
| 🎯 Real-time pose detection | MediaPipe Pose runs entirely in the browser via WebAssembly |
| 🦴 Joint angle calculation | Vector-based angle math on 33 body landmarks |
| 🏋️ 5 exercise modes | Squat, Push-up, Plank, Lunge, Sit-up |
| 📊 Form scoring | Weighted multi-factor score per frame (0–100%) |
| 🔢 Automatic rep counting | Stage machine (UP/DOWN) triggered by angle thresholds |
| ⏱ Plank hold timer | Timer runs only while form is correct |
| 🎯 Goal system | Set a rep target — progress bar tracks completion |
| 🔊 Voice feedback | Web Speech API announces reps and form errors |
| ⟺ Mirror mode | Horizontally flips the canvas for natural self-view |
| 📋 Form guide | Exercise-specific coaching tips per mode |
| 📈 Session summary | Avg score, best score, top errors after each session |

---

## How It Works

### 1. Pose Estimation (MediaPipe)

MediaPipe Pose detects **33 3D body landmarks** from each video frame. Each landmark contains normalized `x`, `y`, `z` coordinates and a `visibility` confidence score. The model runs client-side via WebAssembly — no video data is ever sent to a server.

```
Landmark indices used:
  0  = Nose
 11  = Left shoulder    12 = Right shoulder
 13  = Left elbow       14 = Right elbow
 15  = Left wrist       16 = Right wrist
 23  = Left hip         24 = Right hip
 25  = Left knee        26 = Right knee
 27  = Left ankle       28 = Right ankle
```

### 2. Angle Calculation

Joint angles are calculated using the **arctangent of two vectors** originating from the middle joint:

```javascript
function calcAngle(a, b, c) {
    const r = Math.atan2(c.y - b.y, c.x - b.x)
            - Math.atan2(a.y - b.y, a.x - b.x);
    let deg = Math.abs(r * 180 / Math.PI);
    return deg > 180 ? 360 - deg : deg;
}
```

This computes the angle at joint `b` formed by the vectors `b→a` and `b→c`.

### 3. Exercise Analysis

Each exercise uses a dedicated analysis function:

| Exercise | Primary angle | Rep trigger | Key checks |
|---|---|---|---|
| Squat | Hip–Knee–Ankle | < 90° → DOWN, > 160° → UP | Knee over toe, forward lean, depth |
| Push-up | Shoulder–Elbow–Wrist | < 90° → DOWN, > 155° → UP | Body alignment, elbow flare |
| Plank | Shoulder–Hip–Ankle | — (hold timer) | Hip sag, head drop |
| Lunge | Hip–Knee–Ankle | < 100° → DOWN, > 155° → UP | Knee forward, torso lean, depth |
| Sit-up | Shoulder–Hip–Knee | > 140° → DOWN, < 70° → UP | Neck pull, range of motion |

### 4. Form Scoring

Each frame produces a composite score (0–100%) from weighted sub-scores:

**Squat example:**
```
depthScore  = max(0, 100 - |angle - 90| × 2)       → weight 50%
kneeScore   = knee.x ≤ ankle.x ? 100 : 50           → weight 25%
torsoScore  = max(0, 100 - |forwardLean - 15| × 3)  → weight 25%
finalScore  = depthScore×0.5 + kneeScore×0.25 + torsoScore×0.25
```

Score color coding: `< 50%` red · `50–75%` amber · `≥ 75%` green

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask, Gunicorn |
| Frontend | Vanilla JavaScript, HTML5, CSS3 |
| CV / AI | MediaPipe Pose (WebAssembly, client-side) |
| Fonts | Bebas Neue, DM Mono, Inter (Google Fonts) |
| Voice | Web Speech API (browser-native) |
| Deploy | Render (PaaS) |

> **Note:** OpenCV is not used — all pose estimation runs in the browser via MediaPipe's JavaScript SDK. The Flask backend only serves the HTML template.

---

## Project Structure

```
ai-form-analyzer/
├── app.py               # Flask app — single route serves index.html
├── requirements.txt     # Flask + Gunicorn
├── runtime.txt          # Python version for Render
├── templates/
│   └── index.html       # Full application (CV pipeline, UI, logic)
└── static/
    └── style.css        # (legacy — styles now embedded in index.html)
```

---

## Installation & Running Locally

```bash
# 1. Clone
git clone https://github.com/HamzaSenyuz/squat-ai-trainer.git
cd squat-ai-trainer

# 2. Create virtual environment
python -m venv venv

# 3. Activate
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run
python app.py
```

Open in browser: `http://127.0.0.1:5000`

> Allow camera access when prompted. Works best with good lighting and full-body visibility.

---

## Deployment (Render)

1. Push to GitHub
2. Create a new **Web Service** on [render.com](https://render.com)
3. Connect the GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn app:app`
6. Deploy

---

## Angle Thresholds — Biomechanical Basis

| Exercise | Threshold | Rationale |
|---|---|---|
| Squat depth | < 90° knee angle | Thigh parallel to floor = full squat (NSCA standard) |
| Squat lockout | > 160° | Near-full extension without hyperextension |
| Push-up bottom | < 90° elbow | Standard full range of motion |
| Plank body line | > 160° hip angle | Deviation > 10° from neutral indicates compensations |
| Sit-up top | < 70° torso angle | Torso vertical = full contraction |
| Lunge depth | < 100° knee angle | Front thigh approaching parallel |

---

## Author

**Hamza Şenyüz**  
Computer Engineering Student  
[github.com/HamzaSenyuz](https://github.com/HamzaSenyuz)
