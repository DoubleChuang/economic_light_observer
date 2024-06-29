# Economic Light Observer

## How to use
Create a .env file, and modify the configuration in the file

```
LINE_NOTIFY_TOKEN=YOUR_LINE_TOKEN
```

Build docker image from source code

```
docker build -t economic_light_observer .
```

Run image as a container

```
docker run --rm --name economic_light_observer --env-file .env economic_light_observer
```

Run by Docker Images built with GitHub Actions

```
docker run --rm --name economic_light_observer --env-file .env ghcr.io/doublechuang/economic_light_observer:latest
```


## Issue

💡 **Q:** **Pyppeteer doesn't work in docker image**

> Because Pyppeteer uses the `--no-sandbox` parameter to execute chromium, the docker image needs to install some dependencies
> https://github.com/pyppeteer/pyppeteer/issues/194#issuecomment-739012427

💡 **Q:** **Pyppeteer doesn't support ARM**
 
> I added support for arm and arm64 platforms to the source code of `pyppeteer` to solve this problem.
> https://github.com/pyppeteer/pyppeteer/pull/478
