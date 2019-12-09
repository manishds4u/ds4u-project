# Pull the base image
FROM python:3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /codepred
WORKDIR /codepred
#Upgrade pip
RUN pip install pip -U
ADD requirements.txt /codepred/
#Install dependencies
RUN pip install -r requirements.txt
ADD . /codepred/