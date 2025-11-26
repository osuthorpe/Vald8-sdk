# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.6] - 2025-11-25

### Added
- Support for decorating instance methods directly with `@vald8`. The decorator now implements the descriptor protocol to correctly bind `self`.

### Changed
- Updated documentation to reflect that module-level wrappers are no longer required for class methods.
- Refactored examples to demonstrate direct class method decoration.

## [0.1.5] - 2025-11-24

### Added
- Class method examples and documentation.

### Changed
- Updated Pydantic model serialization to V2 syntax.

## [0.1.4] - 2025-11-24

### Changed
- Migrated Pydantic model configuration to V2 syntax.

## [0.1.3] - 2025-11-24

### Added
- GitHub Actions workflows for testing and PyPI publishing.
- Initial project wiki documentation.

## [0.1.2] - 2025-11-24

### Fixed
- Updated PyPI links in configuration.

## [0.1.1] - 2025-11-23

### Added
- Initial release of Vald8 SDK.