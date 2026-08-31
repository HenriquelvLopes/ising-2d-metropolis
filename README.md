# ising-2d-metropolis

A computational study of the two-dimensional Ising model using the Metropolis algorithm.

## About

The project was developed as a study of statistical mechanics and computational physics, with the goal of exploring how microscopic spin interactions give rise to macroscopic quantities such as energy and magnetization.

The simulation uses a square lattice with periodic boundary conditions and allows the user to specify the lattice size, coupling constant, and temperature interval.

## Physical Model

The Ising model represents a system of interacting spins arranged on a lattice. Each spin can assume one of two possible values,

$$
s_i = \pm 1.
$$

For the two-dimensional square lattice considered here, each spin interacts with its four nearest neighbors.

The energy of a configuration is described by the Hamiltonian

$$
H = -J \sum_{\langle i,j\rangle} s_i s_j,
$$

where:

$J$ is the coupling constant;
$s_i$ and $s_j$ are neighboring spins;
$\langle i,j\rangle$ indicates that the sum is performed over neighboring pairs.

For $J>0$, neighboring spins tend to align, favoring ferromagnetic ordering.

## Periodic Boundary Conditions

Periodic boundary conditions are used so that spins at the edge of the lattice interact with spins on the opposite edge.

This avoids treating the boundary as a special region and makes the lattice effectively behave as a surface with no physical edges.

## Metropolis Algorithm

The equilibrium configurations are sampled using the Metropolis algorithm.

At each Monte Carlo step, a spin is randomly selected and a trial inversion is considered.

The energy variation associated with flipping the spin is

$$
\Delta E = 2J s_{x,y}
\left(
s_{\text{up}}+
s_{\text{down}}+
s_{\text{left}}+
s_{\text{right}}
\right).
$$

If

$$
\Delta E \leq 0,
$$

the inversion is accepted.

For $\Delta E > 0$, the inversion is accepted with probability

$$
P = e^{-\Delta E/T}.
$$

The temperature is taken in reduced units, with Boltzmann's constant effectively set to

$$
k_B = 1.
$$

This procedure allows the system to sample configurations according to the Boltzmann distribution.

## Quantities Measured

For each temperature, the program calculates the average energy and magnetization.

### Energy

The total energy of the lattice is

$$
E = -J \sum_{\langle i,j\rangle} s_i s_j.
$$

The program reports the energy per spin,

$$
\frac{E}{N},
$$

where

$$
N=n^2
$$

is the total number of spins.

### Magnetization

The total magnetization is

$$
M = \sum_i s_i.
$$

The simulation measures the absolute magnetization and reports

$$
\frac{|M|}{N}.
$$

The absolute value is used because, in a finite simulation, the entire system can spontaneously change from predominantly positive magnetization to predominantly negative magnetization. Without taking the absolute value, these transitions could artificially drive the average magnetization toward zero.

## Simulation Procedure

For every temperature in the chosen interval:

1. The system is allowed to thermalize.
2. Random spin-flip attempts are performed using the Metropolis algorithm.
3. Measurements are collected over a number of samples.
4. The average energy and absolute magnetization are calculated.
5. The quantities are normalized by the total number of spins.
6. The temperature is increased and the process is repeated.

The current implementation uses:

- 200 temperature intervals;
- 500 thermalization sweeps per temperature;
- 500 measurement samples per temperature;
- $n^2$ Metropolis attempts per sweep.

These parameters are currently fixed in the source code and may be made configurable in future versions.

## Results

The program generates two plots:

- Energy per spin as a function of temperature;
- Absolute magnetization per spin as a function of temperature.

For the ferromagnetic two-dimensional Ising model, the magnetization decreases as thermal fluctuations become increasingly important. Near the critical temperature, the system undergoes a transition between an ordered and a disordered regime.

For the infinite two-dimensional square-lattice Ising model with zeroexternal magnetic field and $J>0$, the exact critical temperature is

$$
\frac{k_B T_c}{J} =
\frac{2}{\ln(1+\sqrt{2})}
\approx 2.269.
$$


The simulation can therefore be used to investigate the behavior of the system near this critical region and to compare numerical results with the known analytical result.

This project requires:

- Python 3
- Matplotlib

Install Matplotlib using:

```bash
pip install matplotlib
```
## How to Run

python ising.py

The program will ask for:

```text
Digite o tamanho da rede (n x n):
Digite o valor da constante (J):
Digite a temperatura inicial (Ti):
Digite a temperatura final (Tf):
```

For example:

```text
n = 20
J = 1
Ti = 1
Tf = 4
```

The simulation will then calculate the equilibrium properties of the system over the chosen temperature interval.

## Current Scope

This project is primarily a computational study of the Ising model and the Metropolis algorithm.

The current implementation focuses on:

- the two-dimensional square lattice;
- nearest-neighbor interactions;
- periodic boundary conditions;
- Metropolis Monte Carlo sampling;
- energy measurement;
- magnetization measurement;
- temperature-dependent behavior.

More advanced observables and numerical improvements are planned as the project develops.


## References

- H. Moysés Nussenzveig, *Curso de Física Básica, Vol. 3:
  Eletromagnetismo*, Blucher.
  Used as a background reference for magnetic phenomena and
  magnetization.

- M. E. J. Newman and G. T. Barkema,
  *Monte Carlo Methods in Statistical Physics*,
  Oxford University Press, 1999.
  Main reference for the Monte Carlo methods and statistical
  physics concepts used in this project.
