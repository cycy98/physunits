"""
Physical constants for the physunits package.
All constants are represented as `Quantity` objects with correct SI dimensions.
"""

from quantity import Quantity
from prefixes import Prefix
from units import Units

# === Fundamental Constants ===
speed_of_light = Quantity(299792458, Prefix(""), Units(length=1, time=-1))
planck_constant = Quantity(6.62607015e-34, Prefix(""), Units(length=2, mass=1, time=-1))
planck_bar_constant = Quantity(1.054571817e-34, Prefix(""), Units(length=2, mass=1, time=-1))
gravitational_constant = Quantity(6.67430e-11, Prefix(""), Units(length=3, mass=-1, time=-2))
standard_gravity = Quantity(9.80665, Prefix(""), Units(length=1, time=-2))

# === Particle Constants ===
electron_charge = Quantity(1.602176634e-19, Prefix(""), Units(electric_current=1, time=1))
elementary_charge = electron_charge
electron_mass = Quantity(9.1093837015e-31, Prefix(""), Units(mass=1))
proton_mass = Quantity(1.67262192369e-27, Prefix(""), Units(mass=1))
neutron_mass = Quantity(1.67492749804e-27, Prefix(""), Units(mass=1))

# === Atomic & Quantum Constants ===
rydberg_constant = Quantity(10973731.568160, Prefix(""), Units(length=-1))
rydberg_energy = Quantity(13.605693122994, Prefix(""), Units(length=2, mass=1, time=-2))
rydberg_frequency = Quantity(3.289841960355e15, Prefix(""), Units(time=-1))
hartree_energy = Quantity(4.3597447222071e-18, Prefix(""), Units(length=2, mass=1, time=-2))
electron_volt = Quantity(1.602176634e-19, Prefix(""), Units(length=2, mass=1, time=-2))  # 1 eV in Joules

# === Electromagnetism ===
vacuum_permittivity = Quantity(8.854187817e-12, Prefix(""), Units(length=-3, mass=-1, time=4, electric_current=2))
vacuum_permeability = Quantity(1.25663706212e-6, Prefix(""), Units(length=1, mass=1, time=-2, electric_current=-2))
coulomb_constant = Quantity(8.9875517923e9, Prefix(""), Units(length=3, mass=1, time=-4, electric_current=-2))
faraday_constant = Quantity(96485.33212, Prefix(""), Units(electric_current=1, time=1, amount_of_substance=-1))

# === Thermodynamics ===
boltzmann_constant = Quantity(1.380649e-23, Prefix(""), Units(length=2, mass=1, time=-2, temperature=-1))
gas_constant = Quantity(8.314462618, Prefix(""), Units(length=2, mass=1, time=-2, temperature=-1, amount_of_substance=-1))
stefan_boltzmann_constant = Quantity(5.670374419e-8, Prefix(""), Units(length=-2, mass=1, time=-3, temperature=-4))
boltzmann_energy_at_room_temp = Quantity(0.02585, Prefix(""), Units(length=2, mass=1, time=-2))

# === Avogadro & Related ===
avogadro_constant = Quantity(6.02214076e23, Prefix(""), Units(amount_of_substance=1))
