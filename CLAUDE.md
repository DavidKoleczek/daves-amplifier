## General Development Rules
- When writing documentation, you write as if you were a professional and experienced developer making their code availble publicly on GitHub.
- Do not use any emojis unless the user asks.
- You only add comments when they capture intent you can't encode in names, types, or structure.
  - In other words, reserve comments for the "why". Use them to record rationale, trade-offs, links to specs/papers, or non-obvious domain insights—things not obvious from the code itself. Comments should add signal that code can't.
- After adding a new dependency, immediately call `make install` so that that `make check` will not fail because the dependency is not installed.
