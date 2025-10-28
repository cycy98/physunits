# 0 (before release)
## 0.1 Project initiation
### 0.1.0
Creating project
### 0.1.1
Add a `__rmul__` method for `Quantity` to fix multiplication with ints or floats.
Fix prefix mismatches
### 0.1.2
Prefixes:
- Refactored
- Added a `__eq__` and `__hash__` method
Implemented `__hash__` in Units
Changed `to_pretty_string(, tenth=True)` to have better conversion
### 0.1.3
Changed `__hash__` in Units from integers to hashed-tuples
## 0.2 Project enhancement
### 0.2.0
Created more conversions, added more units such as imperial and horsepower.
Added the possibility to add more units
Added error messages in physics functions when a negative square root or division by 0 appears
Made `best_prefix` loopless
Changed order in the `PREFIXES` of thousand and tenths to avoid confuction with 10^-17 (been previously da and hz, now is ad)
Added the support for custom prefixes
Fixed floating-point imprecisions in `convert.py`.
