import sys
import reusable_functions


def print_by_date(date, source):
    for line in source:
        if reusable_functions.get_day(line) == date:
            sys.stdout.write(line)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stdout.write("Niepoprawna ilość argumentów")
    elif len(sys.argv[1]) != 2:
        sys.stdout.write("Podaj dzien w formacie: \"DD\"")
    else:
        print_by_date(sys.argv[1], sys.stdin)




