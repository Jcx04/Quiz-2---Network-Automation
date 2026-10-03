"""network_check.py - Check UP/DOWN status of devices listed in inventory.json.

Default: simulation mode (uses 'simulated_status' from the inventory).
--live : tries a real TCP connection to port 22 (SSH) on each device.
"""
import json
import socket
import sys
from datetime import datetime

INVENTORY_FILE = "inventory.json"
OUTPUT_FILE = "output.json"


def load_inventory(path):
    try:
        with open(path) as f:
            return json.load(f)["devices"]
    except FileNotFoundError:
        sys.exit(f"[ERROR] {path} not found.")
    except (json.JSONDecodeError, KeyError) as e:
        sys.exit(f"[ERROR] Invalid inventory format: {e}")


def check_live(ip, port=22, timeout=2):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return "UP"
    except OSError:
        return "DOWN"


def main():
    live = "--live" in sys.argv
    devices = load_inventory(INVENTORY_FILE)
    results = []
    print(f"Mode: {'LIVE' if live else 'SIMULATION'}\n")
    print(f"{'Hostname':<14}{'IP':<16}{'Status'}")
    print("-" * 36)
    for d in devices:
        try:
            status = check_live(d["ip"]) if live else d.get("simulated_status", "DOWN").upper()
        except Exception as e:
            status = "DOWN"
            print(f"[WARN] Error checking {d.get('hostname')}: {e}")
        print(f"{d['hostname']:<14}{d['ip']:<16}{status}")
        results.append({**{k: d[k] for k in ("hostname", "ip", "device_type", "location")},
                        "status": status})

    output = {"checked_at": datetime.now().isoformat(timespec="seconds"),
              "mode": "live" if live else "simulation",
              "summary": {"total": len(results),
                          "up": sum(r["status"] == "UP" for r in results),
                          "down": sum(r["status"] == "DOWN" for r in results)},
              "results": results}
    try:
        with open(OUTPUT_FILE, "w") as f:
            json.dump(output, f, indent=2)
        print(f"\nResults saved to {OUTPUT_FILE}")
    except OSError as e:
        sys.exit(f"[ERROR] Could not write {OUTPUT_FILE}: {e}")


if __name__ == "__main__":
    main()
