# Hand Gesture Controlled LED System

An interactive computer vision and hardware control project that tracks hand gestures in real-time using OpenCV and MediaPipe (via `cvzone`) and dynamically controls 5 LEDs connected to an Arduino UNO using PyFirmata.

---

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Hardware Requirements](#hardware-requirements)
4. [Software & Library Requirements](#software--library-requirements)
5. [Circuit & Wiring Diagram](#circuit--wiring-diagram)
6. [Pin Mapping](#pin-mapping)
7. [System Architecture](#system-architecture)
8. [Setup & Installation](#setup--installation)
9. [How It Works](#how-it-works)
10. [Author](#author)

---

## Overview

This project uses a webcam to detect hand gestures and count raised fingers in real-time. Based on the finger count (0 to 5), signals are sent through a serial protocol (`pyfirmata`) to an Arduino board to light up a corresponding number of LEDs.

---

## Features

- **Real-Time Hand Tracking:** Powered by `cvzone.HandTrackingModule` (MediaPipe wrapper).
- **Dynamic LED Control:** Lights up 0 to 5 LEDs according to how many fingers are detected.
- **Hardware Abstraction:** Direct communication with Arduino via StandardFirmata, eliminating the need to write custom C++ code on the board.
- **Visual Feedback:** Displays on-screen finger count text overlaying the live camera feed.

---

## Hardware Requirements

1. **Arduino UNO** Development Board
2. **5x LEDs** (Red, Orange, Yellow, Green, Blue)
3. **5x Current-Limiting Resistors** (e.g., $220\,\Omega$)
4. **Breadboard**
5. **Jumper Wires**
6. **USB Cable** (for PC-to-Arduino connection)
7. **Webcam**

---

## Software & Library Requirements

- **Python 3.7+**
- **Libraries:**
  - `opencv-python` (`cv2`)
  - `cvzone`
  - `pyfirmata`
  - `mediapipe`

To install the Python dependencies:
```bash
pip install opencv-python cvzone pyfirmata mediapipe
```

---

## Circuit & Wiring Diagram

The LEDs are connected sequentially from digital pins `8` to `12` on the Arduino UNO, with their cathodes tied to a common ground rail on the breadboard.

---

## Pin Mapping

| Component | Arduino Pin | Control Logic |
| :--- | :--- | :--- |
| **LED 1** | Digital Pin 8 | Active when Finger Count $\ge 1$ |
| **LED 2** | Digital Pin 9 | Active when Finger Count $\ge 2$ |
| **LED 3** | Digital Pin 10 | Active when Finger Count $\ge 3$ |
| **LED 4** | Digital Pin 11 | Active when Finger Count $\ge 4$ |
| **LED 5** | Digital Pin 12 | Active when Finger Count $= 5$ |
| **GND** | GND Rail | Common ground cathode connection |

---

## System Architecture

```
+----------------+      OpenCV / cvzone      +------------------+
|  Webcam Feed   | ------------------------> | Hand Detector    |
+----------------+                           +------------------+
                                                       |
                                            Detects Raised Fingers
                                                       |
                                                       v
+----------------+      PyFirmata (COM)      +------------------+
|  Arduino UNO   | <------------------------ |  Controller.py   |
+----------------+                           +------------------+
        |
    D8 - D12
        v
+----------------+
|  5x LED Array  |
+----------------+
```

---

## Setup & Installation

1. **Upload StandardFirmata to Arduino:**
   - Open **Arduino IDE**.
   - Go to `File` > `Examples` > `Firmata` > `StandardFirmata`.
   - Select your board (**Arduino UNO**) and correct **COM Port**.
   - Click **Upload**.

2. **Configure COM Port in Python:**
   - Check your Arduino's COM port in Device Manager or Arduino IDE (e.g., `COM7`).
   - Open `controller.py` and set the `comport` variable:
     ```python
     comport = 'COM7'  # Replace with your actual COM port
     ```

3. **Run the Project:**
   ```bash
   python new.py
   ```
   - Press **`k`** to exit the application.

---

## How It Works

1. **`new.py` (Vision Pipeline):**
   - Captures frames from the camera, mirrors them horizontally for a natural display.
   - Utilizes `cvzone.HandTrackingModule.HandDetector` to identify hand landmarks.
   - Evaluates which fingers are upright (`detector.fingersUp(hand)` returning a list of 5 binary flags).
   - Calls `cnt.led(fingerUp)` from `controller.py` and renders on-screen status text.

2. **`controller.py` (Hardware Controller):**
   - Connects to the Arduino via `pyfirmata`.
   - Configures pins 8, 9, 10, 11, and 12 as digital outputs.
   - Maps the finger array state to corresponding LED pin outputs (`write(1)` for ON, `write(0)` for OFF).

---

## Author

**Noman Abdullah**

GitHub: [@nomanabdullah26](https://github.com/nomanabdullah26)
