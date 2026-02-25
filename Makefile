


PYTHON = python3
SCRIPT = a_maze_ing.py
CONFIG = config.txt

.PHONY: install run debug clean lint lint-strict

install:
	pip install mypy mazegen.tar.gz

run:
	$(PYTHON) $(SCRIPT) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(SCRIPT) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

lint:
	flake8 .	
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs	
