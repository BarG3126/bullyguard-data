FROM python:3.10-slim

ARG USER_ID
ARG USER_NAME
ENV HOME=/home/${USER_NAME} \
    VIRTUAL_ENV=/home/${USER_NAME}/venv \
    PYTHONPATH=/app

ENV \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    TZ=Asia/Jerusalem \
    PATH="/usr/local/gcloud/google-cloud-sdk/bin:${HOME}/.local/bin:${VIRTUAL_ENV}/bin:${PATH}" \
    PYTHONPATH="/app:${PYTHONPATH}" \
    BUILD_POETRY_LOCK="${HOME}/poetry.lock.build"

RUN apt-get update \
    && apt-get -qq -y install vim gcc curl git build-essential libb64-dev software-properties-common \
    && rm -rf /bar/lib/apt/lists/* \
    && apt-get -qq -y clean

RUN curl https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-426.0.0-linux-x86_64.tar.gz > /tmp/google-cloud-sdk.tar.gz
RUN mkdir -p /usr/local/gcloud \
    && tar -C /usr/local/gcloud -xf /tmp/google-cloud-sdk.tar.gz \
    && /usr/local/gcloud/google-cloud-sdk/install.sh --usage-reporting false --command-completion true --bash-completion true --path-update true --quiet

RUN addgroup --system --gid ${USER_ID} ${USER_NAME} \
    && useradd --system -m --no-log-init --home-dir ${HOME} --uid ${USER_ID} --gid ${USER_NAME} --groups ${USER_NAME} ${USER_NAME}

RUN chown -R ${USER_NAME}:${USER_NAME} ${HOME}
RUN mkdir -p /app && chown -R ${USER_NAME}:${USER_NAME} /app /tmp

RUN curl -sSL https://install.python-poetry.org | HOME=${HOME} python3 - --version 1.7.1

USER ${USER_NAME}

COPY pyproject.toml *.lock /app/
WORKDIR /app

RUN poetry config virtualenvs.create false \
    && python3.10 -m venv ${VIRTUAL_ENV} \
    && python3.10 -m pip install --upgrade pip setuptools \
    && poetry install && cp poetry.lock ${BUILD_POETRY_LOCK} \
    && rm -rf ${HOME}/.cache/*

USER root
COPY ./docker/scripts/* /
RUN chown -R ${USER_NAME} /*.sh && chmod +x /*.sh
USER ${USER_NAME}

COPY . /app/
CMD ["/startup-script.sh"]

# Note: when build&run image for the first time, you should define ssh remore connection to github using:
# 'git remote set-url origin git@github.com:BarG3126/bullyguard-data.git' using the ssh.pub file.
# make sure you have defines the ssh located in: cat ~/.ssh/id_ed25519.pub inside github keys.
# if there's no existing key - use : 'ssh-keygen -t ed25519 -C "bar3126@gmail.com"'


RUN git config --global user.email "bar3126@gmail.com" \
    && git config --global user.name "BarG3126"
