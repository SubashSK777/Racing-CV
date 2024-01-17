import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller, Key

video = cv2.VideoCapture(0)

cv2.namedWindow("DragonBall Controller", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("DragonBall Controller", cv2.WND_PROP_TOPMOST, 1)

detector = HandDetector(detectionCon=0.7, maxHands=2)
keyboard = Controller()

while True:
    _, img = video.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    if hands:
        for hand in hands:
            finger = detector.fingersUp(hand)
            if hand["type"] == "Right":
                if finger == [0,1,0,0,0]:
                    print("Jump")
                    cv2.putText(img, "Jump", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 6)
                    keyboard.press(Key.up)
                    keyboard.release(Key.down)
                    keyboard.release(Key.right)
                    keyboard.release(Key.left)
                    keyboard.release('b')
                    keyboard.release('n')

                if finger == [0,1,1,0,0]:
                    print("Right")
                    cv2.putText(img, "Right", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 6)
                    keyboard.press(Key.right)
                    keyboard.release(Key.down)
                    keyboard.release(Key.up)
                    keyboard.release(Key.left)
                    keyboard.release('b')
                    keyboard.release('n')

                if finger == [0, 1, 1, 1, 1]:
                    print("left")
                    cv2.putText(img, "Left", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 6)
                    keyboard.press(Key.left)
                    keyboard.release(Key.down)
                    keyboard.release(Key.right)
                    keyboard.release(Key.up)
                    keyboard.release('b')
                    keyboard.release('n')

                if finger == [0, 1, 0, 0, 1]:
                    print("Down")
                    cv2.putText(img, "Down", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 6)
                    keyboard.press(Key.down)
                    keyboard.release(Key.up)
                    keyboard.release(Key.right)
                    keyboard.release(Key.left)
                    keyboard.release('b')
                    keyboard.release('n')

                if finger == [1, 0, 0, 0, 0]:
                    print("Swap 1")
                    cv2.putText(img, "Swap 1", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 6)
                    keyboard.press('b')
                    keyboard.release(Key.up)
                    keyboard.release(Key.right)
                    keyboard.release(Key.left)
                    keyboard.release(Key.down)
                    keyboard.release('n')

                if finger == [0, 0, 0, 0, 1]:
                    print("Swap 1")
                    cv2.putText(img, "Swap 1", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 6)
                    keyboard.press('n')
                    keyboard.release('b')
                    keyboard.release(Key.up)
                    keyboard.release(Key.right)
                    keyboard.release(Key.left)
                    keyboard.release(Key.down)

            if hand["type"] == "Left":
                if finger == [0, 1, 0, 0, 0]:
                    print("Skill 1")
                    cv2.putText(img, "Skill 1", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 6)
                    keyboard.press('a')
                    keyboard.release('w')
                    keyboard.release('d')
                    keyboard.release('s')
                    keyboard.release('z')
                    keyboard.release('x')
                    keyboard.release('c')
                    keyboard.release('v')

                if finger == [0, 1, 0, 0, 1]:
                    print("Skill 2")
                    cv2.putText(img, "Skill 2", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 6)
                    keyboard.press('w')
                    keyboard.release('a')
                    keyboard.release('d')
                    keyboard.release('s')
                    keyboard.release('z')
                    keyboard.release('x')
                    keyboard.release('c')
                    keyboard.release('v')

                if finger == [1, 1, 1, 1, 1]:
                    print("Skill 3")
                    cv2.putText(img, "Skill 3", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 6)
                    keyboard.press('d')
                    keyboard.release('w')
                    keyboard.release('a')
                    keyboard.release('s')
                    keyboard.release('z')
                    keyboard.release('x')
                    keyboard.release('c')
                    keyboard.release('v')

                if finger == [1, 1, 0, 0, 1]:
                    print("Skill 4")
                    cv2.putText(img, "Skill 4", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 6)
                    keyboard.press('s')
                    keyboard.release('w')
                    keyboard.release('d')
                    keyboard.release('a')
                    keyboard.release('z')
                    keyboard.release('x')
                    keyboard.release('c')
                    keyboard.release('v')

                if finger == [0, 1, 1, 1, 1]:
                    print("Special Attack")
                    cv2.putText(img, "Special Attack", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 6)
                    keyboard.press('z')
                    keyboard.release('w')
                    keyboard.release('d')
                    keyboard.release('s')
                    keyboard.release('a')
                    keyboard.release('x')
                    keyboard.release('c')
                    keyboard.release('v')

                if finger == [0, 1, 1, 0, 0]:
                    print("Dragon Rush")
                    cv2.putText(img, "Dragon Rush", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 6)
                    keyboard.press('x')
                    keyboard.release('w')
                    keyboard.release('d')
                    keyboard.release('s')
                    keyboard.release('z')
                    keyboard.release('a')
                    keyboard.release('c')
                    keyboard.release('v')

                if finger == [0, 1, 1, 0, 0]:
                    print("Super Dash")
                    cv2.putText(img, "Super Dash", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 6)
                    keyboard.press('c')
                    keyboard.release('w')
                    keyboard.release('d')
                    keyboard.release('s')
                    keyboard.release('z')
                    keyboard.release('a')
                    keyboard.release('x')
                    keyboard.release('v')

                if finger == [0, 1, 1, 0, 0]:
                    print("Vanish")
                    cv2.putText(img, "Vanish", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 6)
                    keyboard.press('v')
                    keyboard.release('w')
                    keyboard.release('d')
                    keyboard.release('s')
                    keyboard.release('z')
                    keyboard.release('a')
                    keyboard.release('c')
                    keyboard.release('x')

            else:
                keyboard.release('n')
                keyboard.release('b')
                keyboard.release(Key.up)
                keyboard.release(Key.right)
                keyboard.release(Key.left)
                keyboard.release(Key.down)
                keyboard.release('v')
                keyboard.release('w')
                keyboard.release('d')
                keyboard.release('s')
                keyboard.release('z')
                keyboard.release('a')
                keyboard.release('c')
                keyboard.release('x')

    cv2.imshow("DragonBall Controller", img)
    if cv2.waitKey(1) == ord("q"):
        break

