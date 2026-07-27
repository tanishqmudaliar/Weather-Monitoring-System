# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.7.0] - 2026-07-27

### Added

- `/runtime-log` endpoint and a separate `runtime.log` file, tracking server start/wake events (idle wake, crash recovery, manual reload) independently of real deploys
- Git diffstat output in the deployment log showing exactly what changed between old and new HEAD after each pull
- File locking (`fcntl.flock`) around git operations so the webhook's deploy and the log-sync script can never interleave
- Deployment flag file (`.deployment_pending`) so the post-restart startup log can tell a real deploy apart from an idle wake or manual reload

### Changed

- Git pull mechanism switched from `git pull` to `git fetch` + `git reset --hard origin/master`, so a dirty working tree can never cause a merge conflict
- `sync_logs.py` no longer commits the live `deployment.log` directly — it now hashes its content and snapshots changes into a new tracked file, `deployment-history.log`
- `log_deployment()` now flushes and fsyncs every write immediately, so an entry survives even if the process is killed by a reload right after logging
- Deployment/runtime log output is now HTML-escaped before being rendered
- GitHub Actions deploy workflow now fails outright on a non-200 response instead of just warning

### Fixed

- Bug where `[LOGS]` auto-commits could still re-trigger a deployment log entry, causing repeated deploy cycles
- `deployment.log` is no longer tracked in git at all (fully gitignored), removing the need to auto-commit it during deploys

**Full Changelog**: https://github.com/tanishqmudaliar/Weather-Monitoring-System/compare/v1.6.0...v1.7.0

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

[Unreleased]: https://github.com/tanishqmudaliar/Weather-Monitoring-System/compare/v1.7.0...HEAD
[1.7.0]: https://github.com/tanishqmudaliar/Weather-Monitoring-System/compare/v1.6.0...v1.7.0
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
