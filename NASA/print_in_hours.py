import reusable_functions
import sys


def print_in_hours(start_hour, end_hour, source):
    end_h = int(end_hour)
    start_h = int(start_hour)
    for line in source:
        hour = reusable_functions.get_hour(line)
        if end_h <= start_h:
            if end_h > hour or hour >= start_h:
                sys.stdout.write(line)
        else:
            if end_h > hour >= start_h:
                sys.stdout.write(line)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stdout.write("Niepoprawna ilość argumentów")
    else:
        print_in_hours(sys.argv[1], sys.argv[2], sys.stdin)
