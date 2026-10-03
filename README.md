# Mini Network Automation Project

## Purpose
Reads a list of Cisco devices from `inventory.json`, checks whether each is UP or DOWN,
prints the result, and saves it to `output.json`.

## Files
- `inventory.json` - device list (hostname, ip, device_type, location, simulated_status)
- `network_check.py` - main program
- `output.json` - generated results

## Usage
```
python network_check.py          # simulation mode (uses simulated_status)
python network_check.py --live   # real TCP check on port 22
```

## Error handling
Missing/invalid inventory file, per-device check failures, and output write errors are handled.

## Requirements
Python 3.6+ (standard library only).
