.DEFAULT_GOAL := install

SUBDIRS := py_projects/_py_project_template py_projects/docs-updater

# Recursive targets that run in all subdirectories
.PHONY: all install first-time check upgrade clean

all: install check

# Install all packages
install:
	@for dir in $(SUBDIRS); do \
		echo "Installing in $$dir..."; \
		$(MAKE) -C $$dir install; \
	done

# Any special first time setup
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

# Clean all .venv directories
clean:
	@for dir in $(SUBDIRS); do \
		echo "Cleaning $$dir..."; \
		$(MAKE) -C $$dir clean; \
	done
