import csv
import datetime
import os.path
import shutil
import sys

import printFunctions


def backup(path):
    if os.path.isdir(path):
        if "BACKUPS_DIR" not in os.environ:
            directory = os.getenv("BACKUPS_DIR", os.path.join(os.path.expanduser("~"), ".backups"))
        else:
            directory = os.environ["BACKUPS_DIR"]
        timestamp = datetime.datetime.now().strftime("%Y.%m.%d%H.%M.%S")
        dirname = os.path.basename(path)

        name = f"{timestamp}--{dirname}.zip"

        try:
            path_zip = shutil.make_archive(os.path.join(directory, name[:len(name) - 4]), "zip", path)
        except:
            printFunctions.print_error("Kompresja katalogu nie powiodła się.")
            return

        if not os.path.isdir(directory):
            os.mkdir(directory)

        shutil.move(path_zip, os.path.join(directory, name))

        with open(os.path.join(directory, "backup_history.csv"), "a", newline='') as csv_file:
            csv.writer(csv_file).writerow([timestamp, path, name])

        shutil.rmtree(path)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        backup(sys.argv[1])
    else:
        printFunctions.print_error("Niepoprawna liczba argumentow!")

