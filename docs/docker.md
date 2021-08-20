# FlightDynamics with docker
These instructions assume the following:

1. `docker` and `docker-compose` are available in the operating system.
2. Pulling containers from `docker-hub` is possible.

## The flight dynamics tool
The flight dynamics software is a `Fortran` based tool, which simulates different flight paths for a `UAV`.

We have created a docker based solution that pre-packages the flight dynamics tool by `SWRI` and lets domain scientists experiment with fixed bemp designs. The mass/inertial properties of the design are estimated using a `PTC-CREO-Surrogate`.


## Deployment Instructions (Manual)
In your system, download the volume (Containing the `propellers` data and `CREO-Surrogate` testbench data) using the following [`url`](https://vanderbilt.box.com/v/fdm-volume-data). Unzip the file and save it to a reachable path in your system.

After unzipping the file, use the copy the following contents to a file `docker-compose.yaml` and replace `YOUR_PATH` with the location that you unzipped the file to.

```yaml
version: "3.9"
services:
  symbench_athens_client:
    image: symbench/symbench-athens-client:latest
    ports:
      - "8888:8888"
    volumes:
      - YOUR_PATH:/home/anaconda/data
    container_name: symbench_athens_client
```

Once done, open up a terminal instance and use the following command to run the container
```shell
$ cd path_to_docker_compose_file
$ docker-compose --file docker-compose.yaml up -d
```

If there are no errors, navigate to [`127.0.0.1:8888`](http://127.0.0.1:8888). If prompted for a `password`
enter `symcps2021`.

An example usage notebook is available in the server itself.

## Updating
Follow the similar process as above for downloading the testbench and propellers data and unzip it to the same previous location.

```shell
$ docker-compose --file docker-compose.yaml down
$ docker-compose --file docker-compose.yaml rm -f
$ docker-compose --file docker-compose.yaml pull
$ docker-compose --file docker-compose.yaml up -d
```
