# AIG Data Quality Eval Engine
[![Run Tests](https://github.com/Cre8tiveStuff/AIG-Data-Quality-Eval-Platform/actions/workflows/tests.yml/badge.svg)](https://github.com/Cre8tiveStuff/AIG-Data-Quality-Eval-Platform/actions/workflows/tests.yml)

**Open towards Team Collaborations & Contract Opportunities.**

A CLI-driven data quality evaluation engine for LLM outputs and datasets. Evaluates completeness and text quality across multiple file formats, with a tested, CI-verified core.

## Status

✅ Stable foundation, actively developed — core evaluation logic, CLI, multi-format loading (JSON/CSV/Parquet), 9 passing tests, CI verified on every push.
🚧 Not yet supported: database connections, large/streaming files, additional formats (Excel, XML). Planned as next milestones.

## Features

- **Completeness scoring** — flags null, empty, and NaN values across all fields
- **Text substantiveness scoring** — flags responses under a configurable word-count threshold
- **Multi-format loading** — JSON, JSONL, CSV, and Parquet
- **CLI tooling** — run evaluations directly from the command line with configurable flags
- **Tested & CI-verified** — 9 passing pytest tests, re-run automatically via GitHub Actions on every push

## Installation

```bash
git clone https://github.com/Cre8tiveStuff/AIG-Data-Quality-Eval-Platform.git
cd AIG-Data-Quality-Eval-Platform
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## Usage

```bash
dq-eval --input data/sample.json
dq-eval --input data/sample.parquet --output results.json --min-words 5
```

| Flag | Description |
|---|---|
| `-i`, `--input` | Path to input dataset (`.json`, `.jsonl`, `.csv`, `.parquet`) |
| `-o`, `--output` | Optional path to save the evaluation report as JSON |
| `--min-words` | Minimum word count for a text field to count as substantive (default: 3) |

## Running tests

```bash
pytest tests/
```

## Tech stack

Python · Pandas · PyArrow · Pytest · GitHub Actions (CI/CD)

## License

MIT License — see [LICENSE](LICENSE) for details.
