FROM ubuntu:latest
MAINTAINER Andrew Krug "andrewkrug@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential libssl-dev libffi-dev python-dev
RUN apt-get install -y openssl-*
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["rp.py"]
