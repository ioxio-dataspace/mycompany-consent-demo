# MyCompany consent backend

## Development

Additional dependencies:

- [Python >=3.9](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org)

To install the dependencies:

```bash
poetry install
```

If you need authentication to work locally, you'll need to set the
`OPENID_CONNECT_CLIENT_ID` and `OPENID_CONNECT_CLIENT_SECRET` environment variables.
This can also be done by storing them in a file called `.env` with content like this:

```bash
OPENID_CONNECT_CLIENT_ID='some-client-id'
OPENID_CONNECT_CLIENT_SECRET='super-secret'
```

Then to run the code:

```bash
poetry run invoke dev
```

Or to run the tests:

```bash
poetry run invoke test
```
