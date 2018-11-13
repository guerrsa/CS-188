#!/usr/bin/env python3

nums = [1, 2, 3, 4, 5, 6]
plusOneNums = [x+1 for x in nums]
print(plusOneNums)
oddNums = [x for x in nums if x % 2 != 0]
print(oddNums)
oddNumsPlusOne = [x + 1 for x in nums if x % 2 == 1]
print(oddNumsPlusOne)


strings = ['hola', 'adios', 'eqweqweqweqweqwe', 'bye']
lowerString = [x.lower() for x in strings if len(x) < 5]
print(lowerString)