#!/usr/bin/env python3

def quickSort(lst):
    if len(lst) <= 1:
        return lst
    smaller = [x for x in lst[1:] if x < lst[0]]
    larger = [x for x in lst[1:] if x >= lst[0]]
    return quickSort(smaller) + [lst[0]] + quickSort(larger)


# Main Function
if __name__ == '__main__':
    lst = [3, 4, 5, 2, 6, 1]
    print(quickSort(lst))
