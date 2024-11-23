# Event Booking


## Generate private and open keys:

```shell
openssl genrsa -out private.pem 2048
```

```shell
openssl rsa -in private.pem -outform PEM -pubout -out public.pem
```

## Running in docker container

```shell
docker-compose up --build
```