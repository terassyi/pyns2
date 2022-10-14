FROM ubuntu:latest

RUN apt update -y && \
	apt install -y iproute2 python3-pip traceroute iptables iputils-ping curl

COPY . /pyns2

RUN pip3 install -r /pyns2/requirements.txt && \
	pip3 install -e /pyns2 && \
	cp /pyns2/bin/pyns2 /usr/local/bin/pyns2

ENV XTABLES_LIBDIR=/usr/lib/x86_64-linux-gnu/xtables

CMD [ "tail", "-f", "/dev/null" ]
