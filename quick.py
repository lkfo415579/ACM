t = [10, 80, 30, 90, 40, 50, 70]


def partition(l, low, high):
    i = low - 1
    pi = l[high]
    for j in range(low, high):
        if l[j] <= pi:
            i += 1
            l[j], l[i] = l[i], l[j]
    l[high], l[i + 1] = l[i + 1], l[high]
    return i + 1


def quicksort(l, low, high):
    if low < high:
        pi = partition(l, low, high)
        # left
        quicksort(l, low, pi - 1)
        # right
        quicksort(l, pi + 1, high)


quicksort(t, 0, len(t) - 1)

print t