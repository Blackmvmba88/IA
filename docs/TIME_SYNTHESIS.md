# Mathematical synthesis of time

This document is the canonical BPME bridge:

**time → phase → angular velocity → gear ratio → geometry → coordinate transform → machining geometry**

The goal is not to imitate a particular watch. The goal is to understand how a mechanical machine can represent time and astronomical cycles.

---

## 1. Time becomes phase

Let (t) be elapsed SI seconds.

A periodic phenomenon with period (P) is represented by phase:

[
\theta(t)=\theta_0+\frac{2\pi}{P}t
]

and angular velocity:

[
\omega=\dot\theta=\frac{2\pi}{P}
]

Examples:

| display | period |
|---|---:|
| seconds hand | 60 s |
| minutes hand | 3600 s |
| hours hand | 43200 s |
| moon phase, mean synodic cycle | 29.530588853 d |
| tropical year, mean | 365.2421897 d |

A watch therefore does not need to "store time" as a number. It continuously transports phase.

---

## 2. The oscillator creates the fundamental rhythm

For an ideal balance + hairspring:

[
I\ddot\theta + c\dot\theta + k\theta = \tau
]

Small-signal natural frequency:

[
f_0=\frac{1}{2\pi}\sqrt{\frac{k}{I}}
]

For BPME's nonlinear H1 model:

[
I\ddot\theta+c\dot\theta+k_1\theta+k_3\theta^3=\tau
]

This lets frequency depend on amplitude, exposing non-isocronism.

---

## 3. The escapement quantizes oscillation

The oscillator is continuous. The gear train advances in discrete release events.

Conceptually:

[
N(t)=\left\lfloor \frac{\phi_{osc}(t)}{\Delta\phi_{unlock}} \right\rfloor
]

Each unlock event permits a tooth/impulse event. The escapement therefore converts continuous oscillation into mechanically countable progression.

---

## 4. Gears scale time

For two external spur gears:

[
\omega_2=-\omega_1\frac{z_1}{z_2}
]

where (z) is tooth count.

Equivalently:

[
\frac{P_2}{P_1}=\frac{z_2}{z_1}
]

for one external mesh by magnitude.

A compound train multiplies stage ratios:

[
\frac{\omega_{out}}{\omega_{in}}
=
\prod_i
\left(-\frac{z_{driver,i}}{z_{driven,i}}\right)
]

Thus a 60 s shaft can be transformed into a 3600 s shaft by an absolute ratio of 60:1, and into a 43200 s shaft by 720:1.

The engineering problem is to factor a large rational ratio into tooth counts that fit the available envelope and avoid impractical tooth numbers.

---

## 5. Integer teeth approximate irrational/astronomical periods

Astronomical periods are generally not neat integer ratios.

Given desired ratio (R), choose integer teeth such that:

[
R\approx\frac{z_2}{z_1}
]

For multiple stages:

[
R\approx
\prod_i\frac{z_{driven,i}}{z_{driver,i}}
]

The accumulated timing/phase error must then be computed explicitly.

This is how a mechanical moon display or calendar becomes an approximation problem in number theory.

---

## 6. Gear geometry is mathematical

For a spur gear with module (m), tooth count (z), and pressure angle (alpha):

[
r_p=\frac{mz}{2}
]

[
r_b=r_p\cos\alpha
]

[
r_a=r_p+m
]

Reference full-depth root radius:

[
r_f\approx r_p-1.25m
]

Circular pitch:

[
p=\pi m
]

Nominal tooth thickness at pitch circle:

[
s=\frac{\pi m}{2}
]

For two standard gears of the same module:

[
a=r_{p1}+r_{p2}
=
\frac{m(z_1+z_2)}{2}
]

---

## 7. The tooth flank is an involute

Base-circle involute parameter (u):

[
x(u)=r_b(\cos u+u\sin u)
]

[
y(u)=r_b(\sin u-u\cos u)
]

Radius along the involute:

[
r(u)=r_b\sqrt{1+u^2}
]

Therefore, to reach a desired radius (r):

[
u=\sqrt{\left(\frac{r}{r_b}\right)^2-1}
]

This curve is not decoration. It is the vector geometry that makes constant velocity ratio possible under ideal involute contact.

---

## 8. Complications are coordinate mappings

Once each shaft has angle (	heta_i(t)), a display is a geometric mapping.

For a hand of radius (R), with zero at 12 o'clock and clockwise positive:

[
x=R\sin\theta
]

[
y=R\cos\theta
]

For an orrery-like display:

[
\mathbf{p}_k(t)=
\begin{bmatrix}
R_k\cos\theta_k(t)\\
R_k\sin\theta_k(t)\\
z_k
\end{bmatrix}
]

The complication is therefore a time-dependent vector field over mechanical geometry.

---

## 9. Tourbillons require moving coordinate frames

A point fixed in a rotating cage is not fixed in the movement.

Use homogeneous transforms:

[
\mathbf{p}_{world}
=
\mathbf{T}_{world,cage}(t)
\mathbf{T}_{cage,part}
\mathbf{p}_{part}
]

For nested cages:

[
\mathbf{T}_{world,part}(t)
=
\mathbf{T}_{1}(t)
\mathbf{T}_{2}(t)
\cdots
\mathbf{T}_{n}(t)
\mathbf{T}_{local}
]

This is why multi-axis tourbillons are naturally described with transformation matrices, not with isolated angles.

---

## 10. Design coordinates must become machine coordinates

A CAD feature lives in a part frame. A machine tool works in a machine/setup frame.

The correct translation is:

[
\mathbf{p}_{machine}
=
\mathbf{T}_{machine,setup}
\mathbf{T}_{setup,part}
\mathbf{T}_{part,feature}
\mathbf{p}_{feature}
]

That equation is the conceptual bridge from mathematical watch design to machining.

Never bury these transforms in ad-hoc offsets. Store them explicitly.

---

## 11. Turning is naturally cylindrical

For an axisymmetric turned part:

[
\mathbf{p}(\varphi,z)=
\begin{bmatrix}
r(z)\cos\varphi\\
r(z)\sin\varphi\\
z
\end{bmatrix}
]

The design variable is the profile (r(z)).

A lathe controller may represent radial position as radius or diameter depending on convention, so BPME must keep **design radius** separate from **controller coordinates**.

---

## 12. Milling/toolpaths are vector curves

A tool-center path is a parametric curve:

[
\mathbf{c}(s)=
\begin{bmatrix}
x(s)\\
y(s)\\
z(s)
\end{bmatrix}
]

Orientation for 5-axis machining adds a tool-axis unit vector:

[
\hat{\mathbf{a}}(s)
]

So a full machining pose is not merely XYZ:

[
\mathcal{P}(s)=
\{\mathbf{c}(s),\hat{\mathbf{a}}(s)\}
]

This matters for inclined cages, bridges, undercuts, and three-dimensional astronomical mechanisms.

---

## 13. The full synthesis chain

A rigorous BPME watch can be expressed as:

[
t
\rightarrow
\phi_{osc}
\rightarrow
N_{esc}
\rightarrow
\theta_{shaft_i}
\rightarrow
\mathbf{T}_i(t)
\rightarrow
\mathbf{p}_{feature}
\rightarrow
\mathbf{p}_{machine}
\rightarrow
\mathbf{p}_{measured}
\rightarrow
\Delta\mathbf{p}
\rightarrow
\text{compensation}
]

That is the complete loop:

**physics → time → kinematics → geometry → manufacturing → metrology → correction**

---

## 14. The machine-readable design vector

A candidate movement can be represented as one parameter vector:

[
\mathbf{q}=
[
I,
k_1,
k_3,
f_0,
m,
\alpha,
z_1...z_n,
P_1...P_n,
\mathbf{a}_1...\mathbf{a}_n,
\mathbf{T}_{setup},
\delta_{process}
]
]

BPME's job is to map:

[
\mathbf{q}
\mapsto
\text{chronometry, geometry, energy, manufacturability}
]

and eventually solve the inverse problem:

[
\text{desired behavior}
\mapsto
\mathbf{q}^*
]

That inverse map is what turns a watch-design program into a synthesis engine.
