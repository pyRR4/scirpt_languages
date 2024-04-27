import os
import sys

import printFunctions


DEFAULT = ""
EXEC = "--executables"
EXEC_SHORT = "-e"


def get_executables(directory):
    executables = []
    iterator = os.scandir(directory)
    for entry in iterator:
        if entry.name.endswith(".exe") or entry.name.endswith(".com"):
            executables.append(entry.name)

    return executables


def validate_flag(flag):
    if flag == EXEC_SHORT or flag == EXEC:
        return True
    elif flag == "":
        return False
    else:
        return "Niezdefiniowana flaga, używam wartości domyślnej"


def get_dict(source):
    files = {}
    for path in source:
        try:
            files[path] = get_executables(path)
        except FileNotFoundError:
            printFunctions.print_error("Nie odnaleziono ścieżki.")

    return files


if __name__ == "__main__":
    paths = os.environ['PATH'].split(os.pathsep)

    if len(sys.argv) == 1:
        printFunctions.print_list(paths)
    elif len(sys.argv) == 2:
        validated_flag = validate_flag(sys.argv[1])
        if isinstance(validated_flag, str):
            printFunctions.print_error(validated_flag)
            printFunctions.print_list(paths)
        elif not validated_flag:
            printFunctions.print_list(paths)
        else:
            printFunctions.print_dict(get_dict(paths))
    else:
        printFunctions.print_error("Niepoprawna liczba argumentow!")

