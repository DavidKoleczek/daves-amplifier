## Dependencies
The latest dependencies are available in the `pyproject.toml` file. You should not use or install any other dependencies unless you ask the user first.
@pyproject.toml

## Python Development Rules
- I am using Python version 3.12, uv as the package and project manager, and Ruff as a linter and code formatter.
- Follow the Google Python Style Guide.
- Instead of importing `Optional` from typing, using the `| `syntax.
- Always add appropriate type hints such that the code would pass Pylance's type check.
- For type hints, use `list`, not `List`. For example, if the variable is `[{"name": "Jane", "age": 32}, {"name": "Amy", "age": 28}]` the type hint should be `list[dict[str. str | int]]`
- Always prefer pathlib for dealing with files. Use `Path.open` instead of `open`. 
- When using pathlib, **always** Use `.parents[i]` syntax to go up directories instead of using `.parent` multiple times.
- When writing multi-line strings, use `"""` instead of using string concatenation. Use `\` to break up long lines in appropriate places.
- When writing tests, use pytest and pytest-asyncio.
- Prefer to use pendulum instead of datetime
- Prefer to use loguru instead of logging
- Follow Ruff best practices such as:
  - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to distinguish them from errors in exception handling
- Do not use relative imports.
- Use dotenv to load environment variables for local development. Assume we have a `.env` file
- Crawl4AI has type issues with their output types. This is the **only** library where you can use `# type: ignore` to fix the issues.
