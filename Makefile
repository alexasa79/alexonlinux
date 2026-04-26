.PHONY: all build serve

HUGO ?= hugo
CACHEDIR ?= /tmp/hugo-cache-alexonlinux
LOCAL_BASEURL ?= http://localhost:1313/alexonlinux.com/

all: build

build:
	$(HUGO) --cacheDir $(CACHEDIR)

serve:
	$(HUGO) server --cacheDir $(CACHEDIR) --baseURL $(LOCAL_BASEURL)
