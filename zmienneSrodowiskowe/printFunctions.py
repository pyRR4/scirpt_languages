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

