# Camels Data API server

## Run the pre-build image

```
docker run -it --rm -p 5050:5000 -v <path/to/camels/data>:/srv/dev ghcr.io/camels-de/camels_serv
```

## Build local docker image
To build docker locally:

```bash
docker build -t camels_serv .
```

Run local build
```bash
docker run -it --rm -p 5050:5000 -v <path/to/camels/data>:/srv/dev camels_serv
```

Then ie. point the browser to `http://localhost:5050/pegel.json`
