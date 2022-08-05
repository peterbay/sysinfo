# TODO adjust docker file exaple
# FROM instruction chooses the parent image for Docker.
# This example uses Alpine.
# Alpine is a minimal Docker image very small in size
FROM alpine:3.3
# LABEL instruction creates labels.
# The first label is maintainer with the value Linux Hint.
# The second label is appname with the value Flask Hello. World
# You can have as many key-to-value pairs as you want.
# You can also choose any name for the keys.
# The choice of maintainer and appname in this example
# is a personal choice.
LABEL "maintainer"="Linux Hint" "appname"="Flask Hello World"
# ENV instruction assigns environment variables.
# The /usr/src directory holds downloaded programs,
# be it source or binary before installing them.
ENV applocation /usr/src
# COPY instruction copies files or directories,
# from the Docker host to the Docker image.
# You'll copy the source code to the Docker image.
# The command below uses the set environment variable.
COPY src/sysinfo $applocation/sysinfo
COPY src/tests $applocation/tests
# Using the ENV instruction again.
ENV flaskapp $applocation/sysinfo
# WORKDIR instruction changes the current directory in Docker image.
# The command below changes directory to /usr/src/flask-helloworld.
# The target directory uses the environment variable.
WORKDIR $flaskapp/
# RUN instruction runs commands,
# just like you do on the terminal,
# but in the Docker image.
# The command below installs Python, pip and the app dependencies.
# The dependencies are in the requirements.txt file.
RUN apk add --update python py-pip
RUN pip install --upgrade pip
RUN pip install -r requirements-test.txt
# EXPOSE instruction opens the port for communicating with the Docker container.
# Flask app uses the port 5000, so you'll expose port 5000.
EXPOSE 5000
# CMD instruction runs commands like RUN,
# but the commands run when the Docker container launches.
# Only one CMD instruction can be used.
CMD ["python", "sysinfo.py"]
