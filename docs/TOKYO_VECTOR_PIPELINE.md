# TOKYO vector pipeline

TOKYO separates four spaces:

1. **time space** — periods, phases, angular velocities;
2. **mechanism space** — shaft axes, gear pitch geometry, cage transforms;
3. **part/setup space** — fixturing and datums;
4. **machine space** — coordinates and tool orientation.

For a periodic display:

[
\theta_i(t)=\theta_{0,i}+\frac{2\pi t}{P_i}
]

A radial display point is:

[
\mathbf p_i(t)=
\begin{bmatrix}
R_i\cos\theta_i\\
R_i\sin\theta_i\\
z_i
\end{bmatrix}
]

Its local moving basis is:

[
\hat{\mathbf r}=
[\cos\theta,\sin\theta,0]^T
]

[
\hat{\mathbf t}=
[-\sin\theta,\cos\theta,0]^T
]

For manufacturing, a design point becomes:

[
\mathbf p_M =
T_{M,S}
T_{S,P}
\mathbf p_P
]

A direction vector does **not** receive translation:

[
\mathbf v_M =
R_{M,S}R_{S,P}\mathbf v_P
]

This distinction matters. Treating a direction like a point corrupts tool orientation.

For a resolved gear stage:

[
d_1=mz_1,quad d_2=mz_2
]

and:

[
a=\frac{d_1+d_2}{2}
=\frac{m(z_1+z_2)}{2}
]

So each temporal ratio selected by the compiler immediately implies physical pitch diameters and center distance once module is chosen.

The intended TOKYO chain is therefore:

[
P_i
\to
z_i
\to
d_i
\to
a_i
\to
\mathbf p_{part}
\to
T
\to
\mathbf p_{machine}
]

That is the translation from a time specification into machining vectors.
