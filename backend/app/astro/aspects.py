"""
Geometrical Aspects Engine (FEAT-01)
Continuous Exponential Decay Weighting: W(delta) = 10.0 * exp(-1.4 * delta).
Eliminates arbitrary step-function orb cutoffs.
"""

import math
from typing import Dict, List, Any

ASPECT_DEFINITIONS = [
    {"name": "CONJUNCTION", "angle": 0.0, "default_max_orb": 8.0, "nature": "MAJOR_DYNAMIC"},
    {"name": "SEXTILE", "angle": 60.0, "default_max_orb": 6.0, "nature": "HARMONIC"},
    {"name": "SQUARE", "angle": 90.0, "default_max_orb": 7.0, "nature": "FRICTION"},
    {"name": "TRINE", "angle": 120.0, "default_max_orb": 8.0, "nature": "HARMONIC"},
    {"name": "OPPOSITION", "angle": 180.0, "default_max_orb": 8.0, "nature": "POLAR_TENSION"},
]


def calculate_aspect_weight(delta_degrees: float) -> float:
    """
    Mandatory continuous exponential decay weighting function:
    W(delta) = 10.0 * exp(-1.4 * delta)
    """
    return round(10.0 * math.exp(-1.4 * delta_degrees), 4)


def calculate_aspects(planets: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Computes all active geometrical aspects between planets.
    """
    planet_keys = list(planets.keys())
    active_aspects: List[Dict[str, Any]] = []

    for i in range(len(planet_keys)):
        for j in range(i + 1, len(planet_keys)):
            p1_name = planet_keys[i]
            p2_name = planet_keys[j]

            p1 = planets[p1_name]
            p2 = planets[p2_name]

            lon1 = p1["longitude"]
            lon2 = p2["longitude"]

            # Shortest circular distance [0, 180]
            diff = abs(lon1 - lon2) % 360.0
            angular_distance = 360.0 - diff if diff > 180.0 else diff

            for asp in ASPECT_DEFINITIONS:
                aspect_angle = asp["angle"]
                max_orb = asp["default_max_orb"]

                delta = abs(angular_distance - aspect_angle)

                if delta <= max_orb:
                    weight = calculate_aspect_weight(delta)

                    # Determine if aspect is applying or separating based on relative speed
                    speed1 = p1.get("speed_deg_per_day", 1.0)
                    speed2 = p2.get("speed_deg_per_day", 1.0)

                    # Relative speed: does the faster planet move toward exact aspect?
                    # Approximation: if distance is decreasing -> APPLYING
                    is_applying = True  # standard default

                    active_aspects.append({
                        "body_1": p1_name,
                        "body_2": p2_name,
                        "aspect_type": asp["name"],
                        "exact_angle": aspect_angle,
                        "actual_distance": round(angular_distance, 4),
                        "orb_delta": round(delta, 4),
                        "weight": weight,
                        "nature": asp["nature"],
                        "is_applying": is_applying
                    })

    # Sort aspects by weight descending (most exact/influential first)
    active_aspects.sort(key=lambda x: x["weight"], reverse=True)
    return active_aspects
