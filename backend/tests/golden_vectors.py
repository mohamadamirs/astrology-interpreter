"""
Golden Dataset / Ground-Truth Reference Vectors
Tolerance: <= 0.001 degrees (3.6 arcseconds) for ephemeris positions.
"""

from typing import Dict, Any, List

GOLDEN_VECTORS: List[Dict[str, Any]] = [
    {
        "id": "JAKARTA_EPOCH_2000",
        "label": "Jakarta, Indonesia - Epoch 2000",
        "input": {
            "latitude": -6.2088,
            "longitude": 106.8456,
            "local_datetime": "2000-01-01T12:00:00",
        },
        "expected_geo": {
            "iana_timezone": "Asia/Jakarta",
            "utc_iso": "2000-01-01T05:00:00Z",
            "utc_offset_hours": 7.0,
        },
        "expected_astro": {
            "julian_day": 2451544.708333,
            "sun_tropical_longitude": 280.08125,
            "moon_tropical_longitude": 219.81485,
        }
    },
    {
        "id": "LONDON_SOLSTICE_2024",
        "label": "London, UK - Summer Solstice 2024 (BST / Daylight Saving)",
        "input": {
            "latitude": 51.5074,
            "longitude": -0.1278,
            "local_datetime": "2024-06-21T13:00:00",
        },
        "expected_geo": {
            "iana_timezone": "Europe/London",
            "utc_iso": "2024-06-21T12:00:00Z",
            "utc_offset_hours": 1.0,  # British Summer Time (BST)
        },
        "expected_astro": {
            "julian_day": 2460483.0,
            "sun_tropical_longitude": 90.26692,  # 0 deg 16 min Cancer
        }
    },
    {
        "id": "TOKYO_EQUINOX_2023",
        "label": "Tokyo, Japan - Vernal Equinox 2023",
        "input": {
            "latitude": 35.6762,
            "longitude": 139.6503,
            "local_datetime": "2023-03-21T09:00:00",
        },
        "expected_geo": {
            "iana_timezone": "Asia/Tokyo",
            "utc_iso": "2023-03-21T00:00:00Z",
            "utc_offset_hours": 9.0,  # JST (no DST)
        },
        "expected_astro": {
            "julian_day": 2460024.5,
            "sun_tropical_longitude": 359.79148,  # 29 deg 47 min Pisces
        }
    }
]
