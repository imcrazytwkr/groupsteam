mkfile_dir := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))

prefix = ${HOME}/.local

.PHONY: format link

clean:
	git clean -d -f -x

format:
	find '$(mkfile_dir)' -type f -iname '*.py' -print0 | xargs -0 black

link: format
	install -dm755 '$(prefix)/bin'
	echo -s -T '$(mkfile_dir)/groupsteam.py' '$(prefix)/bin/groupsteam'
