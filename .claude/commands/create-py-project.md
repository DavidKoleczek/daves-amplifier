You are creating a new Python project (package) which will be located in the `py_projects` directory. Follow these steps in order to successfully create the project.
**VERY IMPORTANT**: You must follow these exact steps, step by step (make a todo list), to ensure that the correct things are updated, deleted, and created.

INITIALIZE FROM TEMPLATE:
- Create a new directory for the project by copying the `py_projects/_py_tool_template` dir which has a `uv` Python project preconfigured.

CUSTOMIZE TEMPLATE:
*Change the template to match the info the user provided*
- Python Package
   - Rename the the _py_tool_template folder to match the user's project description
   - In the `pyproject.toml` update the following
     - `name`
     - `known-first-party`
     - `description`
   - Fix any existing imports that use the old package name `my_tool`, in `provider_openai.py`

UPDATE MAKEFILE:
- Add the Python package to the Makefile (in the root) so that it can be installed from the root as well. Change the `PYTHON_PACKAGES` section to include this project.
- Run `make install` to install the project's venv.
- From this point on, you must fix any issues that `make check` raises.

UPDATE CODE-WORKSPACE:
- Add this new Python project to the `.code-workspace` at the root.

CONTINUE:
- Now build the project according to the user's specifications until it is complete.


## Specific Rules to Making Tools
- Keep the README simple. Only add the commands on how to run it and its options.
