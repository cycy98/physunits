"""
Universal unit and prefix conversion utilities for physunits.
Works directly with Quantity objects.
"""

import math
from .quantity import Quantity, parse_units
from .prefixes import PREFIXES_THOUSANDS, Prefix, PREFIXES
from .units import COMPOSITE_UNITS, Units, UNIT_PRIORITY
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
    factor = Fraction(quantity.prefix.factor) / Fraction(target_prefix.factor)
    new_value = quantity.value * factor  # Final conversion to float
    return Quantity(new_value, target_prefix, quantity.units)

# === Physical unit conversion ===

_CONVERSIONS = {
    # Energy
    ("J", "eV"): Fraction(1, 1602176634) * 10**10,  # Joule to electronvolt
    ("eV", "J"): Fraction(1602176634, 10**19),
    ("J", "kJ"): Fraction(1, 1000),
    ("kJ", "J"): 1000,
    ("J", "MJ"): Fraction(1, 1000000),
    ("MJ", "J"): 1000000,
    ("J", "cal"): Fraction(1000, 4184),  # Joule to calorie (thermochemical)
    ("cal", "J"): Fraction(4184, 1000),
    ("J", "kcal"): Fraction(1, 4184),
    ("kcal", "J"): 4184,
    ("J", "erg"): 10**7,
    ("erg", "J"): Fraction(1, 10**7),
    ("J", "Wh"): Fraction(1, 3600),
    ("Wh", "J"): 3600,
    ("J", "kWh"): Fraction(1, 3600000),
    ("kWh", "J"): 3600000,

    # Length
    ("m", "cm"): 100,
    ("cm", "m"): Fraction(1, 100),
    ("m", "mm"): 1000,
    ("mm", "m"): Fraction(1, 1000),
    ("m", "km"): Fraction(1, 1000),
    ("km", "m"): 1000,
    ("m", "Å"): 10**10,
    ("Å", "m"): Fraction(1, 10**10),
    ("m", "nm"): 10**9,
    ("nm", "m"): Fraction(1, 10**9),
    ("m", "µm"): 10**6,
    ("µm", "m"): Fraction(1, 10**6),
    ("m", "ly"): Fraction(1, 9460730472580800),
    ("ly", "m"): 9460730472580800,
    ("m", "pc"): Fraction(1, 30856775812800000),
    ("pc", "m"): 30856775812800000,
    ("m", "in"): Fraction(10000, 254),
    ("in", "m"): Fraction(254, 10000),
    ("m", "ft"): Fraction(10000, 3048),
    ("ft", "m"): Fraction(3048, 10000),
    ("m", "mi"): Fraction(1000000, 1609344),
    ("mi", "m"): Fraction(1609344, 1000000),

    # Mass
    ("kg", "g"): 1000,
    ("g", "kg"): Fraction(1, 1000),
    ("kg", "mg"): 1000000,
    ("mg", "kg"): Fraction(1, 1000000),
    ("kg", "t"): Fraction(1, 1000),
    ("t", "kg"): 1000,
    ("kg", "lb"): Fraction(100000000, 45359237),
    ("lb", "kg"): Fraction(45359237, 100000000),
    ("kg", "oz"): Fraction(1000000000, 28349523125),
    ("oz", "kg"): Fraction(28349523125, 1000000000),

    # Time
    ("s", "min"): Fraction(1, 60),
    ("min", "s"): 60,
    ("s", "h"): Fraction(1, 3600),
    ("h", "s"): 3600,
    ("s", "day"): Fraction(1, 86400),
    ("day", "s"): 86400,
    ("s", "yr"): Fraction(1, 31557600),
    ("yr", "s"): 31557600,

    # Velocity
    ("m/s", "km/h"): Fraction(18, 5),
    ("km/h", "m/s"): Fraction(5, 18),
    ("m/s", "mph"): Fraction(100000, 44704),
    ("mph", "m/s"): Fraction(44704, 100000),
    ("m/s", "knot"): Fraction(1000000, 514444),
    ("knot", "m/s"): Fraction(514444, 1000000),

    # Power
    ("W", "kW"): Fraction(1, 1000),
    ("kW", "W"): 1000,
    ("W", "MW"): Fraction(1, 1000000),
    ("MW", "W"): 1000000,
    ("W", "hp"): Fraction(1000000000, 745699871582),
    ("hp", "W"): Fraction(745699871582, 1000000000),

    # Pressure
    ("Pa", "kPa"): Fraction(1, 1000),
    ("kPa", "Pa"): 1000,
    ("Pa", "MPa"): Fraction(1, 1000000),
    ("MPa", "Pa"): 1000000,
    ("Pa", "bar"): Fraction(1, 100000),
    ("bar", "Pa"): 100000,
    ("Pa", "atm"): Fraction(1, 101325),
    ("atm", "Pa"): 101325,
    ("Pa", "mmHg"): Fraction(1000000000, 133322387415),
    ("mmHg", "Pa"): Fraction(133322387415, 1000000000),
    ("Pa", "torr"): Fraction(1000000000, 133322387415),
    ("torr", "Pa"): Fraction(133322387415, 1000000000),
    ("Pa", "psi"): Fraction(1000000000, 6894757293168),
    ("psi", "Pa"): Fraction(6894757293168, 1000000000),

    # Force
    ("N", "kN"): Fraction(1, 1000),
    ("kN", "N"): 1000,
    ("N", "dyn"): 100000,
    ("dyn", "N"): Fraction(1, 100000),
    ("N", "lbf"): Fraction(1000000000, 44482216152605),
    ("lbf", "N"): Fraction(44482216152605, 1000000000),

    # Angle (dimensionless)
    ("rad", "deg"): Fraction(180000000, 3141592654),
    ("deg", "rad"): Fraction(3141592654, 180000000),

    # Area
    ("m²", "cm²"): 10000,
    ("cm²", "m²"): Fraction(1, 10000),
    ("m²", "mm²"): 1000000,
    ("mm²", "m²"): Fraction(1, 1000000),
    ("m²", "km²"): Fraction(1, 1000000),
    ("km²", "m²"): 1000000,
    ("m²", "acre"): Fraction(1000000, 40468564224),
    ("acre", "m²"): Fraction(40468564224, 1000000),
    ("m²", "ha"): Fraction(1, 10000),
    ("ha", "m²"): 10000,

    # Volume
    ("m³", "cm³"): 1000000,
    ("cm³", "m³"): Fraction(1, 1000000),
    ("m³", "L"): 1000,
    ("L", "m³"): Fraction(1, 1000),
    ("m³", "mL"): 1000000,
    ("mL", "m³"): Fraction(1, 1000000),
    ("m³", "gal"): Fraction(1000000000, 3785411784),
    ("gal", "m³"): Fraction(3785411784, 1000000000),
    ("m³", "ft³"): Fraction(1000000000, 28316846592),
    ("ft³", "m³"): Fraction(28316846592, 1000000000),

    # Temperature differences
    ("K", "°C"): 1,
    ("°C", "K"): 1,
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
        source_unit = str(quantity.units)
        if source_unit == "dimensionless":
            raise ValueError("Cannot convert dimensionless quantity")

    key = (source_unit, target_unit_symbol)
    if key not in _CONVERSIONS:
        raise ValueError(f"No known conversion from {source_unit} to {target_unit_symbol}")

    factor = _CONVERSIONS[key]
    new_value = quantity.value * factor
    new_units = (COMPOSITE_UNITS[target_unit_symbol]
                 if target_unit_symbol in COMPOSITE_UNITS
                 else parse_units(target_unit_symbol))
    return Quantity(new_value, Prefix(""), new_units)

def register_conversion(source_unit: str, target_unit: str, factor: float | int | Fraction):
    _CONVERSIONS[(source_unit, target_unit)] = factor
    _CONVERSIONS[(target_unit, source_unit)] = 1 / factor
def make_units(unit_dimensions: Units, repr: str, value: float | int | Fraction, priority: None | int = None):
    """Make Units
    unit_dimensions are the unit dimensions
    repr is the representation
    value is the ratio between your unit and the SI combination
    priority is used when printing, for the moment, if you do not have the value of 1, please don't make it more than 1
    """
    if not priority:
        priority = 1
    register_conversion(str(unit_dimensions), repr, value)
    UNIT_PRIORITY[repr] = priority
    COMPOSITE_UNITS[repr] = unit_dimensions

# Precompute exponent-to-prefix (negative for the scale)
_EXPONENT_TO_PREFIX_THOUSANDS = {
    -int(math.log10(float(factor))): symbol
    for symbol, factor in PREFIXES_THOUSANDS.items() if factor != 0
}
_EXPONENT_TO_PREFIX = {
    -int(math.log10(float(factor))): symbol
    for symbol, factor in PREFIXES.items() if factor != 0
}

# === Automatic scaling to best prefix ===

def best_prefix(quantity: Quantity, tenth: bool | None = None) -> Quantity:
    tenth = bool(tenth)
    abs_val = (quantity.value * quantity.prefix.factor
                if abs(quantity.value * float(quantity.prefix.factor))
                else Fraction(-1) * quantity.value * quantity.prefix.factor)
    if abs_val == 0:
        return quantity
    exponent = math.floor(math.log10(abs_val))
    mapping = _EXPONENT_TO_PREFIX if tenth else _EXPONENT_TO_PREFIX_THOUSANDS
    limit = 1 if tenth else 3  # log10(10)=1, log10(1000)=3
    target_exponent = (exponent // limit) * limit
    symbol = mapping.get(target_exponent, "")  # Fallback to no prefix
    if not symbol:
        return quantity
    factor = PREFIXES[symbol]
    new_val = quantity.value * (float(quantity.prefix.factor) / float(factor))
    return Quantity(new_val, Prefix(symbol), quantity.units)


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
