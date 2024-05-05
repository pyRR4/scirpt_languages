import functools

from functionalProgramming.make_generator import make_generator
from functionalProgramming.make_generator import fibonacci


def make_gen_memoized(f):
    @functools.cache
    def mem_function(func):
        return func

    return make_generator(mem_function)


mem_gen = make_gen_memoized(fibonacci)
print(mem_gen)

for i in range(10):
    print(next(mem_gen))

