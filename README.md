# My Company Consent demo application

This repository contains My Company demo app

### Data source with consent

This application uses the data product `draft/Company/Shareholders` from the
`digitalliving:v2` source on the `sandbox.ioxio-dataspace.com` dataspace. It requires a
consent to access the data, so before fetching it, the application is redirecting user
to the Consent Provider's verification page where the user will either accept or deny
the request.

Please note that only the `my-company` app uses consent, the `accountant` app uses the
`v1` source which does not require consent.

### Structure

- `./backend` - contains `FastAPI` application
- `./frontend` - contains `create-react-app` applications `./frontend/accountant` and
  `./frontend/my-company`
- `./nginx` - contains Nginx configuration files and templates

## Development

Generic pre-requisites for development

- [Pre-commit](https://pre-commit.com/#install)
- [Docker](https://docs.docker.com/install/)

To set up the `pre-commit` hooks, run `pre-commit install` in the repo. After that you
can manually run `pre-commit` only for your changes or `pre-commit run --all-files` for
all files.

### Backend

### Running Firestore emulator

- [Firebase CLI](https://firebase.google.com/docs/cli)

To install the `firebase` CLI run:

```bash
npm install -g firebase-tools
```

Run the Google Cloud Firestore Emulator with a predictable port:

```bash
./start_emulator.sh
# or on Windows run the .bat file
start_emulator
```

See `./backend/README.md`

### Frontend

See `./frontend/<app>/README.md`

## Local testing in Docker

This application is served by Nginx. It forwards requests to python backend or returns
static frontend files. In order to test how image will be running in production, you
might want to use the following snippet:

```shell script
export DOCKER_BUILDKIT=1  # optional
docker build -t mycompany-consent-demo .

# Firestore credentials will be set automatically when running on GCR
# But for local testing, please run the emulator on `localhost:8686` first
docker run --rm -p 8080:8080 -p 8686:8686 --env ENV=my-env --env FIRESTORE_EMULATOR_HOST=127.0.0.1:8686 --env OPENID_CONNECT_CLIENT_ID=some-id --env OPENID_CONNECT_CLIENT_SECRET=topsecret --name mycompany-consent-demo mycompany-consent-demo
```
