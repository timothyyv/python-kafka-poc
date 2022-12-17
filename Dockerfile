# pull base image
FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set working dir
WORKDIR /app

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN export LDFLAGS="-L/usr/local/opt/openssl/lib"
RUN pip install -r requirements.txt

COPY entrypoint.sh /app/entrypoint.sh

# copy project from base into docker workdir
COPY . /app

# RUN chmod +x /app/entrypoint.sh
ENTRYPOINT /app/entrypoint.sh