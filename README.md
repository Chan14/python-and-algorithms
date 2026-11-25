# python-and-algorithms

Invariant-first algorithm practice, Python language notes, and ML math
experiments. Tested code lives in an installable package, `pyalgos`.
Notebooks, notes, and experiments import from that package.

## Table of contents

- [Repository layout](#repository-layout)
- [Setup](#setup)
- [Everyday commands](#everyday-commands)
- [Where new work goes](#where-new-work-goes)
- [Contents](#contents)
  - [Algorithms](#algorithms)
  - [Statistics and probability](#statistics-and-probability)
  - [Linear algebra](#linear-algebra)
  - [Calculus](#calculus)
  - [Python language notes](#python-language-notes)
  - [Python challenges](#python-challenges)
  - [Scratch](#scratch)

## Repository layout

```
python-and-algorithms/
├── pyproject.toml        # package metadata, dependencies, pytest and ruff config
├── .python-version       # pinned interpreter (3.13)
├── src/pyalgos/          # importable, tested code, no side effects on import
│   ├── algorithms/
│   │   ├── two_pointers/
│   │   ├── sliding_window/
│   │   └── monotonic_deque/
│   ├── stats/
│   └── paths.py          # repo-relative paths (figures/)
├── tests/                # mirrors src/pyalgos/ one-to-one
├── notebooks/            # finished study notebooks, by topic
├── notes/                # runnable Python concept notes (.py)
├── experiments/          # scripts that compute and save figures
├── figures/              # generated plots, by topic
└── scratch/              # rough work, kept but not polished
```

**Rules that keep this layout sound**

1. `src/pyalgos/` holds only code that is safe to import. Importing a module
   must not print, plot, or write files. Each module's demo runs under
   `if __name__ == "__main__":`.
2. Every module in `src/pyalgos/<path>/<name>.py` has its tests in
   `tests/<path>/test_<name>.py`. Nothing creates the test folders for you;
   make the mirrored folder when you add a module.
3. Notebooks, notes, and experiments never use `sys.path` hacks. They import
   the installed package, for example
   `from pyalgos.stats.covariance_correlation import covariance_matrix`.
4. Any folder named `untracked/`, at any depth, is ignored by git.

## Setup

One time, from the repo root:

```bash
python3.13 -m venv .venv          # or: uv venv  (reads .python-version)
source .venv/bin/activate
pip install -e ".[dev]"           # editable install: edits in src/ apply immediately
nbstripout --install              # strip notebook outputs on commit; local files keep them
python -m ipykernel install --user --name pyalgos --display-name "Python (pyalgos)"
```

Then select the **Python (pyalgos)** kernel in Jupyter or VS Code.

## Everyday commands

```bash
pytest                                        # run all tests
pytest tests/algorithms/sliding_window        # run one topic
python -m pyalgos.algorithms.two_pointers.intersect_three   # run a module's demo
python experiments/linear_algebra/svd_geometry.py           # regenerate figures
ruff check .                                  # lint
```

## Where new work goes

| You are writing...                         | Put it in                          |
| ------------------------------------------ | ---------------------------------- |
| A solved problem you want tested           | `src/pyalgos/...` + `tests/...`    |
| A worked study notebook                    | `notebooks/<topic>/`               |
| A Python concept note you run and read     | `notes/python/<topic>/`            |
| A script that produces plots               | `experiments/<topic>/` → `figures/` |
| Quick tries, throwaway checks              | `scratch/<topic>/`                 |
| Anything that must never reach GitHub      | any `untracked/` folder            |

Number notebooks inside a topic (`01_`, `02_`, ...) when their order matters.

## Contents

### Algorithms

**Two pointers**: `src/pyalgos/algorithms/two_pointers/`

| Module | What it solves |
| ------ | -------------- |
| [`merge_and_intersect.py`](src/pyalgos/algorithms/two_pointers/merge_and_intersect.py) | Merge two sorted arrays; intersect two sorted arrays (output-check version and skip-duplicates-at-source version) |
| [`intersect_three.py`](src/pyalgos/algorithms/two_pointers/intersect_three.py) | Unique intersection of three sorted arrays ("move the minimum" rule) |
| [`merge_sorted_lists.py`](src/pyalgos/algorithms/two_pointers/merge_sorted_lists.py) | Merge two sorted lists without modifying the inputs |
| [`valid_subsequence.py`](src/pyalgos/algorithms/two_pointers/valid_subsequence.py) | Is one array a subsequence of another (first attempt and canonical version) |

**Sliding window**: `src/pyalgos/algorithms/sliding_window/`

| Module | What it solves |
| ------ | -------------- |
| [`min_subarray_len.py`](src/pyalgos/algorithms/sliding_window/min_subarray_len.py) | Smallest subarray with sum ≥ K, positive numbers only |

**Monotonic deque**: `src/pyalgos/algorithms/monotonic_deque/`

| Module | What it solves |
| ------ | -------------- |
| [`shortest_subarray_at_least_k.py`](src/pyalgos/algorithms/monotonic_deque/shortest_subarray_at_least_k.py) | Shortest subarray with sum ≥ K when negatives are allowed (prefix sums and a deque of non-dominated starts) |

**Dynamic programming**: `notebooks/algorithms/dynamic_programming/`

| Notebook | Topic |
| -------- | ----- |
| [`01_climbing_stairs.ipynb`](notebooks/algorithms/dynamic_programming/01_climbing_stairs.ipynb) | Calibration problem: base cases and recursion |
| [`02_count_paths_grid.ipynb`](notebooks/algorithms/dynamic_programming/02_count_paths_grid.ipynb) | Count right/down paths in an m × n grid (in progress) |
| [`03_house_robber_ii.ipynb`](notebooks/algorithms/dynamic_programming/03_house_robber_ii.ipynb) | House Robber II, circular street |

### Statistics and probability

| File | Topic |
| ---- | ----- |
| [`src/pyalgos/stats/covariance_correlation.py`](src/pyalgos/stats/covariance_correlation.py) | Covariance and correlation matrices from a data matrix D, plus visualizations. Run with `python -m pyalgos.stats.covariance_correlation`; plots go to [`figures/stats/covariance/`](figures/stats/covariance/) |
| [`notebooks/stats/covariance_centering.ipynb`](notebooks/stats/covariance_centering.ipynb) | Centering a data matrix: D_c = X − 1μᵀ |
| [`notebooks/stats/importance_sampling.ipynb`](notebooks/stats/importance_sampling.ipynb) | Uniform mini-batch mean estimates vs importance sampling with a proposal q: naive bias, weight correction, variance reduction |

### Linear algebra

| File | Topic |
| ---- | ----- |
| [`experiments/linear_algebra/svd_geometry.py`](experiments/linear_algebra/svd_geometry.py) | Geometry of W = UΣVᵀ applied to a vector, step by step. Plots go to [`figures/linear_algebra/svd/`](figures/linear_algebra/svd/) |

### Calculus

| Notebook | Topic |
| -------- | ----- |
| [`notebooks/calculus/scalar_vector_functions_and_grad_check.ipynb`](notebooks/calculus/scalar_vector_functions_and_grad_check.ipynb) | Scalar-valued vs vector-valued functions; numerical gradient checking |

### Python language notes

`notes/python/`: runnable notes; read the comments, run the file.

| File | Topic |
| ---- | ----- |
| [`classes/value_classes.py`](notes/python/classes/value_classes.py) | Abstract classes, value equality, dataclasses |
| [`classes/hashable_and_comparable.py`](notes/python/classes/hashable_and_comparable.py) | `__eq__`/`__hash__`, `total_ordering`, `NotImplemented` and reflected comparisons |
| [`classes/enums.py`](notes/python/classes/enums.py) | `Enum` creation styles, `auto`, identity and hashing |
| [`classes/multiple_inheritance.py`](notes/python/classes/multiple_inheritance.py) | MRO, C3 linearization, mixins (contains sketch snippets that reference undefined classes, so it stops partway when run) |
| [`files/script_dir_vs_cwd.py`](notes/python/files/script_dir_vs_cwd.py) | Current working directory vs the script's own directory |

### Python challenges

| Notebook | Topic |
| -------- | ----- |
| [`notebooks/python/challenges/01_temperature_analyzer.ipynb`](notebooks/python/challenges/01_temperature_analyzer.ipynb) | Lists vs NumPy boolean masks |
| [`notebooks/python/challenges/02_warmup_problems.ipynb`](notebooks/python/challenges/02_warmup_problems.ipynb) | Comprehensions, dicts, `Counter`/`defaultdict` warm-ups |

### Scratch

| Notebook | What it was for |
| -------- | --------------- |
| [`scratch/algorithms/accumulate_and_deque_checks.ipynb`](scratch/algorithms/accumulate_and_deque_checks.ipynb) | Quick checks of `itertools.accumulate` and empty-deque truthiness |
| [`scratch/python/merge_and_mutable_default_args.ipynb`](scratch/python/merge_and_mutable_default_args.ipynb) | Early merge draft; the mutable-default-argument trap |
