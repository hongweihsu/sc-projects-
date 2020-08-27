"""
File: babygraphics
Name: Dennis Hsu

SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.

Type any name (or searching parts of name on Search bar) on Names bar,
if request name is valid (no illegal character) and contained by database files,
the program will draw data onto canvas to show it's rank for each year.

Extension features:

01. Type any integer between 1 to 1000, you can get name by rank (your input) for each year.
    e.g. Type '50' then the screen will show you which name is ranked 50 for each year.
02. Type 'uptrend_number', you can get most increased name in mount of numbers.
    e.g Type 'uptrend_10' then screen will show you which names are top 10 increased from 1900 to 2010.
03. Every function can work at the same request.
    e.g Type '!abc' 'aaron' '500' 'uptrend_3' in one request, the program will first filter illegal request (!abc),
        showing data of 'Aaron' (cause aaron will be capitalised) and show names of rank 500 of each year,
        moreover, it also provide information about top 3 increased name in last century (1900 - 2010).
"""

import tkinter
import babynames
import babygraphicsgui as gui

#  Global various
FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]   # data resources
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 35  # margin for left, right, bottom edge of canvas
GRAPH_MARGIN_SIZE_TOP = 40  # margin for top edge of canvas
COLORS = ['red', 'purple', 'green', 'blue']  # colors for different line.
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index of the current year in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                              with the specified year.
    """
    distance = (width - 2 * GRAPH_MARGIN_SIZE) / len(YEARS)  # divide equally width for each year on canvas.
    x_coordinate = GRAPH_MARGIN_SIZE + year_index * distance  # x position for beginning of each year.
    return x_coordinate


def draw_fixed_lines(canvas):
    """
    Erases all existing information on the given canvas and then
    draws the fixed background lines on it.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.

    Returns:
        This function does not return any value.
    """

    # Write your code below this line
    #################################

    # top edge
    canvas.create_line((GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE_TOP),
                       (CANVAS_WIDTH - GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE_TOP))
    # bottom edge (upper years words)
    canvas.create_line((GRAPH_MARGIN_SIZE, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE),
                       (CANVAS_WIDTH - GRAPH_MARGIN_SIZE, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE))
    # another bottom edge (under years words)
    canvas.create_line((GRAPH_MARGIN_SIZE, CANVAS_HEIGHT),
                       (CANVAS_WIDTH - GRAPH_MARGIN_SIZE, CANVAS_HEIGHT))
    # right edge
    canvas.create_line((CANVAS_WIDTH - GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE_TOP),
                       (CANVAS_WIDTH - GRAPH_MARGIN_SIZE, CANVAS_HEIGHT))

    # each y-axis for years from left to right.
    for i in range(len(YEARS)):
        x = get_x_coordinate(CANVAS_WIDTH, i)
        canvas.create_line((x, GRAPH_MARGIN_SIZE_TOP), (x, CANVAS_HEIGHT))
        canvas.create_text(x, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE, text=YEARS[i], anchor=tkinter.NW)


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """

    # Write your code below this line
    #################################

    for i in lookup_names:
        line_end = []
        color_index = (lookup_names.index(i) % len(COLORS))
        for year in YEARS:
            if str(year) in name_data[i]:  # if certain year inside the database as a key, the value can be stored as rank.
                rank = int(name_data[i][str(year)])
            else:
                rank = 1000

            #  (x, y) position for ends of line.
            y = (CANVAS_HEIGHT - (GRAPH_MARGIN_SIZE + GRAPH_MARGIN_SIZE_TOP)) * (rank / 1000) + GRAPH_MARGIN_SIZE_TOP
            x = GRAPH_MARGIN_SIZE + YEARS.index(year) * ((CANVAS_WIDTH - 2 * GRAPH_MARGIN_SIZE) / len(YEARS))

            if rank != 1000:
                text = i + ' ' + str(rank)
            else:
                text = i + ' *'  # represent rank as * for no data years.

            canvas.create_text(x + TEXT_DX, y, text=text, anchor=tkinter.SW, fill=COLORS[color_index])

            line_end.append((x, y))
            if len(line_end) == 2:  # when line_end get 2 points, connecting them and removing first point.
                canvas.create_line(line_end[0], line_end[1], fill=COLORS[color_index])
                line_end.remove(line_end[0])


def draw_ranks(canvas, name_data, lookup_ranks):
    """
    Given a dict of baby name data and a number as rank, plots
    the name of the rank of each year onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data.
        lookup_ranks ('str'): For each year, draw name of rank that equals this argument.

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)  # draw the fixed background grid.
    rank_result = {}  # dict to store data in format { 'request rank' : {'year' : ['name_1', 'name_2']}, ...}

    for rank in lookup_ranks:  # lookup_ranks consist of numbers between 1 to 1000, all numbers are string types.
        rank_result[rank] = {}  # create a dict as value of rank. e.g { 'rank' : {}...}
        for year in YEARS:
            rank_result[rank][str(year)] = []  # set empty list as value for each year. e.g { 'rank' : {1900 : []}, ...}

    for name, value in name_data.items():
        for year, rank in value.items():
            if rank in rank_result:  # find rank that requested.
                rank_result[rank][year].append(name)  # e.g { '20' : {'1920' : ['Rose', 'Jack'], ...}

    #  Drawing canvas
    text = ''
    for rank in rank_result:
        y = (CANVAS_HEIGHT - (GRAPH_MARGIN_SIZE + GRAPH_MARGIN_SIZE_TOP)) * (int(rank) / 1000) + GRAPH_MARGIN_SIZE_TOP
        canvas.create_text(GRAPH_MARGIN_SIZE, y, text=rank + ' ', anchor=tkinter.SE, fill='lightgray', font='times 12')

        for year in rank_result[rank]:
            y = (CANVAS_HEIGHT - (GRAPH_MARGIN_SIZE + GRAPH_MARGIN_SIZE_TOP)) * (
                    int(rank) / 1000) + GRAPH_MARGIN_SIZE_TOP
            x = GRAPH_MARGIN_SIZE + YEARS.index(int(year)) * ((CANVAS_WIDTH - 2 * GRAPH_MARGIN_SIZE) / len(YEARS))

            if len(rank_result[rank][year]) == 2:
                text = rank_result[rank][year][0] + '\n' + rank_result[rank][year][1]

            # it might be only one name in certain rank of certain year, since we only chose higher rank for same name.
            elif len(rank_result[rank][year]) == 1:
                text = rank_result[rank][year][0]

            canvas.create_text(x + TEXT_DX, y, text=text, anchor=tkinter.SW, fill='lightgray')


def draw_up_trend(canvas, name_data, inquiry_ranges):
    """
    Given a dict of baby name data and a number as range, plots
    the most increased names within top range onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data.
        inquiry_ranges ('int'): A number used to decide how many data should be draw onto screen form most increased one.

    Returns:
        This function does not return any value.
    """
    lookup_names = []
    uptrend_names = {}  # store names as key and rank changed value as value. e.g {sofia:913}
    for name, value in name_data.items():
        year_box = []
        for year in value.keys():
            year_box.append(int(year))

        initial_rank = int(name_data[name][str(min(year_box))])  # rank for earliest year of one name.
        last_rank = int(name_data[name][str(max(year_box))])  # rank for last year of one name.
        if last_rank - initial_rank < 0:  # rank increased in the last.
            uptrend_names[name] = ((last_rank - initial_rank) * (-1))  # rank changed value of one name.

    # use rank changed value as element to sort decreasingly.
    sorted_uptrend_names = sorted(uptrend_names.items(), reverse=True, key=lambda e: e[1])

    # only draw names inside the range, so extract top range of names into lookup_name, then pass to draw_names.
    for inquiries in range(inquiry_ranges):
        lookup_names.append(sorted_uptrend_names[inquiries][0])
        x = GRAPH_MARGIN_SIZE + inquiries * ((CANVAS_WIDTH - 2 * GRAPH_MARGIN_SIZE) / len(YEARS))
        y = GRAPH_MARGIN_SIZE
        canvas.create_text(x, y, text=sorted_uptrend_names[inquiries][0] + '\u0020' + str(sorted_uptrend_names[inquiries][1]) +
                                       '\u2191', anchor=tkinter.SW, fill='navy', font='times 12', width=80)

    draw_names(canvas, name_data, lookup_names)


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, draw_ranks, draw_up_trend,
                          babynames.search_names)  # tkinter.Canvas

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
