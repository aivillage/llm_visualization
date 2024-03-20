FROM python:3.10-slim-bookworm as build

WORKDIR /opt/llm_dissection

# hadolint ignore=DL3008
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev \
        libssl-dev \
        git \
        nodejs \
        npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"


COPY . /opt/llm_dissection

RUN pip install --no-cache-dir -r requirements.txt
RUN /bin/bash build.sh

FROM python:3.10-slim-bookworm as release
WORKDIR /opt/llm_dissection

# hadolint ignore=DL3008

RUN mkdir -p /opt/llm_dissection/  /opt/llm_dissection/app

RUN useradd \
    --no-log-init \
    --shell /bin/bash \
    -u 1001 \
    llm_dissection \
    && mkdir -p /var/log/llm_dissection /var/uploads \
    && chown -R 1001:1001 /var/log/llm_dissection /var/uploads /opt/llm_dissection/app
    

COPY --chown=1001:1001 --from=build /opt/venv /opt/venv
COPY --chown=1001:1001 --from=build /opt/llm_dissection/logging.yml /opt/llm_dissection/logging.yml
ENV PATH="/opt/venv/bin:$PATH"

USER 1001
EXPOSE 8000
ENTRYPOINT ["uvicorn", "app.admin.main:admin_app", "--reload", "--host", "0.0.0.0", "--log-config", "logging.yml"]
