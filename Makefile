.PHONY: init lint docstyle imports format-check format-code test test-unit test-smoke clean clean-files clean-cache

# ____________________________________ Setup ____________________________________

## Create virtual environment and install dependencies
init:
	conda env update --file environment.yaml


## Instal CUDA (NVIDIA) dependencies for tensorflow and keras
install-gpu-deps:
	pip install -e .[cuda,dev,api,analysis]

## Erase conda venv
clean-env:
	conda env remove -n california-census

# ____________________________________ Linting ____________________________________
## Lint (black,flake8,mypy,isort)
lint: format-check
	python -m flake8 src; \
	python -m mypy src; \
 # TODO imports

docstyle:
	python -m pydocstyle src/

## Check sorting of imports
imports:
	python -m isort - src/

## Check if the code is formated properly
format-check:
	python -m black --check --diff --color -l 120 src

## Format the code according to black standards
format-code:
	python -m black -l 120 src

# ____________________________________ Test ____________________________________
## Test using pytest
test:
	python -m pytest

## Smoke test
test-smoke:
	python -m pytest src/test/smoke/

## Unit test
test-unit:
	python -m pytest src/test/unit/

# ____________________________________ Clean ____________________________________

## Clean all
clean: clean-cache clean-files

## Delete all compiled Python files
clean-files:
	find . | grep -E "build$|\/__pycache__$|\.pyc$|\.pyo$|\.egg-info$|\.ipynb_checkpoints" | xargs rm -rf || echo "Already clean"

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
