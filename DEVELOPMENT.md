# Development Notes — 2D Ising Model (Metropolis Algorithm)

This document records the development process of the project: the approaches tested, the problems encountered, and the decisions made to reach the current version. For an overview of the project and its results, see the README.

## First Approach

The first implementation of the Ising model was made using a small `3×3` lattice. The initial goal was simply to get the lattice, spins, nearest-neighbor interactions, and energy calculations working before worrying about the statistical mechanics of the simulation.

The spins were stored as a list of lists, with each spin having a value of `+1` or `-1`.

The first random initialization was:

```
if t < 0.6:
    spin[x][y] = 1
else:
    spin[x][y] = -1
```

This gave approximately 60% `+1` spins and 40% `-1` spins. I did not initially consider this a major problem because the system would later be evolved through the Metropolis algorithm.

The first implementation also used open boundaries. For example:

```
cima = spin[x-1][y] if x > 0 else 0
```

This avoided Python's negative-index behavior, but meant that spins at the edges effectively had fewer neighbors than spins in the interior.

The energy of a spin was calculated from its nearest neighbors:

```math
E_i=-Js_i\sum_{j\in nn(i)}s_j
```

and the total energy was obtained by summing the local contributions and dividing by two, since every interaction was counted twice.

For a proposed spin flip, I calculated the energy difference directly:

```math
\Delta E=2Js_i\sum_{j\in nn(i)}s_j
```

rather than recalculating the total energy before and after every flip.

The first Metropolis implementation also did not have temperature as an explicit parameter. It was effectively using:

```math
T=1
```

with unfavorable moves accepted according to:

```math
P=e^{-\Delta E}
```

At this point the main goal was simply to make the basic algorithm work.

## Problems Encountered

### 1. Open Boundaries

The first implementation did not have periodic boundary conditions.

This meant that edge spins had fewer neighbors, which changes their interaction energy and introduces boundary effects that are not part of the standard square-lattice model I wanted to study.

### 2. Temperature Was Not Explicit

The first Metropolis step effectively used `T = 1`.

This was enough to test the acceptance rule, but it obviously did not allow the behavior of the system to be studied as a function of temperature.

### 3. Measuring Immediately

After introducing a temperature sweep, I initially performed roughly one Monte Carlo sweep at each temperature and measured the system immediately.

This created a problem.

The lattice does not instantly reach equilibrium when the temperature changes. The configuration still contains information from the previous temperature, so the measurements could not simply be treated as equilibrium averages.

### 4. Initial Randomization

The first initialization used a 60/40 probability instead of 50/50.

This introduced an unnecessary bias into the initial configuration.

Although thermalization should reduce the importance of the initial state, there was no reason to keep this asymmetry once it was noticed.

### 5. Total Quantities

The energy and magnetization were initially stored as total quantities.

This works for a single lattice size, but makes comparisons between different lattice sizes less useful because both quantities grow with the number of spins.

## Changes Made

Based on these problems, the simulation was gradually changed.

### 1. Explicit Temperature

Temperature was added as a parameter to the Metropolis algorithm:

```
metropolis(spin, n, j, T)
```

The acceptance probability became:

```math
P=e^{-\Delta E/T}
```

for `ΔE > 0`.

This allowed the system to be simulated at different temperatures.

### 2. Temperature Sweep

I then introduced an initial and final temperature:

```
Ti = 2
Tf = 8
```

and gradually increased the temperature during the simulation.

At each temperature, `n*n` Metropolis attempts were performed.

Since the lattice contains:

```math
N=n^2
```

spins, this corresponds to approximately one attempted update per spin, which I use as one Monte Carlo sweep.

### 3. Periodic Boundaries

The open-boundary implementation was replaced by periodic boundaries:

```
cima = spin[(x-1) % n][y]
baixo = spin[(x+1) % n][y]
esquerda = spin[x][(y-1) % n]
direita = spin[x][(y+1) % n]
```

The lattice now wraps around in both directions, so every spin has four nearest neighbors.

### 4. Thermalization

I added a thermalization stage before taking measurements.

Initially this was:

```
termalizacao = 100
```

The purpose is to give the system time to move toward the equilibrium distribution at the current temperature.

This is only a numerical choice, however. Using 100 sweeps does not prove that the system has equilibrated.

### 5. Sampling

Instead of taking only one measurement, I started collecting several configurations after thermalization.

The initial sampling value was:

```
amostras = 100
```

with one complete Monte Carlo sweep between measurements.

The energy and magnetization were then averaged over these samples.

For magnetization, I used the absolute value:

```
abs(magnetizacao(spin))
```

because the low-temperature Ising model has two equivalent ordered states, one with positive magnetization and one with negative magnetization.

Averaging signed magnetization could therefore give a value close to zero even when the system is strongly ordered.

### 6. Larger Lattice

The lattice was increased from:

```text
3×3 → 8×8
```

giving:

```text
9 → 64 spins
```

The temperature range was also changed to:

```
Ti = 2
Tf = 10
passos = 200
```

The larger lattice makes the collective behavior easier to see, although it is still small compared with the thermodynamic limit.

### 7. Normalizing the Observables

The energy and magnetization were changed from total quantities to per-spin quantities.

The number of spins is:

```math
N=n^2
```

so I calculate:

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

This makes the results more useful when comparing different lattice sizes.

## Current Version

The current version is more flexible than the earlier versions because the main parameters can now be entered through the terminal:

```
n = int(input("digite o tamanho da rede (n x n):"))
j = float(input("digite o valor da constante (J):"))

Ti = float(input("digite a temperatura inicial (Ti):"))
Tf = float(input("digite a temperatura final (Tf):"))
```

The number of temperature steps is currently fixed at:

```
passos = 200
```

The initial randomization was also corrected from the original 60/40 distribution to a 50/50 distribution:

```
if t < 0.5:
    spin[x][y] = 1
else:
    spin[x][y] = -1
```

The thermalization and sampling values were increased from 100 to 500:

```
termalizacao = 500
amostras = 500
```

So the current simulation approximately follows:

```text
random initialization
        ↓
500 thermalization sweeps
        ↓
500 sampling sweeps
        ↓
average E and |M|
        ↓
divide by N
        ↓
store E/N and |M|/N
        ↓
increase temperature
        ↓
repeat
```

The program also produces two plots:

* energy per spin as a function of temperature;
* absolute magnetization per spin as a function of temperature.

For the infinite two-dimensional square-lattice Ising model, using `J=1` and `k_B=1`, the exact critical temperature is:

```math
T_c=\frac{2}{\ln(1+\sqrt{2})}\approx2.269
```

The current simulation uses a finite lattice, so the transition should not be expected to occur exactly at this value.

## What the Code Measures Now

### Energy per spin

```math
e(T)=\frac{\langle E\rangle}{N}
```

### Absolute magnetization per spin

```math
m(T)=\frac{\langle |M|\rangle}{N}
```

The main behavior I am currently looking at is the change from an ordered low-temperature regime to a more disordered high-temperature regime.

The magnetization should decrease as temperature increases, while the energy should approach the behavior expected for the disordered phase.


## Limitations and Next Steps

There are still several things that need to be investigated.

Thermalization;

Statistical Uncertainty;

Correlation Between Samples;

Heat Capacity;

Magnetic Susceptibility;

Critical Temperature;

Larger Lattices;
