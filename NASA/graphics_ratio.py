import sys
import reusable_functions


def graphics_ratio(source):
    graphics_bytes = 0
    other_bytes = 0
    for line in source:
        req_bytes = reusable_functions.get_bytes(line)
        extension = reusable_functions.get_extension(line)

        if extension in ("gif", "jpg", "jpeg", "xbm"):
            graphics_bytes += req_bytes
        else:
            other_bytes += req_bytes

    return f'Stosunek pobran grafiki do pobran pozostalych zasobow: {graphics_bytes / other_bytes}'


if __name__ == '__main__':
    sys.stdout.write(graphics_ratio(sys.stdin))
