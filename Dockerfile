FROM python:3.9

RUN apt update -y && \
	apt install -y python3-pip traceroute iproute2 iptables

COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /home/pyns2

CMD [ "bash" ]
