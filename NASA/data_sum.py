import reusable_functions
import sys


def bytes_sum(source):
    bytes_count = 0
    for line in source:
        req_bytes = reusable_functions.get_bytes(line)
        bytes_count += int(req_bytes)

    return f'Ilosc gigabajtow danych przeslanych do hostow: {bytes_count * (10 ** -9)}'


if __name__ == '__main__':
    sys.stdout.write(bytes_sum(sys.stdin))
