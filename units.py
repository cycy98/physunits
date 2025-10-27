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

    def composite_name(self):
        for name, unit in COMPOSITE_UNITS.items():
            if self == unit:
                return name
        return None

    def __repr__(self):
        name = self.composite_name()
        if name:
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

COMPOSITE_UNITS = {
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
}
