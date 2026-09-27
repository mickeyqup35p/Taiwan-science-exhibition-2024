THING1_SPEED = 15          #禮物移動速度
THING1_INTERVAL = [30,50]  #禮物出現間隔時間 (左邊小 右邊大、兩個數中間隨機取數)
THING1_RANGE = [100,350]   #可以收到禮物的X座標範圍 (左邊小 右邊大、X座標越大位置越往右)

from datetime import datetime
import pygsheets
import cv2
import mediapipe as mp
import pygame
import os
import random
import csv
player_number = input("輸入班級+座號> ")

FPS = 60
WIDTH = 800
HEIGHT = 800

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)

pygame.init()
clock = pygame.time.Clock()
data = []
file = input("開啟哪個?(要加.csv)> ")
get_score = 0

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)            # 讀取攝影機
lineType = cv2.LINE_AA               # 印出文字的邊框

current_path = os.path.abspath(os.path.dirname(__file__))
## 設置憑證
gc = pygsheets.authorize(service_file=os.path.join(current_path,'game-data-428509-e8de008d2ed0.json'))
sht = gc.open_by_url( "https://docs.google.com/spreadsheets/d/1Sya-stflGtbVlSf5ca5T_wbIzrmNCC48czEfpBm5R1Y/edit?gid=0#gid=0")
## 選擇要操作的 Google Sheet
# 指定工作表
wks = sht.worksheet_by_title('第1頁')

def percent(data):
    global hand_score
    hand_xy = finger_points[0]
    if len(finger_points) == 21:
        hand_score = 0
        hand_width = abs(((finger_points[0][0]-finger_points[9][0])**2+(finger_points[0][1]-finger_points[9][1])**2)**0.5)
        for i in range(20):
            if ((finger_points[i+1][0]/hand_width-hand_xy[0]/hand_width-data[i][0])**2+(finger_points[i+1][1]/hand_width-hand_xy[1]/hand_width-data[i][1])**2)**0.5 < 0.3 and ((finger_points[i+1][0]/hand_width-hand_xy[0]/hand_width-data[i][0])**2+(finger_points[i+1][1]/hand_width-hand_xy[1]/hand_width-data[i][1])**2)**0.5 > -0.3:
                hand_score += 5
                pygame.draw.circle(screen,GREEN,(540-finger_points[i+1][0],finger_points[i+1][1]+200),2,2)
            else:
                pygame.draw.circle(screen,RED,(540-finger_points[i+1][0],finger_points[i+1][1]+200),2,2)
        pygame.draw.circle(screen,BLACK,(540-finger_points[0][0],finger_points[0][1]+200),2,2)
        for i in range(20):
            pygame.draw.circle(screen,BLACK,(540-(data[i][0]*hand_width+hand_xy[0]),data[i][1]*hand_width+hand_xy[1]+200),2,2)
        return hand_score
    else:
        return 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img_people,(180,180))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        if mode == "2":
            self.rect.center = (200,400)
        else:
            self.rect.center = (400,600)
    def update(self,true):
        global result
        try:
            if true:
                result = percent(data)
            else:
                result = 0
        except:
            result = 0
        if result > 80:
            result = True
        else:
            result = False
            
class Thing1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        if data[-1][2] != "0":
            self.image = pygame.transform.scale(img_thing1,(180,180))
            self.image.set_colorkey((0,0,0))
        else:
            self.image = pygame.Surface((50,50))
            self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        if mode == "2":
            self.rect.center = (900,400)
        else:
            self.rect.center = (400,-100)
    def update(self,true):
        global score
        global thing1_kill
        global get_score
        if mode == "2":
            if result and self.rect.left >= THING1_RANGE[0] and self.rect.left <= THING1_RANGE[1]:
                score = score + 1
                get_score = 30
                thing1_kill = thing1_kill+1
                self.kill()
            if not result:
                self.rect.x -= THING1_SPEED
            if self.rect.x < 0:
                thing1_kill = thing1_kill+1
                self.kill()
        else:
            if result and self.rect.bottom <= 800-THING1_RANGE[0] and self.rect.bottom >= 800-THING1_RANGE[1]:
                score = score + 1
                get_score = 30
                thing1_kill = thing1_kill+1
                self.kill()
            if not result:
                self.rect.y += THING1_SPEED
            if self.rect.y > 800:
                thing1_kill = thing1_kill+1
                self.kill()

class Thing2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        if data[-1][3] != "0":
            self.image = pygame.transform.scale(img_thing2,(180,180))
            self.image.set_colorkey((0,0,0))
        else:
            self.image = pygame.Surface((50,50))
            self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (2000,2000)
    def update(self,true):
        if data[-1][3] != "0":
            if true:
                try:
                    if percent(data) > 60:
                        if mode == 2:
                            self.rect.center = (300,400)
                        else:
                            self.rect.center = (400,500)
                except:
                        self.rect.center = (2000,2000)
            else:
                self.rect.center = (2000,2000)
        else:
            self.rect.center = (2000,2000)
            
def draw_text(surf,text,size,x,y,color):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface,text_rect)

def draw_init():
    screen.fill((WHITE))  # 清除畫面
    if background != "0":
        screen.blit(pygame.transform.scale(img_background,(900,900)),(0,0))
    draw_text(screen,"比"+str(data[-2])+"接東西",64,WIDTH/2,HEIGHT/2,BLACK)
    draw_text(screen,"按任意鍵開始",32,WIDTH/2,HEIGHT*4/5,BLACK)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                waiting = False

def draw_finish():
    screen.fill((WHITE))  # 清除畫面
    if background != "0":
        screen.blit(pygame.transform.scale(img_background,(900,900)),(0,0))
    draw_text(screen,"遊戲結束",72,WIDTH/2,HEIGHT/5,BLACK)
    draw_text(screen,"分數"+str(score),64,WIDTH/2,HEIGHT/2,BLACK)
    draw_text(screen,"按任意鍵結束",32,WIDTH/2,HEIGHT*4/5,BLACK)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                waiting = False

def finish_code():
    read = 0
    one_data = 0
    now_time = datetime.now()
    while one_data != "":
        read += 1
        one_data = wks.get_value('A'+str(read))
    wks.update_value('A'+str(read), player_number)
    wks.update_value('B'+str(read), str(now_time))
    wks.update_value('C'+str(read), str(score))
    exit()

current_path = os.path.abspath(os.path.dirname(__file__))
#try:
with open(os.path.join(current_path, "資料", file), newline="") as csvfile:
        # 讀取 CSV 檔案內容
        rows = csv.reader(csvfile)
        screen = pygame.display.set_mode((WIDTH,HEIGHT))
        for row in rows:
            if len(row) == 2:
                data.append([float(row[0]),float(row[1])])
            else:
                data.append(row)
        background = data[-1][0]
        mode = data[-1][1]
        if data[-1][4] != "0":
            img_people = pygame.image.load(os.path.join(current_path, "img", data[-1][4])).convert()#人
        else:
            img_people = pygame.image.load(os.path.join(current_path, "img", "人.png")).convert()#人
        if data[-1][3] != "0":
            img_thing2 = pygame.image.load(os.path.join(current_path, "img", data[-1][3])).convert()#工具
        if data[-1][2] != "0":
            img_thing1 = pygame.image.load(os.path.join(current_path, "img", data[-1][2])).convert()#移動的物品
        if background != "0":
            img_background = pygame.image.load(os.path.join(current_path, "img", background)).convert()#背景
        font_name = os.path.join(current_path,"font.ttf")
        show_init = True
        with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
            if not cap.isOpened():
                print("Cannot open camera")
                pygame.quit()
                exit()
            w, h = 540, 310      # 影像尺寸
            while True:
                ret,img = cap.read()
                img = cv2.resize(img, (w,h))                 # 縮小尺寸，加快處理效率
                img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 轉換成 RGB 色彩
                results = hands.process(img2)                # 偵測手勢
                img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)  # 轉換回 BGR 色彩
                clock.tick(FPS)
                if show_init:
                    time = 0
                    score = 0
                    finger_points = []
                    finish = False
                    all_sprites = pygame.sprite.Group()
                    thing1_sprites = pygame.sprite.Group()
                    player = Player()
                    thing_2 = Thing2()
                    all_sprites.add(player)
                    all_sprites.add(thing_2)
                    show_init = True
                    draw_init()
                    show_init = False
                    finger_log4y = []
                    wait_time = 60
                    result_log = []
                    thing1_amount = 0
                    thing1_kill = 0
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
                else:
                    hand_true = False
                time = time+1
                if time > 2000:
                    finish = True
                if wait_time < 1 and thing1_amount < 20:
                    thing_1 = Thing1()
                    all_sprites.add(thing_1)
                    thing1_sprites.add(thing_1)
                    thing1_amount = thing1_amount+1
                    wait_time = random.randint(THING1_INTERVAL[0],THING1_INTERVAL[1])
                else:
                    try:
                        if not result:
                            wait_time = wait_time-1
                    except:
                        wait_time = wait_time-1
                if thing1_kill > 19:
                    finish = True
                cv2.imshow('1', img2)
                if finish:
                    cv2.destroyAllWindows()
                    draw_finish()
                    finish_code()
                screen.fill((WHITE))  # 清除畫面
                if background != "0":
                    screen.blit(pygame.transform.scale(img_background,(900,900)),(0,0))
                all_sprites.update(hand_true)
                all_sprites.draw(screen)
                if mode == "2":
                    pygame.draw.rect(screen, RED, [225, 300, 50, 200], 10)
                else:
                    pygame.draw.rect(screen, RED, [300, 800-255, 200, 50], 10)
                if get_score != 0:
                    draw_text(screen,"+1",72,100,100,(255,255-get_score*8,255-get_score*8))
                    get_score -= 1
                pygame.display.update()
                if cv2.waitKey(5) == ord('q'):
                    pygame.quit()
                    cap.release()
                    cv2.destroyAllWindows()
                    exit()