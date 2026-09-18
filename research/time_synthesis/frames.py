"""Rigid-frame translation from mechanism coordinates to machine coordinates.

A point is transformed with homogeneous coordinates:

    p_machine =
        T_machine_setup
        @ T_setup_part
        @ T_part_feature
        @ p_feature

This is the bridge between kinematic design space and machining space.
"""

from __future__ import annotations

from math import cos, sin


Matrix4=tuple[
    tuple[float,float,float,float],
    tuple[float,float,float,float],
    tuple[float,float,float,float],
    tuple[float,float,float,float],
]
Vector3=tuple[float,float,float]


def identity() -> Matrix4:
    return (
        (1.0,0.0,0.0,0.0),
        (0.0,1.0,0.0,0.0),
        (0.0,0.0,1.0,0.0),
        (0.0,0.0,0.0,1.0),
    )


def translation(x:float,y:float,z:float)->Matrix4:
    return (
        (1.0,0.0,0.0,x),
        (0.0,1.0,0.0,y),
        (0.0,0.0,1.0,z),
        (0.0,0.0,0.0,1.0),
    )


def rotation_x(a:float)->Matrix4:
    c,s=cos(a),sin(a)
    return (
        (1.0,0.0,0.0,0.0),
        (0.0,c,-s,0.0),
        (0.0,s,c,0.0),
        (0.0,0.0,0.0,1.0),
    )


def rotation_y(a:float)->Matrix4:
    c,s=cos(a),sin(a)
    return (
        (c,0.0,s,0.0),
        (0.0,1.0,0.0,0.0),
        (-s,0.0,c,0.0),
        (0.0,0.0,0.0,1.0),
    )


def rotation_z(a:float)->Matrix4:
    c,s=cos(a),sin(a)
    return (
        (c,-s,0.0,0.0),
        (s,c,0.0,0.0),
        (0.0,0.0,1.0,0.0),
        (0.0,0.0,0.0,1.0),
    )


def matmul(a:Matrix4,b:Matrix4)->Matrix4:
    rows=[]
    for i in range(4):
        row=[]
        for j in range(4):
            row.append(sum(a[i][k]*b[k][j] for k in range(4)))
        rows.append(tuple(row))
    return tuple(rows)  # type: ignore[return-value]


def apply(T:Matrix4,p:Vector3)->Vector3:
    x,y,z=p
    v=(x,y,z,1.0)
    out=tuple(sum(T[i][k]*v[k] for k in range(4)) for i in range(4))
    if abs(out[3])<1e-15:
        raise ValueError("invalid homogeneous transform")
    return (out[0]/out[3],out[1]/out[3],out[2]/out[3])


def compose(*Ts:Matrix4)->Matrix4:
    out=identity()
    for T in Ts:
        out=matmul(out,T)
    return out


def transform_polyline(T:Matrix4,points:list[Vector3])->list[Vector3]:
    return [apply(T,p) for p in points]
