# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.6.0] - 2026-07-14

### Added

- Standalone `sync_logs.py` script that syncs the deployment log to GitHub, using a content hash to skip commits when nothing changed
- Author credit and tagline added to the README

### Changed

- Reworked how the deployment log gets pushed to GitHub after a PythonAnywhere reload — moved from an in-request background thread to a flag-file handoff, then replaced with the external sync script
- Relocated the deployment flag file from `/tmp` into the project directory so it survives across reloads

### Fixed

- Flag-file path bug that could cause a log sync to be missed after a reload

**Full Changelog**: https://github.com/tanishqmudaliar/Weather-Monitoring-System/compare/v1.5.1...v1.6.0

## [1.5.1] - 2026-06-27

### Changed

- Updated theme color and simplified brand logo markup in the header

## [1.5.0] - 2026-02-28

### Added

- Weather alerts for severe conditions (thunderstorms, heavy rain, snow, fog, tornadoes)
- Additional pressure readings (atmospheric, sea level, ground level)
- Expanded air quality index details with full pollutant breakdown

### Changed

- Updated README to document pressure readings and weather alerts

## [1.4.1] - 2026-02-14

### Added

- HTML-formatted deployment log view for improved readability

### Changed

- Hid empty state during loading/error display and adjusted footer spacing

## [1.4.0] - 2026-02-01

### Added

- Docker support (`Dockerfile`, `docker-compose.yml`, `.dockerignore`, `.env.example`)
- README instructions for local development with Docker

### Changed

- Refactored frontend assets (`app.js`, `styles.css`) for readability and maintainability

## [1.3.0] - 2026-01-25

### Added

- SEO meta tags and refined weather data presentation in the UI
- Automatic creation of the deployment log directory

### Changed

- Overhauled README documentation and deployment workflow section
- Updated deployment log path handling in `app.py`

### Fixed

- Title typo in `index.html`

## [1.2.0] - 2026-01-21

### Changed

- Redesigned the weather dashboard UI (major layout and styling overhaul)
- Enhanced and reorganized backend API endpoints

## [1.1.1] - 2026-01-11

### Fixed

- Typo in city name ("Ahemdabad" → "Ahmedabad")
- URL formatting for the PythonAnywhere API reload request
- Removed unnecessary API key validation in `app.py`

### Changed

- Refactored GitHub webhook handling for clarity and improved logging
- Improved startup and environment-variable-check logging

## [1.1.0] - 2026-01-10

### Added

- Automated CI/CD deployment to PythonAnywhere via GitHub Actions
- Quick city tags and additional weather details in the UI

### Changed

- Multiple iterations refining the deployment workflow (error handling, JSON payload, logging)
- Updated README with deployment documentation

## [1.0.0] - 2026-01-08

### Added

- Initial Flask backend and vanilla JS frontend for real-time weather monitoring
- README, `requirements.txt`, and MIT LICENSE
- `.gitignore` for environment files

[Unreleased]: https://github.com/tanishqmudaliar/Weather-Monitoring-System/compare/v1.6.0...HEAD
[1.6.0]: https://github.com/tanishqmudaliar/Weather-Monitoring-System/compare/v1.5.1...v1.6.0
[1.5.1]: https://github.com/tanishqmudaliar/Weather-Monitoring-System/compare/v1.5.0...v1.5.1
[1.5.0]: https://github.com/tanishqmudaliar/Weather-Monitoring-System/compare/v1.4.1...v1.5.0
[1.4.1]: https://github.com/tanishqmudaliar/Weather-Monitoring-System/compare/v1.4.0...v1.4.1
[1.4.0]: https://github.com/tanishqmudaliar/Weather-Monitoring-System/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/tanishqmudaliar/Weather-Monitoring-System/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/tanishqmudaliar/Weather-Monitoring-System/compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/tanishqmudaliar/Weather-Monitoring-System/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/tanishqmudaliar/Weather-Monitoring-System/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/tanishqmudaliar/Weather-Monitoring-System/releases/tag/v1.0.0
