# __logic.py__

A better, faster version of the logic model-checker `logic.py` used in [CS50ai's Chapter 1 (Knowledge)](https://cs50.harvard.edu/ai/2024/weeks/1/)

## Installation

Download `logic.py`. You may replace the provided `logic.py` with this one.

## Testing

`logic_checker.py` is provided as a module tester. It contains a few sets of logical problems, such as the Mastermind problem demonstrated in the lecture, and a difficult Knights and Knaves problem.
Download `logic_checker.py` into the same folder, then run it with `python logic_checker.py`.

## Improvements over original `logic.py`
- Use of a 3rd state, `UNKNOWN`, for quicker inference.
- 100x faster in checking `mastermind.py`, as compared to the original.
- 5x faster in checking the Knights and Knaves problem.

Test
