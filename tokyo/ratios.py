"""Integer gear-ratio search for TOKYO."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Stage:
    driver:int
    driven:int

    @property
    def ratio(self)->float:
        return self.driven/self.driver


def product_ratio(stages:list[Stage])->float:
    r=1.0
    for s in stages:
        r*=s.ratio
    return r


def solve_two_stage_ratio(
    target:float,
    min_teeth:int=12,
    max_teeth:int=120,
)->tuple[list[Stage],float]:
    if target<=0:
        raise ValueError("target must be > 0")
    best=None
    for a in range(min_teeth,max_teeth+1):
        for b in range(min_teeth,max_teeth+1):
            r1=b/a
            # infer second-stage target then search
            rem=target/r1
            for c in range(min_teeth,max_teeth+1):
                d=round(rem*c)
                if d<min_teeth or d>max_teeth:
                    continue
                stages=[Stage(a,b),Stage(c,d)]
                actual=product_ratio(stages)
                err=abs(actual-target)
                if best is None or err<best[0]:
                    best=(err,stages,actual)
    if best is None:
        raise RuntimeError("no ratio solution found")
    return best[1],best[2]
