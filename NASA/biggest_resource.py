import sys
import reusable_functions


def biggest_resource(source):
    biggest_res = 0
    path = ""
    for line in source:
        req_bytes = reusable_functions.get_bytes(line)
        if req_bytes > biggest_res:
            biggest_res = req_bytes
            path = reusable_functions.get_path(line)

    return f'Wielkosc najwiekszego zasobu w bajtach: {biggest_res} \tSciezka do tego zasobu: {path}'


if __name__ == '__main__':
    sys.stdout.write(biggest_resource(sys.stdin))
