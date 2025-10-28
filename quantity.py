import re
from fractions import Fraction
from .prefixes import Prefix, PREFIXES
from .units import Units, COMPOSITE_UNITS

def parse_units(expr: str) -> Units:
    """Parse compound expressions like 'N*m/s^2' or 'kg*m^2/s^3'."""
    expr = expr.replace("·", "*").replace(" ", "").replace(r"//", r"/")
    tokens = re.split(r"([*/])", expr)
    result = Units()
    op = "*"
    for token in tokens:
        if token in ("*", "/"):
            op = token
            continue
        if not token:
            continue
        m = re.match(r"([a-zA-ZµΩ]+)(?:\^(-?\d+))?$", token)
        if not m:
            raise ValueError(f"Invalid unit token: {token}")
        symbol, exp = m.groups()
        exp = int(exp) if exp else 1
        u = COMPOSITE_UNITS.get(symbol)
        if not u:
            if symbol in ["m", "kg", "s", "A", "K", "mol", "cd"]:
                u = Units(**{{
                    "m": "length", "kg": "mass", "s": "time", "A": "electric_current",
                    "K": "temperature", "mol": "amount_of_substance", "cd": "luminous_intensity"
                }[symbol]: 1})
            else:
                raise ValueError(f"Unknown unit: {symbol}")
        u = u ** exp
        result = result * u if op == "*" else result / u
    return result


class Quantity:
    def __init__(self, value, prefix: Prefix, units: Units):
        self.value = value
        self.prefix = prefix
        self.units = units

    def __add__(self, other):
        if self.units != other.units:
            raise ValueError("Incompatible units for addition")
        v = self.value * float(self.prefix.factor) + other.value * float(other.prefix.factor)
        return Quantity(v, Prefix(""), self.units)
    def __sub__(self, other):
        if self.units != other.units:
            raise ValueError("Incompatible units for subtraction")
        v = self.value * float(self.prefix.factor) - other.value * float(other.prefix.factor)
        return Quantity(v, Prefix(""), self.units)
    def __neg__(self):
        return Quantity(-self.value, self.prefix, self.units)

    def __mul__(self, other):
        if isinstance(other, Quantity):
            return Quantity(self.value * other.value, Prefix(""), self.units * other.units)
        return Quantity(self.value * other, self.prefix, self.units)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Quantity):
            return Quantity(self.value / other.value, Prefix(""), self.units / other.units)
        return Quantity(self.value / other, self.prefix, self.units)
    def __rtruediv__(self, other):
        return Quantity(other / self.value, Prefix(""), Units() / self.units)

    def __pow__(self, power):
        return Quantity(self.value ** power, Prefix(""), self.units ** power)

    def simplify(self):
        name = self.units.composite_name()
        return name or str(self.units)

    def convert(self, prefix_str: str):
        target_prefix = Prefix(prefix_str)
        factor = float(self.prefix.factor) / float(target_prefix.factor)
        return Quantity(self.value * factor, target_prefix, self.units)

    def to(self, unit_expr: str):
        """Convert to another compatible unit expression (like 'km' or 'ms')."""
        new_units = parse_units(unit_expr)
        if new_units != self.units:
            raise ValueError(f"Cannot convert {self.units} to {new_units}")
        for p in PREFIXES:
            if unit_expr.startswith(p):
                target_prefix = Prefix(p)
                return self.convert(p)
        return self

    def __repr__(self):
        prefix = str(self.prefix)
        return f"{self.value} {prefix}{str(self.units)}"
    # Comparison operators
    def __eq__(self, other):
        return (self.value * float(self.prefix.factor) == other.value * float(other.prefix.factor)
                and self.units == other.units)
    def __lt__(self, other):
        if self.units != other.units:
            raise ValueError("Incompatible units for comparison")
        return (self.value * float(self.prefix.factor) <
                other.value * float(other.prefix.factor))
    def __le__(self, other):
        if self.units != other.units:
            raise ValueError("Incompatible units for comparison")
        return (self.value * float(self.prefix.factor) <=
                other.value * float(other.prefix.factor))
    def __gt__(self, other):
        if self.units != other.units:
            raise ValueError("Incompatible units for comparison")
        return (self.value * float(self.prefix.factor) >
                other.value * float(other.prefix.factor))
    def __ge__(self, other):
        if self.units != other.units:
            raise ValueError("Incompatible units for comparison")
        return (self.value * float(self.prefix.factor) >=
                other.value * float(other.prefix.factor))
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        return hash((self.value * float(self.prefix.factor), self.units))
