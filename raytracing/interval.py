import sys


class Interval:
    def __init__(self, start=float("+inf"), end=float("-inf")):
        self.start = start
        self.end = end

    def __contains__(self, n):
        return self.start <= n <= self.end

    def surrounds(self, n):
        return self.start < n < self.end

    def __repr__(self):
        return f"i({self.start}, {self.end})"
    def __gt__(self, oth):
        return self.size()>oth.size()
    def size(self):
        return self.end-self.start
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

    def expand(delta):
        padding = delta / 2
        return Interval(self.start - padding, self.end + padding)

    @classmethod
    def merge(cls, a, b):
        return cls(min(a.start, b.start), max(a.end, b.end))
