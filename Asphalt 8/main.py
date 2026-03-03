import cv2
import mediapipe as mp
import numpy as np
import time
import math
import tkinter as tk
from tkinter import messagebox
from directkeys import PressKey, ReleaseKey, up_pressed, down_pressed, left_pressed, right_pressed

# Scan codes
SCAN_UP = up_pressed
SCAN_DOWN = down_pressed
SCAN_LEFT = left_pressed
SCAN_RIGHT = right_pressed
SCAN_NITRO = 0x39  # Space

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.tip_ids = [4, 8, 12, 16, 20]

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        
        hands_data = []
        if self.results.multi_hand_landmarks:
            for hand_no, hand_lms in enumerate(self.results.multi_hand_landmarks):
                # Get hand label (Left/Right)
                label = self.results.multi_handedness[hand_no].classification[0].label
                
                lm_list = []
                for id, lm in enumerate(hand_lms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append([id, cx, cy])
                
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
                
                hands_data.append({"label": label, "lm_list": lm_list})
        
        return hands_data

    def fingers_up(self, hand):
        lm_list = hand["lm_list"]
        label = hand["label"]
        fingers = []

        # Thumb (Logic depends on Left/Right hand)
        if label == "Right":
            if lm_list[self.tip_ids[0]][1] < lm_list[self.tip_ids[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        else: # Left hand
            if lm_list[self.tip_ids[0]][1] > lm_list[self.tip_ids[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if lm_list[self.tip_ids[id]][2] < lm_list[self.tip_ids[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers

class ModernHUD:
    @staticmethod
    def draw_steering_wheel(img, angle):
        h, w, _ = img.shape
        center = (w // 2, h // 2)
        radius = 80
        color = (0, 255, 0) if abs(angle) < 15 else (0, 165, 255)
        if abs(angle) > 40: color = (0, 0, 255)

        # Draw circle
        cv2.circle(img, center, radius, color, 3)
        cv2.circle(img, center, 5, color, -1)

        # Draw spokes based on angle
        rad = math.radians(angle)
        p1 = (int(center[0] - radius * math.cos(rad)), int(center[1] - radius * math.sin(rad)))
        p2 = (int(center[0] + radius * math.cos(rad)), int(center[1] + radius * math.sin(rad)))
        cv2.line(img, p1, p2, color, 5)
        
        # Text
        text = "STRAIGHT"
        if angle < -15: text = "STEER LEFT"
        elif angle > 15: text = "STEER RIGHT"
        cv2.putText(img, text, (center[0] - 60, center[1] + radius + 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    @staticmethod
    def draw_status_bar(img, label, value, pos, color):
        x, y = pos
        bar_len = 150
        cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.rectangle(img, (x, y), (x + bar_len, y + 20), (50, 50, 50), -1)
        if value:
            cv2.rectangle(img, (x, y), (x + bar_len, y + 20), color, -1)
        cv2.rectangle(img, (x, y), (x + bar_len, y + 20), (200, 200, 200), 1)

class InstructionUI:
    def __init__(self, on_start):
        self.root = tk.Tk()
        self.root.title("Asphalt 8 Gesture Controller - Setup")
        self.root.geometry("500x550")
        self.root.configure(bg="#1e1e1e")
        self.on_start = on_start
        
        # Custom Font
        try:
            from tkinter import font
            title_font = font.Font(family="Helvetica", size=18, weight="bold")
            normal_font = font.Font(family="Helvetica", size=11)
        except:
            title_font = ("Arial", 18, "bold")
            normal_font = ("Arial", 11)

        main_frame = tk.Frame(self.root, bg="#1e1e1e", padx=30, pady=30)
        main_frame.pack(fill="both", expand=True)

        tk.Label(main_frame, text="READY TO RACE?", font=title_font, fg="#00ff00", bg="#1e1e1e").pack(pady=(0, 20))
        
        instructions = [
            ("STEER", "Hold both hands up like a steering wheel. Tilt them left/right."),
            ("ACCELERATE", "Open both palms (all fingers up)."),
            ("BRAKE / DRIFT", "Close both hands into fists."),
            ("NITRO", "Give a 'Thumb Up' with either hand."),
            ("QUIT", "Press 'Q' in the camera window to stop.")
        ]

        for title, desc in instructions:
            f = tk.Frame(main_frame, bg="#2d2d2d", pady=8, padx=10)
            f.pack(fill="x", pady=5)
            tk.Label(f, text=title, font=("Helvetica", 10, "bold"), fg="#00aaff", bg="#2d2d2d").pack(anchor="w")
            tk.Label(f, text=desc, font=normal_font, fg="#ffffff", bg="#2d2d2d", wraplength=400, justify="left").pack(anchor="w")

        tk.Button(main_frame, text="START CONTROLLER", bg="#00ff00", fg="#000000", font=("Helvetica", 12, "bold"), 
                  command=self.start, padx=20, pady=10, activebackground="#00cc00").pack(pady=30)
        
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

    def start(self):
        self.root.withdraw()
        self.on_start()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

class Asphalt8Controller:
    def __init__(self):
        self.tracker = HandTracker()
        self.hud = ModernHUD()
        self.cap = cv2.VideoCapture(0)
        self.current_keys = set()
        self.running = False

    def press(self, key):
        if key not in self.current_keys:
            PressKey(key)
            self.current_keys.add(key)

    def release(self, key):
        if key in self.current_keys:
            ReleaseKey(key)
            self.current_keys.discard(key)

    def release_all(self):
        for key in list(self.current_keys):
            ReleaseKey(key)
        self.current_keys.clear()

    def start(self):
        self.running = True
        print("Controller Started. Switch to Asphalt 8 window!")
        
        prev_time = 0
        while self.running:
            success, img = self.cap.read()
            if not success: break
            
            img = cv2.flip(img, 1)
            hands = self.tracker.find_hands(img)
            
            h, w, _ = img.shape
            
            # Action flags
            accel = False
            brake = False
            nitro = False
            angle = 0
            
            if len(hands) == 2:
                # Steering logic
                # Get wrist positions
                h1 = hands[0]["lm_list"][0] # Wrist
                h2 = hands[1]["lm_list"][0] # Wrist
                
                # Sort by X to consistently know left Hand (lowest X) and right Hand (highest X)
                # But MediaPipe already gives "Left"/"Right" labels. 
                # Note: labels are mirrored.
                
                l_hand = next((h for h in hands if h["label"] == "Left"), None)
                r_hand = next((h for h in hands if h["label"] == "Right"), None)
                
                if l_hand and r_hand:
                    p1 = l_hand["lm_list"][0] # Left Wrist
                    p2 = r_hand["lm_list"][0] # Right Wrist
                    
                    # Calculate angle
                    dy = p2[2] - p1[2]
                    dx = p2[1] - p1[1]
                    angle = math.degrees(math.atan2(dy, dx))
                    
                    # Normalizing angle: Horizontal is roughly 0 or 180 depending on order.
                    # With p1 being left and p2 being right, dy > 0 means right hand is lower (tilt right).
                    # dy < 0 means right hand is higher (tilt left).
                    
                    if angle > 15: self.press(SCAN_RIGHT); self.release(SCAN_LEFT)
                    elif angle < -15: self.press(SCAN_LEFT); self.release(SCAN_RIGHT)
                    else: self.release(SCAN_LEFT); self.release(SCAN_RIGHT)

                    # Fingers logic
                    l_fingers = self.tracker.fingers_up(l_hand)
                    r_fingers = self.tracker.fingers_up(r_hand)
                    
                    # Accel: Both hands open
                    if sum(l_fingers) >= 4 and sum(r_fingers) >= 4:
                        accel = True
                        self.press(SCAN_UP)
                        self.release(SCAN_DOWN)
                    # Brake: Both hands closed
                    elif sum(l_fingers) <= 1 and sum(r_fingers) <= 1:
                        brake = True
                        self.press(SCAN_DOWN)
                        self.release(SCAN_UP)
                    else:
                        self.release(SCAN_UP)
                        self.release(SCAN_DOWN)
                        
                    # Nitro: Either thumb up (finger 0)
                    if l_fingers[0] == 1 or r_fingers[0] == 1:
                        nitro = True
                        self.press(SCAN_NITRO)
                    else:
                        self.release(SCAN_NITRO)
            else:
                self.release_all()
                cv2.putText(img, "SHOW BOTH HANDS", (w // 2 - 120, h - 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            # Draw HUD
            self.hud.draw_steering_wheel(img, angle)
            self.hud.draw_status_bar(img, "ACCEL", accel, (20, 50), (0, 255, 0))
            self.hud.draw_status_bar(img, "BRAKE", brake, (20, 100), (0, 0, 255))
            self.hud.draw_status_bar(img, "NITRO", nitro, (20, 150), (0, 165, 255))
            
            # FPS
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time)
            prev_time = curr_time
            cv2.putText(img, f"FPS: {int(fps)}", (w - 100, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            cv2.imshow("Asphalt 8 Controller HUD", img)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False
                break

        self.release_all()
        self.cap.release()
        cv2.destroyAllWindows()

def main():
    def launch_controller():
        controller = Asphalt8Controller()
        controller.start()

    ui = InstructionUI(on_start=launch_controller)
    ui.run()

if __name__ == "__main__":
    main()
