from logic import *


def checkMastermind():
    colors = ["red", "blue", "green", "yellow"]
    symbols = []
    for i in range(4):
        for color in colors:
            symbols.append(Symbol(f"{color}{i}"))

    knowledge = And()

    # Each color has a position.
    for color in colors:
        knowledge.add(Or(
            Symbol(f"{color}0"),
            Symbol(f"{color}1"),
            Symbol(f"{color}2"),
            Symbol(f"{color}3")
        ))

    # Only one position per color.
    for color in colors:
        for i in range(4):
            for j in range(4):
                if i != j:
                    knowledge.add(Implication(
                        Symbol(f"{color}{i}"), Not(Symbol(f"{color}{j}"))
                    ))

    # Only one color per position.
    for i in range(4):
        for c1 in colors:
            for c2 in colors:
                if c1 != c2:
                    knowledge.add(Implication(
                        Symbol(f"{c1}{i}"), Not(Symbol(f"{c2}{i}"))
                    ))

    knowledge.add(Or(
        And(Symbol("red0"), Symbol("blue1"), Not(Symbol("green2")), Not(Symbol("yellow3"))),
        And(Symbol("red0"), Symbol("green2"), Not(Symbol("blue1")), Not(Symbol("yellow3"))),
        And(Symbol("red0"), Symbol("yellow3"), Not(Symbol("blue1")), Not(Symbol("green2"))),
        And(Symbol("blue1"), Symbol("green2"), Not(Symbol("red0")), Not(Symbol("yellow3"))),
        And(Symbol("blue1"), Symbol("yellow3"), Not(Symbol("red0")), Not(Symbol("green2"))),
        And(Symbol("green2"), Symbol("yellow3"), Not(Symbol("red0")), Not(Symbol("blue1")))
    ))

    knowledge.add(And(
        Not(Symbol("blue0")),
        Not(Symbol("red1")),
        Not(Symbol("green2")),
        Not(Symbol("yellow3"))
    ))

    return knowledge


def checkHarry():
    rain = Symbol('rain')
    hagrid = Symbol('hagrid')
    dumbledore = Symbol('dumbledore')

    knowledge = And(
        Implication(Not(rain), hagrid),
        Or(hagrid, dumbledore),
        Not(And(hagrid, dumbledore)),
        dumbledore,
    )

    return knowledge


def myCheck():

    A = Symbol("A")
    B = Symbol("B")
    C = Symbol("C")
    D = Symbol("D")

    knowledge = And(
        Or(A, B),
        Or(A, C),
        Not(A),
    )

    return knowledge


def checkKnights(problem=2):
    if problem == 1:
        # You meet three inhabitants: Betty, Zed and Zoey.
        # Betty claims that Zoey could claim that Zed is a knight.
        # Zed claims that only a knave would say that Zoey is a knave.
        # Zoey tells you that Betty is a knave.
        betty, zed, zoey = (Symbol(f"{x} is a knight") for x in ("Betty", "Zed", "Zoey"))
        knowledge = And(
            Biconditional(betty, Biconditional(zoey, zed)),
            Biconditional(zed, Not(Not(zoey))),
            Biconditional(zoey, Not(betty))
        )
    elif problem == 2:
        # You meet four inhabitants: Homer, Joe, Zed and Betty.
        # Homer tells you that Zed and Betty are not the same.
        # Joe says that Zed could claim that Betty is a knave.
        # Zed tells you that either Joe is a knight or Homer is a knave.
        # Betty says, “I and Homer are different.”
        homer, joe, zed, betty = (Symbol(f"{x} is a knight") for x in ("Homer", "Joe", "Zed", "Betty"))
        knowledge = And(
            Biconditional(homer, Or(And(zed, Not(betty)), And(Not(zed), betty))),
            Biconditional(joe, Biconditional(zed, Not(betty))),
            Biconditional(zed, Or(And(joe, Not(Not(homer))), And(Not(joe), Not(homer)))),
            Biconditional(betty, Or(And(betty, Not(homer)), And(Not(betty), homer)))

        )
    elif problem == 3:
        # You meet eight inhabitants: Dave, Zeke, Sally, Zoey, Bart, Bozo, Alice and Bob.
        # Dave claims that only a knave would say that Bart is a knave.
        # Zeke tells you, “Bob and Sally are different.”
        # Sally tells you that Bob is a knave.
        # Zoey says, “At least one of the following is true: that Bart is a knight or that Bozo is a knave.”
        # Bart says that either Zeke is a knave or Sally is a knight.
        # Bozo claims, “Dave and Bob are knights.”
        # Alice claims that Zoey is a knave and Bart is a knight.
        # Bob tells you that Sally is a knave and Alice is a knight.
        knowledge = And()

        people = ("Dave", "Zeke", "Sally", "Zoey", "Bart", "Bozo", "Alice", "Bob")
        for person in people:
            globals()[person.lower() + "Knight"] = Symbol(f"{person} is a Knight")
            globals()[person.lower() + "Knave"] = Symbol(f"{person} is a Knave")
            knowledge.add(Biconditional(globals()[person.lower() + "Knight"], Not(globals()[person.lower() + "Knave"])))

        knowledge.add(Biconditional(daveKnight, Not(bartKnave)))
        knowledge.add(Biconditional(zekeKnight, Biconditional(daveKnight, sallyKnave)))
        knowledge.add(Biconditional(sallyKnight, bobKnave))
        knowledge.add(Biconditional(zoeyKnight, Or(bartKnight, bozoKnave)))
        knowledge.add(Biconditional(bartKnight, Or(zekeKnave, sallyKnight)))
        knowledge.add(Biconditional(bozoKnight, And(daveKnight, bobKnight)))
        knowledge.add(Biconditional(aliceKnight, And(zoeyKnave, bartKnight)))
        knowledge.add(Biconditional(bobKnight, And(sallyKnave, aliceKnight)))

    return knowledge


def main():
    model = model_check(checkMastermind(), debug=False)
    model = model_check(checkKnights(3), debug=False)
    model = model_check(myCheck(), debug=False)
    model = model_check(checkHarry(), debug=True)
    pass

if __name__ == '__main__':
    main()