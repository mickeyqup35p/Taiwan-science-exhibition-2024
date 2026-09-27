import cv2
import mediapipe as mp
import pygame
import os
import csv
import time

FPS = 60
WIDTH = 540
HEIGHT = 360

WHITE = (255,255,255)
BLACK = (0,0,0)

enter = False
hand_xy = []
hand_width = 0

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)            # 讀取攝影機
lineType = cv2.LINE_AA               # 印出文字的邊框

current_path = os.path.abspath(os.path.dirname(__file__))
font_name = os.path.join(current_path,"font.ttf")

def draw_text(surf,text,size,x,y,color):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface,text_rect)

def page1(finger):
    global enter
    for hand_x,hand_y in finger:
        if hand_y > 0:
            pygame.draw.circle(screen,BLACK,(540-hand_x,hand_y+50),2,2)
    if len(finger) == 21:
        draw_text(screen,"按ENTER確定",24,WIDTH/2,20,BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                enter = True
                screen.fill((WHITE))  # 清除畫面
                draw_text(screen,"在終端機輸入",24,WIDTH/2,20,BLACK)
                pygame.display.update()
                time.sleep(1)
                pygame.quit()
                cap.release()
                cv2.destroyAllWindows()
                name = input("這是甚麼意思?")
                file = input("存到哪裡?(要加.csv)")
                if input("做百分率打'1'、做遊戲打'2'") == "2":
                        background = input("用哪一個背景?不用背景打'0'。(要加副檔名)")
                        mode = input("做直向打'1'、做橫向打'2'")
                        thing1 = input("用哪一個物品移動?用方塊打'0'。(要加副檔名、colorkey是(0,0,0))")
                        thing2 = input("人物拿哪一個物品?不用拿打'0'。(要加副檔名、colorkey是(0,0,0))")
                        people = input("用哪一個人?用預設打'0'。(要加副檔名、colorkey是(0,0,0))")
                        print("儲存中")
                        hand_width = abs(((finger[0][0]-finger[9][0])**2+(finger[0][1]-finger[9][1])**2)**0.5)
                        with open(os.path.join(current_path, "資料", file),"w", newline='') as file:
                            writer = csv.writer(file)
                            hand_xy = finger[0]
                            for i in range(20):
                                writer.writerow([(finger[i+1][0]-hand_xy[0])/hand_width,(finger[i+1][1]-hand_xy[1])/hand_width])
                            writer.writerow([name])
                            writer.writerow([background,mode,thing1,thing2,people])
                        print("完成")
                        exit()
                else:
                        print("儲存中")
                        hand_width = abs(((finger[0][0]-finger[9][0])**2+(finger[0][1]-finger[9][1])**2)**0.5)
                        with open(os.path.join(current_path, "資料", file),"w", newline='') as file:
                            writer = csv.writer(file)
                            hand_xy = finger[0]
                            for i in range(20):
                                writer.writerow([(finger[i+1][0]-hand_xy[0])/hand_width,(finger[i+1][1]-hand_xy[1])/hand_width])
                            writer.writerow([name])
                        print("完成")
                        exit()

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    if not cap.isOpened():
        print("Cannot open camera")
        pygame.quit()
        exit()
    w, h = 540, 310                                  # 影像尺寸
    while True:
        ret,img = cap.read()
        img = cv2.resize(img, (w,h))                 # 縮小尺寸，加快處理效率
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 轉換成 RGB 色彩
        results = hands.process(img2)                # 偵測手勢
        img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)  # 轉換回 BGR 色彩
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                cap.release()
                cv2.destroyAllWindows()
                exit()

        if results.multi_hand_landmarks:
            if not enter:
                hand_true = True
                for hand_landmarks in results.multi_hand_landmarks:
                    finger_points = []                   # 記錄手指節點座標的串列
                    mp_drawing.draw_landmarks(img,hand_landmarks,mp_hands.HAND_CONNECTIONS,mp_drawing_styles.get_default_hand_landmarks_style(),mp_drawing_styles.get_default_hand_connections_style())
                    for i in hand_landmarks.landmark:
                        # 將 21 個節點換算成座標，記錄到 finger_points
                        x = i.x*w
                        y = i.y*h
                        finger_points.append((x,y))
        else:
            hand_true = False
        screen.fill((WHITE))  # 清除畫面
        if hand_true or enter:
            page1(finger_points)
        pygame.display.update()
        if cv2.waitKey(5) == ord('q'):
            pygame.quit()
            cap.release()
            cv2.destroyAllWindows()
            exit()