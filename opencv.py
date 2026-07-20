import cv2
import numpy as np
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

trail = []  # stores drawn points

def count_fingers_up(landmarks):
    """Returns number of extended fingers (thumb excluded for simplicity)."""
    tips = [8, 12, 16, 20]   # index, middle, ring, pinky tips
    bases = [6, 10, 14, 18]  # their lower joints
    count = 0
    for tip, base in zip(tips, bases):
        if landmarks[tip].y < landmarks[base].y:  # tip higher than joint = extended
            count += 1
    return count

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]
        landmarks = hand_landmarks.landmark

        fingers_up = count_fingers_up(landmarks)

        # Index fingertip position (landmark 8)
        tip = landmarks[8]
        x, y = int(tip.x * w), int(tip.y * h)

        if fingers_up == 1:
            # Drawing mode
            trail.append((x, y))
            cv2.circle(frame, (x, y), 8, (0, 255, 0), -1)  # green = drawing
        else:
            # Pause mode — lift pen without drawing
            trail.append(None)  # None = break in the line
            cv2.circle(frame, (x, y), 8, (0, 0, 255), -1)  # red = paused

    # Draw the trail, skipping over None breaks
    for i in range(1, len(trail)):
        if trail[i - 1] is None or trail[i] is None:
            continue
        cv2.line(frame, trail[i - 1], trail[i], (255, 0, 255), 3)

    cv2.putText(frame, "1 finger = draw | 2+ fingers = pause | 'c' clear | 'q' quit",
                (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)

    cv2.imshow("Finger Draw", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        trail = []

cap.release()
cv2.destroyAllWindows()