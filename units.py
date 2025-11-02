from fractions import Fraction

class Units:
    """Represents SI base unit exponents: m, kg, s, A, K, mol, cd."""
    def __init__(self, length=0, mass=0, time=0, electric_current=0,
                 temperature=0, amount_of_substance=0, luminous_intensity=0):
        self.length = length
        self.mass = mass
        self.time = time
        self.electric_current = electric_current
        self.temperature = temperature
        self.amount_of_substance = amount_of_substance
        self.luminous_intensity = luminous_intensity

    def __mul__(self, other):
        return Units(
            self.length + other.length,
            self.mass + other.mass,
            self.time + other.time,
            self.electric_current + other.electric_current,
            self.temperature + other.temperature,
            self.amount_of_substance + other.amount_of_substance,
            self.luminous_intensity + other.luminous_intensity,
        )

    def __truediv__(self, other):
        return Units(
            self.length - other.length,
            self.mass - other.mass,
            self.time - other.time,
            self.electric_current - other.electric_current,
            self.temperature - other.temperature,
            self.amount_of_substance - other.amount_of_substance,
            self.luminous_intensity - other.luminous_intensity,
        )

    def __pow__(self, power):
        return Units(
            self.length * power,
            self.mass * power,
            self.time * power,
            self.electric_current * power,
            self.temperature * power,
            self.amount_of_substance * power,
            self.luminous_intensity * power,
        )

    def __eq__(self, other):
        return vars(self) == vars(other)

    def __repr__(self):
        name = self.composite_name()
        if UNIT_PRIORITY.get(name,1) >= 2:
            return name
        parts = []
        for symbol, exp in zip(
            ["m", "kg", "s", "A", "K", "mol", "cd"],
            [self.length, self.mass, self.time, self.electric_current,
             self.temperature, self.amount_of_substance, self.luminous_intensity]
        ):
            if exp != 0:
                parts.append(f"{symbol}^{exp}" if exp != 1 else symbol)
        return ".".join(parts) if parts else "dimensionless"
    def __hash__(self):
        return hash((
            self.length,
            self.mass,
            self.time,
            self.electric_current,
            self.temperature,
            self.luminous_intensity,
            self.amount_of_substance
        ))

    def composite_name(self):
        best = ""
        best_prio = 0
        for name, unit in COMPOSITE_UNITS.items():
            if self == unit:
                prio = UNIT_PRIORITY.get(name, 2)  # default to medium priority
                if prio > best_prio:
                    best = name
                    best_prio = prio
        return best

COMPOSITE_UNITS = {
    "m": Units(length=1),                                       # Meter or Metre
    "kg": Units(mass=1),                                        # Kilogram
    "s": Units(time=1),                                         # Seconds
    "A": Units(electric_current=1),                             # Amps
    "K": Units(temperature=1),                                  # Kelvin
    "cd": Units(luminous_intensity=1),                          # Candela
    "mol": Units(amount_of_substance=1),                        # Mole
    "N": Units(mass=1, length=1, time=-2),                      # Newton
    "J": Units(mass=1, length=2, time=-2),                      # Joule
    "W": Units(mass=1, length=2, time=-3),                      # Watt
    "Pa": Units(mass=1, length=-1, time=-2),                    # Pascal
    "C": Units(time=1, electric_current=1),                     # Coulomb
    "V": Units(mass=1, length=2, time=-3, electric_current=-1), # Volt
    "F": Units(mass=-1, length=-2, time=4, electric_current=2), # Farad
    "Ω": Units(mass=1, length=2, time=-3, electric_current=-2), # Ohm
    "S": Units(mass=-1, length=-2, time=3, electric_current=2), # Siemens
    "T": Units(mass=1, time=-2, electric_current=-1),           # Tesla
    "H": Units(mass=1, length=2, time=-2, electric_current=-2), # Henry
    "lm": Units(luminous_intensity=1),                          # Lumen
    "lx": Units(length=-2, luminous_intensity=1),               # Lux
    "Hz": Units(time=-1),                                       # Hertz
    "Wb": Units(mass=1, length=2, time=-2, electric_current=-1),# Weber
    "kat": Units(amount_of_substance=1, time=-1),               # Katal
    "Å": Units(length=1),                                       # Angstrom (1 Å = 10^-10 m)
    "ly": Units(length=1),                                      # Light-year
    "pc": Units(length=1),                                      # Parsec
    "in": Units(length=1),                                      # Inch
    "ft": Units(length=1),                                      # Foot
    "mi": Units(length=1),                                      # Mile
    "g": Units(mass=1),                                         # Gram
    "t": Units(mass=1),                                         # Tonne (metric)
    "lb": Units(mass=1),                                        # Pound
    "oz": Units(mass=1),                                        # Ounce
    "cal": Units(mass=1, length=2, time=-2),                    # Calorie (same units as Joule)
    "erg": Units(mass=1, length=2, time=-2),                    # Erg (same units as Joule)
    "Wh": Units(mass=1, length=2, time=-2),                     # Watt-hour (same units as Joule)
    "bar": Units(mass=1, length=-1, time=-2),                   # Bar (same units as Pascal)
    "atm": Units(mass=1, length=-1, time=-2),                   # Atmosphere (same units as Pascal)
    "mmHg": Units(mass=1, length=-1, time=-2),                  # Millimeter of mercury
    "torr": Units(mass=1, length=-1, time=-2),                  # Torr
    "psi": Units(mass=1, length=-1, time=-2),                   # Pound per square inch
    "dyn": Units(mass=1, length=1, time=-2),                    # Dyne (same units as Newton)
    "lbf": Units(mass=1, length=1, time=-2),                    # Pound-force
    "hp": Units(mass=1, length=2, time=-3),                     # Horsepower (same units as Watt)
    "rad": Units(),                                             # Radian (dimensionless)
    "deg": Units(),                                             # Degree (dimensionless)
    "m²": Units(length=2),                                      # Square meter
    "cm²": Units(length=2),                                     # Square centimeter
    "acre": Units(length=2),                                    # Acre
    "ha": Units(length=2),                                      # Hectare
    "m³": Units(length=3),                                      # Cubic meter
    "L": Units(length=3),                                       # Liter
    "gal": Units(length=3),                                     # US gallon
    "ft³": Units(length=3),                                     # Cubic foot
    "mph": Units(length=1, time=-1),                            # Miles per hour
    "knot": Units(length=1, time=-1),                           # Knot
}
UNIT_PRIORITY = {
    # --- SI base units ---
    "m": 5,
    "kg": 5,
    "s": 5,
    "A": 5,
    "K": 5,
    "mol": 5,
    "cd": 5,

    # --- Derived SI units ---
    "N": 4,
    "J": 4,
    "W": 4,
    "Pa": 4,
    "C": 4,
    "V": 4,
    "F": 4,
    "Ω": 4,
    "S": 4,
    "T": 4,
    "H": 4,
    "Hz": 4,
    "Wb": 4,
    "kat": 4,
    "lm": 4,
    "lx": 4,

    # --- Extended SI forms ---
    "m²": 3,
    "m³": 3,

    # --- Accepted non-SI metric units ---
    "L": 2,
    "bar": 2,
    "cal": 2,
    "Wh": 2,
    "erg": 2,
    "ha": 2,
    "rad": 2,
    "deg": 2,

    # --- Non-SI & Imperial/other units ---
    "Å": 1,
    "ly": 1,
    "pc": 1,
    "in": 1,
    "ft": 1,
    "mi": 1,
    "g": 1,
    "t": 1,
    "lb": 1,
    "oz": 1,
    "atm": 1,
    "mmHg": 1,
    "torr": 1,
    "psi": 1,
    "dyn": 1,
    "lbf": 1,
    "hp": 1,
    "acre": 1,
    "gal": 1,
    "ft³": 1,
    "mph": 1,
    "knot": 1,
}
