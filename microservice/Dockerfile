# Example for Ubuntu container with Python3.10 Flask and PyODBC with a MSSQL ODBC driver
FROM ubuntu:22.04
MAINTAINER josejuan98

# Install python3.10, pip and pyomo solvers
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y apt-utils

# Solve -> Ubuntu 20.x, debconf: (TERM is not set, so the dialog frontend is not usable.)
RUN echo 'Solving dialog fronted not usable'
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata
RUN apt-get install -y libodbc1 unixodbc unixodbc-dev dialog curl

RUN apt-get install -y python3.10 && \
    apt-get install -y libpython3.10-dev && \
    apt-get install -y python3-pip && \
    apt-get install -y wget

# Modify symbolic link of python3 to run python3.10
RUN ln -fs /usr/bin/python3.10 /usr/bin/python3

# Solve broken dependencies after changing python version
RUN apt-get remove python3-apt -y

RUN apt-get autoremove -y && \
    apt-get install python3-apt -y

# Install python requirements
COPY ./requirements.txt /app/
COPY ./manifests /app/manifests/
COPY ./src /app/src/
COPY ./test /app/test/
COPY ./__init__.py /app/__init__.py

# Install python packages
# --no-cache-dir to keep the image as small as possible
RUN pip install --upgrade pip && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get autoremove && \
    apt-get autoclean


RUN python3.10 -m pip install --no-cache-dir -r /app/requirements.txt && \
    python3.10 -m pip cache purge

RUN echo "Finished installing requirements!"

# Environment variable, set in the azure-pipeline depending on the repo
ARG APP_ENV
ENV FLASK_ENV=$APP_ENV
ENV FLASK_APP=/app/src/app.py

# Port used for the Flask App
EXPOSE 80

# Port used by default by SQL Server
EXPOSE 1433

RUN echo "FLASK_ENV = $FLASK_ENV & FLASK_APP = $FLASK_APP"

WORKDIR /app/src/

# Use the entrypoint if other services won't start the service
# By not using it, you can test the container and use it in -it mode
# if not with the entrypoint it won't let you execute anything in -it
#ENTRYPOINT ["python3"]
#CMD ["app.py"]
