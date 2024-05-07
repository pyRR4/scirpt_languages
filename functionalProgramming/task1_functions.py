
def even_count(lst):
    filtered_lst = list(filter(lambda x: x % 2 == 0, lst))
    return len(filtered_lst)


def quicksort(lst):
    lst_len = len(lst)
    if lst_len <= 1:
        return lst

    pivot = lst[lst_len // 2]
    left_lst = [x for x in lst if x < pivot]
    right_lst = [x for x in lst if x > pivot]
    piv_lst = [x for x in lst if x == pivot]

    return quicksort(left_lst) + piv_lst + quicksort(right_lst)


def median(lst):
    sorted_lst = quicksort(lst)
    lst_len = len(lst)
    if lst_len % 2 == 0:
        return (sorted_lst[lst_len // 2] + sorted_lst[(lst_len // 2) - 1]) / 2
    else:
        return sorted_lst[lst_len // 2]


def newton_square_root(x, epsilon):
    def stop_condition(y):
        return (y >= 0) and (abs((y ** 2) - x) < epsilon)

    def new_y(y):
        return (y + (x / y)) / 2

    def iterate(y):
        return y if stop_condition(y) else iterate(new_y(y))

    return iterate(1.0)


def map_to_dict(x, split_str):
    x_in_str = [y for y in split_str if x in y]
    return x, x_in_str


def make_alpha_square(string):
    splitted_str = string.split(" ")
    alpha_chars = set(filter(lambda x: x.isalpha(), ''.join(splitted_str)))
    dct = dict(map(lambda x: map_to_dict(x, splitted_str), alpha_chars))

    return dct


def flatten(lst_of_lst):
    return lst_of_lst if len(lst_of_lst) == 0 \
        else (flatten(lst_of_lst[0]) + (flatten(lst_of_lst[1:])) if isinstance(lst_of_lst[0], list)
              else (flatten([flatten([a]) for a in lst_of_lst[0]]) + flatten(lst_of_lst[1:])
                    if isinstance(lst_of_lst[0], tuple) else [lst_of_lst[0]] + flatten(lst_of_lst[1:])))


eve_lst = [1, 2, 3, 4, 5]
print(f"even count for {eve_lst}")
print(even_count(eve_lst))
print('\n')

median_lst = [999, 3213, 3214, 320, 43]
print(f"median for {median_lst}")
print(median(median_lst))
print('\n')

x_arg = 3
epsilon_arg = 0.1
print(f"newton square root for x: {x_arg}, epsilon: {epsilon_arg}")
print(newton_square_root(x_arg, epsilon_arg))
print('\n')

alpha_sq_string = "siema sieniema"
print("make alpha square for \"" + alpha_sq_string + '\"')
print(str(make_alpha_square(alpha_sq_string)))
print('\n')

flatten_structure = [1, 2, [3, 4, [5, 6, [7, 8], 9], 10], (11, (12, 15), 13)]
print(f"flatten for structure: {flatten_structure}")
print(flatten(flatten_structure))
print('\n')

