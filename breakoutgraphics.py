"""
File: breakout
Name: Dennis Hsu / 許宏瑋
----------------------
This is a class can be used to create bricks, ball, paddle and accessories.
"""

"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao
"""

from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel, GPolygon
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5  # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40  # Height of a brick (in pixels).
BRICK_HEIGHT = 15  # Height of a brick (in pixels).
BRICK_ROWS = 12  # Number of rows of bricks.
BRICK_COLS = 10  # Number of columns of bricks.
BRICK_OFFSET = 50  # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10  # Radius of the ball (in pixels).
PADDLE_WIDTH = 90  # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15  # Height of the paddle (in pixels).
PADDLE_OFFSET = 50  # Vertical offset of the paddle from the window bottom (in pixels).

INITIAL_Y_SPEED = 7  # Initial vertical speed for the ball.
MAX_X_SPEED = 6  # Maximum initial horizontal speed for the ball.


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                 paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                 brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                 brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                 brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING,
                 title='Breakout'):

        # Create a graphical window, with some extra space.
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 2.7 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle.
        self.paddle = GRect(paddle_width, paddle_height)
        self.paddle.color = 'navy'
        self.paddle.filled = True
        self.paddle.fill_color = 'navy'
        self.window.add(self.paddle, (self.window.width - self.paddle.width) / 2, self.window.height - paddle_offset)

        # Center a filled ball in the graphical window.
        self.ball = GOval(ball_radius * 2, ball_radius * 2)
        self.ball.color = 'navy'
        self.ball.filled = True
        self.ball.fill_color = 'navy'
        self.window.add(self.ball, (self.window.width - self.ball.width) / 2,
                        (self.window.height - self.ball.height) / 2 + 50)

        # a list dynamically stores four detecting points of the ball
        self.ball_boundary = []

        # Default initial velocity for the ball.
        self.__dx = random.randint(3, MAX_X_SPEED)
        self.__dy = INITIAL_Y_SPEED

        # Initialize our mouse listeners.
        self.mouse_click = False
        onmouseclicked(self.start_game)

        # check accessibility
        self.is_game_over = False

        # total numbers of bricks
        self.total_bricks = brick_rows * brick_cols

        # bricks storing box
        self.bricks_box = []

        # create a list to store random number, if the same number of brick be removed, a magic accessories will appear.
        self.accessories_number = []

        # create a list to store accessories.
        self.accessories_box = {}

        # generate accessories
        self.blue_acc = GRect(0, 0)

        # set a score board
        self.score = 0
        self.score_board_label = GLabel(f'scores:{self.score}')

        # create a heart icon and a list to store these icons.
        # self.heart_point = [(7.5, 15), (0, 5), (3.75, 0), (7.5, 3), (11.25, 0), (15, 5), (7.5, 15)]
        self.heart_icon_box = []

        # give result label to present end of game
        self.result_label = GLabel('Game Over or You Win')

    def dx_getter(self):
        print(f'this is dx value: {self.__dx}.')

    def dy_getter(self):
        print(f'this is dy value: {self.__dy}.')

    def set_velocity(self):
        self.__dx = random.randint(1, MAX_X_SPEED)
        self.__dy = INITIAL_Y_SPEED
        if random.random() > 0.5:
            self.__dx = -self.__dx

    def start_game(self, m):
        """
        The game will triggered by this method once player click the mouse.
        :param m: mouse position in (x,y) expression.
        """
        if not self.is_game_over:
            if self.mouse_click:
                print('Game already start.')
            else:
                self.mouse_click = True
                print('Game started')
                onmousemoved(self.__paddle_move)
        else:
            print('There\'s no chance left')

    def __paddle_move(self, m):
        """
        This method will listen to mouse click, making paddle's position always align to mouse position.
        :param m: mouse position in (x,y) expression.
        """
        if self.mouse_click:
            self.paddle.x = m.x - self.paddle.width / 2
            if self.paddle.x < 0:
                self.paddle.x = 0
            elif self.paddle.x > self.window.width - self.paddle.width:
                self.paddle.x = self.window.width - self.paddle.width

    def ball_move(self, ball_radius=BALL_RADIUS):
        self.ball.move(self.__dx, self.__dy)

        if self.ball.x < 0:  # right and left boundary of window
            self.ball.x = 0
            self.__dx = -self.__dx
        elif self.ball.x > self.window.width - ball_radius * 2:  # left boundary of window
            self.ball.x = self.window.width - ball_radius * 2
            self.__dx = -self.__dx

        elif self.ball.y < 0:  # top boundary of window
            self.ball.y = 0
            self.__dy = -self.__dy

        self.__ball_detect_obj()

    def __ball_detect_obj(self, ball_radius=BALL_RADIUS, brick_width=BRICK_WIDTH,
                          brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, ):
        """
       The method will detects object around the ball, once it detects a brick, the brick will be removed.
       Also, depending on the color of brick removed, different accelerate velocity will be adding to the ball.
        """

        self.ball_boundary = [(self.ball.x, self.ball.y), (self.ball.x + ball_radius * 2, self.ball.y),
                              (self.ball.x, self.ball.y + ball_radius * 2),
                              (self.ball.x + ball_radius * 2, self.ball.y + ball_radius * 2)]

        for i in range(len(self.ball_boundary)):

            my_obj = self.window.get_object_at(self.ball_boundary[i][0], self.ball_boundary[i][1])

            if my_obj in self.bricks_box:  # has detected bricks

                if self.bricks_box.index(my_obj) in self.accessories_number:  # the index of the brick equals accessories number, blue or red blocks will be generated.

                    if self.accessories_number.index(self.bricks_box.index(my_obj)) % 2 == 0:  # create blue accessories
                        self.blue_acc = GRect(15, 15)
                        self.blue_acc.filled = True
                        self.blue_acc.fill_color = 'navy'
                        self.accessories_box[self.blue_acc] = 'navy'
                        self.window.add(self.blue_acc, (my_obj.x + my_obj.width / 2), (my_obj.y + my_obj.height / 2))

                    else:  # create blue accessories
                        self.red_acc = GRect(15, 15)
                        self.red_acc.filled = True
                        self.red_acc.fill_color = 'red'
                        self.accessories_box[self.red_acc] = 'red'
                        self.window.add(self.red_acc, (my_obj.x + my_obj.width / 2), (my_obj.y + my_obj.height / 2))

                self.__dy = -self.__dy
                self.window.remove(my_obj)
                self.total_bricks -= 1

                if 80 <= self.bricks_box.index(my_obj):
                    self.__dy *= random.uniform(1.006, 1.02)
                    self.__dx *= random.uniform(1.006, 1.02)
                    self.score += 1
                elif 50 <= self.bricks_box.index(my_obj) < 80:
                    self.__dy *= random.uniform(1.004, 1.01)
                    self.__dx *= random.uniform(1.004, 1.01)
                    self.score += 3
                elif 20 <= self.bricks_box.index(my_obj) < 50:
                    self.__dy *= random.uniform(1.001, 1.006)
                    self.__dx *= random.uniform(1.001, 1.006)
                    self.score += 5
                elif 0 <= self.bricks_box.index(my_obj) < 20:
                    self.__dy *= random.uniform(1.001, 1.003)
                    self.__dx *= random.uniform(1.001, 1.003)
                    self.score += 10

                self.score_board_label.text = f'scores:{self.score}'
                self.window.add(self.score_board_label, brick_width + brick_spacing, brick_offset - 15)
                return

            elif my_obj is self.paddle:  # has detected the paddle
                self.__dy = -self.__dy
                self.ball.y = my_obj.y - ball_radius * 2  # To avoid ball sticking on paddle by reset y-position of the ball.
                return

    def accessory_move(self):
        for key, value in list(self.accessories_box.items()):

            key.move(2 * self.__dx / abs(self.__dx), random.randint(3, 8))  # accessory blocks move down.

            obj = self.window.get_object_at((key.x + key.width / 2), (key.y + key.height + 1))

            if obj is self.paddle:

                if value == 'navy':  # when paddle get blue block, paddle width increased.
                    self.paddle.width *= 1.4
                    if self.paddle.width > self.window.width * 0.8:
                        self.paddle.width = self.window.width * 0.8

                else:  # when paddle get red block, paddle width cut back.
                    self.paddle.width *= 0.5
                    if self.paddle.width < 50:
                        self.paddle.width = 50

                self.window.remove(key)
                del self.accessories_box[key]  # delete key value pair after the block reaches paddle.
                self.window.remove(self.paddle)
                self.window.add(self.paddle, self.paddle.x, self.paddle.y)  # renew paddle width to screen.

            if key.y > self.window.height:  # It should be removed if accessory block didn't caught by paddle.
                self.window.remove(key)
                del self.accessories_box[key]

    def reset_ball_paddle(self, paddle_offset=PADDLE_OFFSET):
        """
        When ball is out of button range, the method will reset ball and paddle's position and clear accessories.
        :param paddle_offset:
        """
        if self.ball.y > self.window.height:
            print('reset ball and paddle.')
            self.mouse_click = False  # reset mouse state.

            self.ball.x = (self.window.width - self.ball.width) / 2  # reset the x-position of ball.
            self.ball.y = (self.window.height - self.ball.height) / 2  # reset the y-position of ball.

            self.paddle.x = (self.window.width - self.paddle.width) / 2  # reset the x-position of paddle.
            self.paddle.y = self.window.height - paddle_offset  # reset the y-position of paddle.

            for i in self.accessories_box: # clear all accessories on the window.
                self.window.remove(i)
            self.accessories_box.clear()

    def draw_bricks(self, brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                    brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING):
        """
        When player enter game page, this method called by main function, it will displays bricks from left top corner until
        all bricks displayed. It also give bricks different colors depends on which row the brick exactly occupy. Moreover,
        at the moment brick generated, it will be store in list in order to be used later.
        """
        for i in range(12):
            for j in range(10):
                brick = GRect(brick_width, brick_height, x=(brick_width + brick_spacing) * j,
                              y=brick_offset + (brick_height + brick_spacing) * i)
                brick.filled = True
                if i < 2:
                    brick.fill_color = '#204051'
                    self.bricks_box.append(brick)
                    self.window.add(brick)
                elif 2 <= i < 5:
                    brick.fill_color = '#3b6978'
                    self.bricks_box.append(brick)
                    self.window.add(brick)
                elif 5 <= i < 8:
                    brick.fill_color = '#84a9ac'
                    self.bricks_box.append(brick)
                    self.window.add(brick)
                elif 8 <= i < 12:
                    brick.fill_color = '#e4e3e3'
                    self.bricks_box.append(brick)
                    self.window.add(brick)

    def add_score_board(self, brick_width=BRICK_WIDTH,
                        brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, ):
        """
        Setting a score board on to left-top screen and align to second column.
        """
        self.score_board_label.font = '-15'
        self.window.add(self.score_board_label, brick_width + brick_spacing, brick_offset - 15)

    def add_accessories(self, num):
        """
        This method randomly chose numbers between 0 to numbers of total bricks, and each numbers will not be repeated.
        :param num: total number of accessories.
        :return: return self until number of list - self.accessories_number - equals to num.
        """
        if len(self.accessories_number) < num <= len(self.bricks_box):
            for i in range(num - len(self.accessories_number)):
                random_number = random.randint(0, len(self.bricks_box))
                if not random_number in self.accessories_number:
                    self.accessories_number.append(random_number)

            return self.add_accessories(num)
        else:
            return

    def show_result_label(self):
        """
        This method shows game result when game finished, it depends on if the player clears all bricks in three game times.
        """
        if self.is_game_over:
            self.result_label.text = 'Game Over'
            self.result_label.font = '-40'
            self.window.add(self.result_label, (self.window.width - self.result_label.width) / 2,
                            (self.window.height - self.result_label.height) * 3 / 4)
        else:
            self.result_label.text = 'You Win'
            self.result_label.color = 'red'
            self.result_label.font = '-40'
            self.window.add(self.result_label, (self.window.width - self.result_label.width) / 2,
                            (self.window.height - self.result_label.height) / 2)

    def draw_heart_icon(self):
        """
        To represent how many NUM_LIVES left onto screen.
        P.S: I am trying to use GPolygon to create heart shape but it seems to conflict to windows.get_obj_at method.
        """
        self.heart_shape = GOval(15, 15)
        self.heart_shape.color = 'lightgray'
        self.heart_shape.filled = True
        self.heart_shape.fill_color = 'pink'
        self.heart_icon_box.append(self.heart_shape)
        return self.heart_shape
