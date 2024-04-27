
import os.path
import sys

import printFunctions

FOLLOW = "--follow"
BYTES = "--bytes="
LINES = "--lines="


def strip_values(flag):
    stripped_n = flag[flag.index("=") + 1::]
    try:
        value = int(stripped_n)
    except ValueError:
        value = -1

    if value < 0:
        value = "Niepoprawna ilosc linii/bajtow!"

    return value


def validate_flags(flags):
    # [LINES, BYTES, FOLLOW, NUM_OF_LINES/BYTES/ERROR INDICATOR, SOURCE]
    validated_flags = [False, False, False, 10, None]
    for flag in flags:
        if os.path.isfile(flag):
            validated_flags[4] = flag
        elif flag.startswith(LINES):
            validated_flags[0] = True
            validated_flags[3] = strip_values(flag)
        elif flag.startswith(BYTES):
            validated_flags[1] = True
            validated_flags[3] = strip_values(flag)
        elif flag == FOLLOW:
            validated_flags[2] = True
        else:
            validated_flags[3] = "Niepoprawna flaga lub sciezka do pliku!"

        if isinstance(validated_flags[3], str):
            break

    if validated_flags[0] and validated_flags[1]:
        validated_flags[3] = "Nie mozna czytac bajtow i linii jednoczesnie!"
    elif not validated_flags[0] and not validated_flags[1]:
        validated_flags[0] = True

    return validated_flags


def read_bytes(source, num_bytes):
    source.seek(0, 2)
    file_size = source.tell()
    bytes_to_read = min(file_size, num_bytes)
    source.seek(-bytes_to_read, 2)
    data = source.read(num_bytes)
    return data


def tail(flags):
    validated_flags = validate_flags(flags[1:])
    if not isinstance(validated_flags[3], str):
        if not validated_flags[4] is None:
            if validated_flags[0]:
                file = open(validated_flags[4], 'r', encoding='utf8')
                lines = file.readlines()
                lines_to_read = min(len(lines), validated_flags[3])
                printFunctions.print_list(lines[len(lines) - lines_to_read::], False)

            elif validated_flags[1]:
                file = open(validated_flags[4], 'rb')
                data = read_bytes(file, validated_flags[3])
                printFunctions.print_list([data])
        else:
            if validated_flags[0]:
                try:
                    lines = sys.stdin.readlines()[-validated_flags[3]::]
                    printFunctions.print_list(lines, False)
                except FileNotFoundError:
                    printFunctions.print_error("Nie znaleziono pliku.")
            elif validated_flags[1]:
                try:
                    data = read_bytes(sys.stdin.buffer, validated_flags[3])
                    printFunctions.print_list([data])
                except FileNotFoundError:
                    printFunctions.print_error("Nie znaleziono pliku")

        if validated_flags[2]:
            if not validated_flags[4] is None:
                if validated_flags[0]:
                    file = open(validated_flags[4], 'r', encoding='utf8')
                    while True:
                        lines = file.readlines()
                        lines_to_read = min(len(lines), validated_flags[3])
                        printFunctions.print_list(lines[len(lines) - lines_to_read::], False)

                elif validated_flags[1]:
                    file = open(validated_flags[4], 'rb')
                    while True:
                        data = read_bytes(file, validated_flags[3])
                        printFunctions.print_list([data])
            else:
                if validated_flags[0]:
                    while True:
                        try:
                            lines = sys.stdin.readlines()[-validated_flags[3]::]
                            printFunctions.print_list(lines, False)
                        except FileNotFoundError:
                            printFunctions.print_error("Nie znaleziono pliku.")
                elif validated_flags[1]:
                    while True:
                        try:
                            data = read_bytes(sys.stdin.buffer, validated_flags[3])
                            printFunctions.print_list([data])
                        except FileNotFoundError:
                            printFunctions.print_error("Nie znaleziono pliku")

    else:
        printFunctions.print_error(validated_flags[3])


if __name__ == "__main__":
    tail(sys.argv)
