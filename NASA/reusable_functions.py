def get_bytes(line):
    index = (line.rindex(" "))
    bytes = line[index + 1: len(line) - 1: 1]
    if bytes == "-":
        return 0
    else:
        return int(bytes)


def get_path(line):
    start_index = line.index("\"")
    end_index = line.rindex("\"")
    substring = line[start_index: end_index]
    if "/" in substring:
        substring_start = substring.index("/")
        if " " in substring and substring.rindex(" ") > substring_start:
            substring_end = substring.rindex(" ")
        else:
            substring_end = len(substring) - 1
    else:
        return ""

    return substring[substring_start: substring_end]


def get_extension(line):
    path = get_path(line)
    if "." in path:
        dot_index = path.rindex(".")
    else:
        return ""

    return path[dot_index + 1:]


def get_code(line):
    index = (line.rindex(" "))

    return line[index - 3: index: 1]


def get_date(line):
    substring = line[line.index("[") + 1:line.rindex("]") - 1]  # DD/MM/YYYY:HH:MM:SS ?????

    return substring


def get_hour(line):
    substring = get_date(line)
    index = substring.index(":")
    hour = substring[index + 1: index + 3]

    return int(hour)


def get_day(line):
    substring = get_date(line)
    day = substring[0:substring.index("/")]

    return day


def get_domain(line):
    index = line.index("- -")
    substring = line[0:index - 1]
    if not substring.__contains__("."):
        return ""

    domain = substring[substring.rindex(".") + 1: len(substring)]

    return domain


#get_domain("c44.globalvision - - [08/Jul/1995:16:42:51 -0400] \"GET /history/apollo/images/footprint-small.gif HTTP/1.0\" 200 18149")