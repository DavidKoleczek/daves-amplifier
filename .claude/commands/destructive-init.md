The repo was initialized using a GitHub template. Your job is to customize it for the new project.
**VERY IMPORTANT**: You must follow the exact steps, step by step (make a todo list), to ensure that the correct things are updated and deleted.
`make check` will fail while going through this process. That is expected, ignore until this process is over.

COLLECT: 
*Collect the following information from the user*
- The name of the new Python project/package they would like to have created based on `_py_project_template`
  - A brief description of the project
- If they would like a React app created and if so what it should be named.

CHANGE:
*Now initialize from the templates based on the user's previous input*
1. Create a new Python Project by copying `py_projects/_py_project_template` into a new dir under `py_projects`. Then change the following about it based on the user's input
   - Name of the `_py_project_template` folder
   - In `_py_project_template/pyproject.toml`
     - name
     - known-first-party
     - description
   - Rename the folder under `py_project/src` to match the new project name
   - Change any imports using `py_project` in the included `.py` files in the package.
   - In the `Makefile` at the root, add the new folder name to `SUBDIRS` to so it can be built from the root.
   - Now run `make install` and `make check` and fix any errors related to this (if any).
2. Create a new React app, if the user requested it.
   - Copy the `_react-vite-template` template to a new dir under `apps`
   - Update the `package.json` file in the new app directory to match the name the user asked for.
   - Update  `index.html` to have the title match the name the user asked for.
   - In the `Makefile` at the root, add the new folder name to `SUBDIRS` to so it can be built from the root.
   - Now run `make install` and `make check` and fix any related to this (if any).
   - Add the new app to the `launch.json` under the root's `.vscode` folder.
3. Update `daves-amplifier.code-workspace`
   - Change the name of the workspace file to match the name of their repo.
   - Add any newly created Python projects and React apps to the workspace file.
4. README.md
   - The README should just be left with what is under ## Setup (Replace the # daves-amplifier with the new project) and ## Structure
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
