import random
from itertools import combinations
from collections import Counter, deque
from datetime import date, timedelta

# preferences: 0 - dislikes, 1 - tolerates, 2 - likes, 3 - favorite
top = {'bacon':      [2, 2, 2, 0, 2, 2, 2, 2, 2, 2],
       'sausage':    [2, 0, 2, 2, 0, 2, 0, 1, 1, 2],
       'pepperoni':  [1, 2, 1, 0, 0, 2, 2, 2, 2, 2],
       'hamburger':  [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
       'chicken':    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
       'olives':     [2, 0, 2, 2, 2, 2, 2, 2, 2, 2],
       'peppers':    [2, 2, 2, 2, 2, 2, 2, 0, 2, 0],
       'mushrooms':  [0, 0, 2, 2, 2, 2, 0, 0, 0, 2],
       'broccoli':   [2, 2, 2, 2, 2, 2, 2, 0, 2, 1],
       'spinach':    [2, 0, 2, 2, 2, 2, 2, 0, 2, 0],
       'onions':     [0, 2, 2, 2, 1, 2, 0, 0, 2, 1],
       'pineapple':  [0, 2, 0, 2, 2, 0, 0, 0, 2, 0],
       'ricotta':    [0, 0, 2, 2, 2, 2, 2, 0, 2, 2],
       'artichokes': [0, 0, 2, 2, 2, 0, 0, 0, 2, 2]}

piz = {'Chicken pesto':          [0, 0, 0, 2, 2, 3, 2, 0, 2, 0],
       'Chicken Parmigiana':     [2, 3, 2, 2, 2, 3, 3, 0, 2, 3],
       'Ciappino':               [0, 0, 0, 2, 0, 0, 0, 0, 2, 0],
       'Primavera Extravaganza': [0, 0, 0, 2, 2, 0, 0, 0, 0, 0],
       'Mediterranean':          [0, 0, 2, 2, 2, 2, 0, 0, 2, 0],
       'Hawaiian':               [0, 2, 0, 2, 2, 0, 0, 0, 3, 0],
       'Bianca Ricotta':         [0, 0, 2, 2, 2, 2, 2, 0, 3, 2],
       'BBQ Chicken':            [0, 0, 0, 2, 2, 0, 2, 0, 2, 0],
       'Buffalo Chicken':        [0, 0, 0, 2, 0, 2, 0, 0, 2, 0],
       'Eggplant & Ricotta':     [0, 0, 3, 0, 2, 0, 0, 0, 0, 0],
       'Meatball & peppers':     [2, 3, 0, 2, 2, 2, 2, 0, 2, 0]}

toppings, pizzas = list(top), list(piz)

combos = (list(combinations(set(toppings) - {'pineapple'}, 2)) +
          [('pineapple', 'ricotta'), ('pineapple', 'peppers')])

def getComboRanks():
    "Do some math to determine how people would rank a topping combo."
    comb = {}
    for combo in combos:
        comb[combo] = rankSum(top[combo[0]], top[combo[1]])
    return comb

def rankSum(ranks1, ranks2):
    "Determine what the combined ranking is for two topping rankings."
    comboRank = []
    for (x, y) in zip(ranks1, ranks2):
        if x == 0 or y == 0:    comboRank.append(0)
        elif x == 1 or y == 1:  comboRank.append(1)
        elif x == 2 and y == 2: comboRank.append(2)
        elif x == 3 and y == 3: comboRank.append(3)
        else:                   comboRank.append(3) # must be a 3 and 2
    return comboRank

comb = getComboRanks()

def pickThree():
    "Pick three pizzas that satifies everyone."
    two   = random.choice(pizzas)
    three = random.choice(combos)
    one   = random.choice(list(set(toppings) - set(three)))
    oneRank, twoRank, threeRank = top[one], piz[two], comb[three]
    colSum  = [x + y + z for (x, y, z) in zip(oneRank, twoRank, threeRank)]
    colOnes = [x == y == z == 1 for (x, y, z) in zip(oneRank, twoRank, threeRank)]
    if any([x == 0 or x == 1 for x in colSum]) or any(colOnes):
        return pickThree()
    else:
        return one, two, three

def getPizzaFreq(N=10000):
    "Find the pizza frequencies of the pickThree algorithm."
    popularity = Counter()
    for _ in range(N):
        _, pizza, _ = pickThree()
        popularity[pizza] += 1
    return popularity

def createSchedule(numWeeks=10):
    "Create a schedule of pizzas to order such that no pizza is repeated for 3 weeks."
    rolling3 = deque()
    sched = []
    for _ in range(numWeeks):
        pizzs = pickThree()
        while any([x in rolling3 for x in pizzs]):
            pizzs = pickThree()
        if len(rolling3) == 9:
            for _ in range(3):
                rolling3.popleft()
        for pizz in pizzs: rolling3.append(pizz)
        sched.append(pizzs)
    return sched

maxLenTop = max([len(x) for x in toppings])
maxLenPiz = max([len(x) for x in pizzas])

def printSched(sched, startDate=date(2019, 8, 30)):
    "Print a schedule for pizzas."
    currentDate = startDate
    txt = "{}: 1. {:<" + str(maxLenTop) + \
          "} 2. {:<" + str(maxLenPiz) + "} 3. {} and {}"
    for pizzs in sched:
        print(txt.format(
            currentDate, pizzs[0], pizzs[1], pizzs[2][0], pizzs[2][1]))
        currentDate += timedelta(days=7)

printSched(createSchedule())



