#!/usr/bin/env python3
"""
Debug script to dump all registers and find correct PV2 mapping
"""

import sys

try:
    from pymodbus.client import ModbusTcpClient
except ImportError:
    try:
        from pymodbus.client.sync import ModbusTcpClient
    except ImportError:
        print("❌ pymodbus not installed")
        sys.exit(1)

def dump_registers(host, port=502, slave_id=1):
    """Dump raw register values to find correct mapping"""
    
    try:
        client = ModbusTcpClient(host=host, port=port)
        
        if not client.connect():
            print("❌ Failed to connect")
            return
            
        print("🔍 Reading registers 3000-3025...")
        
        try:
            response = client.read_input_registers(
                address=3000, count=26, device_id=slave_id
            )
        except TypeError:
            response = client.read_input_registers(
                3000, 26, slave=slave_id
            )
        
        if hasattr(response, 'registers'):
            registers = response.registers
            
            print("\n📊 RAW REGISTER DUMP:")
            print("Address | Raw Value | Scaled (*0.1) | Likely Meaning")
            print("-" * 60)
            
            for i, val in enumerate(registers):
                addr = 3000 + i
                scaled = val * 0.1
                signed_val = val if val <= 32767 else val - 65536
                signed_scaled = signed_val * 0.1
                
                # Try to identify what each register might be
                meaning = ""
                if addr == 3000: meaning = "Inverter Status"
                elif addr == 3001: meaning = "PV Total Power"
                elif addr == 3003: meaning = "PV1 Voltage (confirmed working)"
                elif addr == 3004: meaning = "PV1 Current (confirmed working)"
                elif addr == 3005: meaning = "PV1 Power"
                elif 3006 <= addr <= 3010: meaning = f"PV2 candidate #{addr-3005}"
                elif addr == 3011: meaning = "AC Power"
                elif addr == 3012: meaning = "AC Frequency"
                elif addr == 3013: meaning = "AC Voltage"
                elif addr == 3014: meaning = "AC Current"
                
                print(f"{addr:4d}    | {val:8d} | {scaled:9.1f} | {meaning}")
            
            # Now analyze which could be PV2 voltage/current
            print("\n🔍 ANALYZING PV2 CANDIDATES:")
            print("Looking for voltage ~400-500V and current ~5-10A...")
            
            # PV1 for reference
            pv1_voltage = registers[3] * 0.1  # 3003
            pv1_current = registers[4] * 0.1  # 3004
            pv1_power_calc = pv1_voltage * pv1_current
            
            print(f"\n✅ PV1 Reference (known good):")
            print(f"  Voltage: {pv1_voltage:.1f}V")
            print(f"  Current: {pv1_current:.1f}A") 
            print(f"  Power (V×I): {pv1_power_calc:.0f}W")
            
            print(f"\n🔍 PV2 Candidates:")
            
            # Check various combinations around the expected area
            candidates = [
                (5, 6),   # 3005, 3006
                (6, 7),   # 3006, 3007 (current wrong mapping)
                (7, 8),   # 3007, 3008
                (8, 9),   # 3008, 3009
                (9, 10),  # 3009, 3010
            ]
            
            for v_idx, c_idx in candidates:
                if v_idx < len(registers) and c_idx < len(registers):
                    voltage = registers[v_idx] * 0.1
                    current = registers[c_idx] * 0.1
                    power = voltage * current
                    
                    v_addr = 3000 + v_idx
                    c_addr = 3000 + c_idx
                    
                    # Check if this looks reasonable
                    voltage_ok = 200 < voltage < 600  # Reasonable PV voltage range
                    current_ok = 0 < current < 20     # Reasonable PV current range
                    power_reasonable = 1000 < power < 5000  # Reasonable for ~2kW string
                    
                    status = "✅ LOOKS GOOD!" if (voltage_ok and current_ok and power_reasonable) else "❌ Suspicious"
                    
                    print(f"  Registers {v_addr},{c_addr}: {voltage:.1f}V, {current:.1f}A, {power:.0f}W {status}")
            
            # Also check if any single register looks like reasonable power
            print(f"\n🔍 Direct Power Register Candidates (~2000W):")
            for i, val in enumerate(registers):
                addr = 3000 + i
                power_1x = val  # Scale 1
                power_01x = val * 0.1  # Scale 0.1
                power_10x = val * 10   # Scale 10
                
                if 1500 < power_1x < 3000:
                    print(f"  Register {addr} (scale 1): {power_1x}W ✅")
                if 1500 < power_01x < 3000:
                    print(f"  Register {addr} (scale 0.1): {power_01x}W ✅")
                if 1500 < power_10x < 3000:
                    print(f"  Register {addr} (scale 10): {power_10x}W ✅")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python register_dump.py <host> [port] [slave_id]")
        sys.exit(1)
    
    host = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 502
    slave_id = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    
    print("🔍 Growatt Register Layout Debug")
    print("=" * 50)
    
    dump_registers(host, port, slave_id)