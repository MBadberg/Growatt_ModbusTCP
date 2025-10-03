#!/usr/bin/env python3
"""
Growatt MIN-10000 Modbus Reader v1.4
Home Assistant Integration Base Script

This script reads data from Growatt MIN series inverters via RS485 Modbus.
Based on Growatt Modbus RTU Protocol documentation.

REQUIREMENTS:
- Python 3.7+
- pymodbus (pip install pymodbus)
- pyserial (pip install pyserial) 
- const.py (register definitions file)

CHANGELOG:
- v1.4: Moved register definitions to const.py, fixed MIN-10000 PV2 mapping
- v1.3: Added intelligent power register fallback (register → calculation)
- v1.2: Added smart meter support and improved error handling  
- v1.1: Added pymodbus version compatibility
- v1.0: Initial release

Hardware Setup:
- Connect RS485-to-USB/TCP converter to inverter SYS COM port pins 3&4
- Set converter to 9600 baud, 8N1, no flow control
"""

import time
import logging
from dataclasses import dataclass
from typing import Dict, Any, Optional
import json

# Import register definitions
try:
    from const import REGISTER_MAPS, STATUS_CODES
except ImportError:
    print("❌ const.py not found! Please ensure const.py is in the same directory.")
    print("   Download it from the same location as this script.")
    exit(1)

try:
    # For RS485-to-USB connection
    import serial
    # Try new import style first (pymodbus 3.x+)
    try:
        from pymodbus.client import ModbusSerialClient as ModbusClient
    except ImportError:
        # Fall back to old import style (pymodbus 2.x)
        from pymodbus.client.sync import ModbusSerialClient as ModbusClient
    SERIAL_AVAILABLE = True
except ImportError:
    SERIAL_AVAILABLE = False

try:
    # For RS485-to-TCP connection (like EW11)
    # Try new import style first (pymodbus 3.x+)
    try:
        from pymodbus.client import ModbusTcpClient
    except ImportError:
        # Fall back to old import style (pymodbus 2.x)
        from pymodbus.client.sync import ModbusTcpClient
    TCP_AVAILABLE = True
except ImportError:
    TCP_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class GrowattData:
    """Container for Growatt inverter data"""
    # Solar Input
    pv1_voltage: float = 0.0          # V
    pv1_current: float = 0.0          # A  
    pv1_power: float = 0.0            # W
    pv2_voltage: float = 0.0          # V
    pv2_current: float = 0.0          # A
    pv2_power: float = 0.0            # W
    pv_total_power: float = 0.0       # W
    
    # Power calculation methods (for debugging)
    pv1_method: str = "unknown"       # "register" or "calculated"
    pv2_method: str = "unknown"       # "register" or "calculated"
    
    # AC Output
    ac_voltage: float = 0.0           # V
    ac_current: float = 0.0           # A
    ac_power: float = 0.0             # W
    ac_frequency: float = 0.0         # Hz
    
    # Grid/Meter Data (when smart meter connected)
    grid_power: float = 0.0           # W (+export, -import)
    grid_voltage: float = 0.0         # V
    grid_current: float = 0.0         # A  
    grid_frequency: float = 0.0       # Hz
    load_power: float = 0.0           # W (house consumption)
    
    # Energy & Status
    energy_today: float = 0.0         # kWh
    energy_total: float = 0.0         # kWh
    temperature: float = 0.0          # °C
    status: int = 0                   # Inverter status
    
    # Device Info
    firmware_version: str = ""
    serial_number: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON/HA integration"""
        return {
            'solar': {
                'pv1_voltage': self.pv1_voltage,
                'pv1_current': self.pv1_current, 
                'pv1_power': self.pv1_power,
                'pv2_voltage': self.pv2_voltage,
                'pv2_current': self.pv2_current,
                'pv2_power': self.pv2_power,
                'total_power': self.pv_total_power
            },
            'ac_output': {
                'voltage': self.ac_voltage,
                'current': self.ac_current,
                'power': self.ac_power,
                'frequency': self.ac_frequency
            },
            'grid': {
                'power': self.grid_power,          # +export, -import
                'voltage': self.grid_voltage,
                'current': self.grid_current,
                'frequency': self.grid_frequency,
                'export_power': max(0, self.grid_power),   # Only positive values
                'import_power': abs(min(0, self.grid_power)) # Only negative values (as positive)
            },
            'load': {
                'power': self.load_power  # House consumption
            },
            'energy': {
                'today_kwh': self.energy_today,
                'total_kwh': self.energy_total
            },
            'system': {
                'temperature': self.temperature,
                'status': self.status,
                'firmware': self.firmware_version,
                'serial': self.serial_number
            }
        }

class GrowattModbus:
    """Growatt MIN series Modbus client"""
    
    def __init__(self, connection_type='tcp', host='192.168.1.100', port=502, 
                 device='/dev/ttyUSB0', baudrate=9600, slave_id=1, 
                 register_map='MIN_10000_VARIANT_A'):
        """
        Initialize Modbus connection
        
        Args:
            connection_type: 'tcp' for RS485-to-TCP converter, 'serial' for RS485-to-USB
            host: IP address for TCP connection
            port: Port for TCP connection
            device: Serial device path for USB connection
            baudrate: Serial baud rate (usually 9600)
            slave_id: Modbus slave ID (usually 1)
            register_map: Which register mapping to use (see const.py)
        """
        self.connection_type = connection_type
        self.slave_id = slave_id
        self.client = None
        self.last_read_time = 0
        self.min_read_interval = 1.0  # 1 second minimum between reads
        
        # Load register map
        if register_map not in REGISTER_MAPS:
            raise ValueError(f"Unknown register map: {register_map}. Available: {list(REGISTER_MAPS.keys())}")
        
        self.register_map = REGISTER_MAPS[register_map]
        self.register_map_name = register_map
        logger.info(f"Using register map: {self.register_map['name']}")
        
        if connection_type == 'tcp':
            if not TCP_AVAILABLE:
                raise ImportError("pymodbus not available for TCP connection")
            
            # Handle different pymodbus versions for TCP client
            try:
                # New style (pymodbus 3.x+) - requires keyword arguments
                self.client = ModbusTcpClient(host=host, port=port)
            except TypeError:
                # Old style (pymodbus 2.x) - accepts positional arguments
                self.client = ModbusTcpClient(host, port)
            
            logger.info(f"Connecting to Growatt via TCP: {host}:{port}")
            
        elif connection_type == 'serial':
            if not SERIAL_AVAILABLE:
                raise ImportError("pymodbus and/or pyserial not available for serial connection")
            
            # Handle different pymodbus versions
            try:
                # New style (pymodbus 3.x+)
                self.client = ModbusClient(
                    port=device,
                    baudrate=baudrate,
                    timeout=3,
                    parity='N',
                    stopbits=1,
                    bytesize=8
                )
            except TypeError:
                # Old style (pymodbus 2.x)
                self.client = ModbusClient(
                    method='rtu',
                    port=device,
                    baudrate=baudrate,
                    timeout=3,
                    parity='N',
                    stopbits=1,
                    bytesize=8
                )
            logger.info(f"Connecting to Growatt via Serial: {device} @ {baudrate} baud")
        else:
            raise ValueError("connection_type must be 'tcp' or 'serial'")
    
    def connect(self) -> bool:
        """Establish connection to inverter"""
        try:
            result = self.client.connect()
            if result:
                logger.info("Successfully connected to Growatt inverter")
            else:
                logger.error("Failed to connect to Growatt inverter")
            return result
        except Exception as e:
            logger.error(f"Connection error: {e}")
            return False
    
    def disconnect(self):
        """Close connection"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from Growatt inverter")
    
    def _enforce_read_interval(self):
        """Ensure minimum time between reads per Growatt spec"""
        current_time = time.time()
        time_since_last = current_time - self.last_read_time
        if time_since_last < self.min_read_interval:
            sleep_time = self.min_read_interval - time_since_last
            logger.debug(f"Sleeping {sleep_time:.2f}s to respect read interval")
            time.sleep(sleep_time)
        self.last_read_time = time.time()
    
    def read_input_registers(self, start_address: int, count: int) -> Optional[list]:
        """Read input registers with error handling"""
        self._enforce_read_interval()
        
        try:
            # Try new parameter name first (device_id), then fall back to old (slave)
            try:
                response = self.client.read_input_registers(
                    address=start_address, count=count, device_id=self.slave_id
                )
            except TypeError:
                # Fall back to older parameter names
                response = self.client.read_input_registers(
                    start_address, count, slave=self.slave_id
                )
            
            # Handle different pymodbus versions for error checking
            if hasattr(response, 'isError'):
                # Old version (2.x)
                if response.isError():
                    logger.error(f"Modbus error reading input registers {start_address}-{start_address+count-1}: {response}")
                    return None
            elif hasattr(response, 'is_error'):
                # New version (3.x)
                if response.is_error():
                    logger.error(f"Modbus error reading input registers {start_address}-{start_address+count-1}: {response}")
                    return None
            elif hasattr(response, 'registers'):
                # Success - has registers attribute
                pass
            else:
                # Unknown response type
                logger.error(f"Unknown response type: {type(response)}")
                return None
                
            return response.registers
        except Exception as e:
            logger.error(f"Exception reading input registers: {e}")
            return None
    
    def read_holding_registers(self, start_address: int, count: int) -> Optional[list]:
        """Read holding registers with error handling"""
        self._enforce_read_interval()
        
        try:
            # Try new parameter name first (device_id), then fall back to old (slave)
            try:
                response = self.client.read_holding_registers(
                    address=start_address, count=count, device_id=self.slave_id
                )
            except TypeError:
                # Fall back to older parameter names
                response = self.client.read_holding_registers(
                    start_address, count, slave=self.slave_id
                )
            
            # Handle different pymodbus versions for error checking
            if hasattr(response, 'isError'):
                # Old version (2.x)
                if response.isError():
                    logger.error(f"Modbus error reading holding registers {start_address}-{start_address+count-1}: {response}")
                    return None
            elif hasattr(response, 'is_error'):
                # New version (3.x)
                if response.is_error():
                    logger.error(f"Modbus error reading holding registers {start_address}-{start_address+count-1}: {response}")
                    return None
            elif hasattr(response, 'registers'):
                # Success - has registers attribute
                pass
            else:
                # Unknown response type
                logger.error(f"Unknown response type: {type(response)}")
                return None
                
            return response.registers
        except Exception as e:
            logger.error(f"Exception reading holding registers: {e}")
            return None

    def read_all_data(self) -> Optional[GrowattData]:
        """Read all relevant data from inverter"""
        data = GrowattData()
        
        # Read main input registers block (3000-3050 to include meter data)
        registers = self.read_input_registers(3000, 51)
        if registers is None:
            logger.error("Failed to read input registers")
            return None
        
        # Get register addresses from the loaded map
        input_regs = self.register_map['input_registers']
        
        # Helper function to find register offset
        def get_offset(address):
            return address - 3000
        
        # Parse input register data using register map
        try:
            
            # PV1 data (standard location)
            data.pv1_voltage = registers[get_offset(3003)] * input_regs[3003]['scale']  # 3003
            data.pv1_current = registers[get_offset(3004)] * input_regs[3004]['scale']  # 3004  
            
            # PV1 Power with intelligent fallback
            pv1_power_register = registers[get_offset(3005)] * input_regs[3005]['scale']  # 3005
            pv1_power_calculated = data.pv1_voltage * data.pv1_current
            pv1_used_register = False
            
            # Use register if it's non-zero and either calculated is zero OR they're close
            if (pv1_power_register > 0 and 
                (pv1_power_calculated == 0 or 
                 abs(pv1_power_register - pv1_power_calculated) < max(1.0, pv1_power_calculated * 0.2))):
                # Register value seems reasonable
                data.pv1_power = pv1_power_register
                pv1_used_register = True
                logger.debug(f"Using PV1 power from register: {pv1_power_register:.1f}W")
            else:
                # Register is 0 or unreliable, use calculation
                data.pv1_power = pv1_power_calculated
                logger.debug(f"Using PV1 calculated power: {pv1_power_calculated:.1f}W (register was {pv1_power_register:.1f}W)")
            
            # PV2 data (using corrected mapping for MIN_10000_VARIANT_A)
            if self.register_map_name == 'MIN_10000_VARIANT_A':
                # For this variant: Power=3006, Voltage=3007, Current=3008
                data.pv2_voltage = registers[get_offset(3007)] * input_regs[3007]['scale']  # 3007
                data.pv2_current = registers[get_offset(3008)] * input_regs[3008]['scale']  # 3008
                pv2_power_register = registers[get_offset(3006)] * input_regs[3006]['scale']  # 3006
            else:
                # Standard mapping: Voltage=3006, Current=3007, Power=3008
                data.pv2_voltage = registers[get_offset(3006)] * input_regs[3006]['scale']  # 3006
                data.pv2_current = registers[get_offset(3007)] * input_regs[3007]['scale']  # 3007
                pv2_power_register = registers[get_offset(3008)] * input_regs[3008]['scale']  # 3008
            
            # PV2 Power with intelligent fallback
            pv2_power_calculated = data.pv2_voltage * data.pv2_current
            pv2_used_register = False
            
            if (pv2_power_register > 0 and 
                (pv2_power_calculated == 0 or 
                 abs(pv2_power_register - pv2_power_calculated) < max(1.0, pv2_power_calculated * 0.2))):
                # Register value seems reasonable
                data.pv2_power = pv2_power_register
                pv2_used_register = True
                logger.debug(f"Using PV2 power from register: {pv2_power_register:.1f}W")
            else:
                # Register is 0 or unreliable, use calculation  
                data.pv2_power = pv2_power_calculated
                logger.debug(f"Using PV2 calculated power: {pv2_power_calculated:.1f}W (register was {pv2_power_register:.1f}W)")
            
            # Status and total power
            data.status = registers[get_offset(3000)]  # 3000
            #data.pv_total_power = registers[get_offset(3001)] * input_regs[3001]['scale']  # 3001
            data.pv_total_power = data.pv1_power + data.pv2_power  # Calculate total from PV1 and PV2

            # Store method used for display
            data.pv1_method = "register" if pv1_used_register else "calculated"
            data.pv2_method = "register" if pv2_used_register else "calculated"
            
            # AC Output data
            data.ac_power = registers[get_offset(3011)] * input_regs[3011]['scale']  # 3011
            data.ac_frequency = registers[get_offset(3012)] * input_regs[3012]['scale']  # 3012
            data.ac_voltage = registers[get_offset(3013)] * input_regs[3013]['scale']  # 3013
            data.ac_current = registers[get_offset(3014)] * input_regs[3014]['scale']  # 3014
            data.temperature = registers[get_offset(3017)] * input_regs[3017]['scale']  # 3017
            data.energy_today = registers[get_offset(3026)] * input_regs[3026]['scale']  # 3026
            
            # Energy total is 32-bit value at 3028-3029
            if len(registers) > get_offset(3029):
                energy_total_raw = (registers[get_offset(3028)] << 16) | registers[get_offset(3029)]  # 3028-3029
                data.energy_total = energy_total_raw * 0.1
            
            # Grid/Meter data (available when smart meter connected)
            if len(registers) > get_offset(3050):
                # Check if we have valid meter data (non-zero values suggest meter is connected)
                grid_power_raw = registers[get_offset(3046)]  # 3046
                if grid_power_raw != 0 or registers[get_offset(3047)] != 0:  # 3047 (grid voltage)
                    # Convert signed 16-bit values for power (can be negative for import)
                    data.grid_power = self._to_signed_16bit(grid_power_raw) * input_regs[3046]['scale']
                    data.grid_voltage = registers[get_offset(3047)] * input_regs[3047]['scale']  # 3047
                    data.grid_current = self._to_signed_16bit(registers[get_offset(3048)]) * input_regs[3048]['scale']  # 3048
                    data.grid_frequency = registers[get_offset(3049)] * input_regs[3049]['scale']  # 3049
                    data.load_power = registers[get_offset(3050)] * input_regs[3050]['scale']  # 3050
                    logger.debug(f"Grid data available: {data.grid_power}W, Load: {data.load_power}W")
                else:
                    logger.debug("No smart meter data detected")
            
        except (IndexError, TypeError, KeyError) as e:
            logger.error(f"Error parsing input registers: {e}")
            return None
        
        # Read device info from holding registers
        holding_regs = self.read_holding_registers(0, 20)
        if holding_regs:
            try:
                holding_map = self.register_map['holding_registers']
                
                # Firmware version at register 3
                if len(holding_regs) > 3 and 3 in holding_map:
                    fw_version = holding_regs[3]
                    data.firmware_version = f"{fw_version >> 8}.{fw_version & 0xFF}"
                
                # Serial number from registers 9-13
                if len(holding_regs) > 13:
                    serial_parts = []
                    for i in range(9, 14):  # registers 9-13
                        if i < len(holding_regs):
                            reg_val = holding_regs[i]
                            # Convert 16-bit register to 2 ASCII characters
                            if reg_val > 0:
                                char1 = (reg_val >> 8) & 0xFF
                                char2 = reg_val & 0xFF
                                if char1 > 0:
                                    serial_parts.append(chr(char1))
                                if char2 > 0:
                                    serial_parts.append(chr(char2))
                    data.serial_number = ''.join(serial_parts).rstrip('\x00')
                    
            except Exception as e:
                logger.warning(f"Error reading device info: {e}")
        
        return data
    
    def _to_signed_16bit(self, value: int) -> int:
        """Convert unsigned 16-bit to signed 16-bit for power values that can be negative"""
        if value > 32767:
            return value - 65536
        return value

    def get_status_text(self, status_code: int) -> str:
        """Convert status code to human readable text"""
        status_info = STATUS_CODES.get(status_code, {'name': f'Unknown ({status_code})', 'desc': 'Unknown status code'})
        return status_info['name']

def main():
    """Example usage"""
    import sys
    
    # Enable debug logging to see fallback decisions
    logging.getLogger().setLevel(logging.DEBUG)
    
    # Check if const.py is available
    try:
        from const import REGISTER_MAPS
    except ImportError:
        print("❌ ERROR: const.py not found!")
        print("📁 Required files:")
        print("   - growatt.py (this file)")  
        print("   - const.py (register definitions)")
        print("\n💡 Make sure both files are in the same directory.")
        return
    
    # Configuration - adjust for your setup
    CONFIG = {
        'connection_type': 'tcp',  # or 'serial'
        'host': '192.168.1.100',   # IP of RS485-to-TCP converter
        'port': 502,
        'device': '/dev/ttyUSB0',  # for serial connection
        'baudrate': 9600,
        'slave_id': 1,
        'register_map': 'MIN_10000_VARIANT_A'  # Use corrected register mapping
    }
    
    # Handle command line arguments
    if len(sys.argv) >= 2:
        CONFIG['host'] = sys.argv[1]
        logger.info(f"Using command line host: {CONFIG['host']}")
    
    if len(sys.argv) >= 3:
        try:
            CONFIG['port'] = int(sys.argv[2])
            logger.info(f"Using command line port: {CONFIG['port']}")
        except ValueError:
            logger.error(f"Invalid port number: {sys.argv[2]}")
            return
    
    if len(sys.argv) >= 4:
        try:
            CONFIG['slave_id'] = int(sys.argv[3])
            logger.info(f"Using command line slave ID: {CONFIG['slave_id']}")
        except ValueError:
            logger.error(f"Invalid slave ID: {sys.argv[3]}")
            return
    
    # Print usage info
    if len(sys.argv) == 1:
        print("Usage: python growatt.py [host] [port] [slave_id]")
        print(f"Using defaults: {CONFIG['host']}:{CONFIG['port']}, slave_id={CONFIG['slave_id']}")
        print(f"Register map: {CONFIG['register_map']}")
        print("\nAvailable register maps:")
        for name, config in REGISTER_MAPS.items():
            print(f"  - {name}: {config['name']}")
    
    # Create and connect to inverter
    inverter = GrowattModbus(**CONFIG)
    
    if not inverter.connect():
        logger.error("Failed to connect. Check your wiring and configuration.")
        return
    
    try:
        # Read data
        logger.info("Reading inverter data...")
        data = inverter.read_all_data()
        
        if data:
            # Print human-readable output
            print("\n" + "="*50)
            print("GROWATT MIN-10000 STATUS")
            print("="*50)
            print(f"Register Map: {inverter.register_map['name']}")
            print(f"Status: {inverter.get_status_text(data.status)}")
            print(f"Serial: {data.serial_number}")
            print(f"Firmware: {data.firmware_version}")
            print(f"Temperature: {data.temperature:.1f}°C")
            
            print("\nSOLAR INPUT:")
            pv1_icon = "📊" if data.pv1_method == "register" else "🧮"
            pv2_icon = "📊" if data.pv2_method == "register" else "🧮"
            
            print(f"  PV1: {data.pv1_voltage:.1f}V, {data.pv1_current:.1f}A, {data.pv1_power:.0f}W {pv1_icon}")
            print(f"  PV2: {data.pv2_voltage:.1f}V, {data.pv2_current:.1f}A, {data.pv2_power:.0f}W {pv2_icon}")
            print(f"  Total: {data.pv_total_power:.0f}W")
            print(f"\n📊 = Register value  🧮 = Calculated (V×I)")
            print("\nAC OUTPUT:")
            print(f"  Voltage: {data.ac_voltage:.1f}V")
            print(f"  Current: {data.ac_current:.1f}A") 
            print(f"  Power: {data.ac_power:.0f}W")
            print(f"  Frequency: {data.ac_frequency:.2f}Hz")
            
            # Show grid data if available (smart meter connected)
            if data.grid_power != 0 or data.grid_voltage != 0:
                print("\nGRID (Smart Meter):")
                print(f"  Power: {data.grid_power:.0f}W", end="")
                if data.grid_power > 0:
                    print(" (EXPORTING)")
                elif data.grid_power < 0:
                    print(" (IMPORTING)")
                else:
                    print(" (BALANCED)")
                print(f"  Voltage: {data.grid_voltage:.1f}V")
                print(f"  Current: {data.grid_current:.1f}A")
                print(f"  Frequency: {data.grid_frequency:.2f}Hz")
                print(f"\nLOAD:")
                print(f"  House Consumption: {data.load_power:.0f}W")
                
                # Energy balance calculation
                print(f"\nENERGY FLOW:")
                print(f"  Solar Production: {data.pv_total_power:.0f}W")
                print(f"  House Consumption: {data.load_power:.0f}W")
                if data.grid_power > 0:
                    print(f"  Grid Export: {data.grid_power:.0f}W")
                    print(f"  Self Consumption: {data.pv_total_power - data.grid_power:.0f}W")
                elif data.grid_power < 0:
                    print(f"  Grid Import: {abs(data.grid_power):.0f}W")
                    print(f"  Self Consumption: {data.pv_total_power:.0f}W")
                else:
                    print(f"  Self Consumption: {data.pv_total_power:.0f}W")
            else:
                print("\nGRID: No smart meter detected")
                print("  (Only inverter AC output available)")
            
            print("\nENERGY:")
            print(f"  Today: {data.energy_today:.1f} kWh")
            print(f"  Total: {data.energy_total:.1f} kWh")
            
            # JSON output for Home Assistant integration
            print("\nJSON DATA (for Home Assistant):")
            print(json.dumps(data.to_dict(), indent=2))
            
        else:
            logger.error("Failed to read data from inverter")
            
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        inverter.disconnect()

if __name__ == "__main__":
    main()