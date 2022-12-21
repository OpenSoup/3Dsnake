import sys
from tk3d import *
from time import *
from keyboard import *
from model import *
from random import*
from pyglet import*


def onClosing():
    global GUI_page
    GUI_page = 'quit'


def keyEvent(event):
    global toward
    key = event.keysym
    if key == 'w' and last_toward != 'z-':  # 检测按键
        toward = 'z+'
    if key == 's' and last_toward != 'z+':
        toward = 'z-'
    if key == 'a' and last_toward != 'x+':
        toward = 'x-'
    if key == 'd' and last_toward != 'x-':
        toward = 'x+'
    if key == 'space' and last_toward != 'y-':
        toward = 'y+'
    if key == 'Shift_L' and last_toward != 'y+':
        toward = 'y-'


def click_button(event):
    global x_mid, y_mid, GUI_page
    # x_mid - 100, y_mid - 50, x_mid + 100, y_mid + 50
    if GUI_page == 'home':
        if x_mid - 100 < event.x < x_mid + 100 and y_mid - 50 < event.y < y_mid + 50:
            GUI_page = 'game'
    if GUI_page == 'game over':
        if x_mid - 100 < event.x < x_mid + 100 and y_mid - 50 < event.y < y_mid + 50:
            GUI_page = 'home'


def move_camera_start(event):
    global start_y, start_x
    start_x = event.x
    start_y = event.y


def move_camera_end(event):
    global start_x, start_y, xD, yD
    xD -= (event.y-start_y)/10
    yD += (event.x-start_x)/10
    if xD < -90:
        xD = -90
    if xD > 0:
        xD = 0
    if yD < -45:
        yD = -45
    if yD > 45:
        yD = 45
    start_x = event.x
    start_y = event.y


font.add_file('ledfont.ttf')  # 加入字体
font.add_file('led_board-7.ttf')

root = Tk()  # 主窗口
root.geometry("1000x600")
root.protocol("WM_DELETE_WINDOW", onClosing)

canvas = Canvas(root, bg="#7fffff")  # 画布
canvas.pack(fill=BOTH, expand=True)

engine = Engine()                    # 3D引擎
camera = Camera(engine, 0, 0, -100)  # 相机

moving_area(engine)  # 创建移动区域模型

GUI_page = 'home'
while True:  # 主循环
    canvas.bind(sequence="<Button-1> ", func=click_button)
    canvas.bind(sequence="<B1-Motion>", func=None)
    root.bind('<Key>', None)
    while GUI_page == 'home':
        x_mid = root.winfo_width() // 2
        y_mid = root.winfo_height() // 2

        canvas.create_text(x_mid, y_mid-200, text='3D SNAKE', font=('LED Board-7', 100))
        canvas.create_rectangle(x_mid - 100, y_mid - 50, x_mid + 100, y_mid + 50,
                                width=10, fill='#7f7f7f')
        canvas.create_text(x_mid, y_mid, text='START', font=('LEDfont', 50))

        root.update()
        canvas.delete(ALL)

    canvas.bind(sequence="<Button-1> ", func=move_camera_start)
    canvas.bind(sequence="<B1-Motion>", func=move_camera_end)
    root.bind('<Key>', keyEvent)

    body = [[10, 0, 10], [11, 0, 10], [12, 0, 10]]  # 蛇身体
    body_block = []  # 设身体上的方块
    last_toward = 'x+'  # 上一次的朝向
    toward = 'x+'  # 朝向
    food = [randint(0, 19), randint(0, 19), randint(0, 19)]  # 食物位置
    food_block = small_block(engine, food[0] - 10, food[1] - 10, food[2] - 10,
                             color1="#ff0000", color2="#7f0000")  # 食物模型
    next_motion = time() + 0.5  # 下次移动的时间
    score = 0

    start_x = 0
    start_y = 0
    xD = 0
    yD = 0
    while GUI_page == 'game':
        y, z = turn(0, -100, 0, 0, -xD)  # 计算旋转视角
        x, z = turn(0, z, 0, 0, -yD)

        camera.change_camera(x=x, y=y, z=z, xDegree=xD, yDegree=yD)  # 调整视角

        if time() >= next_motion:  # 移动
            last_toward = toward
            if toward == 'x+':
                body.append([body[-1][0]+1, body[-1][1], body[-1][2]])
            if toward == 'x-':
                body.append([body[-1][0]-1, body[-1][1], body[-1][2]])
            if toward == 'y+':
                body.append([body[-1][0], body[-1][1]+1, body[-1][2]])
            if toward == 'y-':
                body.append([body[-1][0], body[-1][1]-1, body[-1][2]])
            if toward == 'z+':
                body.append([body[-1][0], body[-1][1], body[-1][2]+1])
            if toward == 'z-':
                body.append([body[-1][0], body[-1][1], body[-1][2]-1])

            if body[-1] in body[0:-1]:
                GUI_page = 'game over'
            if not (0 <= body[-1][0] <= 19):
                GUI_page = 'game over'
            if not (0 <= body[-1][1] <= 19):
                GUI_page = 'game over'
            if not (0 <= body[-1][2] <= 19):
                GUI_page = 'game over'

            if body[-1] == food:
                food = [randint(0, 19), randint(0, 19), randint(0, 19)]
                score += 1
            else:
                del body[0]
            next_motion += 0.5

            for i in body_block:  # 删除原有身体模型
                del_small_block(engine, i)
            for i in body:  # 创建新生体模型
                body_block.append(small_block(engine, i[0] - 10, i[1] - 10, i[2] - 10))

            del_small_block(engine, food_block)
            food_block = small_block(engine, food[0] - 10, food[1] - 10, food[2] - 10, color1="#ff0000", color2="#7f0000")

        camera.draw(canvas)
        canvas.create_text(8, 8, text='SCORE: ' + str(score), font=('LEDfont', 50), anchor=NW)
        root.update()
        canvas.delete(ALL)
    else:
        for i in body_block:  # 删除原有身体模型
            del_small_block(engine, i)
        del_small_block(engine, food_block)

    canvas.bind(sequence="<Button-1> ", func=click_button)
    canvas.bind(sequence="<B1-Motion>", func=None)
    root.bind('<Key>', None)
    while GUI_page == 'game over':
        x_mid = root.winfo_width() // 2
        y_mid = root.winfo_height() // 2

        canvas.create_text(x_mid, y_mid - 200, text='GAME OVER', font=('LED Board-7', 100), fill='#7f0000')
        canvas.create_text(x_mid, y_mid - 100, text='SCORE: ' + str(score), font=('LEDfont', 50))
        canvas.create_rectangle(x_mid - 100, y_mid - 50, x_mid + 100, y_mid + 50,
                                width=10, fill='#7f7f7f')
        canvas.create_text(x_mid, y_mid, text='BACK', font=('LEDfont', 50))

        root.update()
        canvas.delete(ALL)

    if GUI_page == 'quit':
        break
