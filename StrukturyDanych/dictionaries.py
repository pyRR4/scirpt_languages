import sys
import helpFunctions
import lists
import printFunctions


def entry_to_dict(log):
    dict_log = {
        "domain": log[0],
        "date": log[1],
        "operation_type": log[2],
        "path": log[3],
        "http": log[4],
        "code": log[5],
        "file_size": log[6]
    }

    return dict_log


def log_to_dict(logs):
    logs_dict = dict()
    for log in logs:
        key = log[0]
        if key in logs_dict:
            logs_dict[key].append(entry_to_dict(log))
        else:
            logs_dict[key] = [entry_to_dict(log)]

    return logs_dict


def get_addrs(logs_dict):
    key_list = list(logs_dict.keys())

    return key_list


def print_dict_entry_dates(logs_dict):
    code = 200
    logs_to_string = helpFunctions.domain_to_string(logs_dict, code)
    n = 10  # how many to print, just for testing
    lists.print_entries(logs_to_string, n)


if __name__ == '__main__':
    #get_addrs
    if len(sys.argv) == 1:
        lists.print_entries(get_addrs(log_to_dict(lists.read_log(sys.stdin))), 10)
    else:
        printFunctions.print_error("Niepoprawna liczba argumentów!")

    #dict_entry_dates
    if len(sys.argv) == 1:
        print_dict_entry_dates(log_to_dict(lists.read_log(sys.stdin)))
    else:
        printFunctions.print_error("Niepoprawna liczba argumentów!")

