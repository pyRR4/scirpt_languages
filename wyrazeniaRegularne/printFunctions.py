import sys


def print_error(error):
    sys.stdout.write("Wystapil blad! " + str(error) + '\n')


def print_prompt(text):
    sys.stdout.write(text)


def print_list(lst, new_lines=True):
    if new_lines:
        for entry in lst:
            sys.stdout.write(str(entry) + '\n')
    else:
        for entry in lst:
            sys.stdout.write(str(entry))


def print_dict(dictionary, is_list=True):
    for key, entry in dictionary.items():
        if is_list:
            sys.stdout.write(str(key) + '\n')
            for element in entry:
                sys.stdout.write('\t' + element)
            sys.stdout.write('\n' + "---------------------" + '\n')
        else:
            sys.stdout.write(str(key) + '\t' + str(entry) + '\n')


def log_to_str(log):
    date = str(log['timestamp'])
    sshd = log['sshd']
    msg = log['msg']

    return f'{date} - sshd[{sshd}] - {msg}'


def print_list_of_dict(lst):
    for el in lst:
        for key, val in el.items():
            sys.stdout.write(str(val) + " - ")
        sys.stdout.write('\n' + "---------------------" + '\n')


def print_times(times):
    for user, values in times.items():
        sys.stdout.write(user + " | avg: " + str(values[0]) + " | deviation: " + str(values[1]) + '\n')

