"""
File: babynames
Name: Dennis Hsu

Stanford CS106AP Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Sonja Johnson-Yu, Kylie Jue, and Nick Bowman.

This file defines the functions needed to create the GUI for
the Baby Names project.
"""

import tkinter


# provided function to build the GUI
def make_gui(top, width, height, names, draw_names, draw_ranks, draw_up_trend, search_names):
    """
    Set up the GUI elements for Baby Names, returning the Canvas to use.
    top is TK root, width/height is canvas size, names is BabyNames dict.
    """
    # name entry field
    label = tkinter.Label(top, text="Names:")
    label.grid(row=0, column=0, sticky='w')
    entry = tkinter.Entry(top, width=40, name='entry', borderwidth=2)
    entry.grid(row=0, column=1, sticky='w')
    entry.focus()
    error_out = tkinter.Text(top, height=2, width=70, name='errorout', borderwidth=2)
    error_out.grid(row=0, column=2, sticky='w')

    # canvas for drawing
    canvas = tkinter.Canvas(top, width=width, height=height, name='canvas')
    canvas.grid(row=1, columnspan=12, sticky='w')

    space = tkinter.LabelFrame(top, width=10, height=10, borderwidth=0)
    space.grid(row=2, columnspan=12, sticky='w')

    # Search field etc. at the bottom
    label = tkinter.Label(top, text="Search:")
    label.grid(row=3, column=0, sticky='w')
    search_entry = tkinter.Entry(top, width=40, name='searchentry')
    search_entry.grid(row=3, column=1, sticky='w')
    search_out = tkinter.Text(top, height=2, width=70, name='searchout', borderwidth=2)
    search_out.grid(row=3, column=2, sticky='w')

    # When <return> key is hit in a text field .. connect to the handle_draw()
    # and handle_search() functions to do the work.
    entry.bind("<Return>",
               lambda event: handle_draw(entry, canvas, names, error_out, draw_names, draw_ranks, draw_up_trend))
    search_entry.bind("<Return>", lambda event: handle_search(search_entry, search_out, names, search_names))

    top.update()
    return canvas


def handle_draw(entry, canvas, names, error_out, draw_names, draw_ranks, draw_up_trend):
    """
    (provided)
    Called when <return> key hit in given entry text field.
    Gets search text from given entry, draws results
    to the given canvas.
    """
    text = entry.get()  # get input
    canvas.delete('all')
    lookups = [name[0].upper() + name[1:].lower() for name in text.split()]  # handles casing
    lookup_isnumeric = list(filter(lambda e: e.isnumeric(), lookups))  # filter numbers
    lookup_is_string = list(filter(lambda e: not e.isnumeric(), lookups))  # filter words

    # DRAW_RANKS--------------------------------------------------------------------------------------------

    int_lookups = [int(member) for member in lookup_isnumeric]
    lookup_ranks = list(filter(lambda e: e <= 1000, int_lookups))  # numbers less than 1000 in integer type.
    lookup_ranks = [str(member) for member in lookup_ranks]  # trans type form int to str.

    draw_ranks(canvas, names, lookup_ranks)

    # DRAW_UPTREND--------------------------------------------------------------------------------------------

    inquiry_ranges = 0
    special_key = 'Uptrend_'
    key_words = [word for word in lookup_is_string if special_key in word]  # detect 'Uptrend_' if any word consist of it.
    key_words_valid = [word for word in key_words if word[8:].isnumeric()]  # filter out some words like 'Uptrend_!abc'
    if len(key_words_valid) != 0:
        num = []
        for word in key_words_valid:
            num.append(int(word[8:]))
            # if 'Uptrend_10' and 'Uptrend_50' are typed at same request, the program will send max number as request.
            inquiry_ranges = max(num)

        # draw data for most increased name in inquiry_ranges for past century.
        draw_up_trend(canvas, names, inquiry_ranges)

    # DRAW_NAMES--------------------------------------------------------------------------------------------

    lookup_is_string = list(filter(lambda e: e not in key_words_valid, lookup_is_string))  # filter out Uptrend_int

    invalid_names = [name for name in lookup_is_string if name not in names]
    lookup_names = [name for name in lookup_is_string if name in names]

    # Handle error message
    error_out.delete('1.0', tkinter.END)
    if invalid_names:
        if len(invalid_names) == 1:
            out = invalid_names[0] + ' is not contained in the name database.'
        else:
            out = ', '.join(invalid_names) + ' are not contained in the name database.'
        error_out.insert('1.0', out)

    draw_names(canvas, names, lookup_names)


def handle_search(search_entry, search_out, names, search):
    """
    (provided) Called for <return> key in lower search field.
    Calls babynames.search() and displays results in GUI.
    Gets search target from given search_entry, puts results
    in given search_out text area.
    """
    target = search_entry.get().strip()
    if target:
        # Call the search_names function in babynames.py
        result = search(names, target)
        out = ' '.join(result)
        search_out.delete('1.0', tkinter.END)
        search_out.insert('1.0', out)
