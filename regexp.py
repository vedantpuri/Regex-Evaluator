"""A RegEx represents one of the following possible regular expressions:

1. Epsilon                - the re that matches anything (empty string)
2. NullSet                - the re that matches nothing (null)
3. Character              - the re that matches a single character c
4. Sequence(re1,re2)      - the re that matches a sequence of re1 followed by re2
5. Alternative(re1 | re2) - the re that matches an alternative: re1 OR re2
6. Closure(re*)           - the re that matches 0 or more of re
"""


class NullSet:

    def delta(self):
        return NullSet()

    def is_empty(self):
        return False

    def derive(self, char):
        return self

    def normalize(self):
        return self


class Epsilon:
    """ the empty RE """
    def delta(self):
        return Epsilon()

    def is_empty(self):
        return True

    def derive(self, char):
        return NullSet()

    def normalize(self):
        return Epsilon()


class Character:

    def __init__(self, char):
        self.char = char

    def delta(self):
        return NullSet()

    def is_empty(self):
        return False

    def derive(self, char):
        if char == self.char:
            return Epsilon()
        else:
            return NullSet()

    def normalize(self):
        return self


class Sequence:

    def __init__(self, re1, re2):
        self.re1 = re1
        self.re2 = re2

    def delta(self):
        if type(self.re1.delta()) == Epsilon and type(self.re1.delta()) == Epsilon:
            return Epsilon()
        return NullSet()

    def is_empty(self):
        return False

    def derive(self, char):
        return Alternation(Sequence(self.re1.delta(), self.re2.derive(char)), Sequence(self.re1.derive(char), self.re2))

    def normalize(self):
        if type(self.re1) == NullSet or type(self.re2) == NullSet:
            return NullSet()
        if type(self.re1) == Epsilon:
            return self.re2.normalize()
        if type(self.re2) == Epsilon:
            return self.re1.normalize()
        return Sequence(self.re1.normalize(), self.re2.normalize())


class Alternation:

    def __init__(self, re1, re2):
        self.re1 = re1
        self.re2 = re2

    def delta(self):
        if type(self.re1.delta()) == Epsilon or type(self.re2.delta()) == Epsilon:
            return Epsilon()
        return NullSet()

    def is_empty(self):
        return False

    def derive(self, char):
        return Alternation(self.re1.derive(char), self.re2.derive(char))

    def normalize(self):
        if type(self.re2) == NullSet:
            return self.re1.normalize()
        if type(self.re1) == NullSet:
            return self.re2.normalize()
        return Alternation(self.re1.normalize(), self.re2.normalize())


class Closure:

    def __init__(self, re):
        self.re = re

    def delta(self):
        return Epsilon()

    def is_empty(self):
        return True

    def derive(self, char):
        return Sequence(self.re.derive(char), Closure(self.re))

    def normalize(self):
        return Closure(self.re.normalize())


def make_str(str):
    if not str:
        return Epsilon()
    return Sequence(Character(str[0]), make_str(str[1:]))


def matches(regex, str):
    if not str:
        return regex.delta().is_empty()
    normalized_re = regex.derive(str[0]).normalize()
    if normalized_re == NullSet:
        return False
    return matches(normalized_re, str[1:])


if __name__ == '__main__':
    regex = Character('x')
    str_to_match = 'x'
    result = matches(regex, str_to_match)
    print(result)

