#!/usr/bin/env python3
"""Construit les données légères de la carte chaleur/refuges du Val-d'Oise."""

from __future__ import annotations

import csv
import io
import json
import math
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

from shapely import force_2d
from shapely.geometry import Point, mapping, shape
from shapely.strtree import STRtree

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ICU_DATASET = "ilots-de-chaleur-urbains-icu-classification-des-imu-en-zone-climatique-locale-lc"
ICU_BASE = f"https://data.iledefrance.fr/api/explore/v2.1/catalog/datasets/{ICU_DATASET}/exports/csv"
BBOX_POLYGON = "POLYGON((1.60 48.88,2.60 48.88,2.60 49.25,1.60 49.25,1.60 48.88))"


def rounded_coordinates(value):
    if isinstance(value, (list, tuple)):
        if value and isinstance(value[0], (int, float)):
            return [round(float(coordinate), 5) for coordinate in value[:2]]
        return [rounded_coordinates(item) for item in value]
    return value


def fetch(url: str, data: bytes | None = None, timeout: int = 180) -> bytes:
    request = urllib.request.Request(url, data=data, headers={"User-Agent": "DDT95-atlas/1.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def load_boundaries():
    department = shape(json.loads((DATA / "val-doise.geojson").read_text())["features"][0]["geometry"])
    communes_geojson = json.loads((DATA / "communes_95.geojson").read_text())
    communes = []
    for feature in communes_geojson["features"]:
        props = feature["properties"]
        communes.append({
            "code": str(props.get("code") or props.get("code_insee") or props.get("insee")),
            "name": props.get("nom") or props.get("name") or props.get("libelle"),
            "geometry": shape(feature["geometry"]),
        })
    return department, communes


def parse_point(value: str):
    lat, lon = (float(part.strip()) for part in value.split(","))
    return lat, lon


def build_heat(department, communes):
    query = urllib.parse.urlencode({
        "where": f"within(geo_point_2d, geom'{BBOX_POLYGON}')",
        "select": "geo_point_2d,aleaj_note,alean_note,alea_j_cl,alea_n_cl,vulnj_note,vulnn_note,permeable,bati",
        "limit": -1,
    })
    rows = csv.DictReader(io.StringIO(fetch(f"{ICU_BASE}?{query}").decode("utf-8-sig")), delimiter=";")
    grid = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0, 0])
    commune_geoms = [item["geometry"] for item in communes]
    commune_tree = STRtree(commune_geoms)
    summaries = {item["code"]: {"name": item["name"], "day": [], "night": [], "vulnerability": []} for item in communes}

    for row in rows:
        if not row["geo_point_2d"]:
            continue
        lat, lon = parse_point(row["geo_point_2d"])
        point = Point(lon, lat)
        if not department.covers(point):
            continue
        day = float(row["alea_j_cl"] or 0)
        night = float(row["alea_n_cl"] or 0)
        vulnerability = float(row["vulnn_note"] or row["vulnj_note"] or 0)
        # Les classes IPR vont des espaces rafraîchissants (-1) aux îlots les plus chauds.
        intensity_day = max(0.03, min(1.0, (day + 1) / 6))
        intensity_night = max(0.03, min(1.0, (night + 1) / 6))
        key = (round(lat / 0.004) * 0.004, round(lon / 0.005) * 0.005)
        cell = grid[key]
        cell[0] += intensity_day
        cell[1] += intensity_night
        cell[2] += day
        cell[3] += night
        cell[4] += 1

        candidates = commune_tree.query(point)
        for index in candidates:
            item = communes[int(index)]
            if item["geometry"].covers(point):
                summary = summaries[item["code"]]
                summary["day"].append(day)
                summary["night"].append(night)
                summary["vulnerability"].append(vulnerability)
                break

    points = []
    for (lat, lon), (day_i, night_i, day_class, night_class, count) in grid.items():
        points.append([
            round(lat, 5), round(lon, 5), round(day_i / count, 3), round(night_i / count, 3),
            round(day_class / count, 2), round(night_class / count, 2), count,
        ])

    profiles = {}
    for code, values in summaries.items():
        if not values["day"]:
            continue
        hot_day = sum(value >= 3 for value in values["day"]) / len(values["day"]) * 100
        hot_night = sum(value >= 3 for value in values["night"]) / len(values["night"]) * 100
        profiles[code] = {
            "name": values["name"],
            "day": round(sum(values["day"]) / len(values["day"]), 2),
            "night": round(sum(values["night"]) / len(values["night"]), 2),
            "hot_day_pct": round(hot_day, 1),
            "hot_night_pct": round(hot_night, 1),
            "vulnerability": round(sum(values["vulnerability"]) / len(values["vulnerability"]), 2),
            "cells": len(values["day"]),
        }
    (DATA / "heat_points.json").write_text(json.dumps(points, ensure_ascii=False, separators=(",", ":")))
    (DATA / "commune_profiles.json").write_text(json.dumps(profiles, ensure_ascii=False, indent=2))

    polygon_query = urllib.parse.urlencode({
        "where": f"within(geo_point_2d, geom'{BBOX_POLYGON}')",
        "select": "geo_shape,alea_j_cl,alea_n_cl",
        "limit": -1,
    })
    polygon_url = ICU_BASE.replace("/exports/csv", "/exports/geojson") + f"?{polygon_query}"
    polygon_source = json.loads(fetch(polygon_url, timeout=300))
    polygon_features = []
    for feature in polygon_source.get("features", []):
        if not feature.get("geometry"):
            continue
        geometry = force_2d(shape(feature["geometry"]))
        if geometry.is_empty or not department.covers(geometry.representative_point()):
            continue
        geometry = geometry.simplify(0.000025, preserve_topology=True)
        properties = feature.get("properties", {})
        geometry_mapping = mapping(geometry)
        geometry_mapping["coordinates"] = rounded_coordinates(geometry_mapping["coordinates"])
        polygon_features.append({
            "type": "Feature",
            "properties": {
                "day": properties.get("alea_j_cl", -1),
                "night": properties.get("alea_n_cl", -1),
            },
            "geometry": geometry_mapping,
        })
    (DATA / "heat_polygons.geojson").write_text(json.dumps({
        "type": "FeatureCollection", "features": polygon_features,
    }, ensure_ascii=False, separators=(",", ":")))


def build_refuges(department):
    overpass = """
[out:json][timeout:180];
(
  nwr[amenity=library](48.88,1.60,49.25,2.60);
  nwr[amenity=drinking_water](48.88,1.60,49.25,2.60);
  nwr[leisure=park](48.88,1.60,49.25,2.60);
  nwr[leisure=garden](48.88,1.60,49.25,2.60);
  nwr[leisure=swimming_pool](48.88,1.60,49.25,2.60);
  nwr[leisure=water_park](48.88,1.60,49.25,2.60);
);
out center tags;
""".strip()
    payload = urllib.parse.urlencode({"data": overpass}).encode()
    raw = json.loads(fetch("https://overpass-api.de/api/interpreter", data=payload, timeout=240))
    categories = {
        ("amenity", "library"): ("Bibliothèque", "indoor"),
        ("amenity", "drinking_water"): ("Point d’eau", "water"),
        ("leisure", "park"): ("Parc", "outdoor"),
        ("leisure", "garden"): ("Jardin", "outdoor"),
        ("leisure", "swimming_pool"): ("Piscine", "water"),
        ("leisure", "water_park"): ("Base de loisirs", "water"),
    }
    refuges, seen = [], set()
    for element in raw["elements"]:
        center = element.get("center", element)
        if "lat" not in center or "lon" not in center:
            continue
        point = Point(center["lon"], center["lat"])
        if not department.covers(point):
            continue
        tags = element.get("tags", {})
        match = next((value for key, value in categories.items() if tags.get(key[0]) == key[1]), None)
        if not match:
            continue
        label, family = match
        access = (tags.get("access") or "").lower()
        if access in {"private", "no"}:
            continue
        if label == "Piscine":
            # Les bassins résidentiels sont très nombreux dans OSM. Une piscine n'est
            # retenue que si elle est nommée et documentée comme équipement accessible
            # au public, aux clients/adhérents ou gérée par un opérateur identifiable.
            has_public_signal = access in {"yes", "public", "permissive", "customers", "members"}
            has_operator_signal = any(tags.get(key) for key in ("operator", "website", "contact:website", "fee"))
            if not tags.get("name") or not (has_public_signal or has_operator_signal):
                continue
        name = tags.get("name") or ("Fontaine d’eau potable" if label == "Point d’eau" else label)
        signature = (round(center["lat"], 5), round(center["lon"], 5), label)
        if signature in seen:
            continue
        seen.add(signature)
        refuges.append({
            "id": f"osm-{element['type']}-{element['id']}", "name": name, "type": label, "family": family,
            "lat": round(center["lat"], 6), "lon": round(center["lon"], 6),
            "access": tags.get("access", "public/non précisé"), "opening_hours": tags.get("opening_hours"),
            "source": "OpenStreetMap",
        })
    (DATA / "refuges.json").write_text(json.dumps(refuges, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    department_geometry, commune_items = load_boundaries()
    build_heat(department_geometry, commune_items)
    build_refuges(department_geometry)
    print("Données construites dans", DATA)
