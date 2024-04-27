import reusable_functions
import sys


def amount_with_code(code, source):
    counter = 0
    for line in source:
        tmpcode = reusable_functions.get_code(line)
        if tmpcode == str(code):
            counter += 1

    return f'Ilosc wystapien zadan z kodem {code}: {counter}'


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stdout.write("Niepoprawna ilość argumentów")
    else:
        sys.stdout.write(amount_with_code(sys.argv[1], sys.stdin))
