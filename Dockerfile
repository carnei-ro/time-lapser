FROM alpine:3.18

RUN apk add aws-cli ffmpeg coreutils py3-requests --no-cache

COPY entrypoint.sh /entrypoint.sh
COPY telegram.py /telegram.py

WORKDIR /data

ENTRYPOINT ["/entrypoint.sh"]
