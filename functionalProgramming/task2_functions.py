

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
n = 10
print(f"lst: {lst},\nn: {n}")

print("atmost in lst for x <= n")
print(atmost(9, lambda x: x <= n, lst))
print("atleast in lst for x <= n")
print(atleast(11, lambda x: x <= n, lst))
print("exists in lst for x <= n")
print(exists(lambda x: x <= n, lst))
print("forall in lst for x <= n")
print(forall(lambda x: x <= n, lst))
