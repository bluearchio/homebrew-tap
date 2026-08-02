# BlueArch Homebrew Tap

Public Homebrew tap for the BlueArch AWS tools.

This tap only publishes the public `bluearch-aws-*` packages.

## Install

```bash
brew install bluearchio/tap/bluearch-aws-core
brew install bluearchio/tap/bluearch-aws-ops
brew install bluearchio/tap/bluearch-aws-tags
brew install bluearchio/tap/bluearch-aws-governance
```

A fully qualified install automatically adds the tap and trusts only the named
formula. Install Core first so Homebrew records formula-specific trust before it
resolves a product's Core dependency. You do not need to trust the whole tap.

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
python3 -m unittest discover -s tests -v
brew style bluearchio/tap
brew audit --strict --tap=bluearchio/tap
brew readall --no-simulate bluearchio/tap
```

Before changing a formula, confirm the URL points to an immutable public release
asset and the SHA256 was computed from that exact asset. Pull requests also install
and test every formula on a clean ARM64 macOS runner, verify the published version,
and reject legacy private executable names.

## Release Automation

Public release workflows update formulas by opening a pull request against this
tap after the signed macOS release asset is published. Configure each public repo
with `HOMEBREW_TAP_TOKEN_2`, scoped to `bluearchio/homebrew-tap` contents and pull
requests.

Pre-launch formulas may be disabled until their first public GitHub release is
cut. The release automation removes the disabled state when it writes the real
asset URL and SHA256.

### One-Way Legacy Bootstrap

[`config/legacy-dist-exceptions.json`](config/legacy-dist-exceptions.json)
temporarily enables the four exact, checksum-pinned `dist.bluearch.io` archives
that predate the strict public version identity. The approved version, URL, and
SHA256 tuples remain hardcoded in the verifier; adding a name to the JSON file
cannot authorize any other artifact. Each tuple must also emit its exact known
legacy version output sequence.

Every formula update must pass that config to `scripts/update_formula.py`. The
updater removes only the released product from the sorted exception list, and
the generated release PR stages both the formula and config changes. The required
repository contract compares each pull request with its base revision and permits
the enabled set only to shrink. The first bootstrap is accepted only when all four
hardcoded names and tuples match exactly. Once an exception is removed, restoring
the old dist formula or re-adding its name fails CI. GitHub Release URLs never use
this compatibility path and must emit exactly one public `bluearch-aws-*` version
identity.

Formula `version` values intentionally omit the tag's leading `v` because
`brew style` rejects that prefix. This one-time normalization does not add a
formula revision, and the new product version PRs replace the legacy entries,
minimizing unnecessary reinstall exposure during the rollout.

The formula updater accepts stable `vX.Y.Z` release tags only. Prerelease and
build-metadata tags are rejected so the updater, formulas, and version verifier
share one release-version contract.

### One-Time Repository Settings

The product release workflows open a formula pull request and request squash
auto-merge. Configure this repository once before cutting a product release:

1. Enable **Allow auto-merge** and **Allow squash merging** in the repository's
   pull-request settings.
2. Protect `main` with a branch protection rule or ruleset.
3. Require changes to `main` to arrive through a pull request and disallow force
   pushes and branch deletion.
4. Require these exact status-check contexts: `Tap release gate`, `gitleaks`,
   and `Analyze Ruby` (shown under the CI, Secret Scan, and CodeQL workflows,
   respectively). The stable tap gate depends on these individual CI checks:
   `Repository contract`, `Formula quality`, `Install bluearch-aws-core`,
   `Install bluearch-aws-ops`, `Install bluearch-aws-tags`, and
   `Install bluearch-aws-governance`.

Auto-merge will then wait for every formula check to pass before GitHub performs
the squash merge. These are repository settings; release workflows must not
weaken or bypass them.

## Security

Do not commit private buckets, signing credentials, tap tokens, internal release automation, or local paths that expose private account details. Report suspected vulnerabilities privately; see `SECURITY.md`.

## Repositories

- https://github.com/bluearchio/bluearch-aws-core
- https://github.com/bluearchio/bluearch-aws-ops
- https://github.com/bluearchio/bluearch-aws-tags
- https://github.com/bluearchio/bluearch-aws-governance
