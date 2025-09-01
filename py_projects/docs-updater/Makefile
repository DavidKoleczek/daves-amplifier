.DEFAULT_GOAL := install

UV_SYNC_INSTALL_ARGS := --all-extras --all-groups

.PHONY: all install first-time check upgrade clean

all: install check

install:
	uv lock --upgrade && uv sync $(UV_SYNC_INSTALL_ARGS)

first-time:
	uv lock --upgrade && uv sync $(UV_SYNC_INSTALL_ARGS) && uv run crawl4ai-setup

check:
	uv run ruff check --no-cache --fix .
	uv run ruff format --no-cache .
	uv run pyright

upgrade:
	uv lock --upgrade && uv sync --all-extras --all-groups

clean:
	@echo "Cleaning .venv directory..."
	@rm -rf .venv
