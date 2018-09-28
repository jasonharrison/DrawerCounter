#!/usr/bin/env python3

import locale
from prettytable import PrettyTable


locale.setlocale(locale.LC_ALL, 'en_US')


DENOMINATIONS = {
    "hundreds": 10000,
    "fifties": 5000,
    "twenties": 2000,
    "tens": 1000,
    "fives": 500,
    "twos": 200,
    "ones": 100,
    "quarters": 25,
    "dimes": 10,
    "nickels": 5,
    "pennies": 1,
    "other": 1
}

ORDER = [
    'hundreds',
    'fifties',
    'twenties',
    'tens',
    'fives',
    'twos',
    'ones',
    'quarters',
    'dimes',
    'nickels',
    'pennies',
    'other'
]

NUMERICS = {
    'hundreds': '$100',
    'fifties': '$50',
    'twenties': '$20',
    'tens': '$10',
    'fives': '$5',
    'twos': '$2',
    'ones': '$1',
    'quarters': '25c',
    'dimes': '10c',
    'nickels': '5c',
    'pennies': '1c',
    'other': 'other'
}


def is_number(s):
    """Determines whether a string can be converted into a number.

    :param s: The string to be checked
    :type s: str
    :return: If the string can be represented as an integer, True; else, False.
    :rtype: bool
    """
    try:
        int(s)
        return True
    except ValueError:
        return False


def get_input(prompt):
    """Obtains input from the console, then converts the input to an int.
    Returns 0 if the user's input is negative, empty, or not an integer.

    :param prompt: The prompt to display to the user
    :type prompt: str
    :return: User's input as an integer.  If the input is invalid, 0.
    :rtype: int
    """
    user_input = input(prompt)
    if not is_number(user_input):
        return 0
    user_input_as_int = int(user_input)
    if user_input_as_int < 0:
        return 0
    return user_input_as_int


def humanize(pennies):
    """Converts from pennies to human-readable dollars/cents.

    :param pennies: Pennies
    :type pennies: int
    :return: Human readable dollars/cents (e.g. $1,234.56)
    :rtype: str
    """
    dollars = pennies / 100
    return locale.currency(dollars, grouping=True)


class Drawer:
    def __init__(self, **kwargs):
        self.denominations = {}
        data = {}
        if "input" in kwargs:
            for k in ORDER:
                data[k] = get_input(NUMERICS[k] + " x :") * DENOMINATIONS[k]
        for k, v in data.items():
            cents = int(v)
            if k not in DENOMINATIONS:
                raise ValueError("Unknown denomination: %s" % k)
            if not isinstance(v, int):
                raise ValueError("%s is not type int" % k)
            self.denominations[k] = cents

    def display(self):
        table = PrettyTable(["Denomination", "Count", "Value"])
        table.align['Denomination'] = 'l'
        table.align['Count'] = 'c'
        table.align["Value"] = 'r'
        total = 0
        for k in ORDER:
            cents = self.denominations[k]
            count = int(cents / DENOMINATIONS[k])
            table.add_row([NUMERICS[k], count, humanize(cents)])
            total += cents
        table.add_row(["TOTAL", "", humanize(total)])
        return table


if __name__ == "__main__":
    d = Drawer(input=True)
    print(d.display())
