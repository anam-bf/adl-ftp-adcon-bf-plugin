"""
Sample files in the ADCON Burkina Faso export format for the documentation
screenshot harness. Run inside the mock FTP source at start (SAMPLE_ROOT,
SAMPLE_TZ, SAMPLE_HOURS in the environment): one tab-separated file per
station and day, named <WIGOS id>-<YYYYMMDD>.txt, decimal comma, with the
day's 10-minute rows. Nothing here is real data.
"""

import math
import os
import random
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

ROOT = os.environ.get("SAMPLE_ROOT", "/srv/ftp")
TZ = ZoneInfo(os.environ.get("SAMPLE_TZ", "Africa/Ouagadougou"))
HOURS = int(os.environ.get("SAMPLE_HOURS", "48"))

# (WIGOS-style station code used in the filename and the "Code station" column)
STATIONS = ["0-854-0-001", "0-854-0-002", "0-854-0-003"]
COLUMNS = ["Code station", "Date", "Heure", "Temperature", "Humidite", "Pression",
           "Pluie", "Vent vitesse", "Vent direction"]


def fr(value, digits):
    return f"{value:.{digits}f}".replace(".", ",")


def row(code, moment):
    rng = random.Random(f"{code}-{moment:%Y%m%d%H%M}")
    hour = moment.hour + moment.minute / 60
    diurnal = math.sin((hour - 9) / 24 * 2 * math.pi)
    return "\t".join([
        code,
        moment.strftime("%Y%d%m"),      # the export writes YYYYDDMM
        moment.strftime("%H%M"),
        fr(29 + 7 * diurnal + rng.uniform(-0.4, 0.4), 1),
        fr(45 - 20 * diurnal + rng.uniform(-2, 2), 0),
        fr(978 + 1.5 * math.sin(hour / 12 * math.pi) + rng.uniform(-0.3, 0.3), 1),
        fr(rng.choice([0, 0, 0, 0, 0, 0.2, 0.6]) if 15 <= hour <= 18 else 0, 1),
        fr(max(0.0, 2 + 1.5 * diurnal + rng.uniform(-0.6, 0.6)), 1),
        fr((200 + 30 * diurnal + rng.uniform(-20, 20)) % 360, 0),
    ])


def main():
    now = datetime.now(TZ).replace(second=0, microsecond=0)
    now -= timedelta(minutes=now.minute % 10)
    start = now - timedelta(hours=HOURS)
    moments = [start + timedelta(minutes=10 * i) for i in range(HOURS * 6 + 1)]
    by_day = {}
    for m in moments:
        by_day.setdefault(m.date(), []).append(m)

    for code in STATIONS:
        for day, day_moments in by_day.items():
            path = f"{ROOT}/adcon-bf/{code}-{day:%Y%m%d}.txt"
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", newline="") as f:
                f.write("\t".join(COLUMNS) + "\r\n")
                for m in day_moments:
                    f.write(row(code, m) + "\r\n")
    print(f"[mock-ftp] adcon-bf samples for {len(STATIONS)} stations, {len(by_day)} day(s)", flush=True)


if __name__ == "__main__":
    main()
