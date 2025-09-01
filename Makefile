.DEFAULT_GOAL := install

SUBDIRS := py_project tools/_py_tool_template tools/docs-updater

# Recursive targets that run in all subdirectories
.PHONY: all install first-time check upgrade

all: install check

# Install all packages
install:
	@for dir in $(SUBDIRS); do \
		echo "Installing in $$dir..."; \
		$(MAKE) -C $$dir install; \
	done

# First-time setup with crawl4ai (requires sudo)
first-time:
	@for dir in $(SUBDIRS); do \
		echo "First-time setup in $$dir..."; \
		$(MAKE) -C $$dir first-time; \
	done

# Run linting and formatting on all packages
check:
	@for dir in $(SUBDIRS); do \
		echo "Checking $$dir..."; \
		$(MAKE) -C $$dir check; \
	done

# Upgrade all dependencies to their latest version
upgrade:
	@for dir in $(SUBDIRS); do \
		echo "Upgrading $$dir..."; \
		$(MAKE) -C $$dir upgrade; \
	done
