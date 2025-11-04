from fractions import Fraction

PREFIXES_THOUSANDS = {
    "Q": Fraction(10**30), "R": Fraction(10**27), "Y": Fraction(10**24), "Z": Fraction(10**21),
    "E": Fraction(10**18), "P": Fraction(10**15), "T": Fraction(10**12), "G": Fraction(10**9),
    "M": Fraction(10**6), "k": Fraction(10**3), "": Fraction(1),
    "m": Fraction(1, 10**3), "µ": Fraction(1, 10**6), "n": Fraction(1, 10**9),
    "p": Fraction(1, 10**12), "f": Fraction(1, 10**15), "a": Fraction(1, 10**18),
    "z": Fraction(1, 10**21), "y": Fraction(1, 10**24), "r": Fraction(1, 10**27),
    "q": Fraction(1, 10**30)
}
PREFIXES_THOUSANDS["u"] = PREFIXES_THOUSANDS["µ"]

PREFIXES_TENTHS = {
    'da': Fraction(10**1), 'h': Fraction(10**2), 'd': Fraction(1,10**1),
    'c': Fraction(1,10**2), '': Fraction(1)
}

def valid_combo(t, th):
    vt, vth = PREFIXES_TENTHS[t], PREFIXES_THOUSANDS[th]
    return (vt > 1 and vth > 1) or (vt < 1 and vth < 1) or vt == 1 or vth == 1

def build_prefix_dict():
    """Rebuild combined PREFIXES dictionary.""" 
    return {
        th + t: Fraction(PREFIXES_TENTHS[t]) * Fraction(PREFIXES_THOUSANDS[th])
        for th in PREFIXES_THOUSANDS
        for t in PREFIXES_TENTHS
        if valid_combo(t, th)
    }

PREFIXES = build_prefix_dict()

class Prefix:
    def __init__(self, symbol: str):
        if symbol not in PREFIXES:
            raise ValueError(f"Invalid prefix: {symbol}")
        self.symbol = symbol
        self.factor = PREFIXES[symbol]

    def __repr__(self):
        return self.symbol

    def __eq__(self, other):
        return isinstance(other, Prefix) and self.factor == other.factor

    def __hash__(self):
        return hash(self.factor)

def get_prefix_factor(symbol: str):
    try:
        return PREFIXES[symbol]
    except KeyError:
        raise ValueError(f"Unknown prefix: {symbol}")

def add_prefix(symbol: str, factor):
    """
    Add a user-defined prefix.
    rebuilds the global PREFIXES dictionary.
    """
    global PREFIXES
    # Normalize factor
    factor = Fraction(factor)

    # Prevent duplicates
    if symbol in PREFIXES_THOUSANDS or symbol in PREFIXES_TENTHS:
        raise ValueError(f"Prefix '{symbol}' already exists.")

    PREFIXES_THOUSANDS[symbol] = factor
    from .convert import update_exponent_to_prefixes
    # Rebuild combined dictionary
    PREFIXES.clear()
    PREFIXES.update(build_prefix_dict())
    update_exponent_to_prefixes()
    return f"Prefix '{symbol}' added successfully with factor {factor}"
