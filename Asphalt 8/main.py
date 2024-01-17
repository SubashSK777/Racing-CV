import cv2
import mediapipe as mp
import time
from directkeys import right_pressed, left_pressed, down_pressed, up_pressed
from directkeys import PressKey, ReleaseKey

break_key_pressed = left_pressed
down_key_pressed = down_pressed
accelerator_key_pressed = right_pressed
up_key_pressed = up_pressed

time.sleep(2.0)
current_key_pressed = set()

mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

tipIDs = [4, 8, 12, 16, 20]

video = cv2.VideoCapture(0)

cv2.namedWindow("Asphalt 8 Controller", cv2.WINDOW_NORMAL)  # Create a resizable window
cv2.setWindowProperty("Asphalt 8 Controller", cv2.WND_PROP_TOPMOST, 1)

with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:

    while True:
        keyPressed = False
        break_pressed = False
        accelerator_pressed = False
        down_pressed = False
        up_pressed = False
        key_count = 0
        key_pressed = 0
        ret, image = video.read()
        image = cv2.flip(image, 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        lmLists = []

        right_hand_fingers = [0, 0, 0, 0, 0]
        left_hand_fingers = [0, 0, 0, 0, 0]

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                myHands = results.multi_hand_landmarks[0]
                lmList = []
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])

                mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                hand_index = 0 if lmList[0][1] < lmList[5][1] else 1

                for id in range(5):
                    if id == 0:  # Thumb
                        if lmList[tipIDs[id]][2] < lmList[tipIDs[id] - 2][2]:
                            if hand_index == 0:
                                right_hand_fingers[id] = 1
                            else:
                                left_hand_fingers[id] = 1
                    else:
                        if lmList[tipIDs[id]][2] < lmList[tipIDs[id] - 2][2]:
                            if hand_index == 0:
                                right_hand_fingers[id] = 1
                            else:
                                left_hand_fingers[id] = 1

        total_fingers = sum(right_hand_fingers) + sum(left_hand_fingers)

        if total_fingers == 1:
            cv2.rectangle(image, (20, 300), (270, 425), (255, 0, 0), cv2.FILLED)
            cv2.putText(image, "LEFT", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)
            PressKey(break_key_pressed)
            break_pressed = True
            current_key_pressed.add(break_key_pressed)
            key_pressed = break_key_pressed
            keyPressed = True
            key_count = key_count + 1

        elif total_fingers == 5:
            cv2.rectangle(image, (20, 300), (270, 425), (0, 0, 255), cv2.FILLED)
            cv2.putText(image, "RIGHT", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
            PressKey(accelerator_key_pressed)
            key_pressed = accelerator_key_pressed
            accelerator_pressed = True
            keyPressed = True
            current_key_pressed.add(accelerator_key_pressed)
            key_count = key_count + 1

        elif total_fingers == 8:
            cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
            cv2.putText(image, "NITRO", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
            PressKey(down_key_pressed)
            key_pressed = down_key_pressed
            down_pressed = True
            keyPressed = True
            current_key_pressed.add(down_key_pressed)
            key_count = key_count + 1

        if total_fingers == 3:
            cv2.rectangle(image, (20, 290), (290, 425), (50, 0, 0), cv2.FILLED)
            cv2.putText(image, "ACCELE", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
            PressKey(up_key_pressed)
            key_pressed = up_key_pressed
            up_pressed = True
            keyPressed = True
            current_key_pressed.add(up_key_pressed)
            key_count = key_count + 1

        if not keyPressed and len(current_key_pressed) != 0:
            for key in current_key_pressed:
                ReleaseKey(key)
            current_key_pressed = set()
        elif key_count == 1 and len(current_key_pressed) == 2:
            for key in current_key_pressed:
                if key_pressed != key:
                    ReleaseKey(key)
            current_key_pressed = set()

        print("Right Hand Fingers:", right_hand_fingers)
        print("Left Hand Fingers:", left_hand_fingers)
        print("Total Fingers:", total_fingers)

        cv2.imshow("Asphalt 8 Controller", image)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

video.release()
cv2.destroyAllWindows()
