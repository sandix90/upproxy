FROM python:3.8-alpine

COPY . .
RUN apk --no-cache add gcc libc-dev libstdc++ build-base musl-dev
RUN pip install -r requirements.txt

EXPOSE 9000

RUN chmod 755 docker_entrypoint.sh

ENTRYPOINT ["./docker_entrypoint.sh"]