# CS50 AI — Projects

Projects from [CS50's Introduction to Artificial Intelligence with Python](https://cs50.harvard.edu/ai/) (Harvard OpenCourseWare), organized by week. Each project has its own commit and git tag.

## Projects

| Week | Topic | Project | Tag | What it does |
|------|-------|---------|-----|--------------|
| 0 | Search | [degrees](week0-search/degrees) | `week0-degrees` | Shortest path between two actors through shared movies |
| 0 | Search | [tictactoe](week0-search/tictactoe) | `week0-tictactoe` | Unbeatable Tic-Tac-Toe AI using minimax |
| 1 | Knowledge | [knights](week1-knowledge/knights) | `week1-knights` | Knights and Knaves puzzles with propositional logic |
| 1 | Knowledge | [minesweeper](week1-knowledge/minesweeper) | `week1-minesweeper` | Minesweeper AI that infers safe cells and mines |
| 2 | Uncertainty | [pagerank](week2-uncertainty/pagerank) | `week2-pagerank` | PageRank via sampling and iteration |
| 2 | Uncertainty | [heredity](week2-uncertainty/heredity) | `week2-heredity` | Bayesian network for gene and trait probabilities |
| 3 | Optimization | [crossword](week3-optimization/crossword) | `week3-crossword` | Crossword generator as a constraint satisfaction problem |
| 4 | Learning | [shopping](week4-learning/shopping) | `week4-shopping` | k-nearest-neighbor model predicting shopping behavior |
| 4 | Learning | [nim](week4-learning/nim) | `week4-nim` | Nim agent trained with Q-learning |
| 5 | Neural Networks | [traffic](week5-neural-networks/traffic) | `week5-traffic` | CNN classifying traffic sign images |
| 6 | Language | [parser](week6-language/parser) | `week6-parser` | Context-free grammar parser for noun phrases |
| 6 | Language | [attention](week6-language/attention) | `week6-attention` | Masked language model and attention visualization with BERT |

## Tech

Python, NumPy, pandas, scikit-learn, TensorFlow, Transformers

## Running a project

```bash
git clone <repo-url>
cd cs50-projects/week0-search/degrees
pip install -r requirements.txt   # if the project has one
python degrees.py small
```

## Notes

Completed for learning and submitted through CS50's `submit50`, graded with `check50`.

## Honesty

Course specs and starter code belong to CS50 staff. If you are taking the course, write your own solutions.
