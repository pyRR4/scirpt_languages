def make_generator(f):
    def generator():
        n = 1
        while True:
            yield f(n)
            n += 1

    return generator()


def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)


gen1 = make_generator(fibonacci)
gen2 = make_generator(lambda n: 2 ** n)
gen3 = make_generator(lambda n: 2 * n + 15)

print("----------Fibonacci: -------------")
for i in range(10):
    print(next(gen1))

print("----------Geometric: -------------")
for j in range(10):
    print(next(gen2))

print("----------Arithmetic: -------------")
for k in range(10):
    print(next(gen3))

