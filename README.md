<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=250&section=header&text=Racing%20CV&fontSize=60&animation=fadeIn&fontAlignY=38&desc=Next-Gen%20Gesture%20Racing%20Controller&descAlignY=51&descAlign=62" width="100%" />
</p>


# 🧤 Racing CV: Next-Gen Gesture Controller

<p align="center">
  <img src="https://img.shields.io/badge/Asphalt%208-Controller-blue?style=for-the-badge&logo=target" />
  <img src="https://img.shields.io/badge/Python-3.8+-yellow?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/OpenCV-Gaming-green?style=for-the-badge&logo=opencv" />
  <img src="https://img.shields.io/badge/Status-Fully%20Modernized-orange?style=for-the-badge" />
</p>

---

## 🚀 Overview

Experience **Asphalt 8** like never before. **Racing CV** transforms your webcam into a high-precision gesture input device. No controller? No problem. Use your hands to steer, drift, and blast through the competition with Nitro!

### ✨ What's New (v2.0)
- **Object-Oriented Refactor**: Clean, modular code for maximum performance.
- **Modern HUD**: Real-time steering wheel indicator and status bars.
- **Instructional Popup**: Intuitive setup guide before the race begins.
- **Low Latency**: Optimized hand tracking with MediaPipe.

---

## 🎮 Game Controls

| Action | Gesture | Icon |
| :--- | :--- | :---: |
| **STEER** | Rotate hands at 9 & 3 o'clock | <img src="assets/steering.png" width="60"> |
| **ACCELERATE** | Both palms wide open (🖐️ 🖐️) | 💨 |
| **BRAKE/DRIFT** | Both hands as fists (✊ ✊) | 🛑 |
| **NITRO** | Thumb up gesture (👍) | <img src="assets/nitro.png" width="60"> |

---

## 🛠️ Installation

1. **Clone the Repo**
   ```bash
   git clone https://github.com/SubashSK777/Racing-CV.git
   cd Racing-CV/Asphalt 8
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirement.txt
   ```

3. **Ignite the Engine**
   ```bash
   python main.py
   ```

---

## 🧠 How it Works

```mermaid
graph TD
    A[Webcam Feed] --> B(MediaPipe Hand Tracking)
    B --> C{Gesture Recognition}
    C -->|Tilt Angle| D[Virtual Steering Wheel]
    C -->|Fingers Count| E[Pedal Logic]
    D --> F[SendInput API]
    E --> F
    F --> G[Asphalt 8 Game]
    G --> H((Victory! 🏆))
```

---

## 🌟 Visual HUD

The all-new **Modern HUD** provides real-time feedback:
- **Steering Wheel**: Rotates as you tilt your hands.
- **Power Bars**: Visual confirmation for Accel/Brake/Nitro.
- **Safety**: "Show Both Hands" warning when lost.

---

## 🤝 Contributing

Got ideas to make it faster? 🏎️💨
Feel free to fork, star, and submit an issue or PR!

## 📜 License
This project is licensed under the **GPL License**.

---

<p align="center">
  MADE WITH ❤️ FOR RACERS
</p>
