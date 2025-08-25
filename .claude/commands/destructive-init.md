The repo was initialized using a GitHub template. Your job is to customize it for the new project.
**VERY IMPORTANT**: You must follow the exact steps, step by step (make a todo list), to ensure that the correct things are updated and deleted.
`make check` will fail while going through this process. That is expected, ignore until this process is over.

COLLECT: 
*Collect the following information from the user*
- The name of the Python package
- A brief description of the project

CHANGE:
*Now make changes to the template to match the info the user provided*
1. Python Package
   - Name of the py_project folder
   - In `py_project/pyproject.toml`
     - name
     - known-first-party
     - description
   - Rename the folder under `py_project/src` to match the new project name
   - Change any imports using `py_project` in the included `.py` files in the package.
2. Makefile
   - Change the name of the PYTHON_PACKAGES to make the previous changes. By default it will be py_project.
3. `daves-amplifier.code-workspace`
   - Change the name of the workspace file to match the new project name
   - Change the name of the folder in the workspace file to match the new project name
4. README.md
   - The README should just be left with what is under ## Setup (Replace the # daves-amplifier with the new project)
     - Except you should remove the step that starts with: Start claude and run the command /destructive-init...
   - Change the introduction to the user's project name (usually the repo name if they didn't specify exactly)
   - Remove the roadmap section entirely

CLEANUP:
- Remove `.claude/commands/destructive_init.md`

FINAL USER INSTRUCTIONS:
*Tell the briefly user how to continue*
- Have them run `make first-time` (they need to run it because it might ask for sudo access for crawl4ai setup)
- Setup the `.env` with secrets based on `.env.sample`
- In `claude`, run the command `/prime`
