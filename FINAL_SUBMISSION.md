# 🏆 AI Road Guardian — Final Submission Package
### *Snapdragon AI Lab Build & Present Challenge 2026*

---

### **Project Name**
**AI Road Guardian**

---

### **One-Line Pitch**
> *"AI Road Guardian is an on-device AI driver-safety co-pilot that detects phone usage and drowsiness in real time, calculates driver risk, and provides immediate voice warnings before unsafe behaviour can lead to an accident."*

---

### **One-Line Description**
AI-powered driver safety system using computer vision to detect phone usage and drowsiness in real time.

---

### **Problem**
Distracted driving (e.g. mobile phone interaction) and drowsy driving (driver fatigue/microsleep) are leading causes of severe automotive collisions worldwide. Cloud-based safety solutions suffer from high latency and severe privacy compromises by transmitting in-cabin video feeds to remote servers.

---

### **Solution**
A real-time, 100% on-device AI monitoring system running locally on the driver's PC/laptop. The system continuously evaluates driver attentiveness via camera input, calculates a dynamic risk score, and delivers instantaneous multimodal visual HUD alerts and spoken voice warnings to prevent accidents before they happen.

---

### **Core AI Technologies**
- **Phone Detection**: **YOLO11n** (Ultralytics nano model targeting COCO class `67`, confidence $> 0.40$).
- **Drowsiness & Eye Tracking**: **MediaPipe Face Mesh** extracting 468 landmarks and computing the **Eye Aspect Ratio (EAR)** using 6 landmark indices per eye (`EAR < 0.25` for $\ge 15$ consecutive frames).
- **Voice Warning Engine**: Local, thread-safe Windows SAPI5 offline text-to-speech via `pyttsx3` with 5-second cooldown and high-risk escalation alerts.
- **Safety Cockpit Dashboard**: Live **Streamlit** dashboard reading atomic telemetry for real-time risk gauges, incident counters, and alert logs.

---

### **Risk Scoring Matrix**
- **📱 Phone Detected**: `+40 points`
- **😴 Drowsiness Detected**: `+50 points`
- **Maximum Risk Cap**: `100 points`
- **Risk Tiers**:
  - `0 – 39`: 🟢 **LOW RISK** (Safe driving)
  - `40 – 69`: 🟡 **MEDIUM RISK** (Warning state)
  - `70 – 100`: 🔴 **HIGH RISK** (Critical hazard / Emergency voice escalation)

---

### **Deployment & Platform Roadmap**
- **Current Tested Prototype**: Local Windows PC / laptop running Python 3.11, OpenCV, and local webcam.
- **Target Hardware Architecture**: Qualcomm **Snapdragon X Elite** & Snapdragon-powered Windows on ARM PCs.
- **Optimization Roadmap**:
  1. Quantization to INT8 for sub-10ms inference and minimal memory footprint.
  2. Qualcomm AI Hub model optimization for YOLO11n.
  3. ONNX Runtime with Qualcomm QNN Execution Provider for hardware-accelerated Hexagon NPU offloading.

---

### **Privacy & Security**
- **100% Local Edge Processing**: All computer vision inference and telemetry logging occur locally in memory.
- **Zero Cloud Upload**: No video streams, facial images, or telemetry data leave the device.

---

### **Innovation & Impact**
Combines distraction detection, drowsiness tracking, multi-hazard risk scoring, offline voice feedback, and live cockpit telemetry into a unified, lightweight edge application engineered for driver safety without compromising privacy.

---

### **Repository & Demo Links**
- **GitHub Repository**: [https://github.com/abhishek160108/AI-Road-Guardian](https://github.com/abhishek160108/AI-Road-Guardian)
- **Demo Guide**: [`DEMO_SCRIPT.md`](file:///C:/ai%20road%20guardian/DEMO_SCRIPT.md)
