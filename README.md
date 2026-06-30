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

## Repositories

- https://github.com/bluearchio/bluearch-aws-core
- https://github.com/bluearchio/bluearch-aws-ops
- https://github.com/bluearchio/bluearch-aws-tags
- https://github.com/bluearchio/bluearch-aws-governance
