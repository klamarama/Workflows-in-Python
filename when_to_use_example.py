class Result:
    def __init__(self, val, msg):
        self.val = val
        self.msg = msg


class Success(Result):
    def __init__(self, *args, **kwargs):
        super(Success, self).__init__(*args, **kwargs)


class Failure(Result):
    def __init__(self, *args, **kwargs):
        super(Failure, self).__init__(*args, **kwargs)


# similar to the identity function, it wraps the value passed in.
def unit(x):
    return Success(x, '')


def bind(x, f):
    if isinstance(x, Failure):
        return x
    y = f(x.val)
    print(y.msg)
    return y


def workflow(x, *fs):
    for f in fs:
        x = bind(x, f)
    return x
