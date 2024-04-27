import reusable_functions
import sys


def print_line_with_code(code, source):
    for line in source:
        if reusable_functions.get_code(line) == code:
            sys.stdout.write(line)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stdout.write("Niepoprawna ilość argumentów")
    else:
        print_line_with_code(sys.argv[1], sys.stdin)
