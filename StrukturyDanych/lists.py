from datetime import datetime
import sys

from StrukturyDanych import printFunctions


def read_log(source):
    logs = []
    for line in source:
        tab = line.split()
        try:
            domain = tab[0]
            date = datetime.strptime((tab[3])[1::], "%d/%b/%Y:%H:%M:%S")
            timezone = (tab[4])[0:len(tab[4]) - 1]
            operation_type = (tab[5])[1::]
            path = tab[6]
            http = tab[7][0:len(tab[7]) - 1]
            code = int(tab[8])
            file_size = int(tab[9])

            tupled_line = (domain, date, operation_type, path, http, code, file_size, timezone, line)
            logs.append(tupled_line)

        except ValueError:
            pass

        except IndexError:
            pass

    return logs


def sort_log(log, key):
    if not key < len(log):
        return [""]
    sorted_lista = sorted(log, key=lambda x: x[key - 1])
    return sorted_lista


def get_entries_by_addr(logs, domain):
    logs_with_domain = []
    for log in logs:
        if log[0] == domain:
            logs_with_domain.append(log)

    return logs_with_domain


def get_failed_reads(logs, is_single_list=True):
    logs_code_500 = []
    logs_code_400 = []
    for log in logs:
        if log[5] // 100 == 5:
            logs_code_500.append(log)
        elif log[5] // 100 == 4:
            logs_code_400.append(log)

    if is_single_list:
        return logs_code_400 + logs_code_500
    else:
        return logs_code_400, logs_code_500


def get_entries_by_extension(logs, extension):
    extension_logs = []
    for log in logs:
        path = log[3]
        if "." in path:
            dot_index = path.rindex(".")
            if path[dot_index:] == extension:
                extension_logs.append(log)

    return extension_logs


def print_entries(logs, n):
    if 0 < n:
        if not n < len(logs):
            n = len(logs)
        first_n = logs[:n]
        printFunctions.print_list(first_n)
    else:
        printFunctions.print_error("Niepoprawny argument")


if __name__ == '__main__':
    # #read_log
    # if len(sys.argv) == 1:
    #     print_entries(read_log(sys.stdin), 10)
    # else:
    #     printFunctions.print_error("Niepoprawna liczba argumentów!")

    # #sort_log
    # if len(sys.argv) == 2:
    #     try:
    #         arg = int(sys.argv[1])
    #         print_entries(sort_log(read_log(sys.stdin), arg), 10)
    #     except ValueError:
    #         printFunctions.print_error("Niepoprawny typ argumentów!")
    # else:
    #     printFunctions.print_error("Niepoprawna liczba argumentów!")

    # #entries_by_addr
    # if len(sys.argv) == 2:
    #     arg = sys.argv[1]
    #     print_entries(get_entries_by_addr(read_log(sys.stdin), arg), 10)
    # else:
    #     printFunctions.print_error("Niepoprawna liczba argumentów!")
    #
    # #failed_reads
    # if len(sys.argv) == 2:
    #     if sys.argv[1].lower() in ["true", "false"]:
    #         arg = True if sys.argv[1].lower() == "true" else False
    #         reads = get_failed_reads(read_log(sys.stdin), arg)
    #         if arg:
    #             print_entries(reads, 10)
    #         else:
    #             print_entries(reads[0], 5)
    #             print_entries(reads[1], 5)
    #
    #     else:
    #         printFunctions.print_error("Niepoprawny typ argumentów!")
    # else:
    #     printFunctions.print_error("Niepoprawna liczba argumentów!")
    #
    # #entries_by_extension
    if len(sys.argv) == 2:
        arg = sys.argv[1]
        print_entries(get_entries_by_extension(read_log(sys.stdin), arg), 10)
    else:
        printFunctions.print_error("Niepoprawna liczba argumentów!")


