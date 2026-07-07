# BlueArch Homebrew Tap

Public Homebrew tap for the BlueArch AWS tools.

This tap only publishes the public `bluearch-aws-*` packages.

## Install

```bash
brew tap bluearchio/tap
brew install bluearchio/tap/bluearch-aws-core
brew install bluearchio/tap/bluearch-aws-ops
brew install bluearchio/tap/bluearch-aws-tags
brew install bluearchio/tap/bluearch-aws-governance
```

During private pre-launch, a formula may remain disabled until that repo's first
public GitHub release updates the formula through the release automation.

Start the shared local runtime first:

```bash
bluearch-aws-core start --daemon
```

## Commands

The formula names are installed as commands:

- `bluearch-aws-core` starts and manages the shared local runtime.
- `bluearch-aws-ops` runs AWS operations scans and recommendations.
- `bluearch-aws-tags` runs tagging, lifecycle, and FinOps workflows.
- `bluearch-aws-governance` runs Governance Hub.

Core must be running before the product dashboards and backend commands can use
shared setup, account context, storage, and local API services.

## Formulas

- `bluearch-aws-core`: installs the shared local runtime.
- `bluearch-aws-ops`: installs the AWS operations CLI.
- `bluearch-aws-tags`: installs the AWS tagging and FinOps CLI.
- `bluearch-aws-governance`: installs the Governance Hub CLI.

Product formulas depend on `bluearch-aws-core`.

## Migrating From Earlier Private Installs

If your shell still finds an older locally installed binary first, remove that
old executable from your PATH and use the public command names above.

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

## Release Automation

Public release workflows update formulas by opening a pull request against this
tap after the signed macOS release asset is published. Configure each public repo
with `HOMEBREW_TAP_TOKEN_2`, scoped to `bluearchio/homebrew-tap` contents and pull
requests.

Pre-launch formulas may be disabled until their first public GitHub release is
cut. The release automation removes the disabled state when it writes the real
asset URL and SHA256.

## Security

Do not commit private buckets, signing credentials, tap tokens, internal release automation, or local paths that expose private account details. Report suspected vulnerabilities privately; see `SECURITY.md`.

## Repositories

- https://github.com/bluearchio/bluearch-aws-core
- https://github.com/bluearchio/bluearch-aws-ops
- https://github.com/bluearchio/bluearch-aws-tags
- https://github.com/bluearchio/bluearch-aws-governance
