.DEFAULT_GOAL := install

.PHONY: all install first-time check upgrade run

all: install check

install:
	pnpm install

check:
	pnpm lint && pnpm typecheck && pnpm prettier --write .

upgrade:
	pnpm update
