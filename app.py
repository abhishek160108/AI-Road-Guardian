import cv2
import math
import mediapipe as mp
from ultralytics import YOLO
import time
import json
import os
from datetime import datetime

# ==========================================
# 1. LOCAL TELEMETRY LOGGER
# ==========================================
def update_telemetry(data, file_path="telemetry.json"):
    """
    Safely writes real-time telemetry metrics to a local JSON file.
    Does NOT contain or store any personal data.
    """
    try:
        temp_file = file_path + ".tmp"
        with open(temp_file, "w") as f:
            json.dump(data, f, indent=2)
        os.replace(temp_file, file_path)
    except Exception:
        pass


# ==========================================
# 2. INITIALIZATION & MODEL LOADING
# ==========================================
# Load YOLO Model
try:
    phone_model = YOLO("yolo11n.pt")
except Exception as e:
    print(f"[Fatal Error] Could not load YOLO model (yolo11n.pt): {e}")
    exit(1)

# MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Landmark Indices for Eye Aspect Ratio (EAR)
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]


def calculate_ear(landmarks, eye, width, height):
    """Calculates the Eye Aspect Ratio (EAR) for a given set of eye landmarks."""
    points = []
    for i in eye:
        x = int(landmarks[i].x * width)
        y = int(landmarks[i].y * height)
        points.append((x, y))

    vertical1 = math.dist(points[1], points[5])
    vertical2 = math.dist(points[2], points[4])
    horizontal = math.dist(points[0], points[3])

    if horizontal == 0:
        return 1.0

    return (vertical1 + vertical2) / (2 * horizontal)


# ==========================================
# 3. CAMERA SETUP & STATE VARIABLES
# ==========================================
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("[Error] Camera index 0 could not be opened. Checking index 1...")
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("[Fatal Error] No camera available. Please connect a webcam.")
        exit(1)

# Detection & State Parameters
closed_frames = 0

# Metrics & Telemetry Counters
phone_trigger_count = 0
drowsiness_trigger_count = 0
was_phone_active = False
was_drowsy_active = False
last_alert_msg = "None"
start_time = time.time()
frame_count = 0
fps = 0.0
fps_timer = time.time()

print("========================================")
print("  AI ROAD GUARDIAN — Visual Monitor")
print("  Monitoring active. Press 'Q' to stop.")
print("========================================")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("[Warning] Failed to capture camera frame.")
            break

        frame_count += 1
        curr_time = time.time()
        if curr_time - fps_timer >= 1.0:
            fps = frame_count / (curr_time - fps_timer)
            frame_count = 0
            fps_timer = curr_time

        height, width = frame.shape[:2]

        # -------------------------
        # PHONE DETECTION (YOLO11n)
        # -------------------------
        phone_detected = False
        try:
            results = phone_model(frame, verbose=False)
            for result in results:
                for box in result.boxes:
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])

                    # Class 67 = Cell Phone, Confidence > 0.40
                    if cls == 67 and conf > 0.40:
                        phone_detected = True
                        x1, y1, x2, y2 = map(int, box.xyxy[0])

                        # Draw bounding box & label
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        cv2.putText(
                            frame,
                            f"PHONE {conf*100:.0f}%",
                            (x1, max(20, y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (0, 0, 255),
                            2
                        )
        except Exception as e:
            print(f"[YOLO Inference Warning] {e}")

        # Track trigger transition
        if phone_detected and not was_phone_active:
            phone_trigger_count += 1
            last_alert_msg = "Phone Detected"
        was_phone_active = phone_detected

        # -------------------------
        # FACE / DROWSINESS (MediaPipe)
        # -------------------------
        drowsy = False
        ear = 0.0
        face_detected = False

        try:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_results = face_mesh.process(rgb)

            if face_results.multi_face_landmarks:
                face_detected = True
                landmarks = face_results.multi_face_landmarks[0].landmark

                left_ear = calculate_ear(landmarks, LEFT_EYE, width, height)
                right_ear = calculate_ear(landmarks, RIGHT_EYE, width, height)
                ear = (left_ear + right_ear) / 2.0

                if ear < 0.25:
                    closed_frames += 1
                else:
                    closed_frames = 0

                if closed_frames >= 15:
                    drowsy = True
        except Exception as e:
            print(f"[FaceMesh Warning] {e}")

        # Track drowsiness trigger transition
        if drowsy and not was_drowsy_active:
            drowsiness_trigger_count += 1
            last_alert_msg = "Drowsiness Detected"
        was_drowsy_active = drowsy

        # -------------------------
        # RISK CALCULATION
        # -------------------------
        risk_score = 0
        if phone_detected:
            risk_score += 40
        if drowsy:
            risk_score += 50
        if risk_score > 100:
            risk_score = 100

        # Risk Level & Colors
        if risk_score >= 70:
            risk_text = "HIGH RISK"
            risk_color = (0, 0, 255)     # Red
        elif risk_score >= 40:
            risk_text = "MEDIUM RISK"
            risk_color = (0, 255, 255)   # Yellow
        else:
            risk_text = "LOW RISK"
            risk_color = (0, 255, 0)     # Green

        # -------------------------
        # TELEMETRY UPDATE
        # -------------------------
        session_duration = round(curr_time - start_time, 1)
        telemetry_data = {
            "phone_detected": phone_detected,
            "drowsy": drowsy,
            "face_detected": face_detected,
            "EAR": round(ear, 2),
            "risk_score": risk_score,
            "risk_level": risk_text,
            "FPS": round(fps, 1),
            "session_duration": session_duration,
            "phone_trigger_count": phone_trigger_count,
            "drowsiness_trigger_count": drowsiness_trigger_count,
            "last_alert": last_alert_msg,
            "timestamp": datetime.now().isoformat()
        }
        update_telemetry(telemetry_data)

        # -------------------------
        # PROFESSIONAL HUD OVERLAYS
        # -------------------------
        # Semi-transparent top dashboard bar
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (width, 95), (20, 20, 20), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

        # Header Title & FPS
        cv2.putText(frame, "AI ROAD GUARDIAN", (20, 30),
                    cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 255, 255), 2)
        cv2.putText(frame, f"FPS: {fps:.1f} | Trip: {int(session_duration)}s", (20, 58),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (180, 180, 180), 1)

        # Face / EAR status
        if face_detected:
            ear_color = (0, 0, 255) if ear < 0.25 else (0, 255, 0)
            cv2.putText(frame, f"EAR: {ear:.2f}", (240, 58),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, ear_color, 2)
        else:
            cv2.putText(frame, "FACE: NOT FOUND", (240, 58),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 165, 255), 2)

        # Risk Score & Level Badge
        cv2.putText(frame, f"RISK: {risk_score}/100", (width - 240, 32),
                    cv2.FONT_HERSHEY_DUPLEX, 0.7, risk_color, 2)
        cv2.putText(frame, risk_text, (width - 240, 62),
                    cv2.FONT_HERSHEY_DUPLEX, 0.65, risk_color, 2)

        # Warning Banners if Active
        y_alert = 130
        if phone_detected:
            cv2.rectangle(frame, (15, y_alert - 25), (320, y_alert + 10), (0, 0, 180), -1)
            cv2.putText(frame, "PHONE DETECTED!", (25, y_alert),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
            y_alert += 45

        if drowsy:
            cv2.rectangle(frame, (15, y_alert - 25), (370, y_alert + 10), (0, 0, 180), -1)
            cv2.putText(frame, "DROWSINESS WARNING!", (25, y_alert),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

        # Bottom Bar Quit Hint
        cv2.putText(frame, "Press 'Q' to Exit", (width - 160, height - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        # Show Output
        cv2.imshow("AI Road Guardian - Driver Monitor", frame)

        # Clean Exit on 'Q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("\n[Shutdown] 'Q' pressed. Exiting AI Road Guardian...")
            break

except KeyboardInterrupt:
    print("\n[Shutdown] Keyboard interrupt detected.")

finally:
    # Cleanup all resources
    cap.release()
    face_mesh.close()
    cv2.destroyAllWindows()
    print("[Shutdown] All resources released cleanly.")