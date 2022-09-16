## My Company consent demo app

Is made to be easy customized and deployed. Using [theme-ui](https://theme-ui.com/home)
to achieve highly customizible UI.

### Installation

```
pnpm
```

### Development

Create `frontend/.env` file with the following content:

```dotenv
PUBLIC_URL=/my-company
```

Then run:

```
pnpm start
```

```
pnpm build
```

### UI Customization

Places to look at:

- `theme/*`
- `components/*`

### Consent provider caveat

When redirecting user to a Consent Provider, application must tell it a `returnUrl`
where user will land after approving/denying the consent request. Consent Provider will
add some query parameter to this URL, e.g. `status=fail&error=text` or `status=ok`.

Right now there is no special frontend page for that redirect, so user will go back
where it started. It's OK for demo purposes, but in production probably it's better to
create a separate page for that.
