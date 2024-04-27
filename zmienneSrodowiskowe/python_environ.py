import sys
import os

import printFunctions


def get_environmentals(filters=None):
    if filters is None:
        filters = []
    if len(filters) == 0:
        variables = sorted(os.environ)
    else:
        variables = {}
        for filt in filters:
            if isinstance(filt, str):
                for key, val in os.environ.items():
                    if filt in key:
                        variables[key] = val
        variables = dict(sorted(variables.items()))

    return variables


if __name__ == "__main__":
    if len(sys.argv) == 1:
        printFunctions.print_list(get_environmentals())
    else:
        printFunctions.print_dict(get_environmentals(sys.argv[1::]), False)
