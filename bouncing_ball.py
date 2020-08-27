"""
File: bouncing_ball
Name: Dennis Hsu / 許宏瑋
-------------------------
TODO:
"""

from campy.graphics.gobjects import GOval
from campy.graphics.gwindow import GWindow
from campy.gui.events.timer import pause
from campy.gui.events.mouse import onmouseclicked

VX = 3
DELAY = 10
GRAVITY = 1
SIZE = 20
REDUCE = 0.9
START_X = 30
START_Y = 40

window = GWindow(800, 500, title='bouncing_ball.py')

ball = GOval(SIZE, SIZE)
"""when button was turned on, any click from user would be ignored."""
start_button_pressed = False

"""if 'play_numbers' over restriction, nothing happen."""
play_numbers = 0


def main():
    """
    This program simulates a bouncing ball at (START_X, START_Y)
    that has VX as x velocity and 0 as y velocity. Each bounce reduces
    y velocity to REDUCE of itself.
    """
    ball.filled = True
    ball.fill_color = 'black'
    onmouseclicked(ball_fall)
    window.add(ball, START_X, START_Y)


def ball_fall(m):
    global start_button_pressed, play_numbers
    """ setting 'restrict_numbers' to constrain how many times user can play."""
    restrict_numbers = 3
    vertical_speed = 0
    if not start_button_pressed and play_numbers < restrict_numbers:
        start_button_pressed = True
        play_numbers += 1
        while start_button_pressed:
            vertical_speed += GRAVITY
            ball.move(VX, vertical_speed)
            if ball.y + SIZE >= window.height:
                vertical_speed = -vertical_speed * REDUCE
                """ 
                if (ball.y + SIZE) still out of button edge of window, 
                (ball.y + SIZE) is forced to (window.height -1) .
                """
                if ball.y + SIZE + vertical_speed >= window.height:
                    ball.y = window.height - 1 - SIZE

            elif ball.x >= window.width:
                ball.x = START_X
                ball.y = START_Y
                start_button_pressed = False

            pause(DELAY)
    elif play_numbers == restrict_numbers:
        print(f'Sorry, You can only play {restrict_numbers} times.')
    else:
        print('The ball is sporting, please wait.')


if __name__ == "__main__":
    main()
