import sys


def reader():
    for line in sys.stdin:
        sys.stdout.write(line)


if __name__ == '__main__':
    reader()
