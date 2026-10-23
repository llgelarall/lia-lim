# Catalog data contract

`catalog.json` is the website's published dataset. It contains 216 verified configurations from 14 LIA and 13 LIM architectures: unsigned 8-bit operands at LPL 1..7, plus 9-bit LIA at LPL=8 and 8-bit LIM at LPL=8. Numerical metrics come from exhaustive original C evaluation, with per-input equality established for Python and RTL. See `result/validation/`. Supplied comparison CSVs provide area and power for the additional domains; physical delay remains null because its definition is unresolved. Do not insert illustrative architectures, fabricated measurements, or guessed parameter ranges.

Each `components` entry is one architecture, parameter configuration, and characterization context. Give separately characterized instances different IDs. Only equal-width operands are currently supported by this website schema; do not silently fold asymmetric multipliers into it.

Required component fields:

| Field | Meaning |
| --- | --- |
| `id` | Unique case-insensitive filename-safe ID, starting with a letter or digit. |
| `architecture` | Name found in the actual implementation. |
| `kind` | `adder` or `multiplier`. |
| `width` | Positive integer bits per operand. |
| `signed` | Explicit boolean. Record output width, overflow, and truncation behavior in `parameters` and benchmark domain. |
| `lpl` | Implementation-specific integer LPL setting, or `null` when unavailable/not applicable. Its meaning and supported values must come from the actual architecture. |
| `parameters` | Object containing the actual parameter names and values needed by the model; include RTL top module and output width where relevant. |
| `implementations` | Object with `c`, `python`, and `rtl` arrays of site-relative file paths. Include headers, support modules, build instructions, license, and other required files in each applicable array. Use an empty array for unavailable languages. |
| `error` | `me`, `mse`, `mae`, `pe`, `max`, `min`: verified numeric values or `null`. |
| `ppa` | `area`, `power`, `delay`: verified numeric values or `null`. |
| `reported_timing_ns` | Optional finite raw timing from the source. May be negative; does not populate `ppa.delay` or satisfy physical-delay limits without an established definition. |
| `provenance` | Source files and conditions below. |
| `benchmark_group` | A reviewed common benchmark identifier, or `null`, required for claims of equivalent hardware conditions. Raw source-distribution plots retain their own explicit limitations. |

Missing numeric values are `null`, never zero or strings such as `"N/A"`. Do not copy a metric from one LPL to another. Do not merge measurements across configurations or incompatible test conditions. The validator checks basic mathematical relationships, but cannot establish that a number was accurately transcribed from a report.

## Metric conventions

The website uses signed error `approximate - exact`, unnormalized integer-output error, squared output units for MSE, and PE as a fraction in `[0,1]`. `max` and `min` are signed extrema, not absolute extrema. MAR is not accepted. Record any sign reversal, normalization reversal, percentage conversion, and PPA unit conversion in `provenance.notes`, with the original value and source location.

PPA canonical units are area `um2`, power `uW`, delay `ns`. This convention does not establish what area, power, or timing path the source report measured; report definitions are separately required.

## Supplied comparison files and plots

`tools/import_comparisons.py` reads `assets/excels/LIA_final_comparison.csv` and `LIM_final_comparison.csv`. Despite the folder name, the supplied files are CSVs, not Excel workbooks. The importer checks finite metrics, probability/percentage agreement, signed extrema, error moments, vector counts, and all 27 original-library error rows against exhaustive C results. Python and RTL must have passed for those benchmark domains before import.

CSV signed error is `exact - approximate`; publication uses `me=-ME`, `min=-MAX`, `max=-MIN`, with MSE, MAE, and PE unchanged. Raw strings and row numbers remain in `comparisons.json`. Area and power use `area_um2` and `total_uw` directly. Timing retains `delay_ns` verbatim under `reported_timing_ns`. No timing absolute values, interpolated measurements, missing-value replacement, or power reconstruction are used.

`comparisons.json` records all 95 rows, source SHA-256 hashes, conditions, plot counts, and exclusions. `comparison-import-report.json` identifies unresolved timing and missing data. `comparison-plot-points.csv` traces each plotted point to its source file, row, module, metric, and units. SVG and PNG figures are in `assets/plots/`.

Each plot has `svg`/`png` light variants and `dark_svg`/`dark_png` dark variants. Both are rendered from the same sorted data series and share the same traced points, counts, axes, and units. The website switches the displayed image and download links with its selected theme. Theme changes do not change measurements or ranking.

Each library is sorted independently for each metric. Percentile is `100*rank/(count-1)`, starting at rank zero (zero for a singleton). Counts are 14 LIA versus 31 EvoApprox adders, and 13 LIM versus 36 measured EvoApprox multipliers. `mul8u_TD3` is excluded because its PPA fields are absent. All adder timing values are negative; the physical meaning remains unresolved. EvoApprox verification flags remain source-reported.

`benchmark-methodology.json` records the maintainer's description of the common Yosys/ABC Nangate45 flow and pre-layout OpenSTA analysis within OpenROAD, with identical timing, loading, and switching-activity assumptions across architectures. Its source/hash is preserved in `comparisons.json` and the import report, and it is linked in each benchmark record's provenance. Numeric constraints/activity, exact corner/Liberty file, voltage, temperature, tool versions, and original reports were not supplied, so the shared flow remains maintainer-reported rather than independently reproduced. Do not infer those missing values from the library name or from the papers.

The methodology also records the corrected exhaustive domain counts (262,144 pairs for two 9-bit operands; 65,536 for two 8-bit operands), actual RTL report links, original-study references, and paper-review limits. The 2017 EvoApprox8b study has a different technology context; no original-paper measurements are mixed into the CSV plots.

## Provenance

`provenance.source_files` is an array of real site-relative original report/script paths. Include both the error source and PPA source when applicable. Source files are linked in each row. Use `provenance.notes` to identify which file, sheet, row, field, or log line supports each measurement, the implementation revision, and any conversions or unresolved limitations.

`provenance.error` is required when any error metric is present:

| Key | Required content |
| --- | --- |
| `sign` | Exactly `approximate-exact`. |
| `units` | Exactly `integer-output` (MSE is squared). |
| `pe_unit` | Exactly `fraction`. |
| `domain` | Operand domains, signedness, exact reference, output width, overflow/truncation semantics. |
| `coverage` | Exhaustive, sampled, or application workload. Do not infer exhaustiveness from pair count. |
| `distribution` | Input probability/weighting and sampling seed where relevant. |
| `count` | Positive integer number of evaluated cases. |
| `toolchain` | Evaluator/testbench revision and language/compiler/interpreter versions. |

`provenance.ppa` is required when any PPA metric is present:

| Key | Required content |
| --- | --- |
| `units` | Object `{"area":"um2","power":"uW","delay":"ns"}`. |
| `platform`, `corner` | Actual standard-cell library/process and Liberty corner. |
| `voltage_v`, `temperature_c` | Actual voltage and temperature. |
| `constraints` | Clock period, input/output constraints, load, implementation stage, utilization, etc. |
| `activity` | Switching-activity source and frequency; leakage/dynamic treatment. |
| `toolchain` | Synthesis/physical/timing/power tool versions and script revisions. |
| `area_definition` | Cell area, core area, or exact report definition. |
| `power_definition` | Included power components and estimation stage. |
| `delay_definition` | Actual reported path/delay definition and constraints. |

Unknown *conditions* may use the literal string `not recorded`, which is reported as a limitation. Unknown sign, units, or measurement count cannot be published as known metrics. Omit the affected values or resolve them from their source. An entry with unknown conditions cannot join a reviewed common benchmark group. Group members must share the same kind, width, signedness, and error/PPA conditions. Keep record-specific source paths, parameter values, and conversions outside shared conditions so different circuits can be grouped correctly.

## Build and downloads

From the website root:

```text
python tools/catalog.py validate
python tools/catalog.py build
```

To refresh the supplied comparisons and plots first, install `requirements-plots.txt` and run `python tools/import_comparisons.py`. If regenerating models with `prepare_models.py`, do that before importing comparisons; model preparation replaces the selected family's records. See the root README for the complete validation/build order.

The build preserves original implementation bytes. A single-file implementation links directly to its file. Multi-file implementations get per-component language ZIPs. Each family gets one complete ZIP and available C/Python/RTL ZIPs. Archives contain `MANIFEST.json` with configuration parameters, source paths, and SHA-256 hashes. No archive/link is advertised for an unavailable implementation. ZIPs use fixed timestamps for reproducibility. Old unlinked ZIPs are not automatically deleted.

Top-level `libraries` supplies combined source downloads. Each `adder` or `multiplier` entry maps `c`, `python`, and `rtl` to one real combined file per language, and `support` to an array of README/manifest paths. Family ZIPs contain the corresponding integrated sources and support files in addition to standalone implementations. The download section provides direct combined-file links and language archives separately.

`tools/prepare_models.py` creates standalone/combined models and updates the relevant family after full current validation passes. It keeps arithmetic function bodies intact. The repaired multiplier RTL sources differ from their uploaded copies only in the reserved generate-label rename recorded in `result/validation/rtl-compatibility-fixes.json`.

Both static tables show their default single-LPL benchmark settings when JavaScript is disabled. JavaScript supplies accessible tabs, independent filters, and width/LPL selection; plots and downloads work without it. The embedded data supports opening `index.html` directly without a server. Regenerate the page after any catalog change.

Set `site.url` to the actual public site root URL ending in `/` before publication. The build adds its canonical URL, Open Graph URL, and `sitemap.xml`. Keep the repository URL in `site.repository_url`; never substitute a guessed GitHub account or a placeholder domain.
