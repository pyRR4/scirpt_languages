import sys


def print_list(list_to_print):
    for el in list_to_print:
        sys.stdout.write(str(el) + '\n')


def print_error(string):
    sys.stdout.write("Wystąpił błąd! " + string)

