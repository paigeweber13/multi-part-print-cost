# ubuntu as parent
FROM ubuntu
WORKDIR /curaengine-build
COPY install-curaengine.sh /curaengine-build
ENV NAME curaengine-build
RUN apt-get update
# requirements that most linux distros have, but the docker image does
RUN apt-get install -y git sudo autoconf wget g++
# requirements listed in the github pages
RUN apt-get install -y libtool cmake python3-dev python3-sip-dev
# RUN cd ./curaengine-build
RUN chmod +x ./install-curaengine.sh
RUN ./install-curaengine.sh
# starts bash just so we can keep it running with -dit
CMD [ "bash" ]