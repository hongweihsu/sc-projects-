"""
File: largest_digit.py
Name: Dennis Hsu
----------------------------------
This file recursively prints the biggest digit in
5 different integers, 12345, 281, 6, -111, -9453
If your implementation is correct, you should see
5, 8, 6, 1, 9 on Console.
"""


def main():
    print(find_largest_digit(12345))  # 5
    print(find_largest_digit(281))  # 8
    print(find_largest_digit(6))  # 6
    print(find_largest_digit(-111))  # 1
    print(find_largest_digit(-9453))  # 9


def find_largest_digit(n):
    """
    Do recursion to find max integer.
	n: (int) input number.
	return: max number in input number.
	"""
    n = str(n)
    if len(n) == 1:  # base point
        return n
    else:
        if n[0] <= n[1]:  # if head number is smaller than next number, trimming header.
            return find_largest_digit(n[1:])
        else:
            n = n[0] + n[2:]  # if header greater than next number, trimming next number.
            return find_largest_digit(n)


if __name__ == '__main__':
    main()
