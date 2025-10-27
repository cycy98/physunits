"""
Universal unit and prefix conversion utilities for physunits.
Works directly with Quantity objects.
"""

from .quantity import Quantity
from .prefixes import PREFIXES_THOUSANDS, Prefix, PREFIXES
from .units import Units, COMPOSITE_UNITS
from fractions import Fraction

# === Prefix conversion ===

def convert_prefix(quantity: Quantity, target_prefix_str: str) -> Quantity:
    """
    Convert a Quantity to a different SI prefix without changing its physical meaning.

    Example:
        >>> q = Quantity(2, Prefix('k'), Units(length=1))   # 2 km
        >>> convert_prefix(q, '')  # Convert to meters
        2000.0 m
    """
    target_prefix = Prefix(target_prefix_str)
    factor = quantity.prefix.factor / target_prefix.factor
    new_value = quantity.value * float(factor)
    return Quantity(new_value, target_prefix, quantity.units)


# === Physical unit conversion ===

_CONVERSIONS = {
    # Energy
    ("J", "eV"): 1 / 1.602176634e-19,
    ("eV", "J"): 1.602176634e-19,

    # Velocity
    ("m/s", "km/h"): 3.6,
    ("km/h", "m/s"): 1 / 3.6,

    # Pressure
    ("Pa", "atm"): 1 / 101325,
    ("atm", "Pa"): 101325,
    ("Pa", "bar"): 1e-5,
    ("bar", "Pa"): 1e5,

    # Temperature differences (not absolute temperatures!)
    ("K", "°C"): 1.0,
    ("°C", "K"): 1.0,

    # Time
    ("s", "min"): 1 / 60,
    ("min", "s"): 60,
    ("s", "h"): 1 / 3600,
    ("h", "s"): 3600,
}

def convert_unit(quantity: Quantity, target_unit_symbol: str) -> Quantity:
    """
    Convert a quantity to a different but compatible physical unit.

    Example:
        >>> energy = Quantity(1, Prefix(''), COMPOSITE_UNITS['J'])
        >>> convert_unit(energy, 'eV')
        6.241509e+18 eV
    """
    source_unit = quantity.units.composite_name()
    if not source_unit:
        raise ValueError("Cannot convert non-composite or unknown unit")

    key = (source_unit, target_unit_symbol)
    if key not in _CONVERSIONS:
        raise ValueError(f"No known conversion from {source_unit} to {target_unit_symbol}")

    factor = _CONVERSIONS[key]
    new_value = quantity.value * factor
    new_units = COMPOSITE_UNITS[target_unit_symbol] if target_unit_symbol in COMPOSITE_UNITS else quantity.units
    return Quantity(new_value, Prefix(""), new_units)


# === Automatic scaling to best prefix ===

def best_prefix(quantity: Quantity, tenth: bool | None = None) -> Quantity:
    """
    Automatically scale a quantity to the most appropriate SI prefix.
    Example:
        >>> q = Quantity(0.00032, Prefix(''), Units(length=1))
        >>> best_prefix(q)
        0.32 mm
    """
    if tenth is None:
        tenth = False
    if tenth:
        abs_val = abs(quantity.value * float(quantity.prefix.factor))
        # Find prefix that makes number between 1 and 1000
        for symbol, factor in PREFIXES.items():
            value_scaled = abs_val / float(factor)
            if 1 <= value_scaled < 10:
                new_val = quantity.value * (float(quantity.prefix.factor) / float(factor))
                return Quantity(new_val, Prefix(symbol), quantity.units)
    else:
        abs_val = abs(quantity.value * float(quantity.prefix.factor))
        # Find prefix that makes number between 1 and 1000
        for symbol, factor in PREFIXES_THOUSANDS.items():
            value_scaled = abs_val / float(factor)
            if 1 <= value_scaled < 1000:
                new_val = quantity.value * (float(quantity.prefix.factor) / float(factor))
                return Quantity(new_val, Prefix(symbol), quantity.units)
    # Fallback: no better prefix found
    return quantity


# === Human-readable formatting ===

def to_pretty_string(quantity: Quantity, max_precision: int = 4, tenth: bool | None = None) -> str:
    """
    Return a human-friendly string representation with auto-prefixing.

    Example:
        >>> q = Quantity(0.00032, Prefix(''), Units(length=1))
        >>> to_pretty_string(q)
        '0.32 mm'
    """
    q_best = best_prefix(quantity, tenth=tenth)
    val = round(q_best.value, max_precision)
    unit_name = q_best.units.composite_name() or str(q_best.units)
    prefix_str = q_best.prefix.symbol
    return f"{val} {prefix_str}{unit_name}"

