SHELL := /bin/zsh

# Default day is today (2 digits), can be overridden: `make newday DAY=07`
DAY ?= $(shell date +%d)

TEMPLATE   := day00.py
DAY_FILE   := day$(DAY).py
INPUT_DIR  := input_files
INPUT_FILE := $(INPUT_DIR)/input$(DAY).txt
TEST_FILE  := $(INPUT_DIR)/input$(DAY).test.txt

.PHONY: newday venv-activate

newday:
	@echo "Preparing AoC $(YEAR) day $(DAY)..."
	cp "$(TEMPLATE)" "$(DAY_FILE)"
	touch "$(INPUT_FILE)"
	touch "$(TEST_FILE)"
	@echo "Created: $(DAY_FILE)"
	@echo "Created: $(INPUT_FILE)"
	@echo "Created: $(TEST_FILE)"

# This starts a new interactive shell with the virtualenv activated.
# Note: it cannot modify the parent shell environment.
venv-activate:
	@echo "Starting new zsh with venv activated..."
	@exec $(SHELL) -i -c 'source venv/bin/activate && exec $(SHELL) -i'


