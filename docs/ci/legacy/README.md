# Legacy CI workflow (reference only)

This directory preserves a snapshot of the **pre-migration** GitHub Actions workflow that obtained a Webex access token by calling an external HTTP endpoint (`WEBEX_TOKEN_KEEPER_URL`) and used the GitHub Environment `chris-1xrn.wbx.ai`.

- **Retired:** 2026-03-24 (archived for archaeology; not executed by GitHub Actions).
- **Not executed:** Files here are outside `.github/workflows/` on purpose so they do not register as workflows.
- **Replaced by:** [`.github/workflows/build-and-test.yml`](../../../.github/workflows/build-and-test.yml) using OAuth `refresh_token` grant (or optional static `WEBEX_ACCESS_TOKEN` secret) against the `webex-ci` GitHub Environment. See [`../MAINTAINERS.md`](../MAINTAINERS.md).
