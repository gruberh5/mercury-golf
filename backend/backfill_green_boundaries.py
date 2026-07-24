"""
Mercury: Green Boundary Backfill
=================================

Adds each hole's full green polygon boundary to the database, using the
same GeoJSON export files you already saved from Overpass Turbo. This
enables Front/Middle/Back yardage -- calculated from the green's real
shape, not just its center point.

This is a one-off backfill for courses you already imported (Reeves,
Sharon Woods). New courses going forward get this automatically, since
import_course.py has been updated to capture it at import time.

How to run:
  1. Edit the CONFIG block for one course.
  2. Run: python -m backend.backfill_green_boundaries
  3. Edit CONFIG for the next course, run again.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from backend.db import connect

# =====================================================
# CONFIG -- edit for each course you're backfilling
# =====================================================
COURSE_ID = 4              # the course_id from your `courses` table (not the GolfCourseAPI id)
GEOJSON_PATH = r"C:\Users\grube\Downloads\twin-oaks.geojson"  # your saved combined green/tee/hole export for this course
# =====================================================


def haversine_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def load_greens_and_holes(path: str) -> tuple[list[dict], list[dict]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    greens = []
    holes = []

    for feature in data["features"]:
        golf_tag = feature["properties"].get("golf")
        if golf_tag == "green" and feature["geometry"]["type"] == "Polygon":
            ring = feature["geometry"]["coordinates"][0]  # [[lon, lat], ...]
            lats = [pt[1] for pt in ring]
            lons = [pt[0] for pt in ring]
            greens.append({
                "ring": ring,
                "lat": sum(lats) / len(lats),
                "lon": sum(lons) / len(lons),
            })
        elif golf_tag == "hole" and feature["geometry"]["type"] == "LineString":
            coords = feature["geometry"]["coordinates"]
            holes.append({
                "ref": int(feature["properties"]["ref"]),
                "start": (coords[0][1], coords[0][0]),
                "end": (coords[-1][1], coords[-1][0]),
            })

    return greens, holes


def match_greens_to_holes(greens: list[dict], holes: list[dict]) -> dict[int, list]:
    """Same nearest-endpoint matching logic as import_course.py, proven already."""
    matched = {}
    for hole in holes:
        candidates = []
        for endpoint in (hole["start"], hole["end"]):
            best = min(greens, key=lambda g: haversine_meters(endpoint[0], endpoint[1], g["lat"], g["lon"]))
            distance = haversine_meters(endpoint[0], endpoint[1], best["lat"], best["lon"])
            candidates.append((distance, best))
        distance, green = min(candidates, key=lambda c: c[0])
        matched[hole["ref"]] = green["ring"]
    return matched


def backfill() -> None:
    print(f"Backfilling green boundaries for course_id={COURSE_ID}...")
    greens, holes = load_greens_and_holes(GEOJSON_PATH)
    matched = match_greens_to_holes(greens, holes)
    print(f"Found {len(greens)} greens and {len(holes)} hole lines in the GeoJSON file.")
    print(f"Matched {len(matched)} holes to a green boundary.")

    total_rows_affected = 0
    with connect() as conn:
        with conn.cursor() as cur:
            for hole_number, ring in matched.items():
                cur.execute(
                    "UPDATE holes SET green_boundary = %s WHERE course_id = %s AND hole_number = %s",
                    (json.dumps(ring), COURSE_ID, hole_number),
                )
                if cur.rowcount == 0:
                    print(f"  WARNING: hole_number={hole_number} matched nothing in the database -- check COURSE_ID and hole_number values.")
                total_rows_affected += cur.rowcount
        conn.commit()

    print(f"Done. {total_rows_affected} real database rows actually updated.")


if __name__ == "__main__":
    backfill()