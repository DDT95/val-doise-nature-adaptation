#!/usr/bin/env python3
"""Build commune/EPCI nature profiles from the versioned public datasets."""

from __future__ import annotations

import json
import math
import urllib.request
from pathlib import Path

from pyproj import Transformer
from shapely.geometry import mapping, shape
from shapely.ops import transform, unary_union

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TO_METERS = Transformer.from_crs("EPSG:4326", "EPSG:2154", always_xy=True).transform


def read(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def clean(geometry):
    geom = shape(geometry)
    return geom if geom.is_valid else geom.buffer(0)


def hectares(geom):
    return transform(TO_METERS, geom).area / 10_000


def kilometers(geom):
    return transform(TO_METERS, geom).length / 1_000


def clipped_union(features, territory):
    hits = []
    for feature in features:
        geom = clean(feature["geometry"])
        if geom.intersects(territory):
            part = geom.intersection(territory)
            if not part.is_empty:
                hits.append(part)
    return unary_union(hits) if hits else None


def clipped_length(features, territory):
    total = 0.0
    for feature in features:
        geom = clean(feature["geometry"])
        if geom.intersects(territory):
            total += kilometers(geom.intersection(territory))
    return total


def count_points(features, territory):
    return sum(clean(f["geometry"]).intersects(territory) for f in features)


def observations(features, territory):
    total = 0
    last = None
    for feature in features:
        geom = clean(feature["geometry"])
        if geom.intersects(territory):
            props = feature.get("properties", {})
            total += int(props.get("nb_observations") or 0)
            year = props.get("last_observation")
            last = max(last or 0, int(year or 0)) or last
    return total, last


def profile(code, name, geom, sources, population=0, members=None):
    area = hectares(geom)
    vegetation = clipped_union(sources["vegetation"], geom)
    reservoirs = clipped_union(sources["reservoirs"], geom)
    obs, last_obs = observations(sources["observations"], geom)
    veg_area = hectares(vegetation) if vegetation else 0
    reservoir_area = hectares(reservoirs) if reservoirs else 0
    water_km = clipped_length(sources["water"], geom)
    links = count_points(sources["connections"], geom)
    veg_pct = min(100, 100 * veg_area / area) if area else 0
    reservoir_pct = min(100, 100 * reservoir_area / area) if area else 0
    water_density = water_km / (area / 100) if area else 0
    return {
        "code": code,
        "name": name,
        "population": population,
        "members": members or [code],
        "area_ha": round(area, 1),
        "vegetation_ha": round(veg_area, 1),
        "vegetation_pct": round(veg_pct, 1),
        "reservoir_ha": round(reservoir_area, 1),
        "reservoir_pct": round(reservoir_pct, 1),
        "water_km": round(water_km, 1),
        "water_density": round(water_density, 2),
        "connections": links,
        "observations": obs,
        "last_observation": last_obs,
    }


def main():
    communes_fc = read("communes_95.geojson")
    znieff = read("znieff1.json")["features"] + read("znieff2.json")["features"]
    protected = read("espaces-naturels-proteges.json")["features"]
    sources = {
        "vegetation": read("zones-vegetation.geojson")["features"],
        "reservoirs": znieff + protected,
        "water": read("cours_eau.geojson")["features"],
        "connections": read("connexions-ecologiques.json")["features"],
        "observations": read("observations-mailles.json")["features"],
    }
    commune_geoms = {f["properties"]["code"]: clean(f["geometry"]) for f in communes_fc["features"]}
    communes = {}
    for index, feature in enumerate(communes_fc["features"], 1):
        props = feature["properties"]
        code = props["code"]
        print(f"Commune {index:03d}/183 · {props['nom']}")
        communes[code] = profile(code, props["nom"], commune_geoms[code], sources, props.get("population", 0))

    request = urllib.request.Request(
        "https://geo.api.gouv.fr/departements/95/communes?fields=nom,code,population,codeEpci&format=json",
        headers={"User-Agent": "DDT95-nature-adaptation/1.0"},
    )
    api_communes = json.load(urllib.request.urlopen(request, timeout=30))
    groups = {}
    for item in api_communes:
        if item["code"] in commune_geoms and item.get("codeEpci"):
            groups.setdefault(item["codeEpci"], []).append(item["code"])
    epcis = {}
    epci_features = []
    for code, members in sorted(groups.items()):
        req = urllib.request.Request(f"https://geo.api.gouv.fr/epcis/{code}", headers={"User-Agent": "DDT95-nature-adaptation/1.0"})
        info = json.load(urllib.request.urlopen(req, timeout=30))
        geom = unary_union([commune_geoms[m] for m in members])
        epcis[code] = profile(code, info.get("nom", code), geom, sources, sum(communes[m]["population"] for m in members), members)
        epci_features.append({"type": "Feature", "properties": {"code": code, "nom": epcis[code]["name"]}, "geometry": mapping(geom)})
        print(f"EPCI · {epcis[code]['name']}")

    (DATA / "commune_profiles.json").write_text(json.dumps(communes, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (DATA / "epci_profiles.json").write_text(json.dumps(epcis, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (DATA / "epcis_95.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": epci_features}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print("Profiles written.")


if __name__ == "__main__":
    main()
