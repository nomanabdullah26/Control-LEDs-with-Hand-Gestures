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
