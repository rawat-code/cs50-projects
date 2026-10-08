from logic import *


AKnight = Symbol("A is a knight")
AKnave = Symbol("A is a knave")

BKnight = Symbol("B is a knight")
BKnave = Symbol("B is a knave")

CKnight = Symbol("C is a knight")
CKnave = Symbol("C is a knave")


# Puzzle 0
# A says "I am both a knight and a knave."

knowledge0 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Implication(
        AKnight,
        And(AKnight, AKnave)
    ),

    Implication(
        AKnave,
        Not(And(AKnight, AKnave))
    )
)


# Puzzle 1
# A says "We are both knaves."
# B says nothing.

knowledge1 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    Implication(
        AKnight,
        And(AKnave, BKnave)
    ),

    Implication(
        AKnave,
        Not(And(AKnave, BKnave))
    )
)


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."

knowledge2 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    Implication(
        AKnight,
        Or(
            And(AKnight, BKnight),
            And(AKnave, BKnave)
        )
    ),

    Implication(
        AKnave,
        Not(
            Or(
                And(AKnight, BKnight),
                And(AKnave, BKnave)
            )
        )
    ),

    Implication(
        BKnight,
        Or(
            And(AKnight, BKnave),
            And(AKnave, BKnight)
        )
    ),

    Implication(
        BKnave,
        Not(
            Or(
                And(AKnight, BKnave),
                And(AKnave, BKnight)
            )
        )
    )
)


# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave.'"
# B then says "C is a knave."
# C says "A is a knight."

knowledge3 = And(
    # Each person is either a knight or a knave, but not both.
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    # A says either "I am a knight" or "I am a knave".
    #
    # Because A must be one or the other, the statement
    # that A made determines A's truthfulness.
    Biconditional(
        Or(AKnight, AKnave),
        AKnight
    ),

    # B says "A said 'I am a knave.'"
    #
    # B being a knight corresponds to C being a knave.
    Biconditional(
        CKnave,
        BKnight
    ),

    # B's second statement: "C is a knave."
    #
    # If C is a knight, B must be a knave.
    Biconditional(
        CKnight,
        BKnave
    ),

    # C says "A is a knight."
    Biconditional(
        AKnight,
        CKnight
    ),

    # If A is a knave, C is a knave.
    Biconditional(
        AKnave,
        CKnave
    )
)


def main():

    symbols = [
        AKnight, AKnave,
        BKnight, BKnave,
        CKnight, CKnave
    ]

    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]

    for puzzle, knowledge in puzzles:
        print(puzzle)

        for symbol in symbols:
            if model_check(knowledge, symbol):
                print(f"    {symbol}")


if __name__ == "__main__":
    main()
