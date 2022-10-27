PHONY: .docker .docker-release

ifndef BIRTHDAY_BOT_TAG
override BIRTHDAY_BOT_TAG = birthday-bot
endif

docker: build
	docker build -t $(BIRTHDAY_BOT_TAG) .

docker-release: build
	docker buildx build --platform linux/amd64 -t alex4108/birthday-bot:$(BIRTHDAY_BOT_TAG) --push .