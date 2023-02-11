tree:
	tree -I venv -I sample-files

cloc:
	cloc --exclude-dir=.pytest_cache,.vscode,sample-files,target,venv .

clean:
	cargo clean

.PHONY: tree cloc clean