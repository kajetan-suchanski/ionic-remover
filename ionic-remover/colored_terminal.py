import sys

RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
PINK = "\033[95m"
END_COLOR = "\033[0m"


def print_colored(color: str, *values: str):
    sys.stdout.write(color)
    print(*values, file=sys.stdout)
    sys.stdout.write(END_COLOR)


def print_red(*values: str):
    print_colored(RED, *values)


def print_green(*values: str):
    print_colored(GREEN, *values)


def print_blue(*values: str):
    print_colored(BLUE, *values)


def print_pink(*values: str):
    print_colored(PINK, *values)
