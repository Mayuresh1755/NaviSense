import cv2
import pyttsx3
import threading
import queue
import time

from ultralytics import YOLO

# ==============================
# SETTINGS
# ==============================

MODEL_NAME = "yolo11n.pt"

FRAME_WIDTH = 640
FRAME_HEIGHT = 480

CONFIDENCE = 0.50

DETECTION_INTERVAL = 3      # Run YOLO every 3 frames

SPEECH_COOLDOWN = 3         # Seconds before speaking same object again

# ==============================
# LOAD MODEL
# ==============================

print("Loading YOLO...")
model = YOLO(MODEL_NAME)

# ==============================
# TEXT TO SPEECH
# ==============================

engine = pyttsx3.init()

engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)

speech_queue = queue.Queue()


def speech_worker():
    while True:
        text = speech_queue.get()

        if text is None:
            break

        engine.say(text)
        engine.runAndWait()


threading.Thread(target=speech_worker, daemon=True).start()

# ==============================
# CAMERA
# ==============================

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

print("Camera started.")

# ==============================
# VARIABLES
# ==============================

frame_count = 0

last_results = None

last_spoken = {}

prev_time = time.time()

# ==============================
# MAIN LOOP
# ==============================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

    frame_count += 1

    # --------------------------
    # Run YOLO every N frames
    # --------------------------

    if frame_count % DETECTION_INTERVAL == 0:

        last_results = model(
            frame,
            imgsz=416,
            conf=CONFIDENCE,
            verbose=False
        )

    if last_results is not None:

        annotated = last_results[0].plot()

        current_time = time.time()

        for box in last_results[0].boxes:

            cls = int(box.cls[0])

            confidence = float(box.conf[0])

            if confidence < CONFIDENCE:
                continue

            name = model.names[cls]

            # ---------------------------------
            # Direction Detection
            # ---------------------------------

            x1, y1, x2, y2 = box.xyxy[0]

            center_x = (x1 + x2) / 2

            if center_x < FRAME_WIDTH / 3:
                direction = "left"

            elif center_x > 2 * FRAME_WIDTH / 3:
                direction = "right"

            else:
                direction = "ahead"

            speech = f"{name} {direction}"

            # ---------------------------------
            # Cooldown
            # ---------------------------------

            if (
                speech not in last_spoken
                or current_time - last_spoken[speech] > SPEECH_COOLDOWN
            ):

                print("Speaking:", speech)

                speech_queue.put(speech)

                last_spoken[speech] = current_time

    else:

        annotated = frame

    # --------------------------
    # FPS
    # --------------------------

    current = time.time()

    fps = 1 / (current - prev_time)

    prev_time = current

    cv2.putText(
        annotated,
        f"FPS: {int(fps)}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )

    cv2.imshow("NaviSense", annotated)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

# ==============================
# CLEANUP
# ==============================

speech_queue.put(None)

cap.release()

cv2.destroyAllWindows()