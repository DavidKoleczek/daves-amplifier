# Modular Block Approach

## Core Principles

### 1. Think in Modular Blocks
- Treat each piece of functionality as a self-contained module with clear interfaces
- Each module should have well-defined inputs, outputs, and connection points to other modules
- Modules should be independent enough to be modified without affecting the rest of the system

### 2. Work at the Specification Level
- Focus on understanding WHAT needs to be built and WHY
- When given a task, first identify the module boundaries and specifications
- Implement code that fully satisfies the specification within that bounded context

### 3. Maintain Clean Interfaces
- Keep external interfaces (APIs, function signatures, data contracts) stable
- Ensure modules connect through well-defined, documented interfaces
- Changes within a module shouldn't break other modules that depend on it

## Practical Guidelines

### When Building Features
1. Identify module boundaries first - What is the self-contained unit of functionality?
2. Define clear interfaces - What are the inputs, outputs, and connection points?
3. Build complete modules - Create cohesive, self-contained implementations
4. Preserve external contracts - Keep APIs and interfaces stable so other modules continue to work

### When Making Changes
1. **Keep scope bounded** - Work within a single module or tightly coupled set of modules
2. **Maintain compatibility** - Ensure modified code maintains the same external interface
3. **Think holistically** - Consider the entire module's purpose when making changes

### When Refactoring
1. **Think in assemblies** - Group related modules that should be updated together
2. **Preserve system contracts** - The overall system interface should remain unchanged
3. **Focus on behavior** - Ensure the code produces the correct external behavior
