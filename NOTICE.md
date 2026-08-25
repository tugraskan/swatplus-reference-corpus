# Notices

## SWAT+

The SWAT+ Reference Corpus is an independent project and is not the official
SWAT+ documentation repository.

The source analyzed by this version of the corpus comes from:

- Repository: <https://github.com/swat-model/swatplus>
- Branch selected during preparation: `main`
- Pinned commit: `cb442f7c05fc3bfc34349c446010f452d2737ca0`
- Commit date: 2026-07-06

SWAT+ source code is not included in this repository. The `swatref source fetch`
command retrieves configured sources into ignored local directories. At the
pinned commit, the upstream repository contains the GNU Lesser General Public
License version 2.1 in its `LICENSE` file. Refer to the upstream repository for
its complete copyright and licensing notices.

Release schema 62.0.0 is generated from SWAT+ tag `62.0.0`, commit
`de210d64db4f1d75e110bd6af33ea9c333d27b8a`. The Editor comparison report is
derived from a read-only SWAT+ Editor checkout and records that checkout's exact
commit. Neither upstream source tree is redistributed here.

## Corpus provenance

The initial prose corpus was migrated from a reviewed, overlay-based
documentation workflow and then expanded and mechanically checked against the
SWAT+ source fact store. Source-derived signatures, declarations, call graphs,
line spans, and source links are regenerated from the pinned upstream commit.

The tracked modular-database CSV is the reviewed input used to attach parameter
ranges and build field crosswalks. Range and field reports retain unresolved,
quarantined, and non-applicable rows so the derived schema does not silently
guess.
