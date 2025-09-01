.DEFAULT_GOAL := install

.PHONY: all install first-time check upgrade

all: install check

install:
	pnpm install

first-time:
	pnpm install && pnpm dlx shadcn@latest init -f -d

check:
	pnpm lint && pnpm typecheck && pnpm prettier --write .

upgrade:
	pnpm update

clean:
	@rm -rf node_modules
