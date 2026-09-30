# 🎬 AI Road Guardian — 90-Second Hackathon Demo Script
### *Snapdragon AI Lab Build & Present Challenge 2026*

---

### **⏱️ Timeline & Presentation Flow**

#### **[00:00 – 00:10] Introduction & Problem Statement**
- **Presenter**: *"Distracted driving from mobile phone usage and driver fatigue cause thousands of preventable road collisions every year. Today, we present **AI Road Guardian** — an on-device AI driver-safety co-pilot that monitors driver alertness locally, calculates real-time risk, and delivers immediate voice warnings before an unsafe situation turns into an accident."*
- **Visual**: Show project hero slide or GitHub title repository.

---

#### **[00:10 – 00:25] Normal Driving State (Low Risk)**
- **Action**: Launch the AI detector (`python app_voice.py`).
- **Presenter**: *"Here, the driver is attentive. Our MediaPipe Face Mesh extracts 468 landmarks in real time, calculating an Eye Aspect Ratio (EAR) of ~0.30. The system reports **LOW RISK (0/100)** with a clean green HUD."*
- **Visual**: Camera window active, showing `EAR: 0.30`, `RISK: 0/100`, `LOW RISK` (Green badge).

---

#### **[00:25 – 00:40] Scenario 1: Phone Distraction Detection**
- **Action**: Raise a mobile phone into the camera frame.
- **Presenter**: *"As soon as the driver checks a phone, our YOLO11n detector instantly recognizes class 67 with high confidence. The risk score rises by +40 points to Medium Risk, and the system delivers an immediate, non-blocking voice warning."*
- **Audio Output**: 🗣️ *"Warning! Please put your phone down."*
- **Visual**: Red bounding box around phone, `PHONE 85%`, Risk Score $= 40/100$, `MEDIUM RISK` (Yellow).

---

#### **[00:40 – 00:55] Scenario 2: Drowsiness & Microsleep Detection**
- **Action**: Put phone down, close eyes for ~1.5 seconds (15 consecutive frames).
- **Presenter**: *"If the driver experiences fatigue or a microsleep episode, the EAR drops below 0.25. Once 15 closed frames are detected, the system triggers a dedicated drowsiness alert and logs a +50 risk penalty."*
- **Audio Output**: 🗣️ *"Warning! You appear to be drowsy. Please take a break."*
- **Visual**: `EAR: 0.16`, `DROWSINESS WARNING!`, Risk Score $= 50/100$, `MEDIUM RISK`.

---

#### **[00:55 – 01:10] Scenario 3: High-Risk Multi-Hazard Escalation**
- **Action**: Hold phone up while closing eyes / looking drowsy.
- **Presenter**: *"When multiple critical hazards happen simultaneously, the risk score spikes to 90/100. The engine escalates to a High-Risk Emergency state with high-priority audio feedback."*
- **Audio Output**: 🗣️ *"Warning! High risk detected. Please focus on driving."*
- **Visual**: Flashing red HUD alert, Risk Score $= 90/100$, `HIGH RISK` (Red badge).

---

#### **[01:10 – 01:25] Live Telemetry & Streamlit Safety Dashboard**
- **Action**: Switch to the browser showing `http://localhost:8501`.
- **Presenter**: *"All telemetry streams locally via an atomic JSON bridge to our Streamlit Safety Dashboard. Fleet managers and drivers get instant visibility into driver status, trip duration, incident counters, real-time EAR trends, and a complete chronological session alert log."*
- **Visual**: Dashboard updating live, showing KPI cards, Risk Progress Bar, EAR gauge, and incident log table.

---

#### **[01:25 – 01:30] Privacy & Snapdragon NPU Roadmap**
- **Presenter**: *"Crucially, AI Road Guardian processes everything 100% locally with zero cloud video upload for absolute privacy. In our Snapdragon roadmap, we are deploying this pipeline via Qualcomm AI Hub and ONNX Runtime onto the Hexagon NPU for ultra-low latency and all-day energy efficiency. Thank you!"*
