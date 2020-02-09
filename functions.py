import random


# function: an operation that takes some data, returns data.
# (this function is known as the identity function, and it is a pure function)
def function(x):
    return x


# pure function: same input yields the same output every time, with no side effects.
def function(x):
    return x + 1


# impure function: side effects make output unpredictable and untestable.
def impure_function(x):
    # read val from a file that other running apps can mutate
    # ...or just do this. this is unpredictable.
    return random.randint(x, x + 10)


# takes something, returns boolean
def predicate(x):
    return x % 2 == 0


# takes nothing, returns something
def supplier():
    return "it doesn't have to be a string"


# takes something, returns nothing
def consumer(x):
    # do something significant here
    print(x)
    return


# functions can accept and return:
# nothing
# values: number, text
# objects
# homogeneous sets: array, list, sequence, collection, etc.
# heterogeneous sets: tuple or struct
# ...
# and if you're lucky: functions


# takes two integers, returns their sum
def add_two_ints(x, y):
    return x + y


# takes one integer, returns a _function_ that takes an integer and adds it to the one passed into the original function
def build_adder(x):
    def adder(y):
        return x + y
    return adder


# same as above, but more idiomatic to functional programming style
def build_idiomatic_adder(x):
    return lambda y: x + y


# function that takes a function and value
def process(f, x):
    return f(*x)
