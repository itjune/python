import string
from collections import deque

class Info():
    def __init__(self):
        self.used = 0
        self.stage = []

term = set(string.ascii_lowercase)
nterm = set(string.ascii_uppercase)

def first_letters(gram, empty):
    output = set()
    q = deque()
    gram['S'].used = 1
    q.append('S')
    while len(q) > 0:
        letter = q.popleft()
        for item in gram[letter].stage:
            for i in range(len(item)):
                if item[i] in term:
                    output.add(item[i])
                    break
                else:
                    if not gram[item[i]].used:
                        q.append(item[i])
                        gram[item[i]].used = 1
                    if not item[i] in empty:
                        break
    return output


def find_good(nterm_cnts, rules, is_good, flag):
    q = deque(is_good)
    while len(q) > 0:
        x = q.popleft()
        if x in rules:
            for y in rules[x]:
                nterm_cnts[1][y] -= 1
                if nterm_cnts[1][y] == 0 and nterm_cnts[0][y] not in is_good \
                   and (flag or nterm_cnts[2][y] == 0):
                    is_good.add(nterm_cnts[0][y])
                    q.append(nterm_cnts[0][y])

def find_bad(nterm_cnts, rules, right, is_good):
    is_bad = (right - set(nterm_cnts[0]) - term).union(set(nterm_cnts[0]) - is_good)
    q = deque(is_bad)
    bad_rules = []
    while len(q) > 0:
        x = q.popleft()
        if x in rules:
            for y in rules[x]:
                if y not in bad_rules:
                    bad_rules.append(y)
                    tmp = nterm_cnts[0][y]
                    nterm_cnts[0][y] = 0
                    if tmp not in nterm_cnts[0] and tmp not in is_bad:
                        q.append(tmp)
                        is_bad.add(tmp)

def get_gram(nterm_cnts, is_good):
    gram = {}
    for i in range(len(nterm_cnts[0])):
        if nterm_cnts[0][i] in is_good:
            if nterm_cnts[0][i] not in gram:
                gram[nterm_cnts[0][i]] = Info()
            if nterm_cnts[3][i]:
                gram[nterm_cnts[0][i]].stage.append(nterm_cnts[3][i])
    return gram


num_p = int(input())
nterm_cnts = [0] * 4
for i in range(4):
    nterm_cnts[i] = [0] * num_p
rules = {}
right = set()
is_empty = set()
is_good = set()
for i in range(num_p):
    tmp = input()
    nterm_cnts[0][i] = tmp[0]
    if tmp[3] == '$':
        is_empty.add(tmp[0])
    else:
        nterm_cnts[1][i] = len(set(tmp[3:]) & nterm)
        nterm_cnts[2][i] = len(set(tmp[3:]) & term)
        nterm_cnts[3][i] = tmp[3:]
        if nterm_cnts[1][i] == 0:
            is_good.add(tmp[0])
        right = right.union(set(tmp[3:]))
        for x in (set(tmp[3:]) & nterm):
            if x not in rules:
                rules[x] = []
            rules[x].append(i)


if 'S' not in nterm_cnts[0] or right.isdisjoint(term):
    print()
else:
    tmp = nterm_cnts[1][:]
    find_good(nterm_cnts, rules, is_empty, False)
    is_good = is_good.union(is_empty)
    nterm_cnts[1] = tmp[:]
    find_good(nterm_cnts, rules, is_good, True)
    if 'S' in is_good:
        find_bad(nterm_cnts, rules, right, is_good)
        gram = get_gram(nterm_cnts, is_good)
        print (*sorted(first_letters(gram, is_empty)), sep = '')
    else:
        print()

