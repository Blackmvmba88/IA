from tokyo.canonical import canonical_json_bytes,sha256_hex
from tokyo.compiler import certificate,compile_movement


SPEC={
    "id":"東京-tokyo",
    "oscillator":{"frequency_hz":4.0},
    "displays":[
        {"id":"seconds","period_s":60.0},
        {"id":"minutes","source_id":"seconds","period_s":3600.0},
        {"id":"hours","source_id":"minutes","period_s":43200.0},
        {"id":"day","source_id":"hours","period_s":86400.0},
    ]
}


def test_canonical_equivalent_numbers_hash_equal():
    a={"x":1.0,"y":-0.0}
    b={"y":0,"x":1}
    assert canonical_json_bytes(a)==canonical_json_bytes(b)
    assert sha256_hex(a)==sha256_hex(b)


def test_unicode_preserved():
    assert "東京".encode("utf-8") in canonical_json_bytes({"id":"東京"})


def test_compiler_is_deterministic_under_input_reordering():
    a=certificate(SPEC)
    b=certificate({
        "displays":list(reversed(SPEC["displays"])),
        "oscillator":{"frequency_hz":4},
        "id":"東京-tokyo",
    })
    assert a["resolved_sha256"]==b["resolved_sha256"]


def _display(movement,id_):
    return next(d for d in movement.displays if d.id==id_)


def test_seconds_ratio_is_one():
    d=_display(compile_movement(SPEC),"seconds")
    assert d.source_id=="$seconds"
    assert abs(d.resolved_ratio-1.0)<1e-12


def test_minutes_ratio_is_sixty():
    d=_display(compile_movement(SPEC),"minutes")
    assert d.source_id=="seconds"
    assert abs(d.resolved_ratio-60.0)<1e-12


def test_hours_are_resolved_from_minutes_not_seconds():
    d=_display(compile_movement(SPEC),"hours")
    assert d.source_id=="minutes"
    assert abs(d.target_ratio-12.0)<1e-12
    assert abs(d.resolved_ratio-12.0)<1e-12


def test_day_is_two_to_one_from_hours():
    d=_display(compile_movement(SPEC),"day")
    assert abs(d.resolved_ratio-2.0)<1e-12


def test_missing_source_or_cycle_fails_closed():
    bad={
        "id":"bad",
        "oscillator":{"frequency_hz":4},
        "displays":[
            {"id":"a","source_id":"b","period_s":60},
            {"id":"b","source_id":"a","period_s":120}
        ]
    }
    try:
        compile_movement(bad)
    except ValueError as e:
        assert "dependency cycle" in str(e)
    else:
        raise AssertionError("cycle must fail")
