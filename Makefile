.DEFAULT_GOAL := install

PYTHON_PACKAGES := py_project tools/_py_tool_template tools/docs-updater
UV_SYNC_INSTALL_ARGS := --all-extras --all-groups

.PHONY: all install first-time check upgrade
all: install check

# Install all packages without crawl4ai setup
install:
	@for pkg in $(PYTHON_PACKAGES); do \
		(cd $$pkg && \
		uv lock --upgrade && uv sync $(UV_SYNC_INSTALL_ARGS)); \
	done

# First-time setup with crawl4ai (requires sudo)
first-time:
	@for pkg in $(PYTHON_PACKAGES); do \
		(cd $$pkg && \
		uv lock --upgrade && uv sync $(UV_SYNC_INSTALL_ARGS) && \
		uv run crawl4ai-setup); \
	done

# Run linting and formatting on all packages
check:
	@for pkg in $(PYTHON_PACKAGES); do \
		(cd $$pkg && \
		uv run ruff check --no-cache --fix . && \
		uv run ruff format --no-cache . && \
		uv run pyright); \
	done

# Upgrades all dependencies to their latest version
upgrade:
	@for pkg in $(PYTHON_PACKAGES); do \
		(cd $$pkg && \
		uv lock --upgrade && uv sync --all-extras --all-groups); \
	done
