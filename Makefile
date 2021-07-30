NAME=pyns2
VERSION=latest
CWD=`pwd`
WORKDIR=/home/pyns2

build:
	docker build -t $(NAME):$(VERSION) .

run:
	docker run -it --rm \
		--name $(NAME) \
		$(NAME):$(VERSION) bash

run-dev:
	docker run -it --rm \
		-v $(CWD)/:$(WORKDIR) \
		--name $(NAME) \
		--privileged=true \
		$(NAME):$(VERSION) bash

exec:
	docker exec -it $(NAME) bash

stop:
	docker rm -f $(NAME)

test:
	docker run -it --rm \
		-v $(CWD)/:$(WORKDIR) \
		--name $(NAME) \
		--privileged=true \
		$(NAME):$(VERSION) ./test.sh

clean:
	@if [ "$(image)" != "" ] ; then \
		docker rmi $(image); \
	fi
	@if [ "$(contener)" != "" ] ; then \
		docker rm $(contener); \
	fi
