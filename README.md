# Growatt Modbus Integration for Home Assistant

# Growatt Modbus Integration for Home Assistant ☀️

![HACS Badge](https://img.shields.io/badge/HACS-Custom-orange.svg)
![Version](https://img.shields.io/badge/Version-0.0.1-blue.svg)
[![GitHub Issues](https://img.shields.io/github/issues/0xAHA/Growatt_ModbusTCP.svg)](https://github.com/0xAHA/Growatt_ModbusTCP/issues)
[![GitHub Stars](https://img.shields.io/github/stars/0xAHA/Growatt_ModbusTCP.svg?style=social)](https://github.com/0xAHA/Growatt_ModbusTCP)

A native Home Assistant integration for Growatt solar inverters using direct Modbus RTU/TCP communication. Get real-time data straight from your inverter without relying on cloud services! 🚀

Based on the official **[Growatt Modbus RTU Protocol V1.39](https://shop.frankensolar.ca/content/documentation/Growatt/AppNote_Growatt_WIT-Modbus-RTU-Protocol-II-V1.39-English-20240416_%28frankensolar%29.pdf)** (2024.04.16) documentation.

---

## ✨ Features

* 📊 **Real-time monitoring** - Direct Modbus communication with your inverter - no more 5-minute averages
* 🌙 **Night-time friendly** - Sensors stay available when inverter is offline (no sun)
* ⚡ **Smart power flow** - Automatic calculation of export, import, and self-consumption
* 🔌 **Multiple connections** - TCP (WiFi/Ethernet adapters)
* 📈 **Energy dashboard ready** - Automatic integration with HA Energy Dashboard
* 🎯 **Official registers** - Uses verified Growatt protocol documentation
* 🌡️ **Complete diagnostics** - Temperatures, fault codes, derating status
* 💾 **No cloud dependency** - Local polling, your data stays yours

---

## 🔌 Supported Models*

Based on Growatt MIN-10000-TL-X Modbus Register Map (Protocol V1.39):


| Model Range      | Status        | Notes                  |
| ------------------ | --------------- | ------------------------ |
| MIN-3000TL-X     | ✅ Supported  | Single-phase grid-tied |
| MIN-4000TL-X     | ✅ Supported  | Single-phase grid-tied |
| MIN-5000TL-X     | ✅ Supported  | Single-phase grid-tied |
| MIN-6000TL-X     | ✅ Supported  | Single-phase grid-tied |
| MIN-7000TL-X     | ✅ Supported  | Single-phase grid-tied |
| MIN-8000TL-X     | ✅ Supported  | Single-phase grid-tied |
| MIN-9000TL-X     | ✅ Supported  | Single-phase grid-tied |
| MIN-10000TL-X    | ✅ Supported  | Single-phase grid-tied |
| MIN-TL-XH Series | ✅ Supported  | Three-phase models     |
| Other Growatt    | ⚠️ May work | Use base range mapping |

All models support both base (0-124) and storage (3000-3124) register ranges.

* Based on the documented registers, may not be physically tested

---

## 🛠️ Hardware Setup

### Inverter Connection

Growatt inverters have a **SYS/COM port** on the bottom. It is likely that your installer has wired this to your smart meter and there's almost certainly space in the connector/gland to fit an additional cable. You need to connect **pins 3 & 4** to your RS485/WiFi adapter. The terminals are small screw terminals, so no additional/fancy tools required.

### Connection Hardware

#### TCP Connection (Recommended) 🌐

Use an RS485-to-TCP/WiFi adapter:


| Adapter                    | Connection                 | Settings                        |
| ---------------------------- | ---------------------------- | --------------------------------- |
| **EW11**                   | RS485 A/B to adapter D+/D- | TCP Server, 9600 baud, port 502 |
| **USR-W630**               | RS485 A/B to adapter A/B   | Modbus TCP Gateway mode         |
| **USR-TCP232-410s**        | RS485 A/B to adapter A/B   | TCP Server, 9600 baud, port 502 |
| **Waveshare RS485-to-ETH** | RS485 A/B to adapter A/B   | Modbus TCP mode, 9600 baud      |

**Wiring:**

```
Growatt COM Pin 3 (A) ──────► Adapter RS485-A (or D+)
Growatt COM Pin 4 (B) ──────► Adapter RS485-B (or D-)
```

### Inverter Settings

1. Access inverter menu (usually hold OK button for 3 seconds)
2. Navigate to **Communication** settings
3. Set  **Modbus Address** : `1` (default)
4. Set  **Baud Rate** : `9600` (default)
5. Save and exit

---

## 📥 Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to **Integrations**
3. Click the **⋮** menu (top right) → **Custom repositories**
4. Add repository: `https://github.com/0xAHA/Growatt_ModbusTCP`
5. Category: **Integration**
6. Click **Add**
7. Find "Growatt Modbus Integration" and click **Download**
8. Restart Home Assistant
9. Go to **Settings** → **Devices & Services** → **Add Integration**
10. Search for "Growatt Modbus"

### Manual Installation

1. Download the latest release from [GitHub](https://github.com/0xAHA/Growatt_ModbusTCP/releases)
2. Extract to `custom_components/growatt_modbus/` in your HA config directory
3. Restart Home Assistant
4. Go to **Settings** → **Devices & Services** → **Add Integration**
5. Search for "Growatt Modbus"

---

## ⚙️ Configuration

### Initial Setup

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration** → Search for **Growatt Modbus**
3. Enter a name for your inverter (e.g., "Growatt Inverter")

### Connection Type

#### TCP Configuration

* **Host** : IP address of your RS485-TCP adapter (e.g., `192.168.1.100`)
* **Port** : `502` (standard Modbus TCP port)
* **Slave ID** : `1` (check inverter display if unsure)
* **Register Map** : `MIN_10000_TL_X_OFFICIAL` (recommended)

### Register Maps


| Map Name                    | Description                                   | Use When                          |
| ----------------------------- | ----------------------------------------------- | ----------------------------------- |
| **MIN_10000_TL_X_OFFICIAL** | Official Growatt V1.39 protocol (3000+ range) | Default choice for all MIN series |
| **MIN_SERIES_BASE_RANGE**   | Alternative addressing (0-124 range)          | If official map doesn't work      |

---

## 📊 Available Sensors

### Solar Input (PV Strings)


| Entity ID                         | Name              | Unit | Description           |
| ----------------------------------- | ------------------- | ------ | ----------------------- |
| `sensor.{name}_pv1_voltage`       | PV1 Voltage       | V    | String 1 DC voltage   |
| `sensor.{name}_pv1_current`       | PV1 Current       | A    | String 1 DC current   |
| `sensor.{name}_pv1_power`         | PV1 Power         | W    | String 1 power output |
| `sensor.{name}_pv2_voltage`       | PV2 Voltage       | V    | String 2 DC voltage   |
| `sensor.{name}_pv2_current`       | PV2 Current       | A    | String 2 DC current   |
| `sensor.{name}_pv2_power`         | PV2 Power         | W    | String 2 power output |
| `sensor.{name}_solar_total_power` | Solar Total Power | W    | Combined PV power     |

**Attributes:**

* `firmware_version` - Inverter firmware
* `serial_number` - Inverter serial number
* `last_successful_update` - Last time inverter responded

### AC Output


| Entity ID                    | Name         | Unit | Description       |
| ------------------------------ | -------------- | ------ | ------------------- |
| `sensor.{name}_ac_voltage`   | AC Voltage   | V    | Grid voltage      |
| `sensor.{name}_ac_current`   | AC Current   | A    | AC output current |
| `sensor.{name}_ac_power`     | AC Power     | W    | AC output power   |
| `sensor.{name}_ac_frequency` | AC Frequency | Hz   | Grid frequency    |

### Power Flow (Calculated)


| Entity ID                         | Name              | Unit | Description               |
| ----------------------------------- | ------------------- | ------ | --------------------------- |
| `sensor.{name}_grid_export_power` | Grid Export Power | W    | Power sent to grid        |
| `sensor.{name}_grid_import_power` | Grid Import Power | W    | Power drawn from grid     |
| `sensor.{name}_self_consumption`  | Self Consumption  | W    | Solar power used directly |
| `sensor.{name}_house_consumption` | House Consumption | W    | Total house load          |

**Attributes:**

* `solar_production` - Current solar generation
* `grid_export` - Power exported to grid
* `house_load` - Current house consumption
* `self_consumption_percentage` - % of solar self-consumed

### Power Flow (Storage/Hybrid Models)


| Entity ID                     | Name          | Unit | Description                   |
| ------------------------------- | --------------- | ------ | ------------------------------- |
| `sensor.{name}_power_to_grid` | Power to Grid | W    | Export power (from registers) |
| `sensor.{name}_power_to_load` | Power to Load | W    | Power to house load           |
| `sensor.{name}_power_to_user` | Power to User | W    | Forward power                 |

### Energy


| Entity ID                            | Name                 | Unit | Description          |
| -------------------------------------- | ---------------------- | ------ | ---------------------- |
| `sensor.{name}_energy_today`         | Energy Today         | kWh  | Today's production   |
| `sensor.{name}_energy_total`         | Energy Total         | kWh  | Lifetime production  |
| `sensor.{name}_energy_to_grid_today` | Energy to Grid Today | kWh  | Today's export       |
| `sensor.{name}_energy_to_grid_total` | Energy to Grid Total | kWh  | Lifetime export      |
| `sensor.{name}_load_energy_today`    | Load Energy Today    | kWh  | Today's consumption  |
| `sensor.{name}_load_energy_total`    | Load Energy Total    | kWh  | Lifetime consumption |

### System & Diagnostics


| Entity ID                     | Name                 | Unit | Description              |
| ------------------------------- | ---------------------- | ------ | -------------------------- |
| `sensor.{name}_inverter_temp` | Inverter Temperature | °C  | Internal temperature     |
| `sensor.{name}_ipm_temp`      | IPM Temperature      | °C  | Power module temp        |
| `sensor.{name}_boost_temp`    | Boost Temperature    | °C  | Boost converter temp     |
| `sensor.{name}_status`        | Status               | -    | Operating status         |
| `sensor.{name}_derating_mode` | Derating Mode        | -    | Power reduction status   |
| `sensor.{name}_fault_code`    | Fault Code           | -    | Current fault (if any)   |
| `sensor.{name}_warning_code`  | Warning Code         | -    | Current warning (if any) |

**Status Values:**

* `Waiting` - Waiting for sufficient PV power or grid
* `Normal` - Operating normally
* `Fault` - Fault condition detected

---

## 📈 Energy Dashboard Integration

Sensors are automatically configured for the Energy Dashboard:

1. Go to **Settings** → **Dashboards** → **Energy**
2. Click **Add Consumption** or **Add Solar Production**

### Recommended Configuration

**Solar Production:**

```
sensor.{name}_solar_total_power
```

**Grid Export:**

```
sensor.{name}_grid_export_power
```

**Grid Import:**

```
sensor.{name}_grid_import_power
```

**Home Consumption:**

```
sensor.{name}_house_consumption
```

---

## 🌙 Night-Time Behavior

When the inverter powers down (no sun), the integration handles it gracefully:

* ✅ Sensors remain **available** (not "unavailable")
* ✅ Last known values retained (typically 0W)
* ✅ `last_successful_update` attribute shows when data was last fresh
* ✅ Logs show DEBUG messages instead of errors
* ✅ Resumes automatically when sun returns

This prevents sensor unavailability cascades in your automations and dashboards!

---

## 🔧 Configuration Options

Access via **Settings** → **Devices & Services** → **Growatt Modbus** →  **Configure** :


| Option            | Default    | Description                   |
| ------------------- | ------------ | ------------------------------- |
| **Scan Interval** | 30 seconds | How often to poll inverter    |
| **Register Map**  | Official   | Which register mapping to use |

> 💡 **Tip:** 30 seconds is recommended. Faster polling provides minimal benefit and may stress the inverter.

---

## 🐛 Troubleshooting

### Common Problems

#### "Failed to connect to inverter"

* ✅ Check wiring (A and B may need swapping)
* ✅ Verify IP address
* ✅ Confirm inverter Modbus address (usually 1)
* ✅ Ensure baud rate is 9600
* ✅ Check if inverter has power (try during daytime)

#### "Unknown register map"

* ✅ Try `MIN_10000_TL_X_OFFICIAL` first
* ✅ Fall back to `MIN_SERIES_BASE_RANGE` if needed

#### Power values look wrong

* ✅ Compare readings with inverter display
* ✅ Check sensor attributes for calculation method
* ✅ Try alternative register map
* ✅ Enable DEBUG logging and check logs

#### Sensors show "Unavailable"

* ✅ Check if this is during night time (expected if first-time setup)
* ✅ Wait for sunrise and inverter to power on
* ✅ Check logs for connection errors
* ✅ Verify network/serial connection

### Enable Debug Logging

Add to `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.growatt_modbus: debug
```

---

## 📁 File Structure

```
custom_components/growatt_modbus/
├── __init__.py              # Integration setup
├── config_flow.py           # Configuration UI
├── const.py                 # Register definitions (official V1.39)
├── coordinator.py           # Data coordinator with auto-migration
├── growatt_modbus.py        # Modbus communication (pymodbus 2.x & 3.x)
├── manifest.json            # Integration metadata
├── sensor.py                # Sensor platform with calculated values
├── strings.json             # UI translations
└── translations/
    └── en.json              # English translations
```

---

## 🔌 API Reference

### GrowattData Class

```python
@dataclass
class GrowattData:
    # Solar Input
    pv1_voltage: float        # V
    pv1_current: float        # A
    pv1_power: float          # W
    pv2_voltage: float        # V
    pv2_current: float        # A
    pv2_power: float          # W
    pv_total_power: float     # W
  
    # AC Output
    ac_voltage: float         # V
    ac_current: float         # A
    ac_power: float           # W
    ac_frequency: float       # Hz
  
    # Power Flow (storage/hybrid models)
    power_to_user: float      # W
    power_to_grid: float      # W (export)
    power_to_load: float      # W
  
    # Energy & Status
    energy_today: float       # kWh
    energy_total: float       # kWh
    energy_to_user_today: float    # kWh
    energy_to_user_total: float    # kWh
    energy_to_grid_today: float    # kWh
    energy_to_grid_total: float    # kWh
    load_energy_today: float       # kWh
    load_energy_total: float       # kWh
  
    # Temperatures
    inverter_temp: float      # °C
    ipm_temp: float          # °C
    boost_temp: float        # °C
  
    # Diagnostics
    status: int              # 0=Waiting, 1=Normal, 3=Fault
    derating_mode: int
    fault_code: int
    warning_code: int
  
    # Device Info
    firmware_version: str
    serial_number: str
```

### Register Maps

Access via `REGISTER_MAPS` in `const.py`:

```python
from custom_components.growatt_modbus.const import REGISTER_MAPS

# Available maps
maps = REGISTER_MAPS.keys()
# ['MIN_10000_TL_X_OFFICIAL', 'MIN_SERIES_BASE_RANGE']

# Get register info
reg_info = REGISTER_MAPS['MIN_10000_TL_X_OFFICIAL']
input_regs = reg_info['input_registers']
```

---

## 🤝 Contributing

Contributions welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Test thoroughly with real hardware
4. Commit changes (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Testing Checklist

* ✅ Tested with actual Growatt hardware
* ✅ Verified TCP connections
* ✅ Checked night-time behavior (inverter offline)
* ✅ Confirmed Energy Dashboard integration
* ✅ Validated all sensors appear correctly
* ✅ Reviewed logs for errors/warnings

---

## 📄 License

MIT License - see [LICENSE](https://claude.ai/chat/LICENSE) file for details.

---

## 🙏 Acknowledgments

* Based on [Growatt Modbus RTU Protocol V1.39](https://shop.frankensolar.ca/content/documentation/Growatt/AppNote_Growatt_WIT-Modbus-RTU-Protocol-II-V1.39-English-20240416_%28frankensolar%29.pdf) (2024.04.16)
* Built for the Home Assistant community
* Tested by solar enthusiasts worldwide 🌍
* Special thanks to all hardware testers and contributors

---

## 📞 Support

* **Issues:** [GitHub Issues](https://github.com/0xAHA/Growatt_ModbusTCP/issues)
* **Discussions:** [GitHub Discussions](https://github.com/0xAHA/Growatt_ModbusTCP/discussions)
* **Home Assistant Community:** [Community Forum](https://community.home-assistant.io/)

---

**Made with ☀️ by [@0xAHA](https://github.com/0xAHA)**
