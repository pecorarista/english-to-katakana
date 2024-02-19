## Install
```bash
poetry install
poetry env use /usr/bin/python3.11
```

## Run
```bash
poetry run python -m english_to_katakana INPUT_FILENAME
```

## Test

```bash
poetry run pytest -v
```

## Example
Input
```
OをXの位相(topology)，XとOの組(X, O)を位相空間(topological space)という．
```
Output
```
オウをエクスの位相(タポーラジー)，エクスとオウの組(エクス, オウ)を位相空間(タパラージカル スペイス)という．
```
