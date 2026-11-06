# Family Tree Builder

Create a small local genealogy graph with parent links, birth years, cycle checks, and JSON portability.

[![Build and verify](https://github.com/netcodermike/family-tree-builder/actions/workflows/verify.yml/badge.svg)](https://github.com/netcodermike/family-tree-builder/actions/workflows/verify.yml)

**Language:** Python · **Platform:** Windows, macOS, Linux desktop · **App type:** Desktop genealogy graph and local record editor

First-release learning implementation, with explicit scope below. This is one independently runnable app, not a placeholder in a combined repository.

## Features

- Named people and optional birth years
- At most two parent links per child
- Scrollable generation graph
- Validated JSON save/open

## Requirements

Python 3.11+ with Tkinter; no pip packages.

## Quick start

```sh
git clone https://github.com/netcodermike/family-tree-builder.git
cd family-tree-builder
python app.py
```

Commands run from the repository root. Lines marked for a particular operating system apply only there. Language tools are prerequisites, not installed by the app. Close desktop windows normally; terminal/server apps stop with Ctrl+C unless their usage notes say otherwise.

## Example workflow

Add three synthetic people, link two parents to a child, and try a reverse link to trigger cycle rejection. Save/open and inspect the scrollable graph.

## Architecture, configuration, and data

app.py validates version-1 people/edge records, rejects duplicate/self/cyclic parent links, and caps graphs at 200 people/400 edges. UUIDs identify people independently of names. Tkinter lays out generations by longest parent depth and draws arrows with scrollbars. Birth year 0 means unknown. Tests verify serialization and cycle rejection. No network or genealogy service is used.

## Verification

Build with the quick-start command where needed, then run:

```sh
python app.py --self-test
```

Manual acceptance: Add three synthetic people, link two parents to a child, and try a reverse link to trigger cycle rejection. Save/open and inspect the scrollable graph. Also test malformed inputs and an unwritable output destination.

See [validation record](docs/VALIDATION.md) for observed checks and their limits. CI results verify only what the workflow runs; they do not establish native GUI correctness or production readiness.

## Limitations and next steps

No person editing/deletion, partner relationships, source citations, ancestry inference, GEDCOM, photos, privacy sharing, autosave, or birth-year consistency rules. Names can duplicate; selectors show ID prefixes. Layout may have crossing edges. Records are ordinary plaintext JSON; unsaved changes are lost on close.

## Troubleshooting

Use the exact platform/toolchain above. Preserve originals and use synthetic fixtures first. Errors are displayed in the UI or stderr. A headless machine can run the model tests but cannot verify native GUI/audio behavior. Output paths are chosen explicitly; keep backups of important data.

## Source map

- `app.py`

## Development and license

Read [contributing](CONTRIBUTING.md) before changing the app, and [security/privacy](SECURITY.md) before supplying private data. Use synthetic fixtures for tests. No telemetry, paid API key, or account is required by the app itself. Dependencies, when present, are stated in Requirements.

[MIT license](LICENSE), copyright 2026 netcodermike.
