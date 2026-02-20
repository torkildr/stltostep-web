FROM buildpack-deps:stable AS builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    cmake

RUN git clone https://github.com/slugdev/stltostp.git \
 && cd stltostp \
 && cmake . \
 && make

FROM python:3-slim

COPY --from=builder /stltostp/stltostp /web/stltostp
WORKDIR /web
EXPOSE 8000

RUN pip install legacy-cgi

COPY server.py /web/
COPY index.html /web/

ENTRYPOINT /web/server.py

