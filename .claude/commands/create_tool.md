You are creating a new Python tool which will be located in the `tools` directory. Follow these steps in order to successfully create the tool.
**VERY IMPORTANT**: You must follow these exact steps, step by step (make a todo list), to ensure that the correct things are updated, deleted, and created.

INITIALIZE FROM TEMPLATE:
- Create a new directory for the tool by copying the `_py_tool_template` which has a `uv` Python project preconfigured.

CUSTOMIZE TEMPLATE:
*Change the template to match the info the user provided*
- Python Package
   - Rename the the _py_tool_template folder to match the user's tool description
   - In the `pyproject.toml` update the following
     - `name`
     - `known-first-party`
     - `description`
   - Fix any existing imports that use the old package name `my_tool`, in `provider_openai.py`

UPDATE MAKEFILE:
- Add the Python package to the Makefile (in the root) so that you can then run `make install` to install the tool and its dependencies. Change the `PYTHON_PACKAGES` section to include this tool.
- Run `make install` to install the tool's venv so that make check works.
- From this point on, you must fix any issues that `make check` raises.

CONTINUE:
- Now build the tool according to the user's specifications until it is complete.

FINALIZE:
- The tool should be runnable using `uvx --from <relative from the root path> <optional args>`. Do not install the tool globally.
- You can test the tool with a command like `uvx --from <relative from the root path> <optional args> --help`

## Specific Rules to Making Tools
- Keep the README simple. Only add the commands on how to run it and its options.
