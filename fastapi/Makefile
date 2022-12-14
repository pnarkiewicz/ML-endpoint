SHELL = /bin/bash -c
VIRTUAL_ENV = $(PWD)/.venv
export BASH_ENV=$(VIRTUAL_ENV)/bin/activate

$(VIRTUAL_ENV):
	python3 -m venv $(VIRTUAL_ENV)

.PHONY:
	install clean synth diff deploy test lint

install: $(VIRTUAL_ENV)
	conda install numpy scipy matplotlib
	pip install -r requirements.txt

clean:
	[[ -d $(VIRTUAL_ENV) ]] && rm -rf $(VIRTUAL_ENV) || true
	[[ -d .pytest_cache ]] && rm -rf .pytest_cache || true
	[[ -d cdk.out ]] && rm -rf cdk.out || true
	[[ -f .coverage ]] && rm .coverage || true

synth:
	cdk synth

diff:
	cdk diff

deploy: test
	cdk deploy

test: lint
	pytest --cov --cov-report term-missing

lint:
	black .

 $(VERBOSE).SILENT:
