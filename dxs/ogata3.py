import cv2
import mediapipe as mp

# MediaPipe設定
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# 指先の番号
finger_names = {
    4: "親指",
    8: "人差し指",
    12: "中指",
    16: "薬指",
    20: "小指"
}

# 指が伸びているか判定
def finger_up(tip, pip, landmarks):
    return landmarks[tip].y < landmarks[pip].y

# カメラ起動
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("カメラを開けませんでした")
    exit()

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # 鏡表示
    frame = cv2.flip(frame, 1)

    # RGBへ変換
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 手認識
    result = hands.process(rgb)

    gesture = "Unknown"

    if result.multi_hand_landmarks:

        for hand_landmarks in result.multi_hand_landmarks:

            landmarks = hand_landmarks.landmark

            # 指の状態
            index = finger_up(8, 6, landmarks)
            middle = finger_up(12, 10, landmarks)
            ring = finger_up(16, 14, landmarks)
            pinky = finger_up(20, 18, landmarks)

            # 21点表示
            print("----------------")
            for i, lm in enumerate(landmarks):
                print(
                    i,
                    "x:", round(lm.x, 3),
                    "y:", round(lm.y, 3),
                    "z:", round(lm.z, 3)
                )

            # 指先表示
            for number, name in finger_names.items():
                lm = landmarks[number]
                print(
                    name,
                    "x:", round(lm.x, 3),
                    "y:", round(lm.y, 3),
                    "z:", round(lm.z, 3)
                )

            # ジェスチャー判定
            if index and middle and ring and pinky:
                gesture = "Open Hand"

            elif not index and not middle and not ring and not pinky:
                gesture = "Fist"

            elif index and middle and not ring and not pinky:
                gesture = "Scissors"

            # 骨格描画
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    # ジェスチャー表示
    cv2.putText(
        frame,
        gesture,
        (30, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # 映像表示
    cv2.imshow("Hand Skeleton", frame)

    # qキーで終了
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
