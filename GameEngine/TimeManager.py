from time import time


def Speed(function):
    """Speed of function in milliseconds"""

    wide_static = False

    def test(*args, **kwargs):

        k = 100000

        t1 = time()

        for i in range(k):
            function(*args, **kwargs)

        t2 = time()
        speed = (t2 - t1) / k * 1000
        if wide_static:
            print("Results:")
            print(1000 / speed, "times this function can be finished per second")
            print(speed, "ms per call")
        return speed

    return test()