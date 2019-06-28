import os
import logging

from pynput.keyboard import Key, Listener
import random

table = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

MAX_INDEX = 3

AIM = 1024

moved = False

logging.basicConfig(level=logging.DEBUG,
                    filename='key.log',
                    filemode='w',
                    format='%(message)s')


def is_full():
    for line in table:
        if 0 in line:
            return False
    return True


def cannot_plus(table):
    for line in table:
        i = 0
        while i < 3:
            j = next_not_zero(line, i, 1)
            if j != -1 and line[i] == line[j]:
                return False
            i += 1
    return True


def GAME_OVER():  # 函数名要小写
    if is_full() \
            and cannot_plus(table) \
            and cannot_plus(get_table_vertical()):
        print("GAME OVER")
        exit()
    else:
        for line in table:
            if AIM in line:
                print("game pass")
                exit()


def set_moved(have_moved):
    global moved
    moved = have_moved


def there_are_some_zeros():
    for line in table:
        for num in line:
            if num == 0:
                return True

    return False


def new_num():
    if there_are_some_zeros():
        line_index = random.randint(0, MAX_INDEX)
        column_index = random.randint(0, MAX_INDEX)
        if table[line_index][column_index] == 0:
            table[line_index][column_index] = int(random.choice('24'))
        else:
            new_num()


def show_line(line):
    shown_line = ''
    for number in line:
        if number == 0:
            shown_line += '/' + ' '*(6-len(str(number)))
        else:
            shown_line += str(number) + ' '*(6-len(str(number)))
    print(shown_line+'\n')
    logging.debug('\n'+shown_line)


def show_table(table):
    os.system('clear')
    for line in table:
        show_line(line)


def next_not_zero(line, i, step):
    if (i == MAX_INDEX and step == 1) or (i == 0 and step == -1):
        return -1

    i += step
    while i <= MAX_INDEX and i >= 0:
        if line[i] != 0:
            return i
        else:
            i += step
    return -1


def swap_num(line, i, direction):
    if line[i] == 0:
        j = next_not_zero(line, i, direction)
        if j != -1:
            line[i] = line[j]
            line[j] = 0
            set_moved(True)


def move_left(line):
    i = 0
    while i < 4:
        swap_num(line, i, 1)
        i += 1


def plus(line, i, direction):
    j = next_not_zero(line, i, direction)
    if j != -1 and line[i] == line[j]:
        line[i] += line[j]
        line[j] = 0
        set_moved(True)


def plus_left(line):
    i = 0
    while i < MAX_INDEX:
        plus(line, i, 1)
        i += 1


def table_vertical_to_table(tv):
    global table
    table = [
        [tv[0][0], tv[1][0],
            tv[2][0], tv[3][0]],
        [tv[0][1], tv[1][1],
            tv[2][1], tv[3][1]],
        [tv[0][2], tv[1][2],
            tv[2][2], tv[3][2]],
        [tv[0][3], tv[1][3],
            tv[2][3], tv[3][3]]
    ]


def get_table_vertical():
    tv = [
        [table[0][0], table[1][0],
            table[2][0], table[3][0]],
        [table[0][1], table[1][1],
            table[2][1], table[3][1]],
        [table[0][2], table[1][2],
            table[2][2], table[3][2]],
        [table[0][3], table[1][3],
            table[2][3], table[3][3]]
    ]

    return tv


def reverse(table):
    for line in table:
        line.reverse()


def action(table):
    # base action is move left
    for line in table:
        plus_left(line)
        move_left(line)


def up():
    tv = get_table_vertical()
    action(tv)
    table_vertical_to_table(tv)


def down():
    tv = get_table_vertical()
    reverse(tv)
    action(tv)
    reverse(tv)
    table_vertical_to_table(tv)


def left():
    action(table)


def right():
    reverse(table)
    action(table)
    reverse(table)


def on_press(key):
    logging.debug('\n'+str(key))
    if key == Key.up:
        up()
    elif key == Key.down:
        down()
    elif key == Key.right:
        right()
    elif key == Key.left:
        left()
    else:
        exit()

    if moved:
        new_num()

    show_table(table)
    set_moved(False)
    GAME_OVER()


new_num()
new_num()
show_table(table)

with Listener(on_press=on_press) as listener:
    listener.join()
