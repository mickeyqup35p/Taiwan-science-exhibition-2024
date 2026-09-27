#從https://steam.oxxostudio.tw/category/python/ai/ai-mediapipe-gesture.html修改

import cv2
import mediapipe as mp
import math
import time
from PIL import Image, ImageDraw, ImageFont
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
finger_angle1 = []
finger_angle2 = []
finger_angle3 = []
finger_angle4 = []
finger_angle5 = []
hand_x = []
hand_y = []
hand4_x = []
hand4_y = []
hand8_x = []
hand8_y = []
hand_long = []
nose_x = []
nose_y = []
str_hungry = [0,0,0,0,0]
str_to_look_for1 = [1,0,1,1,1]
str_to_look_for2 = [0,0,1,1,1]
str_rob1 = [1,1,1,1,1]
str_rob2 = [0,0,0,0,0]
str_to_lose1 = [0,0,0,0,0]
str_to_lose2 = [1,1,1,1,1]
str_not_to_know = [1,1,1,1,1]
str_to_understand = [0,1,1,0,0]
str_not_right = [1,1,0,0,0]
str_at_once = [1,1,0,0,0]
str_Thanks = [1,0,0,0,0]
str_do_not_want = [1,1,1,1,1]
str_happy = [1,1,1,1,1]
str_angre = [0,1,0,0,0]
str_painful = [0,0,0,0,0]
str_pancil1 = [0,1,0,0,0]
str_pancil2 = [1,0,0,0,0]
str_we = [1,0,0,0,1]
str_nervous1 = [1,1,1,1,1]
str_nervous2 = [0,1,0,0,0]
str_respirator = [1,1,0,0,0]
def cv2AddChineseText(img, text, position, textColor=(0, 255, 0), textSize=30):
    if (isinstance(img, np.ndarray)):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontStyle = ImageFont.truetype(
        "simsun.ttc", textSize, encoding="utf-8")
    draw.text(position, text, textColor, font=fontStyle)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
def vector_2d_angle(v1, v2):
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        angle_= math.degrees(math.acos((v1_x*v2_x+v1_y*v2_y)/(((v1_x**2+v1_y**2)**0.5)*((v2_x**2+v2_y**2)**0.5))))
    except:
        angle_ = 180
    return angle_
# 根據傳入的 21 個節點座標，得到該手指的角度
def hand_angle(hand_):
    angle_list = []
    # thumb 大拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[2][0])),(int(hand_[0][1])-int(hand_[2][1]))),
        ((int(hand_[3][0])- int(hand_[4][0])),(int(hand_[3][1])- int(hand_[4][1])))
        )
    angle_list.append(angle_)
    # index 食指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])-int(hand_[6][0])),(int(hand_[0][1])- int(hand_[6][1]))),
        ((int(hand_[7][0])- int(hand_[8][0])),(int(hand_[7][1])- int(hand_[8][1])))
        )
    angle_list.append(angle_)
    # middle 中指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[10][0])),(int(hand_[0][1])- int(hand_[10][1]))),
        ((int(hand_[11][0])- int(hand_[12][0])),(int(hand_[11][1])- int(hand_[12][1])))
        )
    angle_list.append(angle_)
    # ring 無名指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[14][0])),(int(hand_[0][1])- int(hand_[14][1]))),
        ((int(hand_[15][0])- int(hand_[16][0])),(int(hand_[15][1])- int(hand_[16][1])))
        )
    angle_list.append(angle_)
    # pink 小拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[18][0])),(int(hand_[0][1])- int(hand_[18][1]))),
        ((int(hand_[19][0])- int(hand_[20][0])),(int(hand_[19][1])- int(hand_[20][1])))
        )
    if len(hand_x)>19:
        angle_list.append(angle_)
        del hand_x[0]
        hand_x.append(hand_[0][0])
        del hand_y[0]
        hand_y.append(hand_[0][1])
        del hand4_x[0]
        hand4_x.append(hand_[4][0])
        del hand4_y[0]
        hand4_y.append(hand_[4][1])
        del hand8_x[0]
        hand8_x.append(hand_[8][0])
        del hand8_y[0]
        hand8_y.append(hand_[8][1])
        del hand_long[0]
        hand_long.append(((hand_[0][1]-hand_[12][1])**2+(hand_[0][0]-hand_[12][0])**2)**0.5)
    else:
        angle_list.append(angle_)
        hand_x.append(hand_[0][0])
        hand_y.append(hand_[0][1])
        hand4_x.append(hand_[4][0])
        hand4_y.append(hand_[4][1])
        hand8_x.append(hand_[8][0])
        hand8_y.append(hand_[8][1])
        hand_long.append(((hand_[0][1]-hand_[12][1])**2+(hand_[0][0]-hand_[12][0])**2)**0.5)
    return angle_list
# 根據手指角度的串列內容，返回對應的手勢名稱
def hand_pos(hand_):
    # 小於 50 表示手指伸直，大於等於 50 表示手指捲縮
    try:
        finger_angle_list = [[finger_angle1[0],finger_angle2[0],finger_angle3[0],finger_angle4[0],finger_angle5[0]],[finger_angle1[1],finger_angle2[1],finger_angle3[1],finger_angle4[1],finger_angle5[1]],[finger_angle1[2],finger_angle2[2],finger_angle3[2],finger_angle4[2],finger_angle5[2]],[finger_angle1[3],finger_angle2[3],finger_angle3[3],finger_angle4[3],finger_angle5[3]],[finger_angle1[4],finger_angle2[4],finger_angle3[4],finger_angle4[4],finger_angle5[4]],[finger_angle1[5],finger_angle2[5],finger_angle3[5],finger_angle4[5],finger_angle5[5]],[finger_angle1[6],finger_angle2[6],finger_angle3[6],finger_angle4[6],finger_angle5[6]],[finger_angle1[7],finger_angle2[7],finger_angle3[7],finger_angle4[7],finger_angle5[7]],[finger_angle1[8],finger_angle2[8],finger_angle3[8],finger_angle4[8],finger_angle5[8]],[finger_angle1[9],finger_angle2[9],finger_angle3[9],finger_angle4[9],finger_angle5[9]],[finger_angle1[10],finger_angle2[10],finger_angle3[10],finger_angle4[10],finger_angle5[10]],[finger_angle1[11],finger_angle2[11],finger_angle3[11],finger_angle4[11],finger_angle5[11]],[finger_angle1[12],finger_angle2[12],finger_angle3[12],finger_angle4[12],finger_angle5[12]],[finger_angle1[13],finger_angle2[13],finger_angle3[13],finger_angle4[13],finger_angle5[13]],[finger_angle1[14],finger_angle2[14],finger_angle3[14],finger_angle4[14],finger_angle5[14]],[finger_angle1[15],finger_angle2[15],finger_angle3[15],finger_angle4[15],finger_angle5[15]],[finger_angle1[16],finger_angle2[16],finger_angle3[16],finger_angle4[16],finger_angle5[16]],[finger_angle1[17],finger_angle2[17],finger_angle3[17],finger_angle4[17],finger_angle5[17]],[finger_angle1[18],finger_angle2[18],finger_angle3[18],finger_angle4[18],finger_angle5[18]],[finger_angle1[19],finger_angle2[19],finger_angle3[19],finger_angle4[19],finger_angle5[19]]]
        if finger_angle_list[19]==str_to_look_for1 or finger_angle_list[19]==str_to_look_for2:
            if (hand_y[-1]-hand_y[-5]>4 or hand_y[-1]-hand_y[-5]<0-4) and (hand_y[-1]-hand_y[-5]>4 or hand_y[-1]-hand_y[-5]<0-4):
                    return "尋找"
            if hand_[8][1]-hand_[4][1]>30 or hand_[8][1]-hand_[4][1]<0-20:
                return "上廁所"
            else:
                return "OK"
        elif finger_angle_list[19]==str_happy and (hand8_y[-1]-hand8_y[-5]<0-10 or hand8_y[-1]-hand8_y[-5]>10) and str_to_lose1 not in finger_angle_list:
            if str_at_once in finger_angle_list:
                return "快樂"
            else:
                return "不知道"
        elif hand_long[-1]<80 and hand_long[-15]>80 and finger_angle_list[19]!=[0,0,0,0,0]:
            return "不要"
        elif finger_angle_list[19]==str_hungry and hand_[9][1]-hand_[0][1]>0:
            return "肚子餓"
        elif finger_angle_list[19]==str_angre and finger_angle_list[0]==str_angre and (hand4_y[-1]-hand4_y[-10]<0-20 or hand4_y[-1]-hand4_y[-10]>20):
            return "生氣"
        elif finger_angle_list[19]==str_nervous1 and (hand4_x[-1]-hand4_x[4]>5 or hand4_x[-1]-hand4_x[4]<0-5)and str_nervous2 in finger_angle_list:
            return "緊張"
        elif finger_angle_list[19]==str_not_right and (hand4_x[-1]-hand4_x[4]>5 or hand4_x[-1]-hand4_x[4]<0-5) and (hand_x-nose_x>20 or hand_x-nose_x<0-20) and (nose_x[-1]-nose_x[-3]>2 or nose_x[-1]-nose_x[-3]<0-2):
            return "不是"
        elif finger_angle_list[19]==str_at_once and hand_y[-1]-hand_y[0]<0-5:
            return "立刻"
        elif str_respirator in finger_angle_list and hand_y[-1]-nose_y[-1]>0-40 and hand_y[-1]-nose_y[-1]<20:
            return "口罩"
        elif finger_angle_list[19]==str_pancil2 and str_pancil1 in finger_angle_list:
            return "鉛筆"
        elif finger_angle_list[19]==str_painful and hand_y[-1]-nose_y[-1]<0:
            return "痛苦"
        elif finger_angle_list[19]==str_rob2 and str_rob1 in finger_angle_list:
            return "搶"
        elif finger_angle_list[19]==str_to_lose2 and str_to_lose1 in finger_angle_list:
            return "遺失"
        elif finger_angle_list[19]==str_to_understand and (hand_y[-1]-hand_y[-10]<0-20 or hand_y[-1]-hand_y[-10]>20):
            return "了解"
        elif finger_angle_list[19]==str_we and (hand_x[-1]-hand_x[-10]>10 or hand_x[-1]-hand_x[-10]<0-10):
            return "我們"
        elif finger_angle_list[19]==str_Thanks and (hand4_y[-1]-hand4_y[4]>2 or hand4_y[-1]-hand4_y[4]<0-2):
            if str_respirator in finger_angle_list and (hand_x-nose_x<30 or hand_x-nose_x>0-30):
                return "口罩"
            else:
                return "謝謝"
        else:
            return ""
    except:
        return ""
cap = cv2.VideoCapture(0)            # 讀取攝影機
fontFace = cv2.FONT_HERSHEY_SIMPLEX  # 印出文字的字型
lineType = cv2.LINE_AA               # 印出文字的邊框
mp_face_detection = mp.solutions.face_detection   # 建立偵測方法
# mediapipe 啟用偵測手掌
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    with mp_face_detection.FaceDetection(             # 開始偵測人臉
        model_selection=0, min_detection_confidence=0.5) as face_detection:
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        w, h = 540, 310                                  # 影像尺寸
        while True:
            ret, img = cap.read()
            img = cv2.resize(img, (w,h))                 # 縮小尺寸，加快處理效率
            if not ret:
                print("Cannot receive frame")
                break
            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 轉換成 RGB 色彩
            results = hands.process(img2)                # 偵測手勢
            results2 = face_detection.process(img2)
            time.sleep(0.05)
            if results.multi_hand_landmarks and results2.detections:
                for hand_landmarks in results.multi_hand_landmarks:
                    finger_points = []                   # 記錄手指節點座標的串列
                    mp_drawing.draw_landmarks(img,hand_landmarks,mp_hands.HAND_CONNECTIONS,mp_drawing_styles.get_default_hand_landmarks_style(),mp_drawing_styles.get_default_hand_connections_style())
                for detection in results2.detections:
                    mp_drawing.draw_detection(img, detection)
                    for i in hand_landmarks.landmark:
                        # 將 21 個節點換算成座標，記錄到 finger_points
                        x = i.x*w
                        y = i.y*h
                        finger_points.append((x,y))
                    if finger_points:
                        finger_angle = hand_angle(finger_points) # 計算手指角度，回傳長度為 5 的串列
                        if len(finger_angle1)>19:
                            del finger_angle1[0]
                            if finger_angle[0]<50:
                                finger_angle1.append(1)
                            else:
                                finger_angle1.append(0)
                            del finger_angle2[0]
                            if finger_angle[1]<50:
                                finger_angle2.append(1)
                            else:
                                finger_angle2.append(0)
                            del finger_angle3[0]
                            if finger_angle[2]<50:
                                finger_angle3.append(1)
                            else:
                                finger_angle3.append(0)
                            del finger_angle4[0]
                            if finger_angle[3]<50:
                                finger_angle4.append(1)
                            else:
                                finger_angle4.append(0)
                            del finger_angle5[0]
                            if finger_angle[4]<50:
                                finger_angle5.append(1)
                            else:
                                finger_angle5.append(0)
                            nose_x.append(int(detection.location_data.relative_keypoints[2].x*w))
                            del nose_x[0]
                            nose_y.append(int(detection.location_data.relative_keypoints[2].y*h))
                            del nose_y[0]
                        else:
                            if finger_angle[0]<50:
                                finger_angle1.append(1)
                            else:
                                finger_angle1.append(0)
                            if finger_angle[1]<50:
                                finger_angle2.append(1)
                            else:
                                finger_angle2.append(0)
                            if finger_angle[2]<50:
                                finger_angle3.append(1)
                            else:
                                finger_angle3.append(0)
                            if finger_angle[3]<50:
                                finger_angle4.append(1)
                            else:
                                finger_angle4.append(0)
                            if finger_angle[4]<50:
                                finger_angle5.append(1)
                            else:
                                finger_angle5.append(0)
                            nose_x.append(int(detection.location_data.relative_keypoints[2].x*w))
                            nose_y.append(int(detection.location_data.relative_keypoints[2].y*h))
                            #print(finger_angle)                      # 印出角度 ( 有需要就開啟註解 )
                        print(str([finger_angle1[-1],finger_angle2[-1],finger_angle3[-1],finger_angle4[-1],finger_angle5[-1]]))
                        try:
                            text = hand_pos(finger_points)
                            if text != "":
                                img = cv2AddChineseText(img, text,(10,10),(255,255,255), 100) # 印出文字
                                cv2.imshow("2", img)
                                time.sleep(0.5)
                                finger_angle1 = []
                                finger_angle2 = []
                                finger_angle3 = []
                                finger_angle4 = []
                                finger_angle5 = []
                                hand_x = []
                                hand_y = []
                                hand4_x = []
                                hand4_y = []
                                hand8_x = []
                                hand8_y = []
                                hand_long = []
                                nose_x = []
                                nose_y = []
                            else:
                                img = cv2AddChineseText(img, "",(10,10),(255,255,255), 100)
                        except:
                            img = cv2AddChineseText(img, "",(10,10),(255,255,255), 100)
            cv2.imshow('1', img)
            if cv2.waitKey(5) == ord('q'):
                break
cap.release()
cv2.destroyAllWindows()
