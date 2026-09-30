# 🛡️ AI Road Guardian
### *AI-Powered Real-Time Driver Safety & Risk Monitoring Assistant*

[![Snapdragon AI Lab Challenge 2026](https://img.shields.io/badge/Snapdragon%20AI%20Lab-Challenge%202026-0066CC?style=for-the-badge&logo=qualcomm)](https://github.com/abhishek160108/AI-Road-Guardian)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![YOLO11](https://img.shields.io/badge/Model-YOLO11n-00FFFF?style=for-the-badge)](https://github.com/ultralytics/ultralytics)
[![MediaPipe](https://img.shields.io/badge/Vision-MediaPipe%20Face%20Mesh-FF6F00?style=for-the-badge)](https://developers.google.com/mediapipe)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![Privacy 100% Local](https://img.shields.io/badge/Privacy-100%25%20Edge%20Local-success?style=for-the-badge&logo=shield)](https://github.com/abhishek160108/AI-Road-Guardian)

> **"AI Road Guardian is an on-device AI driver-safety co-pilot that detects phone usage and drowsiness in real time, calculates driver risk, and provides immediate voice warnings before unsafe behaviour can lead to an accident."**

---

## 📌 1. Project Title & Overview
**AI Road Guardian** is a real-time, privacy-preserving driver monitoring assistant designed for the **Snapdragon AI Lab Build & Present Challenge 2026**. Running locally on Windows laptops and Snapdragon-powered PCs, the system continuously analyzes driver alertness via a standard webcam, quantifies risk, and delivers proactive multimodal visual and audio warnings.

---

## 🚨 2. The Problem
- **Mobile Phone Distraction**: Looking at a smartphone while driving increases crash probability by $>400\%$.
- **Driver Fatigue & Microsleep**: Fatigue is responsible for thousands of highway fatalities each year due to delayed reaction times and brief moments of inattention.
- **Cloud Latency & Privacy Risks**: Uploading cabin video to the cloud introduces network latency that can be fatal in critical moments, while simultaneously violating driver privacy.

---

## 💡 3. The Solution
**AI Road Guardian** executes 100% on the local device edge:
- **Instant Response**: Sub-second risk scoring and immediate local voice intervention.
- **Complete Privacy**: Zero camera frames or biometric landmarks leave the user's device.
- **Actionable Telemetry**: Real-time cockpit dashboard displaying risk levels, incident statistics, and session logs.

---

## ⚡ 4. Key Features
- 📱 **Real-Time Phone Detection**: YOLO11n object detector identifies cell phone usage.
- 😴 **Drowsiness & Microsleep Tracking**: MediaPipe Face Mesh extracts eye landmarks to compute Eye Aspect Ratio (EAR).
- 📊 **Dynamic Driver Risk Scoring**: Calculates cumulative risk ($0–100$) mapped to Low, Medium, and High risk tiers.
- 🗣️ **Thread-Safe Local Voice Warnings**: Offline text-to-speech (pyttsx3/SAPI5) with a 5-second cooldown.
- 🚨 **High-Risk Escalation Warning**: Immediate urgent alert when both phone use and drowsiness coincide.
- 📈 **Streamlit Safety Dashboard**: Modern cockpit displaying live telemetry, EAR gauges, and incident logs.
- 🔒 **Edge-First Architecture**: Operates fully offline without internet or API keys.

---

## 🏗️ 5. System Architecture

```text
       Camera Stream (Webcam)
                 │
                 ▼
          OpenCV Preprocessing
                 │
      ┌──────────┴──────────┐
      ▼                     ▼
 YOLO11n Detector    MediaPipe Face Mesh
 (Class 67, >0.40)   (468 Landmarks, EAR)
      │                     │
Phone Detection        Eye Closure /
    State               Drowsiness
      │                     │
      └──────────┬──────────┘
                 ▼
        Risk Scoring Engine
  (Phone: +40 | Drowsy: +50 | Max: 100)
                 │
     ┌───────────┼───────────┐
     ▼           ▼           ▼
Visual HUD   Voice Alert  Atomic Telemetry
  (OpenCV)    (pyttsx3)   (telemetry.json)
                             │
                             ▼
                    Streamlit Dashboard
                 (Live Cockpit & Log Table)
```

---

## 🔬 6. AI Detection Pipeline & Algorithms

### A. Phone Detection
- **Model**: YOLO11 nano (`yolo11n.pt`)
- **Target Class**: COCO Class `67` (*cell phone*)
- **Confidence Threshold**: $\ge 0.40$

### B. Drowsiness Detection (Eye Aspect Ratio — EAR)
Six 3D facial landmarks are tracked per eye:
- **Left Eye Indices**: `[33, 160, 158, 133, 153, 144]`
- **Right Eye Indices**: `[362, 385, 387, 263, 373, 380]`

The **Eye Aspect Ratio (EAR)** formula:
$$\text{EAR} = \frac{\|p_2 - p_6\| + \|p_3 - p_5\|}{2 \cdot \|p_1 - p_4\|}$$

- **Threshold**: $\text{EAR} < 0.25$ indicates eye closure.
- **Trigger**: $\ge 15$ consecutive closed-eye frames triggers a drowsiness event.

### C. Risk Scoring Matrix

$$\text{Risk Score} = \min(100, \text{Phone Risk (40)} + \text{Drowsiness Risk (50)})$$

| Risk Score | Risk Tier | Action Taken |
| :--- | :--- | :--- |
| **0 – 39** | 🟢 **LOW RISK** | Normal monitoring (Green HUD) |
| **40 – 69** | 🟡 **MEDIUM RISK** | Warning alert (Yellow banner + Voice prompt) |
| **70 – 100** | 🔴 **HIGH RISK** | Critical emergency alert (Red HUD + High-Risk Voice) |

### D. Voice Alert System
- **Engine**: Windows SAPI5 via `pyttsx3`
- **Worker Architecture**: Dedicated daemon audio worker thread with `queue.Queue` to prevent OpenCV frame drops.
- **Cooldown**: 5.0-second cooldown per alert type.
- **Phrases**:
  - *Phone Warning*: `"Warning! Please put your phone down."`
  - *Drowsiness Warning*: `"Warning! You appear to be drowsy. Please take a break."`
  - *High-Risk Combined*: `"Warning! High risk detected. Please focus on driving."`

---

## 📊 7. Streamlit Live Dashboard

The web dashboard (`dashboard.py`) provides:
1. **Live System Status**: `🟢 ONLINE` / `🔴 OFFLINE` indicator.
2. **Main KPI Cards**: Driver Status, Phone Status, Drowsiness Status, and Overall Risk Score.
3. **Risk Analysis**: Animated progress gauge with dynamic color coding.
4. **Live Driver Metrics**: Real-time EAR, camera FPS, and session trip timer.
5. **Incident Counters**: Total trip phone and drowsiness events.
6. **Session Alert Log**: Searchable history table of triggered events.

---

## 🛠️ 8. Technologies Used

- **Python 3.11**: Core runtime.
- **OpenCV**: Video capture, frame transformations, HUD graphics.
- **Ultralytics YOLO11n**: Mobile phone object detection.
- **MediaPipe Face Mesh**: 468 facial landmark extraction.
- **pyttsx3 & pywin32**: Windows SAPI5 offline voice generation.
- **Streamlit**: Web-based live monitoring cockpit.
- **JSON Telemetry Bridge**: Atomic local IPC between detector and dashboard.

---

## 🚀 9. Installation & Setup

```bash
# 1. Clone repository
git clone https://github.com/abhishek160108/AI-Road-Guardian.git
cd AI-Road-Guardian

# 2. Create & activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 🎮 10. How to Run

```bash
# Run AI detector with voice warnings
python app_voice.py

# Run silent visual detector
python app.py

# Launch the live dashboard (in a separate terminal)
streamlit run dashboard.py
```

*Press **'Q'** on the camera window to exit cleanly.*

---

## 📁 11. Project Directory Structure

```text
AI-Road-Guardian/
├── .gitignore               # Excludes .venv, cache, local logs, secrets
├── requirements.txt         # Minimal pinned dependencies
├── README.md                # Comprehensive documentation
├── DEMO_SCRIPT.md           # 90-second hackathon presentation script
├── FINAL_SUBMISSION.md      # Final submission package summary
│
├── app.py                   # Visual AI detector with HUD & telemetry
├── app_voice.py             # Full AI detector with thread-safe voice warnings
├── dashboard.py             # Streamlit real-time safety dashboard
├── yolo11n.pt               # YOLO11 nano model weights
│
├── models/                  # Export target for ONNX / Qualcomm QNN models
├── assets/                  # Architecture diagrams & badges
└── screenshots/             # Demo screenshots & dashboard captures
```

---

## ⚡ 12. Snapdragon Optimization Roadmap

| Status | Technology | Description |
| :--- | :--- | :--- |
| **CURRENT (Tested Prototype)** | Python, OpenCV, YOLO11n (`.pt`), MediaPipe FaceMesh, SAPI5 | Fully functional local prototype running on Windows laptop webcam. |
| **TARGET (Snapdragon Optimization)** | Qualcomm AI Hub, ONNX Runtime (`onnxruntime-qnn`), DirectML, INT8 Quantization | Hardware-accelerated inference offloading to Snapdragon Hexagon NPU. |

### Planned Snapdragon Deployment Steps:
1. **Qualcomm AI Hub Model Compilation**: Export YOLO11n and landmark models to optimized Qualcomm Neural Processing SDK (`QNN`) format.
2. **ONNX Runtime with QNN Execution Provider**: Leverage direct Hexagon NPU offload via `onnxruntime-qnn` for sub-8ms latency.
3. **INT8 Quantization**: Quantize weights from FP32 to INT8 to decrease model footprint by $>70\%$ and ensure all-day battery efficiency on Snapdragon X Elite laptops.

---

## 🔒 13. Privacy & Security

- **100% Local Processing**: Video frames and biometric coordinates are processed in volatile RAM and immediately discarded.
- **No Cloud Video Transmission**: Zero external network requests or remote logging.
- **No Stored Biometrics**: Face landmarks are converted to numerical aspect ratios in real time.

---

## ⚠️ 14. Current Limitations & Future Improvements

### Limitations
- Requires adequate in-cabin lighting for webcam face tracking.
- Heavy sunglasses may obscure eye landmarks for EAR calculation.

### Future Improvements
- Head pose estimation for distracted gaze detection (looking away from road).
- Yawning frequency tracking for early fatigue detection.
- Infrared (IR) camera support for night-time driving.
- Native Qualcomm QNN runtime C++ wrapper.

---

## 🏆 15. Hackathon Submission Details

- **Event**: Snapdragon AI Lab Build & Present Challenge 2026
- **Repository**: [https://github.com/abhishek160108/AI-Road-Guardian](https://github.com/abhishek160108/AI-Road-Guardian)
- **License**: MIT License
