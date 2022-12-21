from math import *


def turn(x, y, x2, y2, degree):  # 旋转
    degree = degree * pi / 180
    outx = (x - x2) * cos(degree) - (y - y2) * sin(degree) + x2
    outy = (x - x2) * sin(degree) + (y - y2) * cos(degree) + y2
    return [outx, outy]


class SetCamera():  # 设定相机
    def __init__(self, x=0, y=0, z=0, xDegree=0, yDegree=0, zDegree=0, perspective=99):  # 初始化
        self.x = x
        self.y = y
        self.z = z
        self.xDegree = xDegree
        self.yDegree = yDegree
        self.zDegree = zDegree
        self.perspective = perspective

    def changeCamera(self, x=None, y=None, z=None, xDegree=None, yDegree=None, zDegree=None, perspective=None):  # 改变相机
        if x != None:
            self.x = x
        if y != None:
            self.y = y
        if z != None:
            self.z = z
        if xDegree != None:
            self.xDegree = xDegree
        if yDegree != None:
            self.yDegree = yDegree
        if zDegree != None:
            self.zDegree = zDegree
        if perspective != None:
            self.perspective = perspective

    def forwordCamera(self, p='z', x=True, y=True, step=1):  # 相机前进
        pastX = self.x
        pastY = self.y
        pastZ = self.z
        if p == 'x':
            self.x += step
        if p == 'y':
            self.y += step
        if p == 'z':
            self.z += step
        if y:
            self.x, self.z = turn(self.x, self.z, pastX, pastZ, 0 - self.yDegree)[0], \
                             turn(self.x, self.z, pastX, pastZ, 0 - self.yDegree)[1]
        if x:
            self.y, self.z = turn(self.y, self.z, pastY, pastZ, 0 - self.xDegree)[0], \
                             turn(self.y, self.z, pastY, pastZ, 0 - self.xDegree)[1]

    def point_3D(self, x, y, z, canvas_width=0, canvas_height=0):  # 3D点
        x -= self.x
        y -= self.y
        z -= self.z
        x, z = turn(x, z, 0, 0, self.yDegree)[0], turn(x, z, 0, 0, self.yDegree)[1]
        y, z = turn(y, z, 0, 0, self.xDegree)[0], turn(y, z, 0, 0, self.xDegree)[1]
        x, y = turn(x, y, 0, 0, self.zDegree)[0], turn(x, y, 0, 0, self.zDegree)[1]
        x_2d = ((x * (self.perspective / 100) ** (z - 390)) + canvas_width / 2)
        y_2d = canvas_height - ((y * (self.perspective / 100) ** (z - 390)) + canvas_height / 2)
        return [x_2d, y_2d]
