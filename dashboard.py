import streamlit as st
import json
import os
import time
from datetime import datetime

# ==========================================
# 1. STREAMLIT CONFIG & PROFESSIONAL STYLING
# ==========================================
st.set_page_config(
    page_title="AI Road Guardian — Driver Safety Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Hackathon Presentation
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .status-badge-online {
        background-color: #DCFCE7;
        color: #166534;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
    .status-badge-offline {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
    .privacy-notice {
        background-color: #EFF6FF;
        border-left: 4px solid #3B82F6;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin-top: 1.5rem;
        font-size: 0.9rem;
        color: #1E40AF;
    }
    .kpi-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.6rem;
        font-weight: 700;
        margin-bottom: 4px;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. LOCAL TELEMETRY & ALERT HISTORY HANDLERS
# ==========================================
TELEMETRY_PATH = "telemetry.json"
ALERT_HISTORY_PATH = "alert_history.json"


def load_telemetry():
    """Reads and validates the local telemetry file."""
    if not os.path.exists(TELEMETRY_PATH):
        return None, "Telemetry file not found."
    try:
        with open(TELEMETRY_PATH, "r") as f:
            data = json.load(f)
        return data, None
    except Exception as e:
        return None, f"Error reading telemetry: {e}"


def record_alert_history(alert_type, risk_score, risk_level):
    """Maintains a local log of triggered safety alerts."""
    history = []
    if os.path.exists(ALERT_HISTORY_PATH):
        try:
            with open(ALERT_HISTORY_PATH, "r") as f:
                history = json.load(f)
        except Exception:
            history = []

    # Check if last entry is identical within the last 5 seconds
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if history and history[-1].get("alert_type") == alert_type:
        return history

    new_entry = {
        "timestamp": now_str,
        "alert_type": alert_type,
        "risk_score": risk_score,
        "risk_level": risk_level
    }
    history.append(new_entry)
    # Keep last 50 entries
    history = history[-50:]

    try:
        with open(ALERT_HISTORY_PATH, "w") as f:
            json.dump(history, f, indent=2)
    except Exception:
        pass

    return history


def load_alert_history():
    """Loads recorded alert history."""
    if os.path.exists(ALERT_HISTORY_PATH):
        try:
            with open(ALERT_HISTORY_PATH, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []


# ==========================================
# 3. SIDEBAR — CONTROLS & INFO
# ==========================================
with st.sidebar:
    st.image("https://img.shields.io/badge/Snapdragon%20AI%20Lab-Challenge%202026-blue?style=for-the-badge", use_container_width=True)
    st.title("🛡️ System Controls")

    st.markdown("### ⚙️ Auto-Refresh")
    auto_refresh = st.checkbox("Enable Live Polling", value=True)
    refresh_rate = st.slider("Polling Rate (seconds)", min_value=1.0, max_value=5.0, value=1.0, step=0.5)

    st.divider()

    st.markdown("### 🚀 How to Run AI Engine")
    st.code("python app_voice.py", language="bash")
    st.caption("Runs YOLO11n + MediaPipe Face Mesh + Voice Alerts locally.")

    st.markdown("### 📊 How to Run Dashboard")
    st.code("streamlit run dashboard.py", language="bash")

    st.divider()

    st.markdown("### 🧠 AI Core Architecture")
    st.markdown("""
    - **Phone Detection**: YOLO11n (Class 67, Conf > 0.40)
    - **Drowsiness**: MediaPipe Face Mesh (EAR < 0.25, 15 frames)
    - **Voice Warnings**: Local SAPI5 pyttsx3 Queue
    - **Target Platform**: Snapdragon X Elite / Windows on ARM
    """)

    st.divider()
    if st.button("🗑️ Clear Alert History"):
        if os.path.exists(ALERT_HISTORY_PATH):
            os.remove(ALERT_HISTORY_PATH)
        st.success("Alert history cleared.")
        st.rerun()


# ==========================================
# 4. MAIN HEADER & STATUS
# ==========================================
st.markdown('<div class="main-header">🛡️ AI Road Guardian</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Driver Safety & Real-Time Risk Monitoring System</div>', unsafe_allow_html=True)

# Load Telemetry
telemetry, err_msg = load_telemetry()

# Check Online / Offline State
is_online = False
is_simulated = False
last_update_str = "N/A"

if telemetry and "timestamp" in telemetry:
    try:
        # Check freshness of telemetry data
        t_time = datetime.fromisoformat(telemetry["timestamp"])
        age_seconds = (datetime.now() - t_time).total_seconds()
        if age_seconds <= 4.0:
            is_online = True
        last_update_str = t_time.strftime("%H:%M:%S")
    except Exception:
        last_update_str = telemetry.get("timestamp", "N/A")

# Cloud / Standalone Simulation Mode (when local camera detector is not connected)
if not is_online:
    with st.sidebar:
        st.divider()
        st.markdown("### 🎮 Interactive Cloud Simulator")
        st.caption("Live AI detector is not active on this server. Choose a scenario below to test dashboard telemetry interactively:")
        sim_scenario = st.selectbox(
            "Test Scenario:",
            [
                "🟢 Normal Driving (Attentive)",
                "📱 Phone Distraction Hazard",
                "😴 Drowsiness / Microsleep Alert",
                "🚨 Critical Multi-Hazard Escalation"
            ]
        )
        is_simulated = True

    now_iso = datetime.now().isoformat()
    if sim_scenario == "🟢 Normal Driving (Attentive)":
        telemetry = {
            "phone_detected": False,
            "drowsy": False,
            "face_detected": True,
            "EAR": 0.31,
            "risk_score": 0,
            "risk_level": "LOW RISK",
            "FPS": 30.0,
            "session_duration": 48.0,
            "phone_trigger_count": 0,
            "drowsiness_trigger_count": 0,
            "last_alert": "None",
            "timestamp": now_iso
        }
    elif sim_scenario == "📱 Phone Distraction Hazard":
        telemetry = {
            "phone_detected": True,
            "drowsy": False,
            "face_detected": True,
            "EAR": 0.29,
            "risk_score": 40,
            "risk_level": "MEDIUM RISK",
            "FPS": 29.4,
            "session_duration": 65.0,
            "phone_trigger_count": 1,
            "drowsiness_trigger_count": 0,
            "last_alert": "Phone Detected",
            "timestamp": now_iso
        }
    elif sim_scenario == "😴 Drowsiness / Microsleep Alert":
        telemetry = {
            "phone_detected": False,
            "drowsy": True,
            "face_detected": True,
            "EAR": 0.16,
            "risk_score": 50,
            "risk_level": "MEDIUM RISK",
            "FPS": 29.8,
            "session_duration": 92.0,
            "phone_trigger_count": 0,
            "drowsiness_trigger_count": 1,
            "last_alert": "Drowsiness Detected",
            "timestamp": now_iso
        }
    else:  # Critical Multi-Hazard
        telemetry = {
            "phone_detected": True,
            "drowsy": True,
            "face_detected": True,
            "EAR": 0.14,
            "risk_score": 90,
            "risk_level": "HIGH RISK",
            "FPS": 28.6,
            "session_duration": 124.0,
            "phone_trigger_count": 2,
            "drowsiness_trigger_count": 2,
            "last_alert": "Critical: Phone + Drowsy",
            "timestamp": now_iso
        }
    is_online = True
    last_update_str = datetime.now().strftime("%H:%M:%S")

# Top Status Bar
status_col1, status_col2, status_col3, status_col4 = st.columns([1.8, 1.1, 1.1, 1.8])

with status_col1:
    if is_simulated:
        st.markdown('**System Status:** <span class="status-badge-online" style="background-color:#E0F2FE; color:#0369A1;">🔵 SIMULATOR — ACTIVE</span>', unsafe_allow_html=True)
    elif is_online:
        st.markdown('**System Status:** <span class="status-badge-online">🟢 ONLINE — LIVE LOCAL</span>', unsafe_allow_html=True)
    else:
        st.markdown('**System Status:** <span class="status-badge-offline">🔴 OFFLINE / WAITING</span>', unsafe_allow_html=True)

with status_col2:
    fps_val = telemetry.get("FPS", 0.0) if telemetry and is_online else 0.0
    st.markdown(f"**Camera FPS:** `{fps_val:.1f}`")

with status_col3:
    session_sec = int(telemetry.get("session_duration", 0)) if telemetry and is_online else 0
    mins, secs = divmod(session_sec, 60)
    st.markdown(f"**Trip Duration:** `{mins:02d}:{secs:02d}`")

with status_col4:
    st.markdown(f"**Last Sync:** `{last_update_str}`")

st.divider()


# ==========================================
# 6. MAIN KPI CARDS (4 COLUMNS)
# ==========================================
phone_detected = telemetry.get("phone_detected", False) if telemetry and is_online else False
drowsy = telemetry.get("drowsy", False) if telemetry and is_online else False
risk_score = telemetry.get("risk_score", 0) if telemetry and is_online else 0
risk_level = telemetry.get("risk_level", "LOW RISK") if telemetry and is_online else "LOW RISK"
ear_val = telemetry.get("EAR", 0.0) if telemetry and is_online else 0.0
face_detected = telemetry.get("face_detected", False) if telemetry and is_online else False

# Record alert history if active
if is_online and telemetry:
    last_alert = telemetry.get("last_alert", "None")
    if last_alert and last_alert != "None":
        record_alert_history(last_alert, risk_score, risk_level)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    driver_status = "SAFE" if (not phone_detected and not drowsy and is_online) else ("ATTENTION REQUIRED" if is_online else "IDLE")
    driver_color = "#166534" if driver_status == "SAFE" else ("#DC2626" if is_online else "#64748B")
    st.markdown(f"""
    <div class="metric-card">
        <div class="kpi-title">👤 Driver Status</div>
        <div class="kpi-value" style="color: {driver_color};">{driver_status}</div>
        <small>{'Active tracking' if face_detected else ('Face not detected' if is_online else 'Detector idle')}</small>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    phone_status = "PHONE DETECTED" if phone_detected else "SAFE"
    phone_color = "#DC2626" if phone_detected else "#166534"
    st.markdown(f"""
    <div class="metric-card">
        <div class="kpi-title">📱 Phone Status</div>
        <div class="kpi-value" style="color: {phone_color};">{phone_status}</div>
        <small>YOLO11n (Conf > 0.40)</small>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    drowsy_status = "DROWSINESS DETECTED" if drowsy else "SAFE"
    drowsy_color = "#DC2626" if drowsy else "#166534"
    st.markdown(f"""
    <div class="metric-card">
        <div class="kpi-title">😴 Drowsiness Status</div>
        <div class="kpi-value" style="color: {drowsy_color};">{drowsy_status}</div>
        <small>EAR: {ear_val:.2f} (Threshold: &lt; 0.25)</small>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    if risk_score >= 70:
        score_color = "#DC2626"
    elif risk_score >= 40:
        score_color = "#D97706"
    else:
        score_color = "#166534"
    st.markdown(f"""
    <div class="metric-card">
        <div class="kpi-title">📊 Overall Risk Score</div>
        <div class="kpi-value" style="color: {score_color};">{risk_score} / 100</div>
        <small>{risk_level}</small>
    </div>
    """, unsafe_allow_html=True)

st.write("")


# ==========================================
# 7. RISK ANALYSIS & PROGRESS GAUGE
# ==========================================
st.subheader("🚦 Real-Time Safety Risk Level")

risk_col1, risk_col2 = st.columns([3, 1])

with risk_col1:
    st.progress(min(1.0, max(0.0, risk_score / 100.0)))
    
    if risk_score < 40:
        st.success(f"🟢 **LOW RISK ({risk_score}/100)** — Driver appears attentive and compliant with road safety standards.")
    elif risk_score < 70:
        st.warning(f"🟡 **MEDIUM RISK ({risk_score}/100)** — Warning threshold reached. Immediate driver attention recommended.")
    else:
        st.error(f"🔴 **HIGH RISK ({risk_score}/100)** — CRITICAL SAFETY HAZARD. High probability of collision. Voice escalation triggered.")

with risk_col2:
    st.markdown("""
    **Risk Scoring Matrix:**
    - 📱 Phone Detected: `+40 pts`
    - 😴 Drowsiness Active: `+50 pts`
    - ⚠️ Threshold: `70+ = High Risk`
    """)

st.divider()


# ==========================================
# 8. LIVE DRIVER METRICS & EVENT COUNTERS
# ==========================================
st.subheader("📈 Driver Telemetry & Incident Counters")

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.metric("👁️ Eye Aspect Ratio (EAR)", f"{ear_val:.2f}", delta="Safe (> 0.25)" if ear_val >= 0.25 else "Closed (< 0.25)", delta_color="normal" if ear_val >= 0.25 else "inverse")

with metric_col2:
    phone_triggers = telemetry.get("phone_trigger_count", 0) if telemetry else 0
    st.metric("📱 Phone Triggers (Trip)", f"{phone_triggers} events")

with metric_col3:
    drowsy_triggers = telemetry.get("drowsiness_trigger_count", 0) if telemetry else 0
    st.metric("😴 Drowsiness Triggers (Trip)", f"{drowsy_triggers} events")

with metric_col4:
    last_alert_name = telemetry.get("last_alert", "None") if telemetry else "None"
    st.metric("🔔 Latest Alert Event", f"{last_alert_name}")

st.divider()


# ==========================================
# 9. RECENT ALERT HISTORY TABLE
# ==========================================
st.subheader("📋 Session Alert History")

history_entries = load_alert_history()
if history_entries:
    # Display in reverse chronological order
    formatted_history = []
    for item in reversed(history_entries[-10:]):
        formatted_history.append({
            "Timestamp": item.get("timestamp"),
            "Alert Event": item.get("alert_type"),
            "Risk Score": f"{item.get('risk_score')}/100",
            "Risk Tier": item.get("risk_level")
        })
    st.dataframe(formatted_history, use_container_width=True, hide_index=True)
else:
    st.caption("No safety alerts recorded yet in this session.")


# ==========================================
# 10. PRIVACY & LOCAL PROCESSING GUARANTEE
# ==========================================
st.markdown("""
<div class="privacy-notice">
    <strong>🔒 Local Processing Guarantee:</strong> All computer vision inference (YOLO11n, MediaPipe Face Mesh), voice generation, and telemetry logging execute 100% locally on this device. No camera frames, biometric landmarks, or video streams are transmitted to external servers.
</div>
""", unsafe_allow_html=True)


# ==========================================
# 11. AUTO-REFRESH ENGINE
# ==========================================
if auto_refresh and not is_simulated:
    time.sleep(refresh_rate)
    st.rerun()