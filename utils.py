from random import randint, choice, choices


def get_rand_in_range(min, max):
    return randint(min, max)


def get_rand_items_from_list(items, n=1):

    n = max(n, 0)
    if n == 0:
        return []
    elif n >= len(items):
        return items

    selected = []
    for i in range(0, n):
        c = choice(items)
        selected.append(c)

    return selected


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


def get_transition_for_element(current_state, transition_matrix):
    population = list(transition_matrix.keys())
    weights = list(transition_matrix.values())
    population.append(current_state)
    weights.append(1 - sum(weights))
    return choices(population=population, weights=weights)[0]
