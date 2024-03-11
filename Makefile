.PHONY: analysis_requirements dev_requirements lint environment clean_environment clean test dev_requirements

# ==================================== Constants ====================================

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = california-census
PYTHON_COMMAND = python
PACKAGE_MANAGER = conda
PYTHON_VERSION = 3.11

# ==================================== Rules ====================================

# ____________________________________ Setup ____________________________________

## Create virtual environment and install dependencies
init:
	conda env update --file environment.yaml

# ____________________________________ Linting ____________________________________
## Lint (black,flake8,mypy,isort)
lint: format-check
	python -m flake8 src; \
	python -m mypy src; \
	# python -m isort src # TODO

## Check if the code is formated properly
format-check:
	python -m black --check -l 120 src

## Format the code according to black standards
format-code:
	python -m black -l 120 src

# ____________________________________ Test ____________________________________
## Test using pytest
test:
	python -m pytest -v src/test/

## Smoke test
test-smoke:
	python -m pytest src/test/smoke/

## Unit test
test-unit:
	python -m pytest src/test/unit/

# ____________________________________ Clean ____________________________________

## Delete all compiled Python files
clean: clean-cache
	find . | grep -E "build$|\/__pycache__$|\.pyc$|\.pyo$|\.egg-info" | xargs rm -rf || echo 'Already clean'

## Clean cache
clean-cache:
	conda clean -a -y
	python -m pip cache purge


# ___________________________________ Self Documenting Commands ___________________________________

.DEFAULT_GOAL := help
# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=15 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
