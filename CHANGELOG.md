# Changelog

## [2.0.0] - 2026-11-25

### Changed

- `ReadTfvarsAndWriteJson` now uses `python-hcl2` instead of a line-based parser. Lists, maps, numbers and booleans keep their types, and multi-line values and all comment styles (`#`, `//`, inline) are supported.
- Both scripts accept the input path as an argument and an optional `-o/--output` path.
- Both scripts exit with code `1` on errors.
- `.tf` output no longer includes the extra quotes and internal keys (`__is_block__`, `__comments__`) of `python-hcl2` 8.

### Added

- `requirements.txt` and `requirements-dev.txt`.
- pytest test suite and GitHub Actions workflow.

## [1.0] 

- First version: `.tf` → JSON and `.tfvars` → JSON scripts.
