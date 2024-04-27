import sys
import reusable_functions


def print_by_domain(domain, source):
    for line in source:
        if reusable_functions.get_domain(line) == domain:
            sys.stdout.write(line)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stdout.write("Niepoprawna ilość argumentów")
    else:
        print_by_domain(sys.argv[1], sys.stdin)