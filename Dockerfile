# ----- React build ----- #
FROM digitallivinginternational/nodejs-base:ubuntu20.04-node14 AS mycompany-frontend

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome

RUN set -exu \
 && apt-get update \
 && curl -o google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
 && dpkg -i google-chrome.deb || true \
 && apt-get install -yf \
 && rm -rf /root/.cache \
 && rm -rf /var/lib/apt/lists/* \
 && :

WORKDIR /src/frontend/my-company

# Install dependencies
ADD frontend/my-company/package.json frontend/my-company/pnpm-lock.yaml ./
RUN set -exu \
 && pnpm install --frozen-lockfile \
 && pnpm add puppeteer@1.19.0 \
 && rm -rf /root/.cache \
 && :

# Build the frontend
ADD frontend/my-company ./
RUN pnpm run build

# ----- React build ----- #
FROM digitallivinginternational/nodejs-base:ubuntu20.04-node14 AS accountant-frontend

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome

RUN set -exu \
 && apt-get update \
 && curl -o google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
 && dpkg -i google-chrome.deb || true \
 && apt-get install -yf \
 && rm -rf /root/.cache \
 && rm -rf /var/lib/apt/lists/* \
 && :

WORKDIR /src/frontend/accountant

# Install dependencies
ADD frontend/accountant/package.json frontend/accountant/yarn.lock ./
RUN set -exu \
 && pnpm install --frozen-lockfile \
 && pnpm add puppeteer@1.19.0 \
 && rm -rf /root/.cache \
 && :

# Build the frontend
ADD frontend/accountant ./
RUN pnpm run build


# ----- Server build ----- #

FROM digitallivinginternational/python-base:ubuntu-python3.9 AS mycompany-backend

WORKDIR /src/backend

# Attempt to fix brotli issues
# https://github.com/python-poetry/poetry/issues/3336#issuecomment-831789763
RUN su "${USER}" -c ". ${POETRY_HOME}/env; poetry config experimental.new-installer false"

ADD docker/build-prepare.sh /src/docker/build-prepare.sh
RUN bash /src/docker/build-prepare.sh

ADD docker/build-setup.sh /src/docker/build-setup.sh
ADD backend/pyproject.toml backend/poetry.lock ./
RUN --mount=type=cache,target=/home/${USER}/.cache bash /src/docker/build-setup.sh


# ----- Runtime environment ----- #

FROM digitallivinginternational/python-base:ubuntu20.04-python3.9-nginx as mycompany-runtime

# Copy Nginx configs
RUN rm -rf /etc/nginx/conf.d /etc/nginx/http.d
ADD nginx/ /etc/nginx/

# Copy results from build environments
COPY --from=mycompany-frontend /src/frontend/my-company/build/ /src/frontend/my-company/
COPY --from=accountant-frontend /src/frontend/accountant/build/ /src/frontend/accountant/
COPY --from=mycompany-backend ${WORKON_HOME} ${WORKON_HOME}

# Run docker/runtime-prepare.sh
WORKDIR /src/backend
ADD \
    docker/runtime-prepare.sh \
    docker/runtime-entrypoint.sh \
    docker/nginx-entrypoint.sh \
    /src/docker/

# Copy all the backend code over
ADD backend ./
RUN bash /src/docker/runtime-prepare.sh

USER ${USER}
EXPOSE 8080
ENTRYPOINT ["bash", "/src/docker/runtime-entrypoint.sh"]
