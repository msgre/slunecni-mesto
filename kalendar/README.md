build
docker build . -t msgre/kindle-kalendar

shell
docker run --rm -ti --entrypoint bash -v $PWD:/app msgre/kindle-kalendar

webserver
docker run --rm -ti -p 8085:8085 -v $PWD:/app msgre/kindle-kalendar
