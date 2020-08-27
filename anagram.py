"""
File: anagram.py
Name: Dennis Hsu
----------------------------------
This program recursively finds all the anagram(s)
for the word input by user and terminates when the
input string matches the EXIT constant defined
at line 19

If you correctly implement this program, you should see the
number of anagrams for each word listed below:
    * arm -> 3 anagrams
    * contains -> 5 anagrams
    * stop -> 6 anagrams
    * tesla -> 10 anagrams
    * spear -> 12 anagrams
"""

# Constants
FILE = 'dictionary.txt'  # This is the filename of an English dictionary
EXIT = '-1'  # Code to stop the loop
DATABASE = []  # Used to stored candidate words.
ALL_CHAR = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']  # All english alphabet.


def main():
    """
    Check if input is quit code.
    If not, then star load dictionary and search anagram.
    """
    while True:
        word = input('Welcome to stanCode "Anagram Generator" (or -1 to quit)\nFind anagrams for:')
        word = word.lower()
        if word == '-1':  # quit code
            return
        else:
            if read_dictionary(word):
                if word in DATABASE:
                    ans_list = []   # reset answer list when change input word.
                    find_anagrams(word, ans_list)
            else:
                print('This word not exists, pleas enter again.')


def read_dictionary(word):
    global DATABASE
    with open(FILE, 'r') as f:
        for line in f:
            word_data = line.strip()
            DATABASE.append(word_data)  # load file.

    if word in DATABASE:
        trim_dictionary(word)  # cut down searching range.
        return True
    else:
        return False


def trim_dictionary(word):
    global DATABASE
    print('read')
    char_list = []  # store character from destructed input word.
    word_len = len(word)

    for char in word:
        char_list.append(char)

    another_char = list(filter(lambda e: e not in char_list, ALL_CHAR))  # all character not inside boggle board.

    for char in another_char:
        DATABASE = list(filter(lambda e: char not in e, DATABASE))  # filter words which contain another_char.

    DATABASE = list(filter(lambda e: len(e) >= word_len, DATABASE))  # filter words shorter than input word units.


def find_anagrams(s, ans_list):
    """
    :param ans_list: (list) used to store anagram words.
    :param s: (string) resource word input from user.
    """
    find_anagrams_helper(s, '', ans_list)
    print(f'{len(ans_list)} anagram:', ans_list)


def find_anagrams_helper(s, sub_s, ans_list):
    """
    Do recursion until find all anagram words.
    :param s: (string) resource word input from user.
    :param sub_s: (string) sub_string of resource word.
    :param ans_list: (list) used to store anagram words.
    :return:
    """
    if len(s) == len(sub_s):  # base point.
        if sub_s in DATABASE:  # check answer.
            if sub_s not in ans_list:  # prevent from repeat answer.
                print('Found:', sub_s)
                print('Searching...')
                ans_list.append(sub_s)
        pass
    else:
        for char in s:
            if char in sub_s and sub_s.count(char) == s.count(char):  # avoid to use over times of any char.
                pass
            else:
                sub_s = sub_s + char   # combine next character as sub_string.
                if has_prefix(sub_s):  # check whether are words start with sub_s.
                    find_anagrams_helper(s, sub_s, ans_list)
                    sub_s = sub_s[0:len(sub_s) - 1]
                else:  # no word start with sub_s
                    sub_s = sub_s[0:len(sub_s) - 1]


def has_prefix(sub_s):
    """
    Test possibility of sub_s before doing recursion.
    :param sub_s: sub_string of input word from its head.
    :return: (boolean) whether word stars with sub_s.
    """
    for word in DATABASE:
        if word.startswith(sub_s):
            return True


if __name__ == '__main__':
    main()
