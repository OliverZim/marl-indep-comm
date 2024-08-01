# Makefile

venv: .venv/touchfile


.venv/touchfile: requirements.txt
	test -d .venv || python3 -m venv ./.venv
	. .venv/bin/activate; pip install 'pip<24.1'; pip install 'setuptools<=66';	pip install 'wheel<=0.38.4'; pip install -Ur requirements.txt
	touch .venv/touchfile

clean:
	rm -rf .venv
	find -iname "*.pyc" -delete