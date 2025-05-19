import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

def recognize_sign(landmarks):
    tips_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky

    fingers = []
    # Thumb
    if landmarks[tips_ids[0]].x < landmarks[tips_ids[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Fingers (Index to Pinky)
    for i in range(1, 5):
        if landmarks[tips_ids[i]].y < landmarks[tips_ids[i] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    # Interpret
    if fingers == [0, 0, 0, 0, 0]:
        return "Fist / Yes"
    elif fingers == [1, 1, 1, 1, 1]:
        return "Hello"
    elif fingers == [0, 1, 1, 0, 0]:
        return "Victory"
    elif fingers == [1, 0, 0, 0, 0]:
        return "Good"
    elif fingers == [0, 1, 0, 0, 0]:
        return "One"
    else:
        return "Unknown"

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            sign = recognize_sign(hand_landmarks.landmark)
            cv2.putText(frame, sign, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

    cv2.imshow("Sign Language Translator", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

