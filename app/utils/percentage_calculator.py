def calculate_percentage_difference(declared, actual):
    if actual == 0:
        return 0

    difference = abs(declared - actual)

    return round((difference / actual) * 100, 2)