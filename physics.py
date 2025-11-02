"""
Physics helper functions for physunits.
Each function operates on `Quantity` objects and preserves dimensional consistency.
"""

from quantity import Quantity
from prefixes import Prefix
from units import Units
from constants import (
    standard_gravity, speed_of_light, boltzmann_constant, gas_constant,
    gravitational_constant, planck_constant
)
from math import sqrt
from functools import wraps

def physics_safe(func):
    """
    Decorator for physics functions to catch common errors:
    - Division by zero
    - Negative values for sqrt
    - Velocities exceeding speed of light
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check for Quantity arguments with zero values in denominators
        for i, arg in enumerate(args):
            if hasattr(arg, 'value') and arg.value == 0:
                if func.__name__ in (
                    'speed', 'acceleration', 'power', 'pressure', 'ideal_gas_pressure',
                    'electric_field', 'capacitance', 'current', 'frequency_from_period',
                    'photon_energy_from_wavelength', 'refractive_index', 'gravitational_force',
                    'gravitational_potential_energy', 'density', 'flow_rate',
                    'continuity_equation'
                ):
                    raise ValueError(f"{func.__name__}: argument {i+1} cannot be zero")

        # Special check for sqrt of negative values
        if func.__name__ in ('orbital_velocity', 'escape_velocity'):
            mass = args[0]
            radius = args[1]
            if mass.value < 0:
                raise ValueError("Mass cannot be negative")
            if radius.value <= 0:
                raise ValueError("Radius must be positive")

        # Special check for time_dilation
        if func.__name__ == 'time_dilation':
            velocity = args[1]
            if abs(velocity.value) >= speed_of_light.value:
                raise ValueError("Velocity cannot be equal to or exceed the speed of light")

        return func(*args, **kwargs)
    return wrapper

# === MECHANICS ===
@physics_safe
def speed(distance: Quantity, time: Quantity) -> Quantity:
    """v = d / t"""
    return distance / time
@physics_safe
def acceleration(velocity_change: Quantity, time: Quantity) -> Quantity:
    """a = Δv / t"""
    return velocity_change / time
@physics_safe
def force(mass: Quantity, acceleration: Quantity) -> Quantity:
    """F = m * a"""
    return mass * acceleration

def momentum(mass: Quantity, velocity: Quantity) -> Quantity:
    """p = m * v"""
    return mass * velocity

def impulse(force: Quantity, time: Quantity) -> Quantity:
    """J = F * t"""
    return force * time

def kinetic_energy(mass: Quantity, velocity: Quantity) -> Quantity:
    """E_k = ½ m v²"""
    return Quantity(0.5, Prefix(""), Units()) * mass * (velocity ** 2)

def potential_energy(mass: Quantity, height: Quantity, gravity=standard_gravity) -> Quantity:
    """E_p = m * g * h"""
    return mass * gravity * height

def mechanical_energy(kinetic: Quantity, potential: Quantity) -> Quantity:
    """E_total = E_k + E_p"""
    return kinetic + potential

def work(force: Quantity, distance: Quantity) -> Quantity:
    """W = F * d"""
    return force * distance
@physics_safe
def power(work: Quantity, time: Quantity) -> Quantity:
    """P = W / t"""
    return work / time

def energy_from_power(power: Quantity, time: Quantity) -> Quantity:
    """E = P * t"""
    return power * time


# === ROTATIONAL MOTION ===

def torque(force: Quantity, radius: Quantity) -> Quantity:
    """τ = F * r"""
    return force * radius

def angular_momentum(moment_of_inertia: Quantity, angular_velocity: Quantity) -> Quantity:
    """L = I * ω"""
    return moment_of_inertia * angular_velocity

def rotational_kinetic_energy(moment_of_inertia: Quantity, angular_velocity: Quantity) -> Quantity:
    """E_rot = ½ I ω²"""
    return Quantity(0.5, Prefix(""), Units()) * moment_of_inertia * (angular_velocity ** 2)


# === THERMODYNAMICS ===
@physics_safe
def pressure(force: Quantity, area: Quantity) -> Quantity:
    """P = F / A"""
    return force / area
@physics_safe
def temperature_from_energy_per_particle(energy: Quantity) -> Quantity:
    """T = E / k_B"""
    return energy / boltzmann_constant
@physics_safe
def ideal_gas_pressure(n_moles: Quantity, volume: Quantity, temperature: Quantity) -> Quantity:
    """P = nRT / V"""
    return n_moles * gas_constant * temperature / volume

def heat_from_specific_heat(mass: Quantity, specific_heat_capacity: Quantity, temperature_change: Quantity) -> Quantity:
    """Q = m * c * ΔT"""
    return mass * specific_heat_capacity * temperature_change

def thermal_energy_from_temperature(temperature: Quantity) -> Quantity:
    """E = k_B * T"""
    return boltzmann_constant * temperature


# === ELECTROMAGNETISM ===
@physics_safe
def electric_force(charge1: Quantity, charge2: Quantity, distance: Quantity, k_coulomb: Quantity) -> Quantity:
    """F = k * q1 * q2 / r²"""
    return k_coulomb * charge1 * charge2 / (distance ** 2)
@physics_safe
def electric_field(force: Quantity, charge: Quantity) -> Quantity:
    """E = F / q"""
    return force / charge

def potential_energy_electric(charge: Quantity, potential: Quantity) -> Quantity:
    """U = q * V"""
    return charge * potential

def voltage_from_field(field: Quantity, distance: Quantity) -> Quantity:
    """V = E * d"""
    return field * distance
@physics_safe
def capacitance(charge: Quantity, voltage: Quantity) -> Quantity:
    """C = Q / V"""
    return charge / voltage

def energy_stored_in_capacitor(capacitance: Quantity, voltage: Quantity) -> Quantity:
    """U = ½ C V²"""
    return Quantity(0.5, Prefix(""), Units()) * capacitance * (voltage ** 2)
@physics_safe
def current(charge: Quantity, time: Quantity) -> Quantity:
    """I = Q / t"""
    return charge / time

def voltage_from_current_resistance(current: Quantity, resistance: Quantity) -> Quantity:
    """V = I * R"""
    return current * resistance

def electrical_power(voltage: Quantity, current: Quantity) -> Quantity:
    """P = V * I"""
    return voltage * current


# === WAVES & OPTICS ===

def wave_speed(frequency: Quantity, wavelength: Quantity) -> Quantity:
    """v = f * λ"""
    return frequency * wavelength
@physics_safe
def frequency_from_period(period: Quantity) -> Quantity:
    """f = 1 / T"""
    return Quantity(1, Prefix(""), Units()) / period

def photon_energy(frequency: Quantity, planck_constant: Quantity = planck_constant) -> Quantity:
    """E = h * f"""
    return planck_constant * frequency
@physics_safe
def photon_energy_from_wavelength(wavelength: Quantity, planck_constant: Quantity = planck_constant) -> Quantity:
    """E = h * c / λ"""
    return planck_constant * speed_of_light / wavelength
@physics_safe
def refractive_index(speed_in_vacuum: Quantity, speed_in_medium: Quantity) -> Quantity:
    """n = c / v"""
    return speed_in_vacuum / speed_in_medium


# === ASTRONOMY & RELATIVITY ===
@physics_safe
def gravitational_force(mass1: Quantity, mass2: Quantity, distance: Quantity) -> Quantity:
    """F = G * m1 * m2 / r²"""
    return gravitational_constant * mass1 * mass2 / (distance ** 2)
@physics_safe
def orbital_velocity(mass_central: Quantity, radius: Quantity) -> Quantity:
    """v = sqrt(GM / r)"""
    value = sqrt(gravitational_constant.value * mass_central.value / radius.value)
    return Quantity(value, Prefix(""), Units(length=1, time=-1))
@physics_safe
def escape_velocity(mass: Quantity, radius: Quantity) -> Quantity:
    """v_esc = sqrt(2GM / r)"""
    value = sqrt(2 * gravitational_constant.value * mass.value / radius.value)
    return Quantity(value, Prefix(""), Units(length=1, time=-1))
@physics_safe
def gravitational_potential_energy(mass1: Quantity, mass2: Quantity, distance: Quantity) -> Quantity:
    """U = -G * m1 * m2 / r"""
    return Quantity(-1, Prefix(""), Units()) * gravitational_constant * mass1 * mass2 / distance

def energy_mass_equivalence(mass: Quantity) -> Quantity:
    """E = m * c²"""
    return mass * (speed_of_light ** 2)
@physics_safe
def time_dilation(proper_time: Quantity, velocity: Quantity) -> Quantity:
    """t = t₀ / sqrt(1 - v² / c²)"""
    factor = 1 / sqrt(1 - (velocity.value / speed_of_light.value) ** 2)
    return Quantity(proper_time.value * factor, proper_time.prefix, proper_time.units)
@physics_safe
def gravitational_redshift(delta_phi: Quantity) -> Quantity:
    """z ≈ Δφ / c²"""
    return delta_phi / (speed_of_light ** 2)


# === FLUID DYNAMICS ===
@physics_safe
def density(mass: Quantity, volume: Quantity) -> Quantity:
    """ρ = m / V"""
    return mass / volume
def pressure_from_depth(density: Quantity, gravity: Quantity, depth: Quantity) -> Quantity:
    """P = ρgh"""
    return density * gravity * depth

def buoyant_force(density_fluid: Quantity, volume_submerged: Quantity, gravity: Quantity = standard_gravity) -> Quantity:
    """F_b = ρ * V * g"""
    return density_fluid * volume_submerged * gravity

def bernoulli_pressure(pressure_static: Quantity, density: Quantity, velocity: Quantity, height: Quantity, gravity: Quantity = standard_gravity) -> Quantity:
    """Bernoulli: P_total = P + ½ρv² + ρgh"""
    kinetic_term = Quantity(0.5, Prefix(""), Units()) * density * (velocity ** 2)
    potential_term = density * gravity * height
    return pressure_static + kinetic_term + potential_term
@physics_safe
def flow_rate(volume: Quantity, time: Quantity) -> Quantity:
    """Q = V / t"""
    return volume / time
@physics_safe
def continuity_equation(area1: Quantity, velocity1: Quantity, area2: Quantity) -> Quantity:
    """A₁v₁ = A₂v₂  → v₂ = A₁v₁ / A₂"""
    return (area1 * velocity1) / area2
