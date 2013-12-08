import sys
import os

from math import sqrt, sin, hypot, asin, degrees, tan, radians   # "sqrt, sin, ..."  - new

NEG_ANSWERS = ('n', 'no', 'н', 'нет')

E_INTERVAL = 'Число должно быть в интервале ({0}; {1}).'
E_CONVERT = 'Читайте, пожалуйста, внимательнее.'

I_CONTINUE = 'Повторить ввод ([да]/нет)? '
I_GET_SIDE = 'Введите длину катета: '
I_GET_ANGLE = 'Введите угол противоположный одному из  катетов: '  #new

I_GET_PERIMETER = 'Введите чему равен полупериметр: '   #new

MAIN_INTERFACE = """
Выберите способ задания треугльника:

0. Выход.
1. По двум катетам.
2. Через стороны и угол альфа
3. По формуле Герона
4. По трём сторонам и радиусу описанной окружности
5. По трём сторонам и радиус вписанной окружности

Ваш выбор: """

RESULT = """
Длина катета a1 = {0[0]:.2f}.
Длина катета a2 = {0[1]:.2f}.
Длина гипотенузы b = {0[2]:.2f}.
Угол alfa1 = {0[3]:.2f} градусов.
Угол alfa2 = {0[4]:.2f} градусов.
Периметр треугольника = {0[5]:.2f} (ед.).
Площадь треугольника =  {0[6]:.2f} (ед.).
"""




def get_number(prompt, to_type, left_limit, right_limit):
    while True:
        try:
            try:
                res = to_type(input(prompt))
                if left_limit < res < right_limit:
                    return res
                else:
                    raise SimpleError(E_INTERVAL.format(left_limit, right_limit))
            except ValueError:
                raise SimpleError(E_CONVERT)
        except SimpleError as se:
            print(se.value)
        if input(I_CONTINUE).lower() in NEG_ASWERS:
            break

def get_side(prompt):
    return get_number(prompt, float, 0, float('+inf'))


def get_angle(prompt):
    return get_number(prompt, float, 0, 90)

# new
def get_perimeter(prompt):
    return get_number(prompt, float, 0, float('+inf'))

def t_two_sides():
    a1 = get_side(I_GET_SIDE)
    a2 = get_side(I_GET_SIDE)
    b = hypot(a1, a2) 
    perimeter = a1 + a2 + b    # new
    alfa1 = degrees(asin(a2/b))
    alfa2 = degrees(asin(a1/b))
    Area = a1 * a2 /2   # new
    return a1, a2, b, alfa1, alfa2, perimeter, Area  # "..., perimetr, Square" - new


# Через две стороны и угол
def two_sides_angle():
    a1 = get_side(I_GET_SIDE)
    ANGLE = radians(get_angle(I_GET_ANGLE))
    alfa2 = 90 - degrees(ANGLE)
    alfa1 = degrees(ANGLE)
    a2 = a1 / tan(ANGLE)
    b = hypot(a1,a2)
    perimeter = a1 + a2 + b
    Area = a1 * a2 * 0.5
    return a1, a2, b, alfa1, alfa2, perimeter, Area
    
# По формуле Герона
def formula_gerona():
    SEMIPERIMETER = get_perimeter(I_GET_PERIMETER)
    a1 = get_side(I_GET_SIDE)
    ANGLE = radians(get_angle(I_GET_ANGLE))
    alfa1 = degrees(ANGLE)
    a2 = a1 / tan(ANGLE)
    a3 = 2 * SEMIPERIMETER - a1 - a2
    alfa2 = 90 - degrees(ANGLE)
    b = a3
    perimeter = SEMIPERIMETER * 2
    Area = sqrt(SEMIPERIMETER*(SEMIPERIMETER - a1)*(SEMIPERIMETER - a2) * (SEMIPERIMETER - a3))
    return a1, a2, b, alfa1, alfa2, perimeter, Area


# Описанная окружность
def three_sides_circle():
    a1 = get_side(I_GET_SIDE)
    ANGLE = radians(get_angle(I_GET_ANGLE))
    alfa1 = degrees(ANGLE)
    a2 = a1 / tan(ANGLE)
    alfa2 = 90 - degrees(ANGLE)
    b = hypot(a1,a2)
    RADIUS = b / 2
    perimeter = a1 + a2 + b
    Area = a1 * a2 * b / (4 * RADIUS)
    return a1, a2, b, alfa1, alfa2, perimeter, Area

    
# Вписанная окружность
def semiperimeter_circle():
    a1 = get_side(I_GET_SIDE)
    ANGLE = radians(get_angle(I_GET_ANGLE))
    alfa1 = degrees(ANGLE)
    a2 = a1 / tan(ANGLE)
    b = hypot(a1,a2)
    alfa2 = 90 - degrees(ANGLE)
    perimeter = a1 + a2 + b
    SEMIPERIMETER = perimeter / 2
    RADIUS = sqrt(((SEMIPERIMETER - a1)*(SEMIPERIMETER - a2) * (SEMIPERIMETER - b)) / SEMIPERIMETER)
    Area = SEMIPERIMETER * RADIUS
    return a1, a2, b, alfa1, alfa2, perimeter, Area
    
    

triangle_type = {
    0: sys.exit,
    1: t_two_sides,
    2: two_sides_angle, #new
    3: formula_gerona,      #new
    4: three_sides_circle,      #new
    5: semiperimeter_circle         #new
    }


def draw_triangle(triangle_params):
    a1, a2, b, alfa1, alfa2, perimeter, Area = triangle_params   # "..., perimetr, Square" - new
    for x in range(1, round(max(a1, a2)) + 1):
        print('L.' * int(round(x * tan(radians(min(alfa1, alfa2))))))


def main():
    while True:
        user_choice = get_number(MAIN_INTERFACE, int, -1, 6)
        triangle_params = list(triangle_type[user_choice]())
        print(RESULT.format(triangle_params))
        draw_triangle(triangle_params)
        if input(I_CONTINUE).lower() in NEG_ANSWERS:
            break

if __name__ == '__main__':
    main()
