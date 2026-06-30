# Security Policy

## Supported Versions

Security fixes are provided for the current formulas in `main`.

## Reporting A Vulnerability

Do not open a public issue for a suspected vulnerability. Report it privately through GitHub Security Advisories for this repository, or email the maintainers if advisories are not enabled yet.

Include:

- Formula name and version.
- Release asset URL.
- Expected and actual impact.
- Whether checksum, binary provenance, local files, or credentials are involved.

## Maintainer Checklist

- Keep GitHub secret scanning and Dependabot enabled.
- Update formula URL, version, and SHA256 together.
- Verify release assets are public before merging formula updates.
- Do not commit private tap tokens, private buckets, signing credentials, or internal release automation.
