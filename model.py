from tk3d import *


def moving_area(engine, size=10):  # 移动区域模型
    squre_dot = [engine.dot(-size, -size, size), engine.dot(size, -size, size),
                 engine.dot(-size, -size, -size), engine.dot(size, -size, -size)]

    grid_dot = [engine.dot(-size, size, size), engine.dot(size, size, size),
                engine.dot(-size, size, -size), engine.dot(size, size, -size)]

    squre = [engine.line(squre_dot[0], squre_dot[1], '#7f7f7f'), engine.line(squre_dot[1], squre_dot[3], '#7f7f7f'),
             engine.line(squre_dot[3], squre_dot[2], '#7f7f7f'), engine.line(squre_dot[2], squre_dot[0], '#7f7f7f')]

    grid = [engine.line(grid_dot[0], squre_dot[0]), engine.line(grid_dot[1], squre_dot[1]),
            engine.line(grid_dot[2], squre_dot[2]), engine.line(grid_dot[3], squre_dot[3]),

            engine.line(grid_dot[0], grid_dot[1]), engine.line(grid_dot[1], grid_dot[3]),
            engine.line(grid_dot[3], grid_dot[2]), engine.line(grid_dot[2], grid_dot[0])]


def small_block(engine, x, y, z, x1=None, y1=None, z1=None, color1='#00ff00', color2='#007f00'):
    if x1 is None:
        x1 = x+1
    if y1 is None:
        y1 = y+1
    if z1 is None:
        z1 = z+1
    block_dot = [engine.dot(x, y1, z1), engine.dot(x1, y1, z1),
                 engine.dot(x, y1, z), engine.dot(x1, y1, z),

                 engine.dot(x, y, z1), engine.dot(x1, y, z1),
                 engine.dot(x, y, z), engine.dot(x1, y, z)]

    triangle_list = [
        engine.triangle(block_dot[0], block_dot[1], block_dot[2], color1),
        engine.triangle(block_dot[1], block_dot[2], block_dot[3], color1),

        engine.triangle(block_dot[4], block_dot[5], block_dot[6], color2),
        engine.triangle(block_dot[5], block_dot[6], block_dot[7], color2),

        engine.triangle(block_dot[0], block_dot[4], block_dot[5], color1),
        engine.triangle(block_dot[0], block_dot[1], block_dot[5], color1),

        engine.triangle(block_dot[2], block_dot[6], block_dot[7], color2),
        engine.triangle(block_dot[2], block_dot[3], block_dot[7], color2),

        engine.triangle(block_dot[0], block_dot[4], block_dot[6], color1),
        engine.triangle(block_dot[0], block_dot[2], block_dot[6], color1),

        engine.triangle(block_dot[1], block_dot[5], block_dot[7], color2),
        engine.triangle(block_dot[1], block_dot[3], block_dot[7], color2)]

    return triangle_list


def del_small_block(engine, block):
    for i in block:
        engine.del_triangle(i)
