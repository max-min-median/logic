# __logic.py__

A better, faster version of the logic model-checker `logic.py` used in [CS50ai's Chapter 1 (Knowledge)](https://cs50.harvard.edu/ai/2024/weeks/1/)

## Installation

Download `logic.py`. You may replace the provided `logic.py` with this one.

### Note:
The old `logic.py` has the signature `model_check(knowledge, symbol)`, since it checks each symbol one by one.  
This one checks the entire knowledge base at a go, and thus is called differently. Apologies for breaking the API. You'll therefore need to edit `puzzle.py` to remove the unnecessary loop for the symbols:
```py
# puzzle.py
def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            # CHANGE THIS PART
            model_check(knowledge, debug=True)
            # for symbol in symbols:
            #     if model_check(knowledge, symbol):
            #         print(f"    {symbol}")
```

## Testing

`logic_checker.py` is provided as a module tester. It contains a few sets of logical problems, such as the Mastermind problem demonstrated in the lecture, and a difficult Knights and Knaves problem.
Download `logic_checker.py` into the same folder, then run it with `python logic_checker.py`.

Call `model_check` with `debug=True` to get an insight into how the checker works!

## Improvements over original `logic.py`
- Use of a 3rd state, `UNKNOWN`, for quicker inference.
- 100x faster in checking `mastermind.py`, as compared to the original.
- 5x faster in checking the Knights and Knaves problem.
