"""
File: sierpinski.py
Name: 
---------------------------
This file recursively prints the Sierpinski triangle on GWindow.
The Sierpinski triangle is a fractal described in 1915 by Waclaw Sierpinski.
It is a self similar structure that occurs at different levels of iterations.
"""

from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GLine
from campy.gui.events.timer import pause

# Constants
ORDER = 2  # Controls the order of Sierpinski Triangle
LENGTH = 600  # The legth of order 1 Sierpinski Triangle
UPPER_LEFT_X = 150  # The upper left x coordinate of order 1 Sierpinski Triangle
UPPER_LEFT_Y = 100  # The upper left y coordinate of order 1 Sierpinski Triangle
WINDOW_WIDTH = 950  # The width of the GWindow
WINDOW_HEIGHT = 700  # The height of the GWindow

# Global Variable
window = GWindow(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)  # The canvas to draw Sierpinski Triangle


def main():

	sierpinski_triangle(ORDER, LENGTH, UPPER_LEFT_X, UPPER_LEFT_Y)

def sierpinski_triangle(order, length, upper_left_x, upper_left_y):
	"""
	order: number of layer should print.
	:param length: length of triangle.
	:param upper_left_x: x position of top-left point of triangle.
	:param upper_left_y: y position of top-left point of triangle.
	:return:
	"""
	pause(300)
	if order == 0:  # base point
		pass

	else:

		sierpinski_triangle(order-1, length/2, upper_left_x, upper_left_y)
		sierpinski_triangle(order-1, length/2, upper_left_x+length/2, upper_left_y)
		sierpinski_triangle(order-1, length/2, upper_left_x+length/4, upper_left_y+length*0.886/2)

		point = [(upper_left_x, upper_left_y), (upper_left_x + length, upper_left_y),
			(upper_left_x + length / 2, upper_left_y + length * 0.886)]

		line_top = GLine(point[0][0], point[0][1], point[1][0], point[1][1])
		line_right = GLine(point[1][0], point[1][1], point[2][0], point[2][1])
		line_left = GLine(point[2][0], point[2][1], point[0][0], point[0][1])

		window.add(line_top)
		window.add(line_right)
		window.add(line_left)


if __name__ == '__main__':
	main()
