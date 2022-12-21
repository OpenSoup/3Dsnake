# 导入所需API与库
from tkinter import *  # 导入GUI库
from engine3D import *  # 导入3D引擎库
from defs import *


# 函数
class Engine():  # 创建3D引擎
    def __init__(self):  # 初始化
        """
        创建单个3D引擎空间
        """
        self.dot_list = []  # [[x,y,z], [x,y,z]]
        self.line_list = []  # [[dot1,dot2,color], [dot1,dot2,color]]
        self.triangle_list = []  # [[dot1,dot2,dot3,color], [dot1,dot2,dot3,color]]

    def dot(self, x, y, z):  # 创建关键点
        """
        创建关键点
        :param x: 关键点的x坐标
        :param y: 关键点的y坐标
        :param z: 关键点的z坐标
        :return: 关键点的代表值
        """
        self.dot_list.append([x, y, z])
        return len(self.dot_list) - 1

    def dot_change(self, dot, x, y, z):  # 改变关键点坐标
        """
        改变关键点坐标
        :param dot: 需要改变坐标的关键点代表值
        :param x: 关键点新的x坐标
        :param y: 关键点新的y坐标
        :param z: 关键点新的z坐标
        """
        self.dot_list[dot] = [x, y, z]

    def get_dot_information(self, dot, x=True, y=True, z=True):  # 获取关键点坐标
        """
        获取关键点坐标
        :param dot: 需要获取坐标的关键点代表值
        :param x: 是否需要获取关键点的x坐标
        :param y: 是否需要获取关键点的y坐标
        :param z: 是否需要获取关键点的z坐标
        :return: 关键点的坐标
        """
        info = {}
        if x:
            info['x'] = self.dot_list[dot][0]
        if y:
            info['y'] = self.dot_list[dot][1]
        if z:
            info['z'] = self.dot_list[dot][2]
        return info

    def line(self, dot1, dot2, color="#000000"):  # 创建线段
        """
        创建线段
        :param dot1: 需要关联的第一个关键点代表值
        :param dot2: 需要关联的第二个关键点代表值
        :param color: 线段颜色(html)
        :return: 线段代表值
        """
        self.line_list.append([dot1, dot2, color])
        return len(self.line_list) - 1

    def del_line(self, line):
        """
        删除线段
        :param line: 需要删除的线段代表值
        """
        _del = self.line_list[line][2]
        self.line_list[line][2] = 'hide'
        del _del

    def triangle(self, dot1, dot2, dot3, color="#000000"):  # 创建三角形
        """
        创建三角形
        :param dot1: 需要关联的第一个关键点代表值
        :param dot2: 需要关联的第二个关键点代表值
        :param dot3: 需要关联的第三个关键点代表值
        :param color: 三角形颜色(html)
        :return: 三角形代表值
        """
        self.triangle_list.append([dot1, dot2, dot3, color])
        return len(self.triangle_list) - 1

    def del_triangle(self, triangle):
        """
        删除三角形
        :param triangle: 需要删除的三角形代表值
        """
        _del = self.triangle_list[triangle]
        self.triangle_list[triangle] = None
        del _del


class Camera():  # 创建相机
    def __init__(self, Engine,
                 x=0, y=0, z=0,
                 xDegree=0, yDegree=0, zDegree=0,
                 perspective=99):  # 初始化
        """
        创建相机
        :param Engine: 相机所在的3D引擎空间
        :param x: 相机的x坐标
        :param y: 相机的y坐标
        :param z: 相机的z坐标
        :param xDegree: 相机关于x轴的旋转角度
        :param yDegree: 相机关于y轴的旋转角度
        :param zDegree: 相机关于z轴的旋转角度
        :param perspective: 相机的透视效果
        """
        self.Engine = Engine
        self.camera = SetCamera(x=x, y=y, z=z,
                                xDegree=xDegree, yDegree=yDegree, zDegree=zDegree,
                                perspective=perspective)

    def change_camera(self, Engine=None,
                      x=None, y=None, z=None,
                      xDegree=None, yDegree=None, zDegree=None,
                      perspective=None):  # 改变相机的各项参数
        """
        改变相机的各项参数
        :param Engine: 相机所在的3D引擎空间
        :param x: 相机的x坐标
        :param y: 相机的y坐标
        :param z: 相机的z坐标
        :param xDegree: 相机关于x轴的旋转角度
        :param yDegree: 相机关于y轴的旋转角度
        :param zDegree: 相机关于z轴的旋转角度
        :param perspective: 相机的透视效果
        """
        if Engine != None:
            self.Engine = Engine
        self.camera.changeCamera(x=x, y=y, z=z,
                                 xDegree=xDegree, yDegree=yDegree, zDegree=zDegree,
                                 perspective=perspective)

    def forword_camera(self, p='z', x=True, y=True, step=1):
        """
        让相机前进
        :param p: 相对于相机的方向
        :param x: 移动是否跟x轴的旋转角度相关
        :param y: 移动是否跟y轴的旋转角度相关
        :param step: 移动的距离
        """
        self.camera.forwordCamera(p=p, x=x, y=y, step=step)

    def draw(self, canvas):  # 将相机视角的图形绘制在指定画布上
        """
        将相机视角的图形绘制在指定画布上
        :param canvas: 绘制图形的画布
        """
        # 创建所有会改变的数据
        dot_order = copyList([i for i in self.Engine.dot_list if i is not None])
        line_order = copyList([i for i in self.Engine.line_list if i is not None])
        triangle_order = copyList([i for i in self.Engine.triangle_list if i is not None])

        # 计算所有点和相机的相对位置
        for i in range(len(dot_order)):
            dot_order[i][0] = dot_order[i][0] - self.camera.x
            dot_order[i][1] = dot_order[i][1] - self.camera.y
            dot_order[i][2] = dot_order[i][2] - self.camera.z

            dot_order[i][0], dot_order[i][2] = turn(dot_order[i][0], dot_order[i][2], 0, 0, self.camera.yDegree)
            dot_order[i][1], dot_order[i][2] = turn(dot_order[i][1], dot_order[i][2], 0, 0, self.camera.xDegree)
            dot_order[i][0], dot_order[i][1] = turn(dot_order[i][0], dot_order[i][1], 0, 0, self.camera.zDegree)

        # 去除不显示元素
        for i in range(len(line_order)):
            dot_a_x = dot_order[line_order[i][0]][0]
            dot_a_y = dot_order[line_order[i][0]][1]
            dot_a_z = dot_order[line_order[i][0]][2]

            dot_b_x = dot_order[line_order[i][1]][0]
            dot_b_y = dot_order[line_order[i][1]][1]
            dot_b_z = dot_order[line_order[i][1]][2]
            if dot_a_z < 0 and dot_b_z < 0:
                line_order[i][2] = "hide"

        for i in range(len(triangle_order)):
            dot_a_x = dot_order[triangle_order[i][0]][0]
            dot_a_y = dot_order[triangle_order[i][0]][1]
            dot_a_z = dot_order[triangle_order[i][0]][2]

            dot_b_x = dot_order[triangle_order[i][1]][0]
            dot_b_y = dot_order[triangle_order[i][1]][1]
            dot_b_z = dot_order[triangle_order[i][1]][2]

            dot_c_x = dot_order[triangle_order[i][2]][0]
            dot_c_y = dot_order[triangle_order[i][2]][1]
            dot_c_z = dot_order[triangle_order[i][2]][2]
            if dot_a_z < 0 and dot_b_z < 0 and dot_c_z < 0:
                triangle_order[i][3] = "hide"

        # 比较并排序所有图形
        shape_order = triangle_order + line_order
        for i in range(len(shape_order)):
            for j in range(len(shape_order) - 1):
                # 第一个图形
                if len(shape_order[j]) == 3:
                    shape_a = (((dot_order[shape_order[j][0]][0])**2 + (dot_order[shape_order[j][0]][1])**2 +
                                (dot_order[shape_order[j][0]][2])**2)**0.5 +
                               ((dot_order[shape_order[j][1]][0])**2 + (dot_order[shape_order[j][1]][1])**2 +
                                (dot_order[shape_order[j][1]][2])**2)**0.5
                               ) / 2
                else:
                    shape_a = (((dot_order[shape_order[j][0]][0])**2 + (dot_order[shape_order[j][0]][1])**2 +
                                (dot_order[shape_order[j][0]][2])**2)**0.5 +
                               ((dot_order[shape_order[j][1]][0])**2 + (dot_order[shape_order[j][1]][1])**2 +
                                (dot_order[shape_order[j][1]][2])**2)**0.5 +
                               ((dot_order[shape_order[j][2]][0])**2 + (dot_order[shape_order[j][2]][1])**2 +
                                (dot_order[shape_order[j][2]][2])**2)**0.5
                               ) / 3

                # 第二个图形
                if len(shape_order[j + 1]) == 3:
                    shape_b = (((dot_order[shape_order[j + 1][0]][0])**2 + (dot_order[shape_order[j + 1][0]][1])**2 +
                                (dot_order[shape_order[j + 1][0]][2])**2)**0.5 +
                               ((dot_order[shape_order[j + 1][1]][0])**2 + (dot_order[shape_order[j + 1][1]][1])**2 +
                                (dot_order[shape_order[j + 1][1]][2])**2)**0.5
                               ) / 2
                else:
                    shape_b = (((dot_order[shape_order[j + 1][0]][0])**2 +
                                (dot_order[shape_order[j + 1][0]][1])**2 +
                                (dot_order[shape_order[j + 1][0]][2])**2)**0.5 +
                               ((dot_order[shape_order[j + 1][1]][0])**2 +
                                (dot_order[shape_order[j + 1][1]][1])**2 +
                                (dot_order[shape_order[j + 1][1]][2])**2)**0.5 +
                               ((dot_order[shape_order[j + 1][2]][0])**2 +
                                (dot_order[shape_order[j + 1][2]][1])**2 +
                                (dot_order[shape_order[j + 1][2]][2])**2)**0.5
                               ) / 3

                if shape_a < shape_b:
                    shape_order[j], shape_order[j + 1] = shape_order[j + 1], shape_order[j]

        # 绘制所有图形
        for i in shape_order:
            if len(i) == 4:
                if i[3] != 'hide':
                    a_x = self.Engine.dot_list[i[0]][0]
                    a_y = self.Engine.dot_list[i[0]][1]
                    a_z = self.Engine.dot_list[i[0]][2]

                    b_x = self.Engine.dot_list[i[1]][0]
                    b_y = self.Engine.dot_list[i[1]][1]
                    b_z = self.Engine.dot_list[i[1]][2]

                    c_x = self.Engine.dot_list[i[2]][0]
                    c_y = self.Engine.dot_list[i[2]][1]
                    c_z = self.Engine.dot_list[i[2]][2]

                    a_x2d, a_y2d = self.camera.point_3D(a_x, a_y, a_z, canvas.winfo_width(), canvas.winfo_height())
                    b_x2d, b_y2d = self.camera.point_3D(b_x, b_y, b_z, canvas.winfo_width(), canvas.winfo_height())
                    c_x2d, c_y2d = self.camera.point_3D(c_x, c_y, c_z, canvas.winfo_width(), canvas.winfo_height())
                    canvas.create_polygon((a_x2d, a_y2d, b_x2d, b_y2d, c_x2d, c_y2d), fill=i[3])

            else:
                if i[2] != 'hide':
                    a_x = self.Engine.dot_list[i[0]][0]
                    a_y = self.Engine.dot_list[i[0]][1]
                    a_z = self.Engine.dot_list[i[0]][2]

                    b_x = self.Engine.dot_list[i[1]][0]
                    b_y = self.Engine.dot_list[i[1]][1]
                    b_z = self.Engine.dot_list[i[1]][2]

                    a_x2d, a_y2d = self.camera.point_3D(a_x, a_y, a_z, canvas.winfo_width(), canvas.winfo_height())
                    b_x2d, b_y2d = self.camera.point_3D(b_x, b_y, b_z, canvas.winfo_width(), canvas.winfo_height())
                    canvas.create_line((a_x2d, a_y2d, b_x2d, b_y2d), fill=i[2])


if __name__ == '__main__':
    from time import *
    from keyboard import *
    from tkinter.messagebox import *

    root = Tk()

    canvas = Canvas(root, bg="#ffffff")
    canvas.pack(fill=BOTH, expand=True)

    engine = Engine()
    box_size = 500
    dots = [engine.dot(0, 0, 0), engine.dot(0, 0, box_size), engine.dot(0, box_size, 0),
            engine.dot(0, box_size, box_size),
            engine.dot(box_size, 0, 0), engine.dot(box_size, 0, box_size), engine.dot(box_size, box_size, 0),
            engine.dot(box_size, box_size, box_size)]
    for i in range(1):
        engine.triangle(dots[0], dots[1], dots[2], color='#7f0000')
        engine.triangle(dots[1], dots[2], dots[3], color='#7f0000')
        engine.triangle(dots[4], dots[5], dots[6], color='#ff0000')
        engine.triangle(dots[5], dots[6], dots[7], color='#ff0000')
        engine.triangle(dots[0], dots[1], dots[4], color='#007f00')
        engine.triangle(dots[1], dots[4], dots[5], color='#007f00')
        engine.triangle(dots[2], dots[3], dots[6], color='#00ff00')
        engine.triangle(dots[3], dots[6], dots[7], color='#00ff00')
        engine.triangle(dots[1], dots[3], dots[5], color='#00007f')
        engine.triangle(dots[3], dots[5], dots[7], color='#00007f')
        engine.triangle(dots[0], dots[2], dots[4], color='#0000ff')
        engine.triangle(dots[2], dots[4], dots[6], color='#0000ff')
        camera = Camera(engine, x=box_size / 2, z=box_size / 2)
    print(box_size)
    y = box_size / 2
    xD = 0
    yD = 0
    showinfo('提示', '用“W”，“S”，“A”，“D”控制平移，“up”，“down”，“left”，“right”控制朝向')
    while True:
        camera.change_camera(xDegree=xD, yDegree=yD, y=y)
        if is_pressed('w'):
            camera.forword_camera('z',x=False, step=0.5)
        if is_pressed('s'):
            camera.forword_camera('z',x=False, step=-0.5)
        if is_pressed('a'):
            camera.forword_camera('x',x=False, step=-0.5)
        if is_pressed('d'):
            camera.forword_camera('x',x=False, step=0.5)
        if is_pressed('space'):
            y += 0.5
        if is_pressed('shift'):
            y -= 0.5
        if is_pressed('left'):
            yD -= 1
        if is_pressed('right'):
            yD += 1
        if is_pressed('up'):
            xD += 1
        if is_pressed('down'):
            xD -= 1
        canvas.delete(ALL)
        camera.draw(canvas)
        root.update()
        sleep(0.01)
