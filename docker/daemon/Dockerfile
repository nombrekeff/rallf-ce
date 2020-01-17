FROM debian:buster
ENV DEBIAN_FRONTEND noninteractive

RUN apt update && apt install -y python3 python3-pip procps

RUN pip3 install docker
RUN pip3 install werkzeug
RUN pip3 install json-rpc

COPY . /incubator
WORKDIR /incubator

CMD ["/incubator/docker/daemon/docker-entrypoint.sh"]