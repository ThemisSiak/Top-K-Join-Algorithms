# Top-K Join on Census-Income Dataset

This project implements and compares two algorithms for the Top-K join problem on a filtered census dataset, based on instance weight and age equality.

## Problem Description

Given two datasets (`males_sorted` and `females_sorted`) sorted by instance weight, the task is to find the **top-K male-female pairs** with the same age, whose combined instance weight is the highest.

Pairs are only valid if:
- Both individuals are **18 years or older**
- Neither is **married** (i.e., marital status doesn't start with "Married")

## Algorithms Implemented

### 1. `meros1.py` – HRJN (Hash Rank Join)
- Alternately reads valid entries from each file.
- Maintains age-indexed hash tables.
- Uses a max-heap and dynamic threshold to yield top-K results via a generator.

### 2. `meros2.py` – Hash Join with Filtering
- Reads and indexes all valid male entries first.
- Probes with female entries to find matching age.
- Maintains a min-heap for top-K matches.

### 3. `meros3.py` – Analysis and Comparison
- Runs both algorithms for K ∈ {1, 2, 5, 10, 20, 50, 100}
- Records execution time.
- Plots comparative results.
- Counts valid lines processed.
- Explains performance differences.

## How to Run

Run either algorithm from the command line:

```bash
python meros1.py K
# or
python meros2.py K
```

Where `K` is an integer (e.g., 10).

Each script will:
- Output the top-K matching ID pairs and their score.
- Print execution time.
- Ensure results from both implementations are identical.

## Evaluation

Run `meros3.py` to:
- Measure execution times
- Generate performance chart
- Output statistics and insights

## Notes

- Implemented in Python **without pandas**, as required.
- Uses standard libraries (`heapq`, `time`, etc.).
- Data from: https://kdd.ics.uci.edu/databases/census-income/census-income.html

---
