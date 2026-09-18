# Worked example — synthesizing a mechanical timebase

This example is intentionally educational. It is not a production caliber.

The purpose is to show how a mechanical watch can be derived from equations instead of copied from an existing movement.

---

# 1. Start with the oscillator

Choose a target oscillator frequency:

[
f_0=4	ext{ Hz}
]

That means four complete balance oscillations each second.

A conventional beat count is twice the oscillation frequency:

[
BPH=2f_0(3600)
]

Therefore:

[
BPH=2(4)(3600)=28800
]

The oscillator establishes the smallest repeating time reference.

---

# 2. Connect the oscillator to an escapement abstraction

For this worked example, assume:

**one escape-wheel tooth is released per complete balance oscillation.**

This is a modeling assumption for the example; real escapement event geometry must be modeled explicitly.

With a 15-tooth escape wheel:

[
n_e=
rac{f_0}{15}
=
rac{4}{15}
	ext{ rev/s}
]

Thus:

[
n_e=16	ext{ rpm}
]

and its period is:

[
P_e=rac{60}{16}=3.75	ext{ s/rev}
]

---

# 3. Synthesize a seconds wheel

We want:

[
P_s=60	ext{ s}
]

Required reduction:

[
R_s=rac{60}{3.75}=16
]

One possible compound train is:

[
rac{80}{20}	imesrac{80}{20}=16
]

So:

- stage A: 20 → 80
- stage B: 20 → 80

The resulting shaft turns once every 60 seconds.

That shaft can directly carry a seconds hand.

---

# 4. Synthesize a minutes wheel

Seconds shaft:

[
P_s=60	ext{ s}
]

Minutes shaft:

[
P_m=3600	ext{ s}
]

Required ratio:

[
R_m=rac{3600}{60}=60
]

A possible three-stage integer factorization:

[
60=
4	imes3.75	imes4
]

implemented as:

[
rac{72}{18}
	imes
rac{75}{20}
	imes
rac{72}{18}
=60
]

The final shaft turns once per hour.

---

# 5. Synthesize an hours wheel

Minutes shaft:

[
P_m=3600	ext{ s}
]

Hours shaft:

[
P_h=43200	ext{ s}
]

Therefore:

[
R_h=12
]

A two-stage realization:

[
12=
rac{72}{18}
	imes
rac{60}{20}
=
4	imes3
]

The final shaft turns once every 12 hours.

---

# 6. Direction is separate from ratio

Every external gear mesh reverses rotation:

[
omega_2=-omega_1rac{z_1}{z_2}
]

An idler gear changes direction without changing the magnitude of the ratio.

Therefore:

**ratio design and rotation-direction design should be treated as separate constraints.**

---

# 7. Add a moon-phase display

Mean synodic month:

[
P_{moon}=29.530588853	ext{ days}
]

Suppose we begin with a shaft turning once per day.

Required reduction:

[
R_{moon}=29.530588853
]

Because tooth counts must be integers, the machine needs a rational approximation.

One two-stage candidate within moderate tooth counts is:

[
R_{mech}
=
rac{92}{18}
	imes
rac{104}{18}
]

which gives:

[
R_{mech}=29.5308641975
]

Period error per lunation:

[
Delta P
=
29.5308641975
-
29.530588853
]

[
Delta P
approx0.0002753445	ext{ day}
]

or about:

[
23.8	ext{ s/lunation}
]

That means the mechanical display drifts by roughly one full day of lunar phase after about 294 years if all other errors are ignored.

This is the essence of astronomical watchmaking:

**number theory becomes mechanics.**

---

# 8. A classical simple moon disk for comparison

A common conceptual architecture uses a 59-tooth disk representing two lunar cycles.

One lunation is then approximated as:

[
rac{59}{2}=29.5	ext{ days}
]

Error:

[
29.530588853-29.5
=
0.030588853	ext{ day}
]

which is about 44 minutes per lunation.

That accumulates to roughly one day of phase error after about 2.6 years.

This comparison shows why additional gears can buy enormous astronomical accuracy.

---

# 9. Translate each wheel into geometry

Take a 72-tooth wheel with:

[
m=0.20	ext{ mm}
]

Pitch radius:

[
r_p=rac{mz}{2}
=
rac{0.20(72)}{2}
=
7.2	ext{ mm}
]

With a 20° pressure angle:

[
r_b=r_pcos20^circ
]

[
r_bapprox6.765	ext{ mm}
]

Addendum radius:

[
r_a=r_p+m=7.4	ext{ mm}
]

Reference root radius:

[
r_fapprox r_p-1.25m
]

[
r_fapprox6.95	ext{ mm}
]

Now the time ratio has become a physical object.

---

# 10. The tooth itself is a vector curve

For the base radius (r_b):

[
x(u)=r_b(cos u+usin u)
]

[
y(u)=r_b(sin u-ucos u)
]

This creates one involute flank.

Mirror and rotate it by the tooth pitch:

[
Deltapsi=rac{2pi}{z}
]

to generate the complete wheel.

At this point:

**the abstract number 72 has become cutter geometry.**

---

# 11. Place the gear in the movement

For a 3D feature point:

[
mathbf p_{local}
=
[x,y,z,1]^T
]

Movement placement:

[
mathbf p_{movement}
=
mathbf T_{movement,part}
mathbf p_{local}
]

If the wheel is inside a rotating cage:

[
mathbf p_{movement}(t)
=
mathbf T_{cage}(t)
mathbf T_{part}
mathbf p_{local}
]

Now geometry carries time.

---

# 12. Translate to machining coordinates

A feature designed in movement coordinates still does not tell the machine tool where to cut.

Use:

[
mathbf p_{machine}
=
mathbf T_{machine,setup}
mathbf T_{setup,part}
mathbf T_{part,feature}
mathbf p_{feature}
]

Those transforms contain:

- work offset
- fixture orientation
- part datum
- rotary-axis orientation
- setup inversion
- inspection alignment

The toolpath should be generated only after this chain is explicit.

---

# 13. Closing the loop

After machining, measure:

[
mathbf p_{measured}
]

Compare with nominal:

[
Deltamathbf p
=
mathbf p_{measured}
-
mathbf p_{nominal}
]

Then estimate process compensation:

[
delta_{next}
=
-operatorname{bias}(Deltamathbf p)
]

while leaving nominal design intent unchanged.

So the complete machine is:

[
	ext{oscillation}
ightarrow
	ext{counting}
ightarrow
	ext{gear ratio}
ightarrow
	ext{geometry}
ightarrow
	ext{vectors}
ightarrow
	ext{machining}
ightarrow
	ext{measurement}
ightarrow
	ext{correction}
]

That is mechanical time synthesis.
