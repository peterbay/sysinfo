FROM python:3.10-alpine
# LABEL instruction creates labels.
LABEL "maintainer"="Petr Vavrin" "appname"="sysinfo"

ENV applocation /usr/src
COPY src/sysinfo $applocation/sysinfo
COPY src/tests $applocation/tests
ENV app $applocation/sysinfo
ENV tests $applocation/tests
WORKDIR $app/

RUN apk add --update python py-pip && \
     pip install --upgrade pip && \
     pip install -r requirements-test.txt && \
	 isort $app && \
	 black $app && \
	 autoflake --remove-all-unused-imports  --remove-duplicate-keys --expand-star-imports --recursive --in-place $app && \
	 flake8 --max-line-length=120 --max-complexity 8 $app && \
	 interrogate $app && \
	 mypy $app && \
	 pylint -d C0301 -d R0902 $app && \
	 pytest $tests && \
	 pytest --cov-report term-missing --cov=sysinfo $tests && \
	 safety check && \
	 bandit -r $app

#EXPOSE 5000
CMD ["python", "sysinfo.py"]
