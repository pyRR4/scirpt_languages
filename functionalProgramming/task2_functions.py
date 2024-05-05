

def forall(pred, iterable):
    for item in iterable:
        if not pred(item):
            return False

    return True


def exists(pred, iterable):
    for item in iterable:
        if pred(item):
            return True

    return False


def atleast(n, pred, iterable):
    count = 0
    for item in iterable:
        if pred(item):
            count += 1

    if count >= n:
        return True
    else:
        return False


def atmost(n, pred, iterable):
    count = 0
    for item in iterable:
        if pred(item):
            count += 1

    if count <= n:
        return True
    else:
        return False


lst = [x for x in range(1, 20)]

print(atmost(9, lambda x: x <= 10, lst))
print(atleast(11, lambda x: x <= 10, lst))
print(exists(lambda x: x <= 0, lst))
print(forall(lambda x: x <= 10, lst))