from campy.graphics.gobjects import GRect, GLabel
from campy.graphics.gwindow import GWindow
from campy.gui.events.timer import pause

WIN_WIDTH = 500
WIN_HEIGHT = 500
BAR_WIDTH = WIN_WIDTH * 0.7
BAR_HEIGHT = 10
PLAY_BUTTON_WIDTH = WIN_WIDTH * 0.6
PLAY_BUTTON_HEIGHT = WIN_HEIGHT * 0.06
FB_BUTTON_WIDTH = WIN_WIDTH * 0.6
FB_BUTTON_HEIGHT = WIN_HEIGHT * 0.06


class Log_in_page:
    def __init__(self, bar_width=BAR_WIDTH, bar_height=BAR_HEIGHT, win_width=WIN_WIDTH, win_height=WIN_HEIGHT,
                 play_button_width=PLAY_BUTTON_WIDTH, play_button_height=PLAY_BUTTON_HEIGHT,
                 fb_button_width=WIN_WIDTH * 0.6,
                 fb_button_height=FB_BUTTON_HEIGHT):

        self.window = GWindow(win_width, win_height, title='Welcome')
        self.load_bar = GRect(bar_width, bar_height)
        self.load_label = GLabel('0%')
        self.solid_bar = GRect(0, bar_height)
        self.play_button = GRect(play_button_width, play_button_height)
        self.play_label = GLabel('Start New Game')
        self.fb_button = GRect(fb_button_width, fb_button_height)
        self.fb_label = GLabel('continue with facebook')

    def loading(self):

        self.download_label = GLabel('downloading')
        self.solid_bar.color = 'black'
        self.solid_bar.filled = True
        self.solid_bar.fill_color = 'black'

        self.window.add(self.load_bar, (self.window.width - self.load_bar.width) / 2,
                        self.window.height * 0.7)

        while self.solid_bar.width < self.load_bar.width:
            self.window.remove(self.solid_bar)
            self.window.remove(self.load_label)
            self.solid_bar.width = self.solid_bar.width + 10
            if (bar_ratio := (self.solid_bar.width / self.load_bar.width) * 100) < 100:
                self.load_label.text = f'{int(bar_ratio)} %'
            else:
                self.load_label.text = f'100%'

            self.window.add(self.solid_bar, self.load_bar.x, self.load_bar.y)
            self.window.add(self.load_label, self.load_bar.x + self.load_bar.width - self.load_label.width,
                            self.load_bar.y + self.load_bar.height + self.load_label.height + 5)

            if self.solid_bar.width < self.load_bar.width * 0.33:
                self.download_label.text = 'downloading....'
            elif self.load_bar.width * 0.25 <= self.solid_bar.width < self.load_bar.width * 0.66:
                self.download_label.text = 'downloading........'
            elif self.load_bar.width * 0.5 <= self.solid_bar.width < self.load_bar.width * 0.99:
                self.download_label.text = 'downloading............'

            self.window.add(self.download_label, self.load_bar.x,
                            self.load_bar.y + self.load_bar.height + self.load_label.height + 5)

            pause(100)
            self.window.remove(self.download_label)

        self.download_label.text = 'completed!'
        self.window.add(self.download_label, self.load_bar.x,
                        self.load_bar.y + self.load_bar.height + self.load_label.height + 5)

    def add_play_button(self):
        self.play_button.color = 'black'
        self.play_button.filled = True
        self.play_button.fill_color = 'white'
        self.window.add(self.play_button, (self.window.width - self.play_button.width) / 2, self.window.height * 0.4)

        self.play_label.font = '-15'
        self.play_label.color = 'black'
        self.window.add(self.play_label, self.play_button.x + (self.play_button.width - self.play_label.width) / 2,
                        self.play_button.y + self.play_button.height - (
                                self.play_button.height - self.play_label.height) / 2)

    def add_fb_button(self, fb_button_width=FB_BUTTON_WIDTH, fb_button_height=FB_BUTTON_HEIGHT):
        self.fb_button.color = 'blue'
        self.fb_button.filled = True
        self.fb_button.fill_color = 'blue'
        self.window.add(self.fb_button, (self.window.width - self.fb_button.width) / 2, self.window.height * 0.5)

        self.fb_label.font = '-15'
        self.fb_label.color = 'white'
        self.window.add(self.fb_label, self.fb_button.x + self.fb_button.width * 0.3,
                        self.fb_button.y + self.fb_button.height - (self.fb_button.height - self.fb_label.height) / 2)

        fb_logo = GRect(self.fb_button.height * 0.7, self.fb_button.height * 0.7)
        fb_logo.color = 'white'
        fb_logo.filled = True
        fb_logo.fill_color = 'white'
        self.window.add(fb_logo, self.fb_button.x + self.fb_button.width * 0.1,
                        self.fb_button.y + (self.fb_button.height - fb_logo.height) / 2)

        fb_logo_label = GLabel('f')
        fb_logo_label.color = 'navy'
        fb_logo_label.font = '-25'
        self.window.add(fb_logo_label, fb_logo.x + fb_logo.width * 0.5,
                        fb_logo.y + fb_logo.height + 7)
