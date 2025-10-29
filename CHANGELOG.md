# Changelog

All notable changes to the Growatt Modbus Integration will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.5] - 2025-10-29

### Added - Writable Settings Support for SPH 10000 TL3 BH UP

- **Number Platform**: Added support for writable numeric settings on hybrid inverters
  - Battery charge/discharge time windows (hour and minute controls)
  - AC charge power rate and SOC limit
  - Battery discharge power rate and SOC limit
  - Battery voltage limits (charge and discharge)
- **Select Platform**: Added support for enum-based writable settings
  - Priority mode (Load First, Battery First, Grid First)
  - AC charge enable/disable
  - Grid charge enable/disable
  - Inverter on/off control
- **Modbus Write Support**: Added write methods to GrowattModbus class
  - `write_holding_register()` for single register writes
  - `write_holding_registers()` for multiple register writes
  - Compatibility with pymodbus 2.x and 3.x
- **Coordinator Enhancements**: Added holding register cache and write methods
  - `async_write_holding_register()` for async writes
  - `async_read_holding_registers()` for reading current settings
  - `async_load_holding_registers()` to populate cache on startup
  - Holding register cache for tracking current settings
- **SPH Register Map**: Expanded SPH_3000_10000 holding registers
  - Priority mode control (register 1044)
  - AC charging settings (registers 1090-1096)
  - Battery discharge settings (registers 1100-1105)
  - Battery voltage limits (registers 1110-1111)
  - Grid charge control (register 1120)
- **Documentation**: Comprehensive writable settings documentation
  - Example automations for time-of-use optimization
  - Dynamic priority based on solar production
  - Peak shaving strategies
  - Safety notes and supported models

### Enhanced

- **SPH 10000 TL3 BH UP Support**: Full compatibility confirmed
  - All input registers properly mapped
  - Battery data correctly read from storage range (1000-1124)
  - Writable settings enable powerful automations

### Compatibility

- Supports SPH, TL-XH, MOD, and WIT series hybrid inverters
- Grid-tied models (MIN, MID, MAC, MAX) have limited writable settings

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
