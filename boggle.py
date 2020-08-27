"""
File: boggle.py
Name: Dennis Hsu
----------------------------------------
This file recursively print words form input resource grid, witch default size by constant in line 8.
The program will firstly ask user fill grid by input character only.
Secondly, load dictionary file and decrease number data according to input grid.
Finally, start searching words.
"""

# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it
FILE = 'dictionary.txt'
EXIT_CODE = '-1'
INVALID_WORDS = '.,;!?#&-\'_+=/\\"@$^%()[]{}~234567890'  # if user type these words, it will be rejected.
DICTIONARY = []  # loading dictionary file inside this list.
DATABASE = {}  # save words from dictionary after trimming dictionary.
BOGGLE_ROW = 4  # number of row of boggle board.
BOGGLE_COL = 4  # number of column of boggle board.
ans_list = []  # save qualified words inside as answer.
MIN_STR_LENGTH = 4  # the word length accepted by answer list.

# list of all english charactors
ALL_CHAR = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']


CHAR_BOARD = []  # store user input inside this list as boggle board


class Graph:
    """
	This class represents a single character on the boggle board, and the attribute 'value' is what word
	exactly the character is, 'y', 'x' equals to the positoin of that word and 'n1 ~ n8' are the adjacent neighbors
	of the word. Those neighbors are stored in 'queue_neighbor' and their positions in 'nb_y_x'.
	"""

    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.value = CHAR_BOARD[y][x]
        if y == 0:
            if x - 1 < 0:  # top-left point
                self.n5 = CHAR_BOARD[y][x + 1]
                self.n7 = CHAR_BOARD[y + 1][x]
                self.n8 = CHAR_BOARD[y + 1][x + 1]
                self.queue_neighbor = [self.n5, self.n7, self.n8]
                self.nb_y_x = [(y, x + 1), (y + 1, x), (y + 1, x + 1)]

            elif x + 1 > 3:  # top-right point
                self.n4 = CHAR_BOARD[y][x - 1]
                self.n6 = CHAR_BOARD[y + 1][x - 1]
                self.n7 = CHAR_BOARD[y + 1][x]
                self.queue_neighbor = [self.n4, self.n6, self.n7]
                self.nb_y_x = [(y, x - 1), (y + 1, x - 1), (y + 1, x)]

            else:  # top edge
                self.n4 = CHAR_BOARD[y][x - 1]
                self.n5 = CHAR_BOARD[y][x + 1]
                self.n6 = CHAR_BOARD[y + 1][x - 1]
                self.n7 = CHAR_BOARD[y + 1][x]
                self.n8 = CHAR_BOARD[y + 1][x + 1]
                self.queue_neighbor = [self.n4, self.n5, self.n6, self.n7, self.n8]
                self.nb_y_x = [(y, x - 1), (y, x + 1), (y + 1, x - 1), (y + 1, x), (y + 1, x + 1)]

        elif y == 3:
            if x - 1 < 0:  # bottom-left point
                self.n2 = CHAR_BOARD[y - 1][x]
                self.n3 = CHAR_BOARD[y - 1][x + 1]
                self.n5 = CHAR_BOARD[y][x + 1]
                self.queue_neighbor = [self.n2, self.n3, self.n5]
                self.nb_y_x = [(y - 1, x), (y - 1, x + 1), (y, x + 1)]

            elif x + 1 > 3:  # bottom-right point
                self.n1 = CHAR_BOARD[y - 1][x - 1]
                self.n2 = CHAR_BOARD[y - 1][x]
                self.n4 = CHAR_BOARD[y][x - 1]
                self.queue_neighbor = [self.n1, self.n2, self.n4]
                self.nb_y_x = [(y - 1, x - 1), (y - 1, x), (y, x - 1)]

            else:  # bottom edge
                self.n1 = CHAR_BOARD[y - 1][x - 1]
                self.n2 = CHAR_BOARD[y - 1][x]
                self.n3 = CHAR_BOARD[y - 1][x + 1]
                self.n4 = CHAR_BOARD[y][x - 1]
                self.n5 = CHAR_BOARD[y][x + 1]
                self.queue_neighbor = [self.n1, self.n2, self.n3, self.n4, self.n5]
                self.nb_y_x = [(y - 1, x - 1), (y - 1, x), (y - 1, x + 1), (y, x - 1), (y, x + 1)]

        elif y - 1 >= 0 and y + 1 <= 3:
            if x - 1 < 0:  # left edge
                self.n2 = CHAR_BOARD[y - 1][x]
                self.n3 = CHAR_BOARD[y - 1][x + 1]
                self.n5 = CHAR_BOARD[y][x + 1]
                self.n7 = CHAR_BOARD[y + 1][x]
                self.n8 = CHAR_BOARD[y + 1][x + 1]
                self.queue_neighbor = [self.n2, self.n3, self.n5, self.n7, self.n8]
                self.nb_y_x = [(y - 1, x), (y - 1, x + 1), (y, x + 1), (y + 1, x), (y + 1, x + 1)]

            elif x + 1 > 3:  # right edge
                self.n1 = CHAR_BOARD[y - 1][x - 1]
                self.n2 = CHAR_BOARD[y - 1][x]
                self.n4 = CHAR_BOARD[y][x - 1]
                self.n6 = CHAR_BOARD[y + 1][x - 1]
                self.n7 = CHAR_BOARD[y + 1][x]
                self.queue_neighbor = [self.n1, self.n2, self.n4, self.n6, self.n7]
                self.nb_y_x = [(y - 1, x - 1), (y - 1, x), (y, x - 1), (y + 1, x - 1), (y + 1, x)]

            else:  # inner parts
                self.n1 = CHAR_BOARD[y - 1][x - 1]
                self.n2 = CHAR_BOARD[y - 1][x]
                self.n3 = CHAR_BOARD[y - 1][x + 1]
                self.n4 = CHAR_BOARD[y][x - 1]
                self.n5 = CHAR_BOARD[y][x + 1]
                self.n6 = CHAR_BOARD[y + 1][x - 1]
                self.n7 = CHAR_BOARD[y + 1][x]
                self.n8 = CHAR_BOARD[y + 1][x + 1]
                self.queue_neighbor = [self.n1, self.n2, self.n3, self.n4, self.n5, self.n6, self.n7, self.n8]
                self.nb_y_x = [(y - 1, x - 1), (y - 1, x), (y - 1, x + 1), (y, x - 1), (y, x + 1), (y + 1, x - 1),
                               (y + 1, x), (y + 1, x + 1)]


def main():
    """
	Main function requires user to input character to build boggle board.
	Only english character can be accepted, it will also be change to lowercase if uppercase one typed.
	Each character should be separate by space and should not be longer than one character unit.
	After boggle board established, main function will start to load dictionary and trim it.
	Dictionary will be trimmed according to words in boggle board.
	If a character do not appear on the boggle board, any word stars with the character will not be stored in database too.
	It will star boggle from top-left of boggle board after database established.
	"""

    for item in range(BOGGLE_ROW):
        word = input(f'{item + 1} row of letters:')
        word = word.lower().strip().split()  # insensitive, trim header and trailer of input and separate by space.

        if word == [EXIT_CODE]:  # quit code
            return

        for char in word:
            if char in INVALID_WORDS or char == '1':
                print('Illegal input')
                return

        word = [char for char in word if len(char) == 1]  # check words in row are legally

        if len(word) == BOGGLE_COL:  # check only 4 (in this case) words in one row
            CHAR_BOARD.append(word)
            pass

        else:
            print('Illegal input')
            return

    read_dictionary()  # star to import dictionary.

    for i in range(0, BOGGLE_ROW):  # star boggle from top-left of board.
        for j in range(0, BOGGLE_COL):
            boggling(Graph(i, j))

    print(f'There are {len(ans_list)} words in total.')


def boggling(graph):
    """
    This function chose sub dictionary as database and pass to helper function with node.
    graph: node on the boggle board, input by user.
    """
    global DATABASE
    sub_database = DATABASE[graph.value]
    boggle_helper(graph, graph.value, sub_database)


def boggle_helper(graph, sub_s, sub_database):
    """
    This is a recursive function aim to find words longer than 4 units, exist in database and can spell by character
    on the boggle board.
    :param graph: node on the boggle board, input by user.
    :param sub_s: string consist of node value and grow incrementally with its neighbors.
    :param sub_database: some words from database only start with same character.
    """
    if sub_s in sub_database:
        print('Found "', sub_s, '"')
        ans_list.append(sub_s)  # find answer

        for char in graph.queue_neighbor:  # keep searching recursion after find answer
            sub_s = sub_s + char
            if has_prefix(sub_s, graph, sub_database):
                index = graph.queue_neighbor.index(char)
                boggle_helper(Graph(graph.nb_y_x[index][0], graph.nb_y_x[index][1]), sub_s, sub_database)
                sub_s = sub_s[0:len(sub_s) - 1]

    else:
        for char in graph.queue_neighbor:
            sub_s = sub_s + char  # extent string with its neighbor.

            if has_prefix(sub_s, graph, sub_database):  # if there is any word star with sub_s.
                index = graph.queue_neighbor.index(char)  # if there are repeat neighbor, index() only give first index.
                graph.queue_neighbor[index] = None  # changing searched neighbor to None to avoid that situation.

                # using neighbor as parameter to boggle_helper function
                boggle_helper(Graph(graph.nb_y_x[index][0], graph.nb_y_x[index][1]), sub_s, sub_database)
                sub_s = sub_s[0:-1]  # trim last character to add another neighbor.
            else:  # if there is no word star with sub_s.
                sub_s = sub_s[0:-1]  # trim last character to add another neighbor.


def read_dictionary():
    """
	This function reads file "dictionary.txt" stored in FILE variable,
	and appends words in each line into a Python list.
	"""
    with open(FILE, 'r') as f:
        for line in f:
            word_data = line.strip()
            DICTIONARY.append(word_data)

    trim_dictionary(DICTIONARY)


def trim_dictionary(dictionary):
    """
    This function will remove words made up by character that do not inside boggle board,
    and build a dict using character as key and words starts with that character as value.
    dictionary: all the data from outside file.
    """
    global DATABASE
    for row in CHAR_BOARD:
        for char in row:
            DATABASE[char] = []  # create diction using character as key.

    char_list = list(DATABASE.keys())
    another_char = list(filter(lambda e: e not in char_list, ALL_CHAR))  # all character not inside boggle board.

    for char in another_char:
        dictionary = list(filter(lambda e: char not in e, dictionary))  # filter words which contain another_char.

    dictionary = list(filter(lambda e: len(e) >= MIN_STR_LENGTH, dictionary))  # filter words shorter than 4 units.

    for char in char_list:
        DATABASE[char] = list(filter(lambda e: e.startswith(char), dictionary))  # import data to database


def has_prefix(sub_s, graph, sub_database):
    """
	sub_database: database of specific character.
	param graph: node on google board.
	sub_s: (str) A substring that is constructed by neighboring letters on a 4x4 square grid.
	return: (bool) If there is any words with prefix stored in sub_s.
	"""

    if sub_s in ans_list:  # pass process for repeat words
        return False

    if len(sub_s) >= 3:  # fix backing searches to same character.
        if sub_s[-1] is sub_s[-3]:
            if graph.queue_neighbor.count(sub_s[-1]) >= 2:  # if there is neighbor with same value, it's valid.
                for word in sub_database:
                    if word.startswith(sub_s):
                        return True
            return False

    for word in sub_database:
        if word.startswith(sub_s):  # keep searching next character or find answer.
            return True


if __name__ == '__main__':
    main()
