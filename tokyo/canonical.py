"""Canonical serialization rules for TOKYO certificates."""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any


def _normalize_number(x: float) -> int | float:
    if not math.isfinite(x):
        raise ValueError("NaN/Infinity are forbidden in TOKYO canonical data")
    if x == 0.0:
        return 0
    if x.is_integer():
        return int(x)
    return x


def normalize(value: Any) -> Any:
    if isinstance(value, bool) or value is None or isinstance(value, str):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return _normalize_number(value)
    if isinstance(value, list):
        return [normalize(v) for v in value]
    if isinstance(value, tuple):
        return [normalize(v) for v in value]
    if isinstance(value, dict):
        return {str(k): normalize(value[k]) for k in sorted(value)}
    raise TypeError(f"unsupported canonical type: {type(value).__name__}")


def canonical_json_bytes(value: Any) -> bytes:
    normalized = normalize(value)
    return json.dumps(
        normalized,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",",":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256_hex(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()
