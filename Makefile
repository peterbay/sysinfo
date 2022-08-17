NAME=sysinfo
IMAGE_NAME=sysinfo

ifndef VERSION
VERSION := $(shell python3 -c "from setup import find_version;find_version("src/sysinfo/__init__.py")" || echo 0.0.0)
endif

ifndef BRANCH
BRANCH := $(shell git branch --show-current)
endif

ifndef COMMIT
COMMIT := $(shell git log -n1 --format="%h")
endif

ifndef SRC
SRC := src/sysinfo/*.py
endif

ifndef TESTS
TESTS := src/tests
endif

BUILD_RUN=docker run --rm "$(IMAGE_NAME):$(COMMIT)"

.PHONY: git black lint build test coverage security

git:
	@echo $(branch: [$(BRANCH)] commit: [$(COMMIT)])

black:
	isort $(SRC)
	black $(SRC)
	autoflake --remove-all-unused-imports  --remove-duplicate-keys --expand-star-imports --recursive --in-place $(SRC)

lint:
	flake8 --max-line-length=120 --max-complexity 8 $(SRC)
	interrogate $(SRC)
	mypy $(SRC)
	pylint -d C0301 -d R0902 $(SRC)

build:
	python setup.py build

install:
	python setup.py install

build_docker:
	docker build -t $(IMAGE_NAME):$(COMMIT) . -f docker/build.Dockerfile

test_docker:
	docker build -t $(IMAGE_NAME):$(COMMIT) . -f docker/test.Dockerfile

test:
	pytest $(TESTS)

coverage:
	pytest --cov-report term-missing --cov=sysinfo $(TESTS)

security:
	safety check
	bandit -r $(SRC)
