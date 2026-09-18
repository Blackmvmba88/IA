from .model import CageAxis, TourbillonTopology


CLASSICAL_60S = TourbillonTopology(
    name="classical-60s",
    axes=(CageAxis((0.0, 0.0, 1.0), 60.0),),
    cage_inertia_kg_m2=1.0e-9,
    friction_torque_nm=2.0e-8,
)

INCLINED_25DEG_24S = TourbillonTopology(
    name="inclined-25deg-24s",
    axes=(CageAxis((0.422618, 0.0, 0.906308), 24.0),),
    cage_inertia_kg_m2=1.0e-9,
    friction_torque_nm=2.0e-8,
)

BIAXIAL_60_120 = TourbillonTopology(
    name="biaxial-60-120",
    axes=(
        CageAxis((1.0, 0.0, 0.0), 60.0),
        CageAxis((0.0, 1.0, 0.0), 120.0),
    ),
    cage_inertia_kg_m2=1.0e-9,
    friction_torque_nm=2.0e-8,
)

TRIAXIAL_60_120_300 = TourbillonTopology(
    name="triaxial-60-120-300",
    axes=(
        CageAxis((1.0, 0.0, 0.0), 60.0),
        CageAxis((0.0, 1.0, 0.0), 120.0),
        CageAxis((0.0, 0.0, 1.0), 300.0),
    ),
    cage_inertia_kg_m2=1.0e-9,
    friction_torque_nm=2.0e-8,
)
