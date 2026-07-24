"""
Mercury: Course Importer
========================

What this does, in order:
  1. Calls GolfCourseAPI for one course -> gets club/course name, tees,
     and each hole's par/yardage/stroke-index per tee.
  2. Reads a GeoJSON file you already exported from Overpass Turbo for
     that same course -> gets real green locations and OSM's own
     hole ref/par tags.
  3. Matches each OSM green polygon to the correct hole number by
     finding which green is physically closest to each hole line's
     green-side end.
  4. Inserts everything into courses / holes / tees / tee_holes.

How to run it:
  1. Edit the CONFIG block right below these instructions for the
     course you're importing.
  2. Run:  python import_course.py
  3. Check the printed summary at the end, then verify in your SQL
     client with:  SELECT * FROM courses; SELECT * FROM holes; etc.
  4. Edit the CONFIG block again for the next course, run again.

This is a one-off tool you run once per course, not something the
app runs automatically (yet).
"""

from __future__ import annotations

import json
import math
import os
from pathlib import Path

import requests

from backend.db import _load_local_env, connect


# =====================================================
# CONFIG -- edit these three values for each course you import
# =====================================================

GOLFCOURSEAPI_COURSE_ID = 17465          # the "id" field from your earlier /v1/search or /v1/courses/{id} test
GEOJSON_PATH = r"C:\Users\grube\Downloads\raintree-north-2.geojson"  # path to the combined green/tee/hole export you saved
COURSE_LABEL = "Raintree_North"     # just for the printed summary, not stored

# =====================================================


def haversine_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Straight-line distance between two lat/lon points, in meters."""
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def polygon_centroid(coordinates: list[list[float]]) -> tuple[float, float]:
    """Simple average-of-vertices centroid. Good enough for a feature the
    size of a putting green -- true area-weighted centroid isn't needed
    at this scale."""
    lons = [pt[0] for pt in coordinates]
    lats = [pt[1] for pt in coordinates]
    return sum(lats) / len(lats), sum(lons) / len(lons)


def fetch_golfcourseapi_data(course_id: int) -> dict:
    _load_local_env()
    api_key = os.getenv("GOLFCOURSEAPI_KEY")
    if not api_key:
        raise SystemExit("Set GOLFCOURSEAPI_KEY in your .env file first.")

    response = requests.get(
        f"https://api.golfcourseapi.com/v1/courses/{course_id}",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()["course"]


def load_osm_export(path: str) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    greens = []
    holes = []

    for feature in data["features"]:
        golf_tag = feature["properties"].get("golf")
        if golf_tag == "green" and feature["geometry"]["type"] == "Polygon":
            ring = feature["geometry"]["coordinates"][0]
            lat, lon = polygon_centroid(ring)
            greens.append({"lat": lat, "lon": lon, "ring": ring})
        elif golf_tag == "hole" and feature["geometry"]["type"] == "LineString":
            coords = feature["geometry"]["coordinates"]
            holes.append(
                {
                    "ref": int(feature["properties"]["ref"]),
                    "par": int(feature["properties"]["par"]),
                    "start": (coords[0][1], coords[0][0]),  # (lat, lon)
                    "end": (coords[-1][1], coords[-1][0]),
                }
            )

    return {"greens": greens, "holes": holes}


def match_greens_to_holes(osm: dict) -> dict[int, dict]:
    """Returns {hole_number: {"par": int, "green_lat": float, "green_lon": float}}"""
    matched: dict[int, dict] = {}

    for hole in osm["holes"]:
        # whichever endpoint is closer to ITS nearest green is the green-side end
        candidates = []
        for endpoint in (hole["start"], hole["end"]):
            best_green = min(
                osm["greens"],
                key=lambda g: haversine_meters(endpoint[0], endpoint[1], g["lat"], g["lon"]),
            )
            distance = haversine_meters(endpoint[0], endpoint[1], best_green["lat"], best_green["lon"])
            candidates.append((distance, best_green))

        distance, green = min(candidates, key=lambda c: c[0])

        if distance > 60:  # meters -- a green shouldn't be this far from its own hole line
            print(f"  WARNING: hole {hole['ref']} nearest green is {distance:.0f}m away -- check manually")

        matched[hole["ref"]] = {
            "par": hole["par"],
            "green_lat": green["lat"],
            "green_lon": green["lon"],
            "green_boundary": green["ring"],
        }

    return matched


def import_course(course_id: int, geojson_path: str, label: str) -> None:
    print(f"Importing {label}...")

    api_data = fetch_golfcourseapi_data(course_id)
    osm = load_osm_export(geojson_path)
    matched_holes = match_greens_to_holes(osm)

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT course_id FROM courses WHERE golfcourseapi_id = %s
                """,
                (course_id,),
            )
            if cur.fetchone():
                raise SystemExit(f"Course {course_id} already imported. Skipping to avoid duplicates.")

            cur.execute(
                """
                INSERT INTO courses (golfcourseapi_id, club_name, course_name, city, state, country, address, has_osm_mapping)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING course_id
                """,
                (
                    course_id,
                    api_data["club_name"],
                    api_data["course_name"],
                    api_data["location"].get("city"),
                    api_data["location"].get("state"),
                    api_data["location"].get("country"),
                    api_data["location"].get("address"),
                    len(osm["greens"]) > 0,
                ),
            )
            new_course_id = cur.fetchone()["course_id"]

            # holes: one row per hole_number, using OSM's par when we have a
            # match, otherwise falling back to GolfCourseAPI's hole array
            hole_id_by_number: dict[int, int] = {}
            any_tee_group = next(iter(api_data["tees"].values()))[0]
            for i, hole_from_api in enumerate(any_tee_group["holes"], start=1):
                osm_match = matched_holes.get(i)
                par = osm_match["par"] if osm_match else hole_from_api["par"]
                green_lat = osm_match["green_lat"] if osm_match else None
                green_lon = osm_match["green_lon"] if osm_match else None
                green_boundary = json.dumps(osm_match["green_boundary"]) if osm_match else None

                cur.execute(
                    """
                    INSERT INTO holes (course_id, hole_number, par, green_lat, green_lon, green_boundary)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING hole_id
                    """,
                    (new_course_id, i, par, green_lat, green_lon, green_boundary),
                )
                hole_id_by_number[i] = cur.fetchone()["hole_id"]

            # tees + tee_holes
            for gender, tee_list in api_data["tees"].items():
                for tee in tee_list:
                    cur.execute(
                        """
                        INSERT INTO tees (course_id, tee_name, gender, course_rating, slope_rating, total_yards, par_total)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        RETURNING tee_id
                        """,
                        (
                            new_course_id,
                            tee["tee_name"],
                            gender,
                            tee["course_rating"],
                            tee["slope_rating"],
                            tee["total_yards"],
                            tee["par_total"],
                        ),
                    )
                    tee_id = cur.fetchone()["tee_id"]

                    for i, hole_from_api in enumerate(tee["holes"], start=1):
                        cur.execute(
                            """
                            INSERT INTO tee_holes (tee_id, hole_id, yardage, handicap_index)
                            VALUES (%s, %s, %s, %s)
                            """,
                            (tee_id, hole_id_by_number[i], hole_from_api["yardage"], hole_from_api["handicap"]),
                        )

        conn.commit()

    matched_count = len(matched_holes)
    print(f"Done. Inserted course_id={new_course_id}, {len(hole_id_by_number)} holes ({matched_count} with real green coordinates).")


if __name__ == "__main__":
    import_course(GOLFCOURSEAPI_COURSE_ID, GEOJSON_PATH, COURSE_LABEL)