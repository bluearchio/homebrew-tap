# BlueArch Homebrew Tap

Public Homebrew tap for the BlueArch AWS tools.

## Install

```bash
brew tap bluearchio/tap
brew install bluearchio/tap/bluearch-aws-core
brew install bluearchio/tap/bluearch-aws-ops
brew install bluearchio/tap/bluearch-aws-tags
brew install bluearchio/tap/bluearch-aws-governance
```

Start the shared local runtime first:

```bash
bluearch-core start --daemon
```

## Formulas

- `bluearch-aws-core`: installs the `bluearch-core` local runtime.
- `bluearch-aws-ops`: installs the `bluearch` AWS operations CLI.
- `bluearch-aws-tags`: installs the `tag-manager` AWS tagging and FinOps CLI.
- `bluearch-aws-governance`: installs the `cloud-governance` Governance Hub CLI.

Product formulas depend on `bluearch-aws-core`.

## Update

```bash
brew update
brew upgrade bluearchio/tap/bluearch-aws-core
brew upgrade bluearchio/tap/bluearch-aws-ops
brew upgrade bluearchio/tap/bluearch-aws-tags
brew upgrade bluearchio/tap/bluearch-aws-governance
```

## Uninstall

```bash
brew uninstall bluearch-aws-governance bluearch-aws-tags bluearch-aws-ops bluearch-aws-core
brew untap bluearchio/tap
```

## Validate Formula Changes

```bash
for formula in Formula/*.rb; do ruby -c "$formula"; done
```

Before changing a formula, confirm the URL points to a public GitHub release asset and the SHA256 was computed from that exact asset.

## Security

Do not commit private buckets, signing credentials, tap tokens, internal release automation, or local paths that expose private account details. Report suspected vulnerabilities privately; see `SECURITY.md`.

## Repositories

- https://github.com/bluearchio/bluearch-aws-core
- https://github.com/bluearchio/bluearch-aws-ops
- https://github.com/bluearchio/bluearch-aws-tags
- https://github.com/bluearchio/bluearch-aws-governance
