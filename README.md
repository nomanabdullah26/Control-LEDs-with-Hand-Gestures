# Hand Gesture Controlled LED System

An interactive computer vision and hardware control project that tracks hand gestures in real-time using OpenCV and MediaPipe (via `cvzone`) and dynamically controls 5 LEDs connected to an Arduino UNO using PyFirmata.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Demonstration & Execution Photos](#demonstration--execution-photos)
4. [Hardware Requirements](#hardware-requirements)
5. [Software & Library Requirements](#software--library-requirements)
6. [Circuit & Wiring Diagram](#circuit--wiring-diagram)
7. [Pin Mapping](#pin-mapping)
8. [System Architecture](#system-architecture)
9. [Source Code](#source-code)
10. [Setup & Installation](#setup--installation)
11. [How It Works](#how-it-works)
12. [Author](#author)

---

## Overview

This project uses a webcam to detect hand gestures and count raised fingers in real-time. Based on the finger count (0 to 5), signals are sent through a serial communication protocol (`pyfirmata`) to an Arduino board to dynamically light up a corresponding number of LEDs on a breadboard.

---

## Features

- **Real-Time Hand Tracking:** Powered by `cvzone.HandTrackingModule` (built on top of MediaPipe).
- **Dynamic Hardware Control:** Lights up 0 to 5 LEDs instantly based on detected fingers.
- **Hardware Abstraction:** Direct board manipulation from Python via `StandardFirmata`.
- **On-Screen Visual Feedback:** Live webcam feed overlaid with finger count status text and hand landmark skeletons.

---

## Demonstration & Execution Photos

| Finger Count: 0 (All LEDs OFF) | Finger Count: 2 (2 LEDs ON) | Finger Count: 5 (All 5 LEDs ON) |
| :---: | :---: | :---: |
| ![Finger Count 0](project%20photo-3.jpg) | ![Finger Count 2](project%20photo-1.jpg) | ![Finger Count 5](project%20photo-2.jpg) |

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

![Circuit Wiring Diagram](Screenshot%202026-10-15%20053344.png)

The LEDs are connected sequentially from digital pins `8` to `12` on the Arduino UNO, with their cathodes connected through resistors to a common ground rail on the breadboard.

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

```text
+----------------+      OpenCV / cvzone      +------------------+
|  Webcam Feed   | ------------------------> | Hand Detector    |
+----------------+                           +------------------+
                                                       |
                                            Detects Raised Fingers
                                                       |
                                                       v
+----------------+      PyFirmata (COM)      +------------------+
|  Arduino UNO   | <------------------------ |  controller.py   |
+----------------+                           +------------------+
        |
    D8 - D12
        v
+----------------+
|  5x LED Array  |
+----------------+
```

---

## Source Code

### 1. `new.py` (Main Gesture Detection Script)

```python
import cv2
import controller as cnt
from cvzone.HandTrackingModule import HandDetector

# Initialize HandDetector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Start webcam
video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    frame = cv2.flip(frame, 1)  # Mirror image
    hands, img = detector.findHands(frame)

    if hands:
        hand = hands[0]
        lmList = hand['lmList']
        fingerUp = detector.fingersUp(hand)

        print(fingerUp)
        cnt.led(fingerUp)  # Send data to Arduino

        # Display finger count
        if fingerUp == [0, 0, 0, 0, 0]:
            text = 'Finger count: 0'
        elif fingerUp == [0, 1, 0, 0, 0]:
            text = 'Finger count: 1'
        elif fingerUp == [0, 1, 1, 0, 0]:
            text = 'Finger count: 2'
        elif fingerUp == [0, 1, 1, 1, 0]:
            text = 'Finger count: 3'
        elif fingerUp == [0, 1, 1, 1, 1]:
            text = 'Finger count: 4'
        elif fingerUp == [1, 1, 1, 1, 1]:
            text = 'Finger count: 5'
        else:
            text = ''

        if text:
            cv2.putText(frame, text, (20, 460),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    if k == ord("k"):  # press 'k' to exit
        break

video.release()
cv2.destroyAllWindows()
```

### 2. `controller.py` (Arduino Communication Script)

```python
import pyfirmata
import time

# Set your COM port (check in Arduino IDE or Device Manager)
comport = 'COM7'
board = pyfirmata.Arduino(comport)

# Define LED pins
led_1 = board.get_pin('d:8:o')
led_2 = board.get_pin('d:9:o')
led_3 = board.get_pin('d:10:o')
led_4 = board.get_pin('d:11:o')
led_5 = board.get_pin('d:12:o')

def led(fingerUp):
    if fingerUp == [0, 0, 0, 0, 0]:
        led_1.write(0)
        led_2.write(0)
        led_3.write(0)
        led_4.write(0)
        led_5.write(0)

    elif fingerUp == [0, 1, 0, 0, 0]:
        led_1.write(1)
        led_2.write(0)
        led_3.write(0)
        led_4.write(0)
        led_5.write(0)

    elif fingerUp == [0, 1, 1, 0, 0]:
        led_1.write(1)
        led_2.write(1)
        led_3.write(0)
        led_4.write(0)
        led_5.write(0)

    elif fingerUp == [0, 1, 1, 1, 0]:
        led_1.write(1)
        led_2.write(1)
        led_3.write(1)
        led_4.write(0)
        led_5.write(0)

    elif fingerUp == [0, 1, 1, 1, 1]:
        led_1.write(1)
        led_2.write(1)
        led_3.write(1)
        led_4.write(1)
        led_5.write(0)

    elif fingerUp == [1, 1, 1, 1, 1]:
        led_1.write(1)
        led_2.write(1)
        led_3.write(1)
        led_4.write(1)
        led_5.write(1)

    # small delay to stabilize communication
    time.sleep(0.05)
```

---

## Setup & Installation

1. **Upload StandardFirmata to Arduino:**
   - Open **Arduino IDE**.
   - Navigate to `File` > `Examples` > `Firmata` > `StandardFirmata`.
   - Select your board (**Arduino UNO**) and the appropriate **COM Port**.
   - Click **Upload**.

2. **Configure COM Port in Python:**
   - Verify the connected port in Device Manager or Arduino IDE (e.g., `COM7`).
   - Open `controller.py` and update the `comport` variable:
     ```python
     comport = 'COM7'  # Update with your active port
     ```

3. **Run the System:**
   ```bash
   python new.py
   ```
   - Press **`k`** on your keyboard while the video feed window is focused to safely terminate the program.

---

## How It Works

1. **Computer Vision Processing (`new.py`):**
   - Captures real-time frames from the webcam and mirrors them.
   - `HandDetector` locates hand keypoints and checks which fingers are extended.
   - Converts finger states into binary list arrays (`[thumb, index, middle, ring, pinky]`).
   - Renders text overlays on screen for visual identification.

2. **Hardware Serial Execution (`controller.py`):**
   - Receives the finger array and maps each gesture combination to digital pin outputs (`1` for HIGH, `0` for LOW).
   - Updates pins 8 through 12 on the Arduino via PyFirmata serial commands.

---

## Author

**Noman Abdullah**

GitHub: [@nomanabdullah26](https://github.com/nomanabdullah26)
