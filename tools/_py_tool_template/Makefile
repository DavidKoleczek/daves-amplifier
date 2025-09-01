.DEFAULT_GOAL := install

UV_SYNC_INSTALL_ARGS := --all-extras --all-groups

.PHONY: all install first-time check upgrade

all: install check

# Install package dependencies
install:
	uv lock --upgrade && uv sync $(UV_SYNC_INSTALL_ARGS)

# First-time setup with crawl4ai (requires sudo)
first-time:
	uv lock --upgrade && uv sync $(UV_SYNC_INSTALL_ARGS) && uv run crawl4ai-setup

# Run linting and formatting
check:
	uv run ruff check --no-cache --fix .
	uv run ruff format --no-cache .
	uv run pyright

# Upgrade all dependencies to their latest version
upgrade:
	uv lock --upgrade && uv sync --all-extras --all-groups