from fractions import Fraction

# Define metric prefixes (powers of 10)
PREFIXES_THOUSANDS = {
    "Q": 10**30, "R": 10**27, "Y": 10**24, "Z": 10**21, "E": 10**18,
    "P": 10**15, "T": 10**12, "G": 10**9, "M": 10**6, "k": 10**3, "": 1,
    "m": Fraction(1, 10**3), "µ": Fraction(1, 10**6), "n": Fraction(1, 10**9),
    "p": Fraction(1, 10**12), "f": Fraction(1, 10**15), "a": Fraction(1, 10**18),
    "z": Fraction(1, 10**21), "y": Fraction(1, 10**24), "r": Fraction(1, 10**27),
    "q": Fraction(1, 10**30)
}

PREFIXES_TENTHS = {
    'da': 10**1, 'h': 10**2, 'd': 10**-1, 'c': 10**-2, '': 1
}

def valid_combo(t, th):
    """Filter out invalid combinations."""
    # never allow deci + atto (would form "da")
    if t == "d" and th == "a":
        return False
    # special case: allow "hz" (hecto + zepto)
    if t == "h" and th == "z":
        return True

    vt, vth = PREFIXES_TENTHS[t], PREFIXES_THOUSANDS[th]
    # allow only same-kind combinations (>1 or <1 or ==1)
    return (vt > 1 and vth > 1) or (vt < 1 and vth < 1) or vt == 1 or vth == 1

# Build combined prefix dictionary
PREFIXES = {
    t + th: Fraction(PREFIXES_TENTHS[t]) * Fraction(PREFIXES_THOUSANDS[th])
    for th in PREFIXES_THOUSANDS
    for t in PREFIXES_TENTHS
    if valid_combo(t, th)
}

class Prefix:
    def __init__(self, symbol: str):
        if symbol not in PREFIXES:
            raise ValueError(f"Invalid prefix: {symbol}")
        self.symbol = symbol
        self.factor = PREFIXES[symbol]

    def __repr__(self):
        return self.symbol
