#!/usr/bin/env python3
"""
Growatt MIN-10000 Modbus Reader
Home Assistant Integration Base Script

This script reads data from Growatt MIN series inverters via RS485 Modbus.
Based on Growatt Modbus RTU Protocol documentation.

Hardware Setup:
- Connect RS485-to-USB/TCP converter to inverter SYS COM port pins 3&4
- Set converter to 9600 baud, 8N1, no flow control
"""

import time
import logging
from dataclasses import dataclass
from typing import Dict, Any, Optional
import json

try:
    # For RS485-to-USB connection
    import serial
    from pymodbus.client.sync import ModbusSerialClient as ModbusClient
    SERIAL_AVAILABLE = True
except ImportError:
    SERIAL_AVAILABLE = False

try:
    # For RS485-to-TCP connection (like EW11)
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
    
    # AC Output
    ac_voltage: float = 0.0           # V
    ac_current: float = 0.0           # A
    ac_power: float = 0.0             # W
    ac_frequency: float = 0.0         # Hz
    
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
    
    # Register mappings for MIN series (TL-X type)
    # Input registers (Function 04) - Real-time data
    INPUT_REGISTERS = {
        3000: {'name': 'inverter_status', 'scale': 1, 'unit': ''},
        3001: {'name': 'pv_total_power', 'scale': 0.1, 'unit': 'W'},
        3003: {'name': 'pv1_voltage', 'scale': 0.1, 'unit': 'V'},
        3004: {'name': 'pv1_current', 'scale': 0.1, 'unit': 'A'},
        3005: {'name': 'pv1_power', 'scale': 0.1, 'unit': 'W'},
        3006: {'name': 'pv2_voltage', 'scale': 0.1, 'unit': 'V'},
        3007: {'name': 'pv2_current', 'scale': 0.1, 'unit': 'A'},
        3008: {'name': 'pv2_power', 'scale': 0.1, 'unit': 'W'},
        3011: {'name': 'ac_power', 'scale': 0.1, 'unit': 'W'},
        3012: {'name': 'ac_frequency', 'scale': 0.01, 'unit': 'Hz'},
        3013: {'name': 'ac_voltage', 'scale': 0.1, 'unit': 'V'},
        3014: {'name': 'ac_current', 'scale': 0.1, 'unit': 'A'},
        3017: {'name': 'temperature', 'scale': 0.1, 'unit': '°C'},
        3026: {'name': 'energy_today', 'scale': 0.1, 'unit': 'kWh'},
        3028: {'name': 'energy_total', 'scale': 0.1, 'unit': 'kWh'},  # 32-bit value
    }
    
    # Holding registers (Function 03) - Configuration/device info
    HOLDING_REGISTERS = {
        0: {'name': 'safety_func_en', 'scale': 1, 'unit': ''},
        3: {'name': 'firmware_version', 'scale': 1, 'unit': ''},
        9: {'name': 'serial_number_1', 'scale': 1, 'unit': ''},
        10: {'name': 'serial_number_2', 'scale': 1, 'unit': ''},
        11: {'name': 'serial_number_3', 'scale': 1, 'unit': ''},
        12: {'name': 'serial_number_4', 'scale': 1, 'unit': ''},
        13: {'name': 'serial_number_5', 'scale': 1, 'unit': ''},
    }
    
    def __init__(self, connection_type='tcp', host='192.168.1.100', port=502, 
                 device='/dev/ttyUSB0', baudrate=9600, slave_id=1):
        """
        Initialize Modbus connection
        
        Args:
            connection_type: 'tcp' for RS485-to-TCP converter, 'serial' for RS485-to-USB
            host: IP address for TCP connection
            port: Port for TCP connection
            device: Serial device path for USB connection
            baudrate: Serial baud rate (usually 9600)
            slave_id: Modbus slave ID (usually 1)
        """
        self.connection_type = connection_type
        self.slave_id = slave_id
        self.client = None
        self.last_read_time = 0
        self.min_read_interval = 1.0  # 1 second minimum between reads
        
        if connection_type == 'tcp':
            if not TCP_AVAILABLE:
                raise ImportError("pymodbus not available for TCP connection")
            self.client = ModbusTcpClient(host, port)
            logger.info(f"Connecting to Growatt via TCP: {host}:{port}")
            
        elif connection_type == 'serial':
            if not SERIAL_AVAILABLE:
                raise ImportError("pymodbus and/or pyserial not available for serial connection")
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
            response = self.client.read_input_registers(
                start_address, count, unit=self.slave_id
            )
            if response.isError():
                logger.error(f"Modbus error reading input registers {start_address}-{start_address+count-1}: {response}")
                return None
            return response.registers
        except Exception as e:
            logger.error(f"Exception reading input registers: {e}")
            return None
    
    def read_holding_registers(self, start_address: int, count: int) -> Optional[list]:
        """Read holding registers with error handling"""
        self._enforce_read_interval()
        
        try:
            response = self.client.read_holding_registers(
                start_address, count, unit=self.slave_id
            )
            if response.isError():
                logger.error(f"Modbus error reading holding registers {start_address}-{start_address+count-1}: {response}")
                return None
            return response.registers
        except Exception as e:
            logger.error(f"Exception reading holding registers: {e}")
            return None
    
    def read_all_data(self) -> Optional[GrowattData]:
        """Read all relevant data from inverter"""
        data = GrowattData()
        
        # Read main input registers block (3000-3030)
        registers = self.read_input_registers(3000, 31)
        if registers is None:
            logger.error("Failed to read input registers")
            return None
        
        # Parse input register data
        try:
            data.status = registers[0]  # 3000
            data.pv_total_power = registers[1] * 0.1  # 3001
            data.pv1_voltage = registers[3] * 0.1  # 3003
            data.pv1_current = registers[4] * 0.1  # 3004  
            data.pv1_power = registers[5] * 0.1  # 3005
            data.pv2_voltage = registers[6] * 0.1  # 3006
            data.pv2_current = registers[7] * 0.1  # 3007
            data.pv2_power = registers[8] * 0.1  # 3008
            data.ac_power = registers[11] * 0.1  # 3011
            data.ac_frequency = registers[12] * 0.01  # 3012
            data.ac_voltage = registers[13] * 0.1  # 3013
            data.ac_current = registers[14] * 0.1  # 3014
            data.temperature = registers[17] * 0.1  # 3017
            data.energy_today = registers[26] * 0.1  # 3026
            
            # Energy total is 32-bit value at 3028-3029
            if len(registers) > 28:
                energy_total_raw = (registers[28] << 16) | registers[29]  # 3028-3029
                data.energy_total = energy_total_raw * 0.1
            
        except (IndexError, TypeError) as e:
            logger.error(f"Error parsing input registers: {e}")
            return None
        
        # Read device info from holding registers
        holding_regs = self.read_holding_registers(0, 20)
        if holding_regs:
            try:
                # Firmware version at register 3
                if len(holding_regs) > 3:
                    fw_version = holding_regs[3]
                    data.firmware_version = f"{fw_version >> 8}.{fw_version & 0xFF}"
                
                # Serial number from registers 9-13
                if len(holding_regs) > 13:
                    serial_parts = []
                    for i in range(9, 14):  # registers 9-13
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

    def get_status_text(self, status_code: int) -> str:
        """Convert status code to human readable text"""
        status_map = {
            0: "Standby",
            1: "Normal", 
            2: "Fault",
            3: "Permanent Fault"
        }
        return status_map.get(status_code, f"Unknown ({status_code})")

def main():
    """Example usage"""
    # Configuration - adjust for your setup
    CONFIG = {
        'connection_type': 'tcp',  # or 'serial'
        'host': '192.168.1.100',   # IP of RS485-to-TCP converter
        'port': 502,
        'device': '/dev/ttyUSB0',  # for serial connection
        'baudrate': 9600,
        'slave_id': 1
    }
    
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
            print(f"Status: {inverter.get_status_text(data.status)}")
            print(f"Serial: {data.serial_number}")
            print(f"Firmware: {data.firmware_version}")
            print(f"Temperature: {data.temperature:.1f}°C")
            print("\nSOLAR INPUT:")
            print(f"  PV1: {data.pv1_voltage:.1f}V, {data.pv1_current:.1f}A, {data.pv1_power:.0f}W")
            print(f"  PV2: {data.pv2_voltage:.1f}V, {data.pv2_current:.1f}A, {data.pv2_power:.0f}W")
            print(f"  Total: {data.pv_total_power:.0f}W")
            print("\nAC OUTPUT:")
            print(f"  Voltage: {data.ac_voltage:.1f}V")
            print(f"  Current: {data.ac_current:.1f}A") 
            print(f"  Power: {data.ac_power:.0f}W")
            print(f"  Frequency: {data.ac_frequency:.2f}Hz")
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
