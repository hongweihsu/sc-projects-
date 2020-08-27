"""
File: breakout
Name: Dennis Hsu / 許宏瑋
----------------------
This is a game aiming to break all bricks.

Game features:

Only 3 chances to challenge, you can restart after game finished.
Get blue accessory to add board width.
Do not get red accessory or board width will decrease.
Ball speed will increase after break our bricks.

"""

"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao
"""

from campy.graphics.gobjects import GRect
from campy.gui.events.timer import pause
from log_in_page import Log_in_page
from breakoutgraphics import BreakoutGraphics
from campy.gui.events.mouse import onmouseclicked

"""
Global Variables
"""
FRAME_RATE = 1000 / 500  # 120 frames per second.
NUM_LIVES = 3  # this number represent the left chances to challenge the game.
log_in_page = Log_in_page()


def main():
    """
    In the beginning, a loading animation will start, once it achieve 100%, two button will show on windows.
    If player click these two button, game animation loop will be triggered and game page will show.
    """
    onmouseclicked(animation_loop)
    log_in_page.loading()
    log_in_page.add_play_button()
    log_in_page.add_fb_button()


def animation_loop(m):
    global NUM_LIVES
    enter_game_page(m)

    while graphics.total_bricks != 0 and NUM_LIVES != 0:

        if graphics.mouse_click:
            graphics.ball_move()
            graphics.accessory_move()
            if graphics.ball.y > graphics.window.height:
                graphics.reset_ball_paddle()
                NUM_LIVES -= 1
                graphics.window.remove(graphics.heart_icon_box[NUM_LIVES])
        pause(FRAME_RATE)

    if NUM_LIVES == 0:
        graphics.is_game_over = True
        graphics.show_result_label()
        onmouseclicked(play_again)
        print('Game Over')
    else:
        graphics.show_result_label()
        print('You Win!')
        onmouseclicked(play_again)


def enter_game_page(m):
    global graphics  # set graphics object to global so animation loop can call it.

    obj = log_in_page.window.get_object_at(m.x, m.y)
    if obj is log_in_page.play_button or obj is log_in_page.play_label or obj is log_in_page.fb_button \
            or obj is log_in_page.fb_label or obj is log_in_page:
        graphics = BreakoutGraphics()  # new window will show at this moment.
        log_in_page.window.close()  # close the login window.
        graphics.draw_bricks()
        graphics.add_score_board()
        graphics.add_accessories(10)  # give argument to determine the total number of blue/red blocks will show.
        graphics.dx_getter()
        graphics.dy_getter()

        """
        The following part has some bugs I still figuring out, that is, when I use GPolygon to draw a heart 
        shape and add it to window, it seems to conflict to method: window.get_object_at(x,y). Though it's not perfect,
        I use GOval to represent NUM_LIVES on the right-top window. 
        """
        for i in range(NUM_LIVES):
            heart = graphics.draw_heart_icon()
            graphics.window.add(heart, graphics.window.width - graphics.heart_shape.width * (i + 1) - 5 * (i + 1),
                                graphics.score_board_label.y - graphics.heart_shape.height)


def play_again(n):
    """
    After finishing the game, if player click the result label, which show Game over or You win, the login page will
    show up again and player can start new run of game.
    :param n: the mouse positional information after game finished.
    """
    global log_in_page, NUM_LIVES
    if graphics.window.get_object_at(n.x, n.y) is graphics.result_label:

        NUM_LIVES = 3
        log_in_page = Log_in_page()
        graphics.window.remove(graphics.result_label)
        graphics.window.close()
        log_in_page.add_play_button()
        log_in_page.add_fb_button()
        log_in_page.solid_bar = GRect(log_in_page.load_bar.width, log_in_page.load_bar.height)
        log_in_page.loading()
        log_in_page.window.add(log_in_page.solid_bar, log_in_page.load_bar.x, log_in_page.load_bar.y)
        log_in_page.load_label.text = '100%'
        log_in_page.window.add(log_in_page.load_label,
                               log_in_page.load_bar.x + log_in_page.load_bar.width - log_in_page.load_label.width,
                               log_in_page.load_bar.y + log_in_page.load_bar.height + log_in_page.load_label.height + 5)
        onmouseclicked(animation_loop)


if __name__ == '__main__':
    main()
