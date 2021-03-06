"""
File: pyramid.py
----------------
YOUR DESCRIPTION HERE
"""

import tkinter
import time
import random
import math

# import numpy as np
# import matplotlib.pyplot as plt

CANVAS_WIDTH = 800  # Width of drawing canvas in pixels
CANVAS_HEIGHT = 600  # Height of drawing canvas in pixels
HEADER_HEIGHT = 40
PLAYER_1_SCORE_OFFSET_X = CANVAS_WIDTH // 4
PLAYER_2_SCORE_OFFSET_X = CANVAS_WIDTH * 3 / 4
HEADER_TEXT_OFFSET_Y = HEADER_HEIGHT // 2
SCORE_TEXT = 'LIVES: '
PLAY_AREA_HEIGHT = CANVAS_HEIGHT - HEADER_HEIGHT
PLAY_AREA_WIDTH = CANVAS_WIDTH
PLAY_AREA_OFFSET_Y = HEADER_HEIGHT
PLAY_AREA_OFFSET_X = 0
PLAY_AREA_LEFT = PLAY_AREA_OFFSET_X
PLAY_AREA_RIGHT = PLAY_AREA_LEFT + PLAY_AREA_WIDTH
PLAY_AREA_TOP = PLAY_AREA_OFFSET_Y
PLAY_AREA_BOTTOM = PLAY_AREA_TOP + PLAY_AREA_HEIGHT
PLAYER_COUNT = 2
SPACE_BETWEEN_BARRIERS = 3
BARRIER_COLUMN_COUNT_PER_PLAYER = 4
SPACE_BETWEEN_BARRIER_COLUMNS = 3
BARRIER_COUNT_PER_COLUMN = 10
BARRIER_WIDTH = 10
BARRIER_HEIGHT = ((PLAY_AREA_HEIGHT - SPACE_BETWEEN_BARRIERS) // BARRIER_COUNT_PER_COLUMN) - SPACE_BETWEEN_BARRIERS
SPACE_ABOVE_AND_BELOW_BARRIERS = (PLAY_AREA_HEIGHT - (
        BARRIER_COUNT_PER_COLUMN * (BARRIER_HEIGHT + SPACE_BETWEEN_BARRIERS) - SPACE_BETWEEN_BARRIERS)) // 2
PLAYER_2_COLOR = '#ff4d4d'
PLAYER_1_COLOR = '#668cff'
PADDLE_HEIGHT = 60
PADDLE_WIDTH = 30
PADDLE_OFFSET = 10
PLAYER_1_PADDLE_X = PADDLE_OFFSET
PLAYER_2_PADDLE_X = PLAY_AREA_RIGHT - PADDLE_OFFSET - PADDLE_WIDTH
PLAYER_1_PADDLE_UP_KEY = 'q'
PLAYER_1_PADDLE_DOWN_KEY = 'a'
PLAYER_2_PADDLE_UP_KEY = ']'
PLAYER_2_PADDLE_DOWN_KEY = "'"
VALID_KEYS = [PLAYER_1_PADDLE_UP_KEY, PLAYER_1_PADDLE_DOWN_KEY, PLAYER_2_PADDLE_UP_KEY, PLAYER_2_PADDLE_DOWN_KEY]
PADDLE_MOVE_STEP = 5
PADDLE_MIN_Y = PLAY_AREA_TOP + PADDLE_HEIGHT // 2
PADDLE_MAX_Y = PLAY_AREA_BOTTOM - PADDLE_HEIGHT // 2
BALL_INITIAL_X_OFFSET = 100
BALL_INITIAL_Y_OFFSET = PLAY_AREA_HEIGHT // 2
BALL_VELOCITY = 5
BALL_RADIUS = 20
BALL_COLOR_PLAYER_1 = '#668cff'
BALL_COLOR_PLAYER_2 = '#ff4d4d'


def main():
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Ball Game')

    game_state = initialize(canvas)
    keyboard_handler = create_keyboard_handler(game_state)
    canvas.bind('<KeyPress>', keyboard_handler)
    # canvas.bind('<KeyRelease>', keyboard_handler)
    canvas.after(20, drawFrame, canvas, game_state)

    canvas.mainloop()


def create_keyboard_handler(game_state):
    def keyboard_handler(event):
        is_not_valid_key = len(list(filter(lambda x: x == event.char, VALID_KEYS))) == 0
        if is_not_valid_key: return

        direction = 'none'
        if event.char == PLAYER_1_PADDLE_DOWN_KEY or event.char == PLAYER_1_PADDLE_UP_KEY:
            paddle = list(filter(lambda x: x['player'] == 1, game_state['paddles']))[0]
            if event.char == PLAYER_1_PADDLE_UP_KEY and paddle['move_direction'] != 'up': direction = 'up'
            if event.char == PLAYER_1_PADDLE_DOWN_KEY and paddle['move_direction'] != 'down': direction = 'down'
            paddle['move_direction'] = direction

        if event.char == PLAYER_2_PADDLE_DOWN_KEY or event.char == PLAYER_2_PADDLE_UP_KEY:
            paddle = list(filter(lambda x: x['player'] == 2, game_state['paddles']))[0]
            if event.char == PLAYER_2_PADDLE_UP_KEY and paddle['move_direction'] != 'up': direction = 'up'
            if event.char == PLAYER_2_PADDLE_DOWN_KEY and paddle['move_direction'] != 'down': direction = 'down'
            paddle['move_direction'] = direction

    return keyboard_handler


def initialize(canvas):
    game_state = {'barriers': initialize_barriers(canvas),
                  'paddles': initialize_paddles(canvas),
                  'balls': initialize_balls(canvas),
                  'scores': initialize_header(canvas)}

    return game_state


def create_score_for_player(player, canvas, lives):
    x_offset = PLAYER_1_SCORE_OFFSET_X if player == 1 else PLAYER_2_SCORE_OFFSET_X
    return canvas.create_text(x_offset, HEADER_TEXT_OFFSET_Y, text=SCORE_TEXT + str(lives))


def initialize_header(canvas):
    scores = [{'player': 1, 'lives': 10}, {'player': 2, 'lives': 10}]
    canvas.create_line(PLAY_AREA_LEFT, PLAY_AREA_TOP, PLAY_AREA_RIGHT, PLAY_AREA_TOP, fill='#101010')
    for score in scores:
        player = score['player']
        lives = score['lives']
        score['item'] = create_score_for_player(player, canvas, lives)
    return scores


def new_ball_direction(player):
    max_angle = math.atan(PLAY_AREA_HEIGHT / PLAY_AREA_WIDTH)
    rand = random.randint(-1000, 1000)
    random_angle = rand * max_angle / 1000
    x_step = BALL_VELOCITY * math.cos(random_angle)
    y_step = BALL_VELOCITY * math.sin(random_angle)

    if player == 2:
        x_step *= -1

    return {'x_step': x_step, 'y_step': y_step}


def set_ball_color(ball, canvas):
    color = BALL_COLOR_PLAYER_1 if ball['player'] == 1 else BALL_COLOR_PLAYER_2
    canvas.itemconfig(ball['item'], fill=color, outline=color)


def initialize_ball(ball, canvas):
    player = ball['player']
    ball_direction = new_ball_direction(player)
    if player == 1:
        ball['x'] = PLAY_AREA_LEFT + BALL_INITIAL_X_OFFSET
    if player == 2:
        ball['x'] = PLAY_AREA_RIGHT - BALL_INITIAL_X_OFFSET

    ball['y'] = PLAY_AREA_TOP + BALL_INITIAL_Y_OFFSET
    ball['x_step'] = ball_direction['x_step']
    ball['y_step'] = ball_direction['y_step']

    ball['item'] = canvas.create_oval(ball['x'] - BALL_RADIUS, ball['y'] - BALL_RADIUS, ball['x'] + BALL_RADIUS,
                                      ball['y'] + BALL_RADIUS)
    set_ball_color(ball, canvas)


def initialize_balls(canvas):
    balls = [{'player': 1},
             {'player': 2}]

    for ball in balls:
        initialize_ball(ball, canvas)

    return balls


def initialize_barriers(canvas):
    width_of_all_barrier_columns = PLAYER_COUNT * BARRIER_COLUMN_COUNT_PER_PLAYER * (
            BARRIER_WIDTH + SPACE_BETWEEN_BARRIER_COLUMNS) - SPACE_BETWEEN_BARRIER_COLUMNS
    starting_x_of_barriers = PLAY_AREA_LEFT + (PLAY_AREA_WIDTH - width_of_all_barrier_columns) // 2
    starting_y_of_barriers = PLAY_AREA_TOP + SPACE_ABOVE_AND_BELOW_BARRIERS
    barriers = []
    for i in range(PLAYER_COUNT * BARRIER_COLUMN_COUNT_PER_PLAYER):
        even = ((i % 2) == 0)
        x = starting_x_of_barriers + i * (BARRIER_WIDTH + SPACE_BETWEEN_BARRIER_COLUMNS)
        for j in range(BARRIER_COUNT_PER_COLUMN):
            y = starting_y_of_barriers + j * (BARRIER_HEIGHT + SPACE_BETWEEN_BARRIERS)
            barriers.append(
                {'x1': x, 'y1': y, 'x2': x + BARRIER_WIDTH, 'y2': y + BARRIER_HEIGHT, 'player': 1 if even else 2})
    for barrier in barriers:
        color = PLAYER_1_COLOR if barrier['player'] == 1 else PLAYER_2_COLOR
        barrier['item'] = canvas.create_rectangle(barrier['x1'], barrier['y1'], barrier['x2'], barrier['y2'],
                                                  fill=color, outline=color)
        barrier['active'] = True

    return barriers


def initialize_paddles(canvas):
    paddles = [
        {'x': PLAYER_1_PADDLE_X, 'y': PLAY_AREA_TOP + PLAY_AREA_HEIGHT // 2, 'player': 1, 'move_direction': 'none'},
        {'x': PLAYER_2_PADDLE_X, 'y': PLAY_AREA_TOP + PLAY_AREA_HEIGHT // 2, 'player': 2, 'move_direction': 'none'}]

    for paddle in paddles:
        color = PLAYER_1_COLOR if paddle['player'] == 1 else PLAYER_2_COLOR
        start = 270 if paddle['player'] == 1 else 90
        extent = 180
        top_left = {'x': paddle['x'], 'y': paddle['y'] - PADDLE_HEIGHT // 2}
        bottom_right = {'x': paddle['x'] + PADDLE_WIDTH, 'y': paddle['y'] + PADDLE_HEIGHT // 2}
        paddle['item'] = canvas.create_arc(top_left['x'], top_left['y'], bottom_right['x'], bottom_right['y'],
                                           start=start,
                                           extent=extent, outline=color, fill=color)

    return paddles


def check_paddle_bounds(paddle):
    if paddle['y'] < PADDLE_MIN_Y:
        paddle['y'] = PADDLE_MIN_Y

    if paddle['y'] > PADDLE_MAX_Y:
        paddle['y'] = PADDLE_MAX_Y


def update_paddles(canvas, game_state):
    paddles = game_state['paddles']
    for paddle in paddles:
        old_y = paddle['y']
        if paddle['move_direction'] == 'up':
            paddle['y'] -= PADDLE_MOVE_STEP
        if paddle['move_direction'] == 'down':
            paddle['y'] += PADDLE_MOVE_STEP
        check_paddle_bounds(paddle)
        canvas.move(paddle['item'], 0, paddle['y'] - old_y)


def update_barriers(canvas, game_state):
    barriers = game_state['barriers']
    return


def ball_overlaps_barrier(ball, barrier):
    if not barrier['active']: return False
    overlaps = False

    if ball['x'] + BALL_RADIUS > barrier['x1'] and ball['x'] - BALL_RADIUS < barrier['x2'] and ball['y'] + BALL_RADIUS > \
            barrier['y1'] and ball['y'] - BALL_RADIUS < barrier['y2']:
        overlaps = True
    return overlaps


def ball_collided_with_barrier(ball, barrier, canvas):
    """
    If the ball overlaps with a barrier AND the ball and barrier are for the same player the barrier is destroyed and
    the ball bounces back.
    If the ball overlaps with a barrier that is for the other player, the ball keeps going
    :param ball:
    :param barrier:
    :param canvas:
    :return:
    """
    collision = False
    if ball['player'] == barrier['player'] and ball_overlaps_barrier(ball, barrier):
        ball['x_step'] *= -1
        canvas.delete(barrier['item'])
        barrier['active'] = False
        collision = True
    return collision


def ball_overlaps_paddle(ball, paddle):
    overlaps = False
    px1 = paddle['x'] - PADDLE_WIDTH // 2
    px2 = paddle['x'] + PADDLE_WIDTH // 2
    py1 = paddle['y'] - PADDLE_HEIGHT // 2
    py2 = paddle['y'] + PADDLE_HEIGHT // 2

    if ball['x'] + BALL_RADIUS > px1 and ball['x'] - BALL_RADIUS < px2 and ball['y'] + BALL_RADIUS > \
            py1 and ball['y'] - BALL_RADIUS < py2:
        overlaps = True
    return overlaps


def ball_collided_with_paddle(ball, paddle):
    collision = False

    if ball_overlaps_paddle(ball, paddle):
        ball['x_step'] *= -1
        ball['player'] = paddle['player']
        collision = True

    return collision


def player_missed(player, canvas, game_state):
    scores = game_state['scores']
    score = list(filter(lambda x: x['player'] == player, scores))[0]
    score['lives'] -= 1
    canvas.delete(score['item'])
    score['item'] = create_score_for_player(player, canvas, score['lives'])


def check_ball_bounds(ball, game_state, canvas):
    barriers = game_state['barriers']
    paddles = game_state['paddles']
    if ball['y'] < PLAY_AREA_TOP + BALL_RADIUS:
        ball['y_step'] *= -1
        ball['y'] = PLAY_AREA_TOP + BALL_RADIUS
    if ball['y'] > PLAY_AREA_BOTTOM - BALL_RADIUS:
        ball['y_step'] *= -1
        ball['y'] = PLAY_AREA_BOTTOM - BALL_RADIUS
    for barrier in barriers:
        if ball_collided_with_barrier(ball, barrier, canvas):
            break
    for paddle in paddles:
        if ball_collided_with_paddle(ball, paddle):
            set_ball_color(ball, canvas)
            break

    ball_missed = False
    if ball['x'] + BALL_RADIUS > PLAY_AREA_RIGHT:
        player_missed(2, canvas, game_state)
        ball_missed = True

    if ball['x'] - BALL_RADIUS < PLAY_AREA_LEFT:
        player_missed(1, canvas, game_state)
        ball_missed = True

    if ball_missed:
        canvas.delete(ball['item'])
        initialize_ball(ball, canvas)

    return


def update_balls(canvas, game_state):
    balls = game_state['balls']
    for ball in balls:
        check_ball_bounds(ball, game_state, canvas)
        ball['x'] += ball['x_step']
        ball['y'] += ball['y_step']
        canvas.move(ball['item'], ball['x_step'], ball['y_step'])
    return


def update_header(canvas, game_state):
    return


def drawFrame(canvas, game_state):
    # update world
    update_paddles(canvas, game_state)
    update_barriers(canvas, game_state)
    update_balls(canvas, game_state)
    update_header(canvas, game_state)

    canvas.update()

    # pause
    canvas.after(20, drawFrame, canvas, game_state)


######## These helper methods use "lists" ###########
### Which is a concept you will learn Monday ###########

def get_left_x(canvas, object):
    return canvas.coords(object)[0]


def get_top_y(canvas, object):
    return canvas.coords(object)[1]


######## DO NOT MODIFY ANY CODE BELOW THIS LINE ###########

# This function is provided to you and should not be modified.
# It creates a window that contains a drawing canvas that you
# will use to make your drawings.
def make_canvas(width, height, title):
    """
    DO NOT MODIFY
    Creates and returns a drawing canvas
    of the given int size with a blue border,
    ready for drawing.
    """
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1, borderwidth=0, highlightthickness=0)
    canvas.focus_set()

    canvas.pack()
    return canvas


if __name__ == '__main__':
    main()
