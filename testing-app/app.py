def addition(x, y) -> int | float:
    return x + y


def divide(x, y):
      if y == 0:
        raise ValueError("Cannot divide by zero must be a nonzero number")

    return x / y
