# Contributing

Thanks for helping improve the BlueArch Homebrew tap.

## Validate Formulas

```bash
for formula in Formula/*.rb; do ruby -c "$formula"; done
```

Before merging release updates:

- Confirm the release asset URL is public.
- Confirm the SHA256 matches the exact uploaded asset.
- Keep formula names aligned with the public repositories.
- Do not add private buckets, signing credentials, tap tokens, or internal release automation.

## Pull Requests

- Keep formula updates focused on one release set.
- Include the command used to compute each SHA256.
- Update the README if formula names or install commands change.
