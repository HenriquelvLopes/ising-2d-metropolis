# Development Notes — 2D Ising Model (Metropolis Algorithm)

These are notes on how the 2D Ising model simulation was developed. The idea here is to keep track of what was tried, what went wrong, what was changed, and what still needs to be improved.

This is not meant to be a polished description of the final program. The README is for that. Here I am keeping the development process itself.

## v1 — Lattice, neighbors, and local energy

**Goal:** get the basic lattice and interactions working.

I started with a small `3×3` lattice just to test the basic structure of the model.

* `n = 3`
* spins stored as a list of lists
* spins are either `+1` or `-1`
* random initialization
* nearest-neighbor interaction
* local energy
* total energy
* random spin inversion

The first random initialization was actually asymmetric:

```
if t < 0.6:
    spin[x][y] = 1
else:
    spin[x][y] = -1
```

So the initial lattice had approximately 60% `+1` spins and 40% `-1` spins.

I left this like that initially and only came back to it later. It was corrected in v6.

### Open boundaries

For the first version, I handled the edges like this:

```
cima = spin[x-1][y] if x > 0 else 0
```

This avoided Python's negative-index behavior, but it also meant that an edge spin simply did not have a neighbor on that side.

So this was an **open-boundary lattice**.

That is not what I wanted for the square-lattice Ising model, since the edge spins then have fewer interactions than the spins in the middle.

### Energy

I implemented the local energy as:

```math
E_i = -Js_i\sum_{j \in nn(i)}s_j
```

and calculated the total energy by summing the local contributions and dividing by two, since every interaction is counted twice.

For a proposed spin flip, I used the local energy difference instead of recalculating the entire lattice:

```math
\Delta E = 2Js_i\sum_{j \in nn(i)}s_j
```

This is much cheaper than calculating the total energy before and after every flip.

### First Metropolis step

The first Metropolis implementation did not have temperature as a parameter yet.

It was effectively using:

```math
T=1
```

The rule was:

```math
\Delta E \leq 0
```

→ accept the flip.

Otherwise:

```math
P=e^{-\Delta E}
```

→ accept with that probability.

At this point I was mostly checking whether the algorithm itself was behaving correctly.

## v2 — Explicit temperature

**Goal:** put temperature into the Metropolis algorithm properly.

The function changed from:

```
metropolis(spin, n, j)
```

to:

```
metropolis(spin, n, j, T)
```

The probability for an unfavorable flip became:

```math
P=e^{-\Delta E/T}
```

while favorable or neutral flips were still accepted automatically:

```math
\Delta E\leq0
```

Nothing else major changed in this version.

The point was simply to stop treating `T = 1` as something implicit before trying to vary the temperature.

## v3 — Temperature sweep

**Goal:** see what happens when the temperature changes.

I added a temperature range:

```
Ti = 2
Tf = 8
passos = 1000
```

and calculated:

```
deltaT = (Tf - Ti) / passos
```

At each temperature I performed `n*n` Metropolis attempts.

Since:

```math
N=n^2
```

this means approximately one attempted update per spin.

I started using this as one **Monte Carlo sweep**.

### Magnetization

I also added magnetization:

```math
M=\sum_i s_i
```

The idea was to start looking at how the system changes as temperature increases.

At this point I was just recording the energy and magnetization after each sweep.

### Problem

There was an obvious problem with this approach: I was changing the temperature and immediately measuring the system.

The configuration had not necessarily had enough time to adapt to the new temperature.

So the lattice was carrying information from the previous temperature, and the first state was also completely arbitrary.

The graphs from this version were therefore useful for seeing that *something* was happening, but I would not treat them as proper equilibrium averages.

This led to the next change.

## v4 — Periodic boundaries, thermalization, and sampling

**Goal:** fix the boundary problem and stop measuring immediately after changing temperature.

### Periodic boundaries

I replaced the open boundaries with periodic boundaries:

```
cima = spin[(x-1) % n][y]
baixo = spin[(x+1) % n][y]
esquerda = spin[x][(y-1) % n]
direita = spin[x][(y+1) % n]
```

Now the lattice wraps around.

The top is connected to the bottom, and the left side is connected to the right side.

This means every spin has four nearest neighbors, including the spins on the edges.

This is much closer to the standard square-lattice Ising model I wanted to simulate.

### Thermalization

I added a thermalization stage:

```
termalizacao = 100
```

Before taking measurements at a given temperature, the program performs 100 Monte Carlo sweeps.

The idea is simply to give the lattice some time to forget the arbitrary state it started from and move toward the equilibrium distribution.

Of course, 100 sweeps is just a numerical choice. It does not prove that the system is actually equilibrated.

### Sampling

After thermalization, I started collecting several measurements instead of using just one configuration.

I used:

```
amostras = 100
```

and performed one complete sweep between measurements:

```
for i in range(amostras):
    for k in range(n*n):
        metropolis(spin, n, j, T)

    soma_E += energia(spin, j)
    soma_M += abs(magnetizacao(spin))
```

Then I averaged the results.

### Absolute magnetization

I used:

```
abs(magnetizacao(spin))
```

instead of the signed magnetization.

The reason is that the Ising model has two equivalent ordered states.

For example, at low temperature the lattice can be mostly:

```text
+ + + + + 
+ + + + +
+ + + + +
```

or mostly:

```text
- - - - -
- - - - -
- - - - -
```

Both are ordered states, but their magnetizations have opposite signs.

If the system switches between them, averaging signed `M` can give something close to zero even though the lattice is strongly ordered.

So for the quantity I wanted to plot, I used:

```math
|M|
```

At this point the quantities were still totals for the entire lattice.

## v5 — 8×8 lattice and per-spin quantities

**Goal:** use a somewhat larger lattice and make the observables independent of the total number of spins.

I changed the lattice from:

```text
3×3 → 8×8
```

so that the number of spins became:

```text
9 → 64
```

I also changed the temperature range:

```
Ti = 2
Tf = 10
passos = 200
```

The thermalization and sampling were still:

```text
100 thermalization sweeps
100 samples
```

but now each sweep contains 64 attempted spin updates.

### Normalization

The total energy and magnetization depend on the number of spins, so I started dividing by:

```math
N=n^2
```

The code became:

```
energia_spin = energia_media / (n*n)
magnetizacao_spin = magnetizacao_media / (n*n)
```

giving:

```math
e(T)=\frac{\langle E\rangle}{N}
```

and:

```math
m(T)=\frac{\langle |M|\rangle}{N}
```

This makes the quantities easier to compare if I later change the lattice size.

# v6 — User input, better initialization, and more sampling

**Goal:** make the program less dependent on values hardcoded in the source and increase the thermalization and sampling time.

This version is where the program started becoming more convenient to actually experiment with.

### User-defined parameters

Instead of fixing everything in the code, the user can now enter:

```
n = int(input("digite o tamanho da rede (n x n):"))
j = float(input("digite o valor da constante (J):"))

Ti = float(input("digite a temperatura inicial (Ti):"))
Tf = float(input("digite a temperatura final (Tf):"))
```

So I can change the lattice size, `J`, and temperature range without editing the program itself.

The number of temperature steps is still fixed:

```
passos = 200
```

and the temperature increment is calculated from the chosen range:

```
deltaT = (Tf - Ti) / passos
```

I am leaving `passos` fixed for now rather than adding another input.

### Fixing the initial random state

The 60/40 initialization from v1 was finally corrected.

It is now:

```
if t < 0.5:
    spin[x][y] = 1
else:
    spin[x][y] = -1
```

So `+1` and `-1` have equal probability.

This was a small change, but it removes an unnecessary bias from the initial configuration.

### More thermalization

I increased:

```text
100 → 500 sweeps
```

for thermalization.

So at every temperature the lattice now evolves for 500 sweeps before I start collecting measurements.

This should give the system more time to relax, although I still need to actually test whether 500 is enough, especially around the critical region.

### More samples

I also increased:

```text
100 → 500 samples
```

The current structure is therefore:

```text
500 thermalization sweeps
        ↓
500 sampling sweeps
        ↓
average E and |M|
        ↓
divide by N
```

This gives me more measurements than before, but the samples are not necessarily independent. Consecutive configurations can still be correlated.

That is something I will need to look at later rather than assuming that 500 samples automatically means 500 independent samples.

### Two graphs

I also changed the plotting so that the program shows both graphs after the simulation:

1. Energy per spin vs. temperature.
2. Absolute magnetization per spin vs. temperature.

The magnetization graph is limited to:

```
plt.ylim(0, 1)
```

since:

```math
0\leq\frac{|M|}{N}\leq1
```

for spins with values `+1` and `-1`.

## What the code does now

The current process is roughly:

```text
choose n, J, Ti and Tf
        ↓
random 50/50 initialization
        ↓
periodic boundaries
        ↓
500 thermalization sweeps
        ↓
500 sampling sweeps
        ↓
average E and |M|
        ↓
divide by N
        ↓
store T, E/N and |M|/N
        ↓
increase T
        ↓
repeat
        ↓
plot the results
```

So the simulation is now at a point where I can start worrying less about whether the basic Metropolis implementation works and more about whether the numerical results are actually reliable.

## What I am measuring now

### Energy per spin

```math
e(T)=\frac{\langle E\rangle}{N}
```

### Absolute magnetization per spin

```math
m(T)=\frac{\langle |M|\rangle}{N}
```

The main thing I want to see is the change from an ordered state at low temperature to a disordered state at high temperature.

For comparison, the exact critical temperature of the infinite 2D square-lattice Ising model, using `J=1` and `k_B=1`, is:

```math
T_c=\frac{2}{\ln(1+\sqrt{2})}\approx2.269
```

The simulation uses a finite lattice, so I should not expect the transition to appear exactly at `2.269`.

## Things I have not implemented yet

### Heat capacity

Not implemented yet.

The idea is to obtain it from energy fluctuations using the fluctuation-dissipation relation.

I want to derive and understand that relation before just putting the formula into the code.

### Magnetic susceptibility

Also not implemented yet.

This will involve magnetization fluctuations, and I need to be careful about the distinction between `M` and `|M|`.

### Finding `T_c` properly

The current simulation can show the transition region qualitatively, but I would not call it a precise numerical determination of `T_c`.

To do that properly I will eventually need things such as:

* different lattice sizes;
* more statistics;
* uncertainty estimates;
* correlation/autocorrelation analysis;
* finite-size effects;
* and probably finite-size scaling.

## Current limitations / next steps

* 500 thermalization enough?
* 500 samples enough?
* How correlated are consecutive samples?
* How large are the statistical uncertainties?
* How does the transition region move with lattice size?
* heat capacity 
* susceptibility be obtained correctly from magnetization fluctuations
* critical temperature

I will add new thing to the code the more I improve it
