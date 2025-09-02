# daves-amplifier

My AI-first development environment template. It is currently configured best for use with Claude Code.

Based on [ai-code-project-template](https://github.com/bkrabach/ai-code-project-template/tree/main).


## Setup

1. Install prerequisites 
   1. [uv](https://github.com/astral-sh/uv)
   2. [pnpm](https://pnpm.io/installation)
   3. [claude code](https://docs.anthropic.com/en/docs/claude-code/setup)
   4. make
       - On Windows, you can download it using [UniGetUI](https://github.com/marticliment/UnigetUI) and use [ezwinports make](https://github.com/microsoft/winget-pkgs/tree/master/manifests/e/ezwinports/make)
2. Start `claude` and run the command `/destructive-init`. Claude will ask you a few brief questions then customize the template for you.
3. Run `make first-time` for initial setup
   1. This will prompt you for your `sudo` password to install browser dependencies for crawl4ai
   2. For subsequent env updates, just run `make`
4. Setup your `.env` based on `.env.sample`
5. Open the VSCode workspace using `daves-amplifier.code-workspace`
6. In `claude`, run the command `/prime`


## Structure

### `py_projects`

Contains Python `uv` packages.

### `apps`

Vite + React + TypeScript apps.
Includes these common dependencies: Tailwind CSS, Shadcn, React Router (declarative), Motion, and Lucide React


# Roadmap

## Features
- [ ] Claude Code SDK

## Bug Fixes
- [ ] Format on save does not work for `.tsx` files
