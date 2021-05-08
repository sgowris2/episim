from random import randint, choice


def get_rand_in_range(min, max):
    return randint(min, max)


def pop_rand_items_from_list(items, n=1):

    n = max(n, 0)
    if n == 0:
        return [], items
    elif n >= len(items):
        return items, []

    selected = []
    for i in range(0, n):
        c = choice(items)
        selected.append(c)
        items.remove(c)

    return selected, items
