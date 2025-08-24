.DEFAULT_GOAL := install

PYTHON_PACKAGES := py_project tools/_py_tool_template
UV_SYNC_INSTALL_ARGS := --all-extras --all-groups

# Define a macro to run commands in each package directory
# Usage: $(call run_in_packages,commands)
define run_in_packages
	@for pkg in $(PYTHON_PACKAGES); do \
		dir_count=$$(echo $$pkg | tr '/' '\n' | wc -l); \
		cd $$pkg && \
		$(1) && \
		for i in $$(seq 1 $$dir_count); do cd ..; done; \
	done
endef

.PHONY: all install first-time check upgrade
all: install check

# Install all packages without crawl4ai setup
install:
	$(call run_in_packages,uv lock --upgrade && uv sync $(UV_SYNC_INSTALL_ARGS))

# First-time setup with crawl4ai (requires sudo)
first-time:
	$(call run_in_packages,uv lock --upgrade && uv sync $(UV_SYNC_INSTALL_ARGS) && . .venv/bin/activate && crawl4ai-setup)

# Run linting and formatting on all packages
check:
	$(call run_in_packages,. .venv/bin/activate && ruff check --no-cache --fix . && ruff format --no-cache . && pyright)

# Upgrades all dependencies to their latest version
upgrade:
	$(call run_in_packages,. .venv/bin/activate && uv lock --upgrade && uv sync --all-extras --all-groups)
