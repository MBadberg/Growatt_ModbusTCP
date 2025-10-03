# Changelog

All notable changes to the Growatt Modbus Integration will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-09-28

### Added

- Initial release of Growatt Modbus Integration
- Complete Home Assistant integration with config flow UI
- Support for TCP and Serial Modbus connections
- Multiple register mappings (MIN_SERIES_STANDARD, MIN_10000_VARIANT_A)
- Comprehensive sensor coverage (PV, AC, Grid, Energy, Status)
- Smart meter support for grid import/export monitoring
- Intelligent power calculation with register/calculated fallbacks
- Built-in Solar Bar Card with auto-entity detection
- Connection testing during setup
- Device and entity discovery
- Energy Dashboard integration support
- Configurable polling intervals and timeouts
- Installation script and comprehensive documentation

### Features

- **Sensors**: 20+ sensors covering all inverter parameters
- **Connection Types**: TCP (RS485-to-Ethernet) and Serial (USB-to-RS485)
- **Register Maps**: Support for different Growatt model variants
- **Smart Meter**: Automatic detection and grid flow monitoring
- **Solar Bar Card**: Beautiful power distribution visualization
- **Auto-Configuration**: Automatic entity detection for Solar Bar Card
- **Services**: Manual data refresh, connection testing, register debugging
- **HACS Support**: Full HACS integration compatibility

### Solar Bar Card Features

- Auto-detection of Growatt entities
- Manual entity configuration support
- Solcast integration support
- Real-time power distribution visualization
- Configurable display options (header, stats, legend)
- Responsive design for all screen sizes

### Hardware Support

- Growatt MIN-3000TL-X through MIN-10000TL-X series
- RS485-to-TCP converters (EW11, USR-W630, etc.)
- USB-to-RS485 adapters (CH340, FTDI, etc.)
- Smart meters connected to Growatt inverters

### Technical Details

- pymodbus 2.x and 3.x compatibility
- Automatic pymodbus version detection
- Rate limiting to respect inverter specifications
- Robust error handling and recovery
- Signed 16-bit value support for grid power
- 32-bit energy total calculations
- Device information extraction (serial, firmware)

## [Unreleased]

### Planned Features

- Additional register mappings for other Growatt models
- Battery storage system support (SPF/SPH series)
- String-level monitoring for larger installations
- Historical data export functionality
- Advanced diagnostics and troubleshooting tools
- Integration with other solar monitoring platforms

### Under Consideration

- MQTT discovery support
- Telegram/Discord notification integration
- Advanced energy flow diagrams
- Cost/savings calculations
- Weather correlation features
- Performance analytics and reporting

## Version Support Matrix


| Integration Version | Home Assistant | pymodbus | Python |
| --------------------- | ---------------- | ---------- | -------- |
| 1.0.0               | 2023.1+        | 2.5+     | 3.7+   |

## Breaking Changes

None for this initial release.

## Migration Guide

This is the initial release, so no migration is required.

## Known Issues

### v1.0.0

- Some MIN-6000 units may require register map adjustments
- Serial connection may require dialout group membership on Linux
- Very old firmware versions (<1.0) may have limited register support
- Smart meter detection requires proper inverter configuration

### Workarounds

- Try different register maps if power readings are incorrect
- Add user to dialout group: `sudo usermod -a -G dialout homeassistant`
- Update inverter firmware if available
- Check inverter menu for smart meter settings

## Testing

Each release is tested with:

- Home Assistant Core (latest stable)
- Home Assistant OS (latest stable)
- Real MIN-10000 hardware with firmware 3.17
- EW11 TCP converter and USB-RS485 adapters
- Smart meter configurations (when available)

## Support

For issues, feature requests, and discussions:

- GitHub Issues: Bug reports and feature requests
- GitHub Discussions: General questions and community support
- Home Assistant Community: Integration discussion thread

## Contributors

Thanks to all contributors who helped test, debug, and improve this integration:

- Hardware testers with various Growatt models
- Community members who provided register mappings
- Beta testers who validated the release
