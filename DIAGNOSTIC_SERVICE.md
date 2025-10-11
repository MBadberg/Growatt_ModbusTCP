# 🔧 Built-In Diagnostic Service

**Having connection issues?** Use our built-in diagnostic service to test your connection **before** installing the integration!

---

## ✨ What It Does

The diagnostic service:

* ✅ Tests TCP connection to your adapter
* ✅ Reads key registers for your inverter model
* ✅ Validates responses are correct
* ✅ Shows results as a notification
* ✅ Logs detailed output
* ✅ **No Terminal or SSH needed!**

---

## 🚀 How to Use

### Step 1: Install the Integration Files

You don't need to *configure* the integration, just have the files installed:

1. **Download** the latest release
2. **Extract** to `/config/custom_components/growatt_modbus/`
3. **Restart** Home Assistant

The diagnostic service will be available immediately!

### Step 2: Run the Diagnostic

1. Go to **Developer Tools** → **Services**
2. Search for **"Growatt Modbus: Run Diagnostic Test"**
3. Fill in the form:
   * **IP Address:** Your RS485-TCP adapter IP (e.g., `192.168.1.100`)
   * **Port:** Usually `502`
   * **Slave ID:** Usually `1` (check inverter display)
   * **Inverter Series:** Select your model from dropdown
   * **Send Notification:** Leave checked
4. Click **"Call Service"**

### Step 3: Check Results

**Option A: Notification (if enabled)**

* A persistent notification will appear in the top-right
* Shows test results and troubleshooting advice
* Click to expand full details

**Option B: Logs**

* Go to **Settings** → **System** → **Logs**
* Search for `growatt_modbus`
* View detailed test results

---

## 📊 Example Results

### ✅ All Tests Passed

```
🔌 Growatt Diagnostic: MIN 7000-10000TL-X

✅ All tests passed (6/6)

Results:
• ✅ Connected to 192.168.1.147:502
• ✅ Register 3000 (Status): Normal
• ✅ Register 3003 (PV1 Voltage): 284.50 V
• ✅ Register 3007 (PV2 Voltage): 289.00 V
• ✅ Register 3011 (PV3 Voltage): 291.20 V
• ✅ Register 3026 (AC Voltage): 240.10 V

✅ Next Steps:
Your inverter is responding correctly!
You can now install the integration.
```

### ⚠️ Partial Success

```
🔌 Growatt Diagnostic: SPH 3000-10000

⚠️ Partial success (3/6)

Results:
• ✅ Connected to 192.168.1.100:502
• ✅ Register 0 (Status): Normal
• ✅ Register 3 (PV1 Voltage): 285.30 V
• ✅ Register 7 (PV2 Voltage): 0.00 V
• ❌ Register 38 (AC Voltage): Read error
• ❌ Register 1013 (Battery Voltage): Read error
• ❌ Register 1014 (Battery SOC): Read error

⚠️ Troubleshooting:
Some registers failed. Try:
• Test during daytime (inverter on)
• Check if correct model selected
• Wait for inverter to fully boot
```

### ❌ All Tests Failed

```
🔌 Growatt Diagnostic: MIN 7000-10000TL-X

❌ All tests failed (0/6)

Results:
• ✅ Connected to 192.168.1.147:502
• ❌ Register 3000 (Status): Read error
• ❌ Register 3003 (PV1 Voltage): Read error
• ❌ Register 3007 (PV2 Voltage): Read error
• ❌ Register 3011 (PV3 Voltage): Read error
• ❌ Register 3026 (AC Voltage): Read error

❌ Troubleshooting:
No registers responded. Check:
• Wiring (try swapping A/B)
• Slave ID (try 1, 2, or 3)
• Inverter is powered on
• Baud rate is 9600
```

---

## 🎯 What Gets Tested

### MIN 3000-6000TL-X

* Status register
* PV1 & PV2 voltage
* AC voltage
* AC frequency

### MIN 7000-10000TL-X

* Status register
* PV1, PV2, PV3 voltage
* AC voltage

### SPH 3000-10000 (Hybrid)

* Status register (base range)
* PV1 & PV2 voltage
* AC voltage
* Battery voltage
* Battery SOC

### MID 15000-25000TL3-X (Three-phase)

* Status register
* PV1 voltage
* Grid voltages (R, S phases)
* Grid frequency

### MOD 6000-15000TL3-XH (Three-phase hybrid)

* Status register
* PV1 voltage
* AC voltage (R phase)
* Battery voltage
* Battery SOC

---

## 🐛 Troubleshooting

### "Service not found"

* Integration files not installed correctly
* Restart Home Assistant after installing files
* Check `/config/custom_components/growatt_modbus/` exists

### "Connection refused"

* Adapter not listening on port 502
* Check adapter web interface settings
* Verify TCP Server or Modbus Gateway mode

### "Timeout" errors

* Inverter is offline (try during daytime)
* Wrong IP address
* Network connectivity issue

### All registers fail but connection succeeds

* Wrong slave ID (try 1, 2, 3)
* RS485 wiring incorrect (swap A/B)
* Wrong inverter model selected
* Baud rate mismatch (should be 9600)

### Some registers work, others don't

* Normal if inverter is offline (night time)
* Some values may be 0V during standby
* Battery registers won't work on non-hybrid models
* Try again during daytime with sun

---

## 🔄 Testing Different Settings

You can run the diagnostic multiple times with different settings:

**Test different slave IDs:**

```yaml
host: 192.168.1.100
slave_id: 1    # Try 1, then 2, then 3
```

**Test different models:**

```yaml
inverter_series: min_7000_10000_tl_x    # Try different profiles
```

**Test without notification:**

```yaml
notify: false    # Results only in logs
```

---

## ✅ Next Steps After Success

Once your diagnostic passes:

1. **Configure the integration:**
   * Go to **Settings** → **Devices & Services**
   * Click **Add Integration**
   * Search for **Growatt Modbus**
   * Select your inverter model
   * Enter the same connection details
2. **Check your sensors:**
   * Verify all expected sensors appear
   * Compare values with inverter display
   * Add to Energy Dashboard if desired
3. **Configure options:**
   * Set scan interval (default 30s)
   * Enable grid power inversion if needed
   * Adjust connection timeout if necessary

---

## 📝 Reporting Issues

If diagnostic fails, include this info when reporting:

1. **Full notification text** or log output
2. **Inverter model** (exact model number)
3. **Adapter type** (EW11, USR-W630, etc.)
4. **Time of day** you tested
5. **Inverter display shows** (voltage, status, etc.)

Post in [GitHub Issues](https://github.com/0xAHA/Growatt_ModbusTCP/issues) with this information!

---

## 🎨 Advanced: Automation Example

You can even automate diagnostics! Run tests automatically:

```yaml
automation:
  - alias: "Test Inverter Connection at Sunrise"
    trigger:
      - platform: sun
        event: sunrise
        offset: "+00:30:00"  # 30 min after sunrise
    action:
      - service: growatt_modbus.run_diagnostic
        data:
          host: "192.168.1.100"
          port: 502
          slave_id: 1
          inverter_series: "min_7000_10000_tl_x"
          notify: true
```

---

## 💡 Tips

* **Test during daytime** - Inverter needs to be powered on
* **Wait 30 seconds** after wiring changes before testing
* **Try all slave IDs** - Some inverters use 2 or 3 instead of 1
* **Check adapter LEDs** - Activity lights should blink during test
* **Compare with display** - Values should match inverter screen
* **Test twice** - First test might fail as inverter wakes up

---

**Questions?** Ask in [GitHub Discussions](https://github.com/0xAHA/Growatt_ModbusTCP/discussions)

**Found a bug?** Report in [GitHub Issues](https://github.com/0xAHA/Growatt_ModbusTCP/issues)

*Made with 🔧 and ☕ for easier troubleshooting from the comfort of your HA UI!*
