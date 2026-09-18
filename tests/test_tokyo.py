from tokyo.canonical import canonical_json_bytes,sha256_hex
from tokyo.compiler import certificate,compile_movement


SPEC={
    "id":"東京-tokyo",
    "oscillator":{"frequency_hz":4.0},
    "displays":[
        {"id":"seconds","period_s":60.0},
        {"id":"minutes","period_s":3600.0},
        {"id":"hours","period_s":43200.0}
    ]
}


def test_canonical_equivalent_numbers_hash_equal():
    a={"x":1.0,"y":-0.0}
    b={"y":0,"x":1}
    assert canonical_json_bytes(a)==canonical_json_bytes(b)
    assert sha256_hex(a)==sha256_hex(b)


def test_unicode_preserved():
    assert "東京".encode("utf-8") in canonical_json_bytes({"id":"東京"})


def test_compiler_is_deterministic():
    a=certificate(SPEC)
    b=certificate({
        "displays":list(reversed(SPEC["displays"])),
        "oscillator":{"frequency_hz":4},
        "id":"東京-tokyo",
    })
    assert a["resolved_sha256"]==b["resolved_sha256"]


def test_seconds_ratio_is_one():
    movement=compile_movement(SPEC)
    seconds=next(d for d in movement.displays if d.id=="seconds")
    assert abs(seconds.resolved_ratio-1.0)<1e-12


def test_minutes_ratio_is_sixty():
    movement=compile_movement(SPEC)
    minutes=next(d for d in movement.displays if d.id=="minutes")
    assert abs(minutes.resolved_ratio-60.0)<1e-12


def test_hours_ratio_is_720():
    movement=compile_movement(SPEC)
    hours=next(d for d in movement.displays if d.id=="hours")
    assert abs(hours.resolved_ratio-720.0)<1e-12
