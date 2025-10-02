# Changelog

All notable changes to the Energy Tracker project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Contributing guidelines (CONTRIBUTING.md)
- Changelog documentation
- API documentation for developers
- Deployment guide
- Troubleshooting guide

### Changed
- Improved documentation structure

## [1.0.0] - 2025-10-02

### Added
- Initial release of Energy Tracker Django web application
- MeterReading model for storing energy usage data
- Tariff model for pricing information
- Dashboard view with energy cost visualization using Matplotlib
- Input forms for meter readings and tariff data
- SQLite database integration
- Responsive web interface with custom CSS styling
- Energy cost trend charts with date-based plotting
- Recent readings display with calculated costs

### Features
- **Data Input**: Easy-to-use forms for entering meter readings and energy tariffs
- **Visualization**: Interactive charts showing energy cost trends over time
- **Dashboard**: Comprehensive overview of recent readings and calculated costs
- **Cost Calculation**: Automatic calculation of energy costs based on usage and tariff rates
- **Data Persistence**: SQLite database for storing historical data

### Technical Details
- Built with Django 5.1.7
- Python 3.13+ support
- Matplotlib integration for chart generation
- Base64 encoded chart rendering for web display
- Form validation and error handling
- Database migrations included

### Dependencies
- Django 5.1.7
- Matplotlib 3.10.1
- Pandas 2.2.3
- NumPy 2.2.3
- Pillow 11.1.0
- SQLparse 0.5.3

### Database Schema
- MeterReading: date, kwh_used
- Tariff: price_per_kwh (stored in pence)

### Known Issues
- Single tariff system (no time-based pricing)
- Basic error handling for missing data
- Charts are static (no interactivity)

---

## Version Format

- **Major.Minor.Patch** (e.g., 1.0.0)
- **Major**: Breaking changes or significant new features
- **Minor**: New features, backwards compatible
- **Patch**: Bug fixes and minor improvements

## Types of Changes

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements