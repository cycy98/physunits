from fractions import Fraction

PREFIXES_THOUSANDS = {
    "Q": 10**30, "R": 10**27, "Y": 10**24, "Z": 10**21, "E": 10**18,
    "P": 10**15, "T": 10**12, "G": 10**9, "M": 10**6, "k": 10**3, "": 1,
    "m": Fraction(1, 10**3), "µ": Fraction(1, 10**6), "n": Fraction(1, 10**9),
    "p": Fraction(1, 10**12), "f": Fraction(1, 10**15), "a": Fraction(1, 10**18),
    "z": Fraction(1, 10**21), "y": Fraction(1, 10**24), "r": Fraction(1, 10**27),
    "q": Fraction(1, 10**30)
}
# Wrap thousands so we can control which tenths are offered per-thousands during the nested comprehension.
_ORIG_PREFIXES_THOUSANDS = PREFIXES_THOUSANDS

class _ThousandsProxy:
    def __init__(self, base):
        self._base = base

    def items(self):
        # We'll wrap the existing PREFIXES_TENTHS dict on-the-fly for each thousands entry.
        global PREFIXES_TENTHS
        for th, thv in self._base.items():
            original_tens = PREFIXES_TENTHS

            class _TensWrapper:
                def __init__(self, base, th, thv):
                    self._base = base
                    self._th = th
                    self._thv = thv

                def items(self):
                    for t, val in self._base.items():
                        vt = Fraction(val)
                        vth = Fraction(self._thv)

                        # never allow deci + atto (would form "da")
                        if t == "d" and self._th == "a":
                            continue

                        # allow only same-kind combinations (both >1 or both <1)
                        if vt > 1 and vth > 1:
                            yield (t, val)
                        elif vt < 1 and vth < 1:
                            yield (t, val)
                        elif vt == 1 or vth == 1:
                            yield (t, val)
                        else:
                            # special replacement: include "hz" (hecto + zepto) in place of "da"
                            if t == "h" and self._th == "z":
                                yield (t, val)
                            # otherwise skip mixed-sign combos
                            continue

            # Replace the global PREFIXES_TENTHS with our wrapper for the duration of the inner loop
            PREFIXES_TENTHS = _TensWrapper(original_tens, th, thv)
            try:
                yield (th, thv)
            finally:
                PREFIXES_TENTHS = original_tens

# Install proxy
PREFIXES_THOUSANDS = _ThousandsProxy(_ORIG_PREFIXES_THOUSANDS)
PREFIXES_TENTHS = {'da': 10**1, 'h': 10**2, 'd': 10**-1, 'c': 10**-2, '': 1} # bigger first so 10^-17 is not stored as "da"

PREFIXES = {
    t + th: val * thv
    for th, thv in PREFIXES_THOUSANDS.items()
    for t, val in PREFIXES_TENTHS.items()
}

class Prefix:
    def __init__(self, symbol: str):
        if symbol not in PREFIXES:
            raise ValueError(f"Invalid prefix: {symbol}")
        self.symbol = symbol
        self.factor = PREFIXES[symbol]

    def __repr__(self):
        return self.symbol
