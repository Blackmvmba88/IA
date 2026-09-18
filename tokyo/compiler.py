"""TOKYO deterministic movement compiler."""

from __future__ import annotations

from dataclasses import dataclass,asdict
from math import pi

from tokyo.canonical import sha256_hex
from tokyo.ratios import solve_two_stage_ratio


@dataclass(frozen=True)
class ResolvedDisplay:
    id:str
    period_s:float
    target_ratio_from_second:float
    resolved_ratio:float
    ratio_error:float
    stages:list[dict]


@dataclass(frozen=True)
class ResolvedMovement:
    id:str
    oscillator_frequency_hz:float
    displays:list[ResolvedDisplay]

    def payload(self)->dict:
        return {
            "id":self.id,
            "oscillator_frequency_hz":self.oscillator_frequency_hz,
            "displays":[asdict(d) for d in self.displays],
        }

    def hash(self)->str:
        return sha256_hex(self.payload())


def compile_movement(spec:dict)->ResolvedMovement:
    f=float(spec["oscillator"]["frequency_hz"])
    if f<=0:
        raise ValueError("oscillator frequency must be > 0")

    displays=[]
    for d in sorted(spec["displays"], key=lambda x:x["id"]):
        period=float(d["period_s"])
        target=period/60.0
        stages,actual=solve_two_stage_ratio(target)
        displays.append(
            ResolvedDisplay(
                id=d["id"],
                period_s=period,
                target_ratio_from_second=target,
                resolved_ratio=actual,
                ratio_error=actual-target,
                stages=[
                    {"driver":s.driver,"driven":s.driven}
                    for s in stages
                ],
            )
        )

    return ResolvedMovement(
        id=spec["id"],
        oscillator_frequency_hz=f,
        displays=displays,
    )


def certificate(spec:dict)->dict:
    resolved=compile_movement(spec)
    payload=resolved.payload()
    return {
        "compiler":"TOKYO",
        "version":"0.1.0",
        "resolved":payload,
        "resolved_sha256":resolved.hash(),
    }
