# physunits

A lightweight physics units and dimensional-analysis helper for Python.

This small package provides:

- A minimal `Units` representation for SI base units and composite units.
- `Prefix` support (k, m, µ, etc.) via a `PREFIXES` mapping.
- A `Quantity` type combining numeric value, prefix and units with arithmetic that preserves dimensional consistency.
- A collection of common physical constants as `Quantity` objects (c, h, G, k_B, etc.).
- Many physics helper functions (mechanics, thermodynamics, electromagnetism, waves, gravity, fluids).

This README summarizes usage, the public API, and quick examples based on the repository contents.

## Installation

This project has no external runtime dependencies and targets Python 3.8+. Install with:

```powershell
# from the project root (editable install)
python -m pip install -e .
```

Or copy the `physunits` package into your project.

## Quick start

Basic example — compute speed from distance and time:

```python
from physunits import Quantity, Prefix, Units, speed

# 1000 meters
distance = Quantity(1000, Prefix(""), Units(length=1))
# 100 seconds
time = Quantity(100, Prefix(""), Units(time=1))

velocity = speed(distance, time)
print(velocity)  # shows a Quantity representing 10.0 m/s
```

Parsing a compound unit expression into the internal `Units` representation:

```python
from physunits import parse_units

u = parse_units('N*m/s^2')
print(u)  # Units object (may resolve to composite names like J, N, etc.)
```

Converting prefixes on a `Quantity`:

```python
from physunits import Quantity, Prefix, Units

q = Quantity(1, Prefix('k'), Units(length=1))  # 1 km
q2 = q.convert('')  # convert to base (m)
print(q2)  # 1000.0 m
```

## Main API

- Classes/types
  - `Units` — represents exponents of the seven SI base dimensions (m, kg, s, A, K, mol, cd).
  - `Quantity` — (value, prefix, units) with arithmetic operators defined.
  - `Prefix` — holds a prefix symbol and its factor; `PREFIXES` contains available prefixes.

- Helpers
  - `parse_units(expr: str) -> Units` — parse strings like `kg*m^2/s^3` or `N·m` into `Units`.

- Constants (examples)
  - `speed_of_light`, `planck_constant`, `planck_bar_constant`, `standard_gravity`
  - `gravitational_constant`, `electron_charge`, `elementary_charge`, `electron_mass`, `proton_mass`, `neutron_mass`
  - `rydberg_constant`, `rydberg_energy`, `hartree_energy`, `electron_volt`
  - `vacuum_permittivity`, `vacuum_permeability`, `coulomb_constant`, `faraday_constant`
  - `boltzmann_constant`, `gas_constant`, `stefan_boltzmann_constant`, `avogadro_constant`

- Physics helper functions
  - Mechanics: `speed`, `acceleration`, `force`, `momentum`, `impulse`, `kinetic_energy`, `potential_energy`, `mechanical_energy`, `work`, `power`, `energy_from_power`
  - Rotation: `torque`, `angular_momentum`, `rotational_kinetic_energy`
  - Thermodynamics: `pressure`, `temperature_from_energy_per_particle`, `ideal_gas_pressure`, `heat_from_specific_heat`, `thermal_energy_from_temperature`
  - Electromagnetism: `electric_force`, `electric_field`, `potential_energy_electric`, `voltage_from_field`, `capacitance`, `energy_stored_in_capacitor`, `current`, `voltage_from_current_resistance`, `electrical_power`
  - Waves & Photons: `wave_speed`, `frequency_from_period`, `photon_energy`, `photon_energy_from_wavelength`, `refractive_index`
  - Gravity & Relativity: `gravitational_force`, `orbital_velocity`, `escape_velocity`, `gravitational_potential_energy`, `energy_mass_equivalence`, `time_dilation`, `gravitational_redshift`
  - Fluids: `density`, `pressure_from_depth`, `buoyant_force`, `bernoulli_pressure`, `flow_rate`, `continuity_equation`

All of the above are re-exported from `physunits.__init__` and available via `from physunits import <name>`.

## Examples

Compute gravitational potential energy of two masses:

```python
from physunits import Quantity, Prefix, Units, gravitational_potential_energy

m1 = Quantity(5.972e24, Prefix(''), Units(mass=1))  # Earth mass (kg)
m2 = Quantity(7.348e22, Prefix(''), Units(mass=1))  # Moon mass (kg)
r = Quantity(3.844e8, Prefix(''), Units(length=1))  # average distance (m)

U = gravitational_potential_energy(m1, m2, r)
print(U)
```

Photon energy from frequency:

```python
from physunits import photon_energy, Quantity, Prefix, Units

f = Quantity(5e14, Prefix(''), Units(time=-1))  # visible light frequency (Hz)
E = photon_energy(f)
print(E)
```

## Development notes

- The package is intentionally small and dependency-free.
- Units are represented as simple integer exponents; composite names are available in `COMPOSITE_UNITS` (e.g. 'N', 'J').
- `Quantity` arithmetic checks unit compatibility for operations like addition/subtraction.
- `parse_units` supports `*`, `/`, `^` and recognizes composite symbols and base SI symbols.

## Tests and quick verification

Run a quick import check:

```powershell
python -c "import physunits; print(len(physunits.__all__))"
```

Consider adding unit tests (pytest) that validate arithmetic, conversions and the physics helper outputs.

## Contributing

PRs welcome. If you add features, please include tests and doc examples.

## License

Add a LICENSE file or include license text as appropriate for your project.
