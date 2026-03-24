# CI integration tests (Webex) — maintainer notes

This document describes how the GitHub Actions **Build and Test** workflow authenticates to Webex and which settings must be aligned so the suite can run against a shared org.

## Webex integration and org (stakeholder alignment)

Before running CI against a Webex org, maintainers should agree on:

- **Integration (Developer portal):** A single Webex integration used for **CI only** (bot or service user), with OAuth scopes sufficient for the API tests in `tests/api/`.
- **Control Hub org:** The org that hosts test users, licenses (e.g. **Advanced Messaging** where required by tests), and admin actions for people/rooms. Document who can grant licenses and manage the integration.
- **Rotation:** Multiple repository admins should have GitHub permission to manage **Environment secrets** for the `webex-ci` environment so updates are not blocked by a single person.

## GitHub Environment: `webex-ci`

Create a GitHub [Environment](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment) named **`webex-ci`** (or rename the workflow to match if you choose a different name).

1. In the repo or organization: **Settings → Environments → New environment**.
2. Add **several** trusted maintainers as admins who can edit secrets and variables.
3. Configure **Environment secrets** and **Environment variables** as below (or move secrets from the old `chris-1xrn.wbx.ai` environment after migrating).

### Variables (GitHub Environment or repository)

| Variable | Purpose |
|----------|---------|
| `WEBEX_TEST_DOMAIN` | Email domain used for synthetic test addresses (see `tests/environment.py`). |
| `WEBEX_TEST_ID_START` | Starting index for generated test email addresses. |
| `WEBEX_TEST_FILE_URL` | URL of a downloadable file used by fixtures. |

### Secrets (GitHub Environment)

| Secret | Required | Purpose |
|--------|----------|---------|
| `WEBEX_GUEST_ISSUER_ID` | Yes | Guest issuer for tests that need it. |
| `WEBEX_GUEST_ISSUER_SECRET` | Yes | Guest issuer secret. |
| `WEBEX_CLIENT_ID` | Yes for OAuth path | Webex integration OAuth client ID. |
| `WEBEX_CLIENT_SECRET` | Yes for OAuth path | Webex integration OAuth client secret. |
| `WEBEX_REFRESH_TOKEN` | Yes for OAuth path | OAuth refresh token for the CI user/bot (obtained via authorization code flow). |
| `WEBEX_ACCESS_TOKEN` | Optional | **Alternative:** If set, the workflow uses this token directly and skips the OAuth refresh step (useful for short-term testing or when refresh setup is not ready). Prefer OAuth refresh for production CI. |

**Deprecated:** `WEBEX_TOKEN_KEEPER_URL` is no longer used by CI. The legacy keeper-based workflow is archived under [`docs/ci/legacy/`](legacy/README.md).

## Obtaining and rotating OAuth refresh tokens

1. In the [Webex Developer Portal](https://developer.webex.com/), open your CI integration and note **Client ID** and **Client Secret**.
2. Complete the OAuth **authorization code** flow for the CI identity to obtain an initial `access_token` and `refresh_token`.
3. Store `WEBEX_CLIENT_ID`, `WEBEX_CLIENT_SECRET`, and `WEBEX_REFRESH_TOKEN` in the `webex-ci` environment secrets.
4. The workflow exchanges the refresh token at **`POST https://webexapis.com/v1/access_token`** (`grant_type=refresh_token`). If the response includes a new `refresh_token`, update the secret in GitHub.

If refresh fails (invalid grant, revoked token), repeat the authorization code flow and update `WEBEX_REFRESH_TOKEN`.

## Fork and pull request limitations

- **Secrets are not available to workflows triggered from forks** by default. Contributors pushing from a fork will not run integration tests with real Webex credentials unless you use a different, carefully reviewed pattern (e.g. `pull_request_target` with strict guards — not recommended without security review).
- **Practical approach:** Run full integration tests on branches in the **main repository** (e.g. maintainer branches), or rely on scheduled runs / `push` to `main` after merge.

## Legacy reference

The previous token-keeper workflow (`WEBEX_TOKEN_KEEPER_URL`, environment `chris-1xrn.wbx.ai`) is preserved for reference only:

- [`docs/ci/legacy/build-and-test.token-keeper.yml`](legacy/build-and-test.token-keeper.yml)
- [`docs/ci/legacy/README.md`](legacy/README.md)
