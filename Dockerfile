ARG BASE_IMAGE=ubuntu:22.04
FROM ${BASE_IMAGE}

ENV DEBIAN_FRONTEND=noninteractive

ARG STATICJINJAPLUS_VERSION="latest"
ARG STATICJINJAPLUS_COMMIT="main"
ARG STATICJINJAPLUS_CHECKSUM=""
ARG CACHE_BUST=1


RUN if [ "${BASE_IMAGE#python:}" = "${BASE_IMAGE}" ]; then \
        apt-get update && \
        apt-get install -y --no-install-recommends \
            python3 \
            python3-pip \
            python3-venv && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
        ln -s /usr/bin/python3 /usr/bin/python; \
    fi

WORKDIR /app


ADD --checksum=sha256:${STATICJINJAPLUS_CHECKSUM} \
    https://github.com/MrDave/StaticJinjaPlus/archive/${STATICJINJAPLUS_COMMIT}.tar.gz \
    /app/package.tar.gz


RUN tar -xzf /app/package.tar.gz -C /app --strip-components=1 && \
    rm /app/package.tar.gz


RUN if [ "${BASE_IMAGE#python:}" = "${BASE_IMAGE}" ]; then \
        pip3 install --break-system-packages --no-cache-dir -r requirements.txt; \
    else \
        pip install --break-system-packages --no-cache-dir -r requirements.txt; \
    fi

ENTRYPOINT ["python", "main.py"]