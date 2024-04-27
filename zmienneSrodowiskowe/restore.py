import csv
import os
import shutil
import sys

import printFunctions


def get_backups():
    if "BACKUPS_DIR" not in os.environ:
        printFunctions.print_error("Nie mozna znalezc folderu z kopiami zapasowymi")
        return
    else:
        directory = os.environ["BACKUPS_DIR"]

    history = history = os.path.join(directory, "backup_history.csv")
    with open(history, "r", newline='') as csv_file:
        backups_list = list(csv.reader(csv_file))

    if len(backups_list) == 0:
        printFunctions.print_error("Brak kopii zapasowych")
        sys.exit(1)

    str_list = []
    for i in range(len(backups_list)):
        elem = f"{i + 1}. {backups_list[i][0]} : {backups_list[i][1]}"
        str_list.append(elem)

    return str_list


def restore(backup_num, path):
    if "BACKUPS_DIR" not in os.environ:
        return
    else:
        directory = os.environ["BACKUPS_DIR"]
    history = os.path.join(directory, "backup_history.csv")

    with open(history, "r", newline='') as csv_file:
        backups_list = list(csv.reader(csv_file))

    if 0 < backup_num <= len(backups_list):
        backup = backups_list[backup_num - 1]
        compressed_file = os.path.join(directory, backup[2])

        try:
            shutil.unpack_archive(compressed_file, path)
        except:
            printFunctions.print_error("Nie udalo sie przywrocic kopii zapasowej.")
    else:
        printFunctions.print_error("Niepoprawny numer kopii.")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        path = os.getcwd()
    elif len(sys.argv) == 2:
        path = sys.argv[1]
    else:
        printFunctions.print_error("Niepoprawna liczba argumentow.")
        sys.exit(2)

    printFunctions.print_list(get_backups(), True)
    try:
        index = int(input("Wybierz numer kopii z podanych powyzej: \n"))
        restore(index, path)
    except ValueError:
        printFunctions.print_error("Niepoprawna wartosc, sprobuj ponownie")
