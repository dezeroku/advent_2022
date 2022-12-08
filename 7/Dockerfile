FROM ubuntu:22.04
WORKDIR /custom-filesystem
ENV DATA_FILE=/data
ENV DATA_PREPROCESSED=/data-preprocessed
ENV FILESYSTEM_ROOT=/custom-filesystem

COPY solve-helper.sh /solve.sh

CMD ["/solve.sh"]
