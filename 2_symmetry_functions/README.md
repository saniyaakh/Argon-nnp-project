# Symmetry Functions (Yu Cai's Improved Method)

## Files:
- `new-Ar.ipynb` - Jupyter notebook for Argon-specific symmetry functions
- `generated_symfuncs.txt` - Generated 1085 symmetry functions for Argon
- `replace_symfuncs.sh` - Script to integrate functions into input.nn

## Generated Functions:
- G2 (radial): Short-range, long-range, and center-mode
- G4 (angular): Narrow and wide angle coverage
- Total: 1085 symmetry functions
- Optimized parameters for Argon (zeta < 16, proper eta values)

## Key Improvements:
- Fixed out-of-range issues (zeta values < 16)
- Optimized eta values to reduce extrapolation warnings
- Argon-specific parameter tuning
