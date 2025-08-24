# daves-amplifier

My AI-first development environment template. It is currently configured to work with Claude Code.

Based on [ai-code-project-template](https://github.com/bkrabach/ai-code-project-template/tree/main).


## Setup

1. Install prerequisites 
   1. [uv](https://github.com/astral-sh/uv)
   2. [claude code](https://docs.anthropic.com/en/docs/claude-code/setup)
   3. make
       - On Windows, you can download it using [UniGetUI](https://github.com/marticliment/UnigetUI) and use [ezwinports make](https://github.com/microsoft/winget-pkgs/tree/master/manifests/e/ezwinports/make)
2. Start `claude` and run the command `/destructive-init`. Claude will ask you a few brief questions then customize the template for you.
3. Run `make`
   1. Note this might prompt you for your `sudo` password to install browser dependencies.
4. Setup your `.env` based on `.env.sample`
5. In `claude`, run the command `/prime`


# Roadmap

- [ ] Tool to fetch docs
- [ ] Claude Code SDK
