# LIM model downloads

The uploaded original C and notebook implementations passed exhaustive equality checks for unsigned 8-bit operands, LPL 1 through 7. Each configuration covers all 65,536 ordered pairs from 0 through 255, including a separately reported 0 through 127 subset. This establishes implementation agreement, not an error-optimality claim.

- `c/`: one self-contained C file per architecture. Public function names match the original C. Compile with C99 and link `-lm` when needed. Helpers have internal linkage so different standalone files can be linked together.
- `python/`: one self-contained Python file per architecture; call `compute(a, b, width_a, width_b, lpl)` or the original class method.
- `lim_all.c`: all C architectures in one self-contained file. The original multiplier's declaration-only local header include is omitted; arithmetic function bodies are preserved.
- `lim_all.py`: all Python architectures in one file; `COMPONENTS` maps each RTL architecture ID to its callable.
- `lim_all.v`: all original RTL modules in one file; choose the desired module as top. All modules use parameters `N` and `LPL`.

Use either the combined implementation or the standalone files in a build. Combining both representations duplicates the same public functions/modules. LIA results retain N+1 bits; LIM results retain 2*N bits. For LIM, the software argument VBL corresponds to RTL LPL.

Base validation covers N=8 and LPL=1..7. Additional benchmark validation is recorded below; other settings remain unverified. Keep each configuration's parameters when downloading a shared parameterized file. Hardware measurement availability is specific to each configuration; see the catalog provenance.

Original sources and hashes, the architecture/function mapping, and generated file hashes are recorded in `model-manifest.json`. Error metrics and exact rational aggregates are in the website's `result/validation/` reports. No arithmetic algorithm was changed during splitting or combination.

## Additional benchmark validation

Unsigned N=8, LPL=8 also passed exhaustive original C/Python/RTL agreement: 65,536 ordered input pairs per architecture. Reports: `result/validation/multiplier8-lpl8-c-python.json` and `result/validation/multiplier8-lpl8-rtl.json`. The parameterized arithmetic implementations are unchanged. Area and power are imported from `assets/excels/LIM_final_comparison.csv`; reported timing has no confirmed propagation-delay definition.
