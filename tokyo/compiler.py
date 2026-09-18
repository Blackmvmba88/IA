"""TOKYO deterministic movement compiler.

Displays form a dependency graph. Each display transforms the period of a
resolved upstream shaft instead of always reducing directly from seconds.

Example:
    seconds -> minutes -> hours -> day -> moon -> year
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

from tokyo.canonical import sha256_hex
from tokyo.ratios import solve_two_stage_ratio


BASE_SECOND_ID="$seconds"
BASE_SECOND_PERIOD_S=60.0


@dataclass(frozen=True)
class ResolvedDisplay:
    id:str
    source_id:str
    source_period_s:float
    period_s:float
    target_ratio:float
    resolved_ratio:float
    ratio_error:float
    stages:list[dict]
    kind:str|None=None
    radius_mm:float|None=None
    z_mm:float|None=None


@dataclass(frozen=True)
class ResolvedMovement:
    id:str
    oscillator_frequency_hz:float
    displays:list[ResolvedDisplay]

    def payload(self)->dict:
        return {
            "id":self.id,
            "oscillator_frequency_hz":self.oscillator_frequency_hz,
            "displays":[asdict(d) for d in sorted(self.displays,key=lambda x:x.id)],
        }

    def hash(self)->str:
        return sha256_hex(self.payload())


def _resolve_graph(displays:list[dict])->list[ResolvedDisplay]:
    ids=[d["id"] for d in displays]
    if len(ids)!=len(set(ids)):
        raise ValueError("display ids must be unique")

    pending={d["id"]:dict(d) for d in displays}
    periods={BASE_SECOND_ID:BASE_SECOND_PERIOD_S}
    resolved:list[ResolvedDisplay]=[]

    while pending:
        progress=False
        for display_id in sorted(list(pending)):
            d=pending[display_id]
            source_id=d.get("source_id") or BASE_SECOND_ID
            if source_id not in periods:
                continue

            source_period=float(periods[source_id])
            period=float(d["period_s"])
            if period<=0:
                raise ValueError(f"{display_id}: period_s must be > 0")

            target=period/source_period
            if target<=0:
                raise ValueError(f"{display_id}: invalid period ratio")

            stages,actual=solve_two_stage_ratio(target)
            resolved.append(
                ResolvedDisplay(
                    id=display_id,
                    source_id=source_id,
                    source_period_s=source_period,
                    period_s=period,
                    target_ratio=target,
                    resolved_ratio=actual,
                    ratio_error=actual-target,
                    stages=[
                        {"driver":s.driver,"driven":s.driven}
                        for s in stages
                    ],
                    kind=d.get("kind"),
                    radius_mm=d.get("radius_mm"),
                    z_mm=d.get("z_mm"),
                )
            )
            periods[display_id]=period
            del pending[display_id]
            progress=True

        if not progress:
            unresolved=", ".join(sorted(pending))
            raise ValueError(
                "movement graph has missing sources or a dependency cycle: "
                + unresolved
            )

    return resolved


def compile_movement(spec:dict)->ResolvedMovement:
    f=float(spec["oscillator"]["frequency_hz"])
    if f<=0:
        raise ValueError("oscillator frequency must be > 0")

    displays=_resolve_graph(list(spec["displays"]))
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
        "version":"0.2.0",
        "resolved":payload,
        "resolved_sha256":resolved.hash(),
    }
