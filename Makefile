.DEFAULT_GOAL := install

PYTHON_PACKAGES := py_project
UV_SYNC_INSTALL_ARGS := --all-extras --all-groups

ifeq ($(OS),Windows_NT)
    ACTIVATE_PYENV := .venv\Scripts\activate
else
    ACTIVATE_PYENV := . .venv/bin/activate
endif

.PHONY: all install check
all: install check

# Install all packages
install:
	@for pkg in $(PYTHON_PACKAGES); do \
		cd $$pkg && uv lock --upgrade && uv sync $(UV_SYNC_INSTALL_ARGS) && $(ACTIVATE_PYENV) && crawl4ai-setup && cd ..; \
	done

# Run linting and formatting on all packages
check:
	@for pkg in $(PYTHON_PACKAGES); do \
		cd $$pkg && $(ACTIVATE_PYENV) && ruff check --no-cache --fix . && ruff format --no-cache . && pyright && cd ..; \
	done

# Upgrades all dependencies to their latest version
upgrade:
	@for pkg in $(PYTHON_PACKAGES); do \
		cd $$pkg && $(ACTIVATE_PYENV) && uv lock --upgrade && uv sync --all-extras --all-groups && cd ..; \
	done
