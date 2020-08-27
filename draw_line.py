"""
File: draw_line
Name: Dennis Hsu / 許宏瑋
-------------------------
TODO:
"""

from campy.graphics.gobjects import GOval, GLine
from campy.graphics.gwindow import GWindow
from campy.gui.events.mouse import onmouseclicked

SIZE = 10
window = GWindow()
line_position = []
point = GOval(SIZE, SIZE)


def main():
    """
    This program creates lines on an instance of GWindow class.
    There is a circle indicating the user’s first click. A line appears
    at the condition where the circle disappears as the user clicks
    on the canvas for the second time.
    """
    onmouseclicked(draw)


def draw(m):
    """
    The position from a user clicks will be stored in 'line_position', in addition,
    when the list contains two members, it will trigger 'if' condition to draw a line by
    linking two positions.
    :param m: information of mouse position
    """
    window.add(point, m.x - SIZE / 2, m.y - SIZE / 2)
    line_position.append((m.x, m.y))

    if len(line_position) == 2:
        line = GLine(line_position[0][0], line_position[0][1], line_position[1][0], line_position[1][1])
        window.add(line)
        window.remove(point)
        line_position.clear()


if __name__ == "__main__":
    main()
