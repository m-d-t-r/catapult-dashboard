"""Check data.json against the shape index.html and map.html expect.

Fails the workflow (exit 1) so a malformed file is never committed.
"""
import datetime
import json
import sys

SECTIONS = {"closingSoon": "c", "openRolling": "o", "running": "r", "horizon": "h", "none": "n"}
REQUIRED = ["org", "name", "desc", "deadlineLabel", "url", "status", "short"]

path = sys.argv[1] if len(sys.argv) > 1 else "data.json"
errors = []
warnings = []

try:
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
except Exception as e:  # noqa: BLE001
    print(f"FAIL: {path} is not valid JSON: {e}")
    sys.exit(1)

try:
    datetime.date.fromisoformat(d.get("lastChecked", ""))
except ValueError:
    errors.append("lastChecked missing or not YYYY-MM-DD")

for key in ["changes", "gaps", *SECTIONS]:
    if not isinstance(d.get(key), list):
        errors.append(f"'{key}' missing or not a list")

total = 0
for section, code in SECTIONS.items():
    for i, item in enumerate(d.get(section) or []):
        total += 1
        where = f"{section}[{i}] ({item.get('name', '?')})"
        for field in REQUIRED:
            if not item.get(field):
                errors.append(f"{where}: missing '{field}'")
        if item.get("status") and item["status"] != code:
            errors.append(f"{where}: status '{item['status']}' does not match section (expected '{code}')")
        if section == "closingSoon":
            try:
                datetime.date.fromisoformat(item.get("deadline", ""))
            except ValueError:
                errors.append(f"{where}: closingSoon item needs an ISO 'deadline'")
        for line in (item.get("short") or "").split("|"):
            if len(line) > 28:
                warnings.append(f"{where}: map label line over 28 characters: '{line}'")

if total < 10:
    errors.append(f"only {total} programmes in total; refusing to commit a near-empty file")

for w in warnings:
    print("warning:", w)

if errors:
    print("FAIL:")
    for e in errors:
        print(" -", e)
    sys.exit(1)

print("ok", {k: len(v) for k, v in d.items() if isinstance(v, list)})
