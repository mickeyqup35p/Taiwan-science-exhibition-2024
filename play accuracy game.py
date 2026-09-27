from datetime import datetime
import pygsheets
import csv
import mediapipe as mp
import pygame
import cv2
import os
player_number = input("輸入班級+座號> ")

FPS = 60
WIDTH = 540
HEIGHT = 410

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)

score = 0
hand_xy = [0,0]
data = []
hand_width = 0
schedule = ["wait",10]
wait_time = 0
score_log = []
time_log = []
now_time = datetime.now().strftime("%H:%M:%S")
wait_percent = 0

current_path = os.path.abspath(os.path.dirname(__file__))
# 個人
gc_personal = pygsheets.authorize(service_file=os.path.join(current_path,"game-data-428509-e8de008d2ed0.json"))
sht_personal = gc_personal.open_by_url( "https://docs.google.com/spreadsheets/d/1YaDE6jNlvgIGeML8XXjObm4XMPCl6vQrt38O9kk7fHU/edit?usp=sharing")
try:
    wks_personal = sht_personal.worksheet_by_title(player_number[-2:])
except:
    print("找不到座號")
# 班級
gc_class = pygsheets.authorize(service_file=os.path.join(current_path,"game-data-428509-e8de008d2ed0.json"))
sht_class = gc_class.open_by_url( "https://docs.google.com/spreadsheets/d/1h4BIMqtTArO62W27n0x_1jDarSYDBM4fu70sSNxPoEc/edit?usp=sharing")
wks_class = sht_class.worksheet_by_title(player_number[:3])

pygame.init()
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

def percent(data):
    hand_xy = finger_points[0]
    if len(finger_points) == 21:
        score = 0
        hand_width = abs(((finger_points[0][0]-finger_points[9][0])**2+(finger_points[0][1]-finger_points[9][1])**2)**0.5)
        for i in range(20):
            if ((finger_points[i+1][0]/hand_width-hand_xy[0]/hand_width-data[i][0])**2+(finger_points[i+1][1]/hand_width-hand_xy[1]/hand_width-data[i][1])**2)**0.5 < 0.3 and ((finger_points[i+1][0]/hand_width-hand_xy[0]/hand_width-data[i][0])**2+(finger_points[i+1][1]/hand_width-hand_xy[1]/hand_width-data[i][1])**2)**0.5 > -0.3:
                score += 5
                pygame.draw.circle(screen,GREEN,(540-finger_points[i+1][0],finger_points[i+1][1]+100),2,2)
            else:
                pygame.draw.circle(screen,RED,(540-finger_points[i+1][0],finger_points[i+1][1]+100),2,2)
        pygame.draw.circle(screen,BLACK,(540-finger_points[0][0],finger_points[0][1]+100),2,2)
        for i in range(20):
            pygame.draw.circle(screen,BLACK,(540-(data[i][0]*hand_width+hand_xy[0]),data[i][1]*hand_width+hand_xy[1]+100),2,2)
        return score
    else:
        return 0

def finish_code():
    global wait_percent
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()
    print("儲存中，不要關掉。")
    read = 0
    one_data = 0
    now_time = datetime.now().strftime("%H:%M:%S")
    # 班級
    while one_data != "":
        read += 1
        one_data = wks_class.get_value("A"+str(read))
    for a in range(5):
        print(str(wait_percent)+"%")
        wks_class.update_value("A"+str(read+a), player_number)
        wks_class.update_value("B"+str(read+a), str(time_log[a]))
        wks_class.update_value("C"+str(read+a), str(score_log[a]))
        wait_percent += 10
    # 個人
    read = 0
    one_data = "1"
    while one_data != "":
        read += 1
        one_data = wks_personal.get_value("A"+str(read))
    for a in range(5):
        print(str(wait_percent)+"%")
        wks_personal.update_value("A"+str(read+a), player_number)
        wks_personal.update_value("B"+str(read+a), str(time_log[a]))
        wks_personal.update_value("C"+str(read+a), str(score_log[a]))
        wait_percent += 10
    print("100%")
    print("完成")
    exit()

# 開啟 CSV 檔案
with open(os.path.join(current_path, "資料", input("開啟哪個?(要加.csv)")), newline="") as csvfile:
    # 讀取 CSV 檔案內容
    rows = csv.reader(csvfile)
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    for row in rows:
        if len(row) == 2:
            data.append([float(row[0]),float(row[1])])
        else:
            data.append(row)
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
            if wait_time != 0:
                wait_time -= 1
            ret,img = cap.read()
            img = cv2.resize(img, (w,h))                 # 縮小尺寸，加快處理效率
            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 轉換成 RGB 色彩
            results = hands.process(img2)                # 偵測手勢
            img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)  # 轉換回 BGR 色彩
            clock.tick(FPS)
            screen.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    cap.release()
                    cv2.destroyAllWindows()
                    exit()

            if results.multi_hand_landmarks:
                hand_true = True
                for hand_landmarks in results.multi_hand_landmarks:
                    finger_points = []                   # 記錄手指節點座標的串列
                    mp_drawing.draw_landmarks(img,hand_landmarks,mp_hands.HAND_CONNECTIONS,mp_drawing_styles.get_default_hand_landmarks_style(),mp_drawing_styles.get_default_hand_connections_style())
                    for i in hand_landmarks.landmark:
                        # 將 21 個節點換算成座標，記錄到 finger_points
                        x = i.x*w
                        y = i.y*h
                        finger_points.append((x,y))
                score = percent(data)
                draw_text(screen,"正確率 : "+str(score)+"%",24,WIDTH/2,70,BLACK)
            else:
                hand_true = False

            draw_text(screen,"比出"+str(data[20]),24,WIDTH/2,20,BLACK)
            if schedule[0] == "wait":
                draw_text(screen,str(schedule[1])+"秒後開始",12,500,20,BLACK)
            else:
                draw_text(screen,"還有"+str(schedule[1])+"秒",12,500,70,BLACK)

            if now_time != datetime.now().strftime("%H:%M:%S"):
                if schedule[1] != 0:
                    if schedule[0] == "start":
                        if hand_true:
                            score_log.append(score)
                            time_log.append(datetime.now())
                        else:
                            score_log.append(0)
                    schedule[1] -= 1
                elif schedule[0] == "wait":
                    schedule[0] = "start"
                    schedule[1] = 5
                else:
                    finish_code()
                now_time = datetime.now().strftime("%H:%M:%S")

            pygame.display.update()
            if cv2.waitKey(5) == ord('q'):
                pygame.quit()
                cap.release()
                cv2.destroyAllWindows()
                exit()