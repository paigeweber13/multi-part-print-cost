# Dependencies:
## install-curaengine.sh
Should automatically get dependencies. Tested on Ubuntu, should work on all
debian-based distributions. If you are on another distribution, dependencies
include:
 - libtool
 - cmake
 - python3 development headers
 - python3-sip development headers

 # To Start Docker Image:
```
docker build -t=curaengine-build .
docker run --name my-curaengine-build -dit curaengine-build
```

To get a shell inside this image, run `docker exec -it my-curaengine-build bash
`