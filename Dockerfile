# ubuntu as parent
FROM ubuntu
WORKDIR /curaengine-build
COPY install-curaengine.sh /curaengine-build
ENV NAME curaengine-build
CMD [ "apt-get", "install", "git", "sudo", "wget" ]
# starts bash just so we can keep it running with -dit
CMD [ "bash" ]