FROM python:3.10-alpine
# LABEL instruction creates labels.
LABEL "maintainer"="Petr Vavrin" "appname"="sysinfo"

ENV applocation /usr/src
COPY src/sysinfo $applocation/sysinfo
ENV app $applocation/sysinfo
WORKDIR $app/

RUN apk add --update python py-pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
#EXPOSE 5000
CMD ["python", "sysinfo.py"]
