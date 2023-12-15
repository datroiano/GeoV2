def closest_number(numbers_set, target):
    closest = None
    min_difference = float('inf')

    for number in numbers_set:
        difference = abs(number - target)
        if difference < min_difference:
            min_difference = difference
            closest = number

    return closest
