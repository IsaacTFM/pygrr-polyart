"""
This small module has an optimised way of calling math functions.
"""

# import functools cache decorator
from functools import lru_cache


# decorate the function to ensure it caches output
@lru_cache(maxsize=None)
def cached_pow(number: float, power: float) -> float:
    """
    Raises number to power.
    Caches the previous results so that if a same set of
    arguments is passed, it will fetch from the cache.
    """
    return pow(number, power)


# decorate the function to ensure it caches output
@lru_cache(maxsize=None)
def cached_square(number: float) -> float:
    """
    Squares the number.
    Caches the previous results so that if a same set of
    arguments is passed, it will fetch from the cache.
    """
    return number * number


# decorate the function to ensure it caches output
@lru_cache(maxsize=None)
def cached_squareroot(number: float) -> float:
    """
    Square roots the number.
    Caches the previous results so that if a same set of
    arguments is passed, it will fetch from the cache.
    """
    return pow(number, 0.5)


# decorate the function to ensure it caches output
@lru_cache(maxsize=None)
def cached_hypot(a: float, b: float) -> float:
    """
    Calculates the hypotenuse (c) of the sides a and b.
    Caches the previous results so that if a same set of
    arguments is passed, it will fetch from the cache.
    """
    return cached_squareroot(cached_square(a) + cached_square(b))
