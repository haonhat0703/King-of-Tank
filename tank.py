import pygame, sys, random
pygame.init()

# Set âm thanh trong trò chơi
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
mix1 = pygame.mixer.Sound('./sounds/exp.wav')
mix2 = pygame.mixer.Sound('./sounds/gun10.wav')
mix3 = pygame.mixer.Sound('./sounds/gun9.wav')
# điều chỉnh âm lượng 
mix1.set_volume(0.5)
mix2.set_volume(0.5)
mix3.set_volume(0.5)
#######################################################
#Các biến trong trò chơi
STEP = 50
MOVE = 3
FPS = 50
WIDTH = 800
HEIGHT = 600
SIZE_TANK = 25
walls = [] #nhân vật tường
gun_tank = [] #nhân vật đạn của xe tăng xanh
tank_enemy = [] #nhân vật xe tăng đỏ
gun_enemy = [] 
bullet_enemy = [] #Nhân vật đạn của xe tăng đỏ
rotate = 90 # gốc quay của xe tăng xanh
tank_blue_x = WIDTH//2 # vị trí x ban đầu của xe tăng xanh
tank_blue_y = HEIGHT - SIZE_TANK*2 # vị trí y ban đầu của xe tăng xanh
up, down, left, right = False, False, False, False # Biến giúp xe tăng xanh di chuyển êm
cout_tank, cout_tank2 = 0, 0 # số lượng xe tăng đỏ
######################################################
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # set màn hình trò chơi
pygame.display.set_caption('King of Tank')# tên trò chơi 
clock = pygame.time.Clock() # FPS
######################################################
# ảnh của các nhân vật
screen_main = pygame.image.load('./images/grass.png').convert_alpha()# sàn chơi
wall = pygame.image.load('./images/wall.png').convert_alpha() # tường
tank_blue_main = pygame.image.load('./images/tank_blue.png').convert_alpha() # tăng xanh
tank_enemy_main = pygame.image.load('./images/tank_red.png').convert_alpha() # tăng đỏ
tank_blue = pygame.transform.rotate(tank_blue_main, 90) # vị trí ban đầu theo gốc quay của tăng xanh
gun_of_tank = pygame.image.load('./images/bulletblue2.png').convert_alpha() # đạn xanh
gun_of_enemy = pygame.image.load("./images/bulletred2.png").convert_alpha() # đan đỏ
###################################################
# tạo sự kiện trong trò chơi
change = pygame.USEREVENT # tạo sự kiện 
pygame.time.set_timer(change, 700)
move_change = pygame.USEREVENT + 1
pygame.time.set_timer(move_change, 100)
bul_change = pygame.USEREVENT + 2
pygame.time.set_timer(bul_change, 500)
####################################################
# xây dựng vị trí  ngẫu nhiên tường và vị trí của các xe tăng đỏ xuất hiện
for x in range(16):
    for y in range(9):
        if random.randint(0, 100) < 50:
            walls.append((x*50, y*50 + 50))
        elif (cout_tank <= 2 or cout_tank2 <= 3) and random.randint(10, 200) % 3 == 1:
            ranf = random.randint(0, 3)
            if x*50 < WIDTH//2 and cout_tank <= 2:
                tank_enemy.append([[x*50, y*50 + 60], 90*ranf])
                cout_tank += 1
            elif x*50 >= WIDTH//2 and cout_tank <= 3:
                tank_enemy.append([[x*50, y*50 + 60], 90*ranf])
                cout_tank2 += 1
######################################################
# Các hàm trong trò chơi                    
def set_enemy():# Xét góc quay cho xe tăng đỏ - ngẫu nhiên
    global tank_enemy
    for i in range(len(tank_enemy)):
        luck = random.randint(0, 5)
        if  luck == 1:
            tank_enemy [i][1] = 90
        elif luck == 2:
            tank_enemy [i][1] = 180
        elif luck == 3:
            tank_enemy[i][1] = 270
        elif luck == 4:
            tank_enemy[i][1] = 0    
def drawWalls():# vẽ tường lên screen
    for x in range(len(walls)):
        screen.blit(wall, walls[x])
def check_coll(x, y, walls, SIZE_TANK = 33):# Xác định có va chạm giữa tường và vị trí mới của xe tăng xanh không 
    global STEP
    for wall in walls:
        if (wall[0] <= x <= wall[0] + STEP and wall[1] <= y <= wall[1] + STEP) or (wall[0]<= x + SIZE_TANK <= wall[0] + STEP and wall[1] <= y <= wall[1] + STEP) or (wall[0] <= x + SIZE_TANK<= wall[0] + STEP and wall[1] <= y + SIZE_TANK <= wall[1] + STEP) or (wall[0] <= x <= wall[0] + STEP and wall[1] <= y + SIZE_TANK <= wall[1] + STEP):
            return False
    return True
def tank_set():# di chuyển xe tăng xanh dựa trên kiểm tra vị trí mới có va chạm hay không và điều khiển bằng các nút mũi tên
    global tank_blue_x, tank_blue_y, tank_blue, rotate 
    if up  and check_coll(tank_blue_x, tank_blue_y - MOVE, walls ) and tank_blue_y - MOVE >= 0:
        tank_blue_y -= MOVE
        tank_blue = pygame.transform.rotate(tank_blue_main, 90)
        rotate = 90
    if down and check_coll(tank_blue_x, tank_blue_y + MOVE, walls) and tank_blue_y + MOVE <= HEIGHT-50:
        tank_blue_y += MOVE
        tank_blue = pygame.transform.rotate(tank_blue_main, 270)
        rotate = 270
    if left and check_coll(tank_blue_x - MOVE, tank_blue_y, walls) and tank_blue_x - MOVE >= 0:
        tank_blue_x -= MOVE
        tank_blue = pygame.transform.rotate(tank_blue_main, 180)
        rotate = 180
    if  right and check_coll(tank_blue_x + MOVE, tank_blue_y, walls) and tank_blue_x + MOVE <= WIDTH-50:
        tank_blue_x += MOVE
        tank_blue = pygame.transform.rotate(tank_blue_main, 0)
        rotate = 0
def tank_bullets_set():# set hướng và vị trí cho đạn xanh xuất hiện
    global rotate, gun_tank
    if event.key == pygame.K_SPACE:
        if rotate == 90: 
            gun_tank.append([[tank_blue_x + 17, tank_blue_y - 8], rotate])
        elif rotate == 0:
            gun_tank.append([[tank_blue_x + 40, tank_blue_y + 17], rotate])
        elif rotate == 270:
            gun_tank.append([[tank_blue_x + 17, tank_blue_y + 40], rotate])
        elif rotate == 180:
            gun_tank.append([[tank_blue_x - 8, tank_blue_y + 17], rotate])
def update():
    tank_set()
def check_coll_2(x, y, wall, SIZE_TANK = 5):# xác định có va chạm giữa đạn và tường khồng
    global STEP
    if (wall[0] <= x <= wall[0] + STEP and wall[1] <= y <= wall[1] + STEP) or (wall[0]<= x + SIZE_TANK <= wall[0] + STEP and wall[1] <= y <= wall[1] + STEP) or (wall[0] <= x + SIZE_TANK<= wall[0] + STEP and wall[1] <= y + SIZE_TANK <= wall[1] + STEP) or (wall[0] <= x <= wall[0] + STEP and wall[1] <= y + SIZE_TANK <= wall[1] + STEP):
            return True
    return False
MOVE2 = 2

def move_enemy():# di chuyển ngẫu nhiên xe tăng đỏ theo hướng hiện tại của nó
    global tank_enemy, MOVE2
    for i in range(len(tank_enemy)):
        if tank_enemy [i][1] == 270:
            if check_coll(tank_enemy [i][0][0], tank_enemy [i][0][1] + MOVE2, walls) and tank_enemy [i][0][1] + MOVE2 <= HEIGHT - 10:
                    tank_enemy [i][0][1] += MOVE2 
        elif tank_enemy [i][1] == 180:
            if check_coll(tank_enemy [i][0][0] - MOVE2, tank_enemy [i][0][1] , walls) and tank_enemy [i][0][0] - MOVE2 >= 0:
                    tank_enemy [i][0][0] -= MOVE2
        elif tank_enemy [i][1] == 0:
            if check_coll(tank_enemy [i][0][0] + MOVE2, tank_enemy [i][0][1], walls) and tank_enemy [i][0][0] + MOVE2 <= WIDTH - 10  :
                    tank_enemy [i][0][0] += MOVE2
        elif tank_enemy [i][1] == 90:
            if check_coll(tank_enemy [i][0][0], tank_enemy [i][0][1] - MOVE2, walls) and tank_enemy [i][0][1] - MOVE2 > 0:
                    tank_enemy [i][0][1] -= MOVE
score = 0
def shot_enemy():# bắn đạn đỏ 
    global tank_enemy, bullet_enemy
    for i in range(len(tank_enemy)):
        if tank_enemy [i][1] == 270 and random.randint(1, 3) == 2 :
            bullet_enemy.append([[tank_enemy [i][0][0] + 17, tank_enemy [i][0][1] + 40], 270])
        elif tank_enemy [i][1] == 180 and random.randint(1, 3) == 2:
            bullet_enemy.append([[tank_enemy [i][0][0] - 8, tank_enemy [i][0][1] + 17], 180])
        elif tank_enemy [i][1] == 0 and random.randint(1, 3) == 2:
            bullet_enemy.append([[tank_enemy [i][0][0] + 40, tank_enemy [i][0][1] + 17], 0])
        elif tank_enemy [i][1] == 90 and random.randint(1, 3) == 2:
            bullet_enemy.append([[tank_enemy [i][0][0] + 17, tank_enemy [i][0][1] - 8], 90])

def check_Two():# va chạm giữa đạn và xe tăng của nhau
    global gun_tank, tank_enemy, ok, score
    for (x, gun) in enumerate(gun_tank):
        for (y, tank) in enumerate(tank_enemy):
            if check_coll_2(gun[0][0], gun[0][1], [tank[0][0], tank[0][1]]):
                del gun_tank[x], tank_enemy[y]
                score += 1
                mix1.play()
    for (x, gun) in enumerate(bullet_enemy):
        if check_coll_2(gun[0][0], gun[0][1], [tank_blue_x, tank_blue_y]):
            ok = False            
    if score == 7 :
        ok = False         
################################################################
ok = True
# trò chơi bắt đầu
while ok:
    screen.blit(screen_main, (0, 0))
    drawWalls()
    check_Two()
    screen.blit(tank_blue, (tank_blue_x, tank_blue_y))
    for enemy in tank_enemy:
        tank_hide = pygame.transform.rotate(tank_enemy_main, enemy[1]) 
        screen.blit(tank_hide, (enemy[0][0], enemy[0][1]))
    xx = -1
    for x in gun_tank:
        xx += 1
        yy = -1
        if x[0][0] > WIDTH or x[0][0] < 0 or x[0][1] > HEIGHT or x[0][1] < 0:
                del gun_tank[xx]
        for y in walls:
            yy += 1
            if check_coll_2(x[0][0], x[0][1], y):
                del gun_tank[xx], walls[yy]
                mix3.play()
    xx = -1
    for x in bullet_enemy:
        xx += 1
        yy = -1
        if x[0][0] > WIDTH or x[0][0] < 0 or x[0][1] > HEIGHT or x[0][1] < 0:
                del bullet_enemy[xx]
        for y in walls:
            yy += 1
            if check_coll_2(x[0][0], x[0][1], y):
                del bullet_enemy[xx], walls[yy]
                mix2.play()
    for gun in bullet_enemy:
        gun_draw = pygame.transform.rotate(gun_of_enemy, gun[1])
        if gun[1] == 90:
            gun[0][1] -= 5
        elif gun[1] == 0:
            gun[0][0] += 5
        elif gun[1] == 270:
            gun[0][1] += 5                
        elif gun[1] == 180:
            gun[0][0] -= 5                    
        screen.blit(gun_draw, (gun[0][0], gun[0][1]))
    for gun in gun_tank:
        gun_draw = pygame.transform.rotate(gun_of_tank, gun[1])
        if gun[1] == 90:
            gun[0][1] -= 10
        elif gun[1] == 0:
            gun[0][0] += 10
        elif gun[1] == 270:
            gun[0][1] += 10                
        elif gun[1] == 180:
            gun[0][0] -= 10                    
        screen.blit(gun_draw, (gun[0][0], gun[0][1]))
    for event in pygame.event.get():
        if event.type == bul_change:
            shot_enemy()
        if event.type == move_change:
            move_enemy()
        if event.type == change:
            set_enemy()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            tank_bullets_set()
            if event.key == pygame.K_UP:
                up = True
            elif event.key == pygame.K_DOWN:
                down = True
            elif event.key == pygame.K_LEFT:
                left = True   
            elif event.key == pygame.K_RIGHT:
                right = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                up = False
            elif event.key == pygame.K_DOWN:
                down = False
            elif event.key == pygame.K_LEFT:
                left = False   
            elif event.key == pygame.K_RIGHT:
                right = False
    update()
    pygame.display.update()
    clock.tick(FPS)        
