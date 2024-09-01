import sys


class Interval:
    def __init__(self, start=float("+inf"), end=float("-inf")):
        self.start = start
        self.end = end

    def __contains__(self, n):
        return self.start <= n <= self.end

    def surrounds(self, n):
        return self.start < n < self.end

    @classmethod
    @property
    def empty(cls):
        return cls()

    @classmethod
    @property
    def universe(cls):
        return cls(float("-inf"), float("+inf"))

    def clamp(self, n):
        if n < self.start:
            return self.start
        if n > self.end:
            return self.end
        return n
