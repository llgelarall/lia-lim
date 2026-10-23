# LIA / LIM: approximate adders and multipliers

A static research reference website developed by [Gelara](https://gisink.com/) for LIA imprecise adders and LIM imprecise multipliers, with a compact layout inspired by [EvoApproxLib](https://ehw.fit.vutbr.cz/evoapproxlib/). The original architectures and C libraries are attributed to their authors in the ICVLSI research group at Shahid Beheshti University, Tehran, Iran. Open `index.html` directly or serve this directory. No JavaScript framework, external font, or runtime build is required.

The navbar carries the project name. A plain attribution note distinguishes the original libraries from this website, while the footer links to Gelara's [personal page](https://gisink.com/) and [GitHub profile](https://github.com/llgelarall). Neither the group nor the developer is highlighted in bold branding. The colors follow the light blue-gray and charcoal-green palettes of the personal page.

A dark-theme toggle follows the operating-system preference initially and remembers an explicit choice in browser storage. Tables, controls, objective badges, validation reports, and all six plots support both themes. Plot downloads follow the selected theme. Without JavaScript, the system theme and static plots still work through CSS and picture sources. Printing uses the light palette.

## Included and validated

The uploaded C, Python notebooks, and Verilog RTL contain 14 LIA architectures and 13 LIM architectures. Separate adder and multiplier tabs show one width and LPL at a time, with model downloads above each table and metric definitions in its footnotes. Features, use cases, and attribution appear after the introduction.

The catalog contains 216 independently verified configurations: unsigned 8-bit operands at LPL 1 through 7 for both families, plus 9-bit LIA at LPL=8 and 8-bit LIM at LPL=8. Python and RTL match the original C baseline for every tested output: **16,908,288 comparisons per representation, zero mismatches**. The 8-bit reports also include the complete 0–127 operand subset.

The four feature summaries describe configurable imprecision, the narrower observed area/power ranges relative to the supplied EvoApprox sets, stable mean-error targets in selected designs, and studies of individual error criteria and Pareto trade-offs. The physical-cost observation is specific to the supplied benchmarks and does not establish identical PPA. LOA (`lia_05`) has ME=-0.25 using the source's `exact - approximate` convention, or +0.25 using the table's convention, under uniform exhaustive inputs at the validated settings. This is a mean-bias property; other errors can vary with LPL or workload. The supplied 8-bit multiplier implementations support LPL=1..8; eight is not their minimum.

Each component has a badge rotated -90 degrees before its name, with 12 px bold lettering and stronger text/background contrast. ME, MAE, MSE, and PE targets come from complete criterion tokens in the original C function name, rather than from a numerical ranking. The joint MAE/PE adder displays both badges. The original function suffix appears below the component ID, with the full name in its tooltip and provenance. These labels record design intent and do not assert universal minima or Pareto optimality.

ME, MSE, MAE, PE, and signed maximum/minimum error are measured from the C outputs using `approximate - exact`, uniform input weighting, no normalization, and PE as a fraction. Exact rational aggregates and full-precision values are preserved in the reports and CSV. No arithmetic algorithms were changed.

Only the domains listed above are established by these checks. Template parameterization does not establish correctness at other widths or LPL values.

The supplied `assets/excels/LIA_final_comparison.csv` and `LIM_final_comparison.csv` provide area, total power, and reported timing at the additional LPL=8 settings. Their signed errors use `exact - approximate`; after reversing ME and swapping/negating extrema, all 27 LIA/LIM rows agree with the exhaustive C baseline. The original CSV values are preserved. Physical delay remains null: timing-path definitions were not supplied and every adder timing value is negative. No absolute-value conversion is applied.

Six small, downloadable SVG/PNG line plots compare the supplied libraries. Values are sorted independently within each library against percentile 0–100, following the supplied plot examples. The adder benchmark compares 9-bit LIA at LPL=8 (14 circuits) with 8-bit EvoApprox adders extended by an MSB (31 circuits). The multiplier benchmark compares 8-bit LIM at LPL=8 (13 circuits) with 8-bit EvoApprox multipliers (36 measured circuits); `mul8u_TD3` has no PPA report and is omitted. Counts come from these CSVs. EvoApprox verification flags are source-reported and have not been independently rerun here.

The maintainer reports a common synthesis and characterization flow for all comparison architectures: Yosys with ABC technology mapping to the Nangate45 standard-cell library, followed by pre-layout timing and power evaluation using OpenSTA within OpenROAD under identical timing, loading, and switching-activity assumptions. [Methodology provenance](data/benchmark-methodology.json) records this statement separately from the CSV measurements. Tool versions, the exact Liberty corner, voltage/temperature, numerical constraints/activity, and original analysis reports remain unavailable; the flow was not independently rerun here.

The validation description uses the saved report counts: two unsigned 9-bit operands require 262,144 ordered pairs per LIA architecture; two unsigned 8-bit operands require 65,536 per LIM architecture.

See [the readable validation report](result/validation/index.html), [summary JSON](result/validation/summary.json), and [error metrics CSV](result/validation/error-metrics.csv).

## Download structure

- Each component table row links to a self-contained C file, a self-contained Python file, and its individual RTL module. Parameters recorded in the row apply to all three.
- `models/lia/` and `models/lim/` contain separate `c/` and `python/` files, one combined `.c`, `.py`, and `.v` per family, usage instructions, and a source/hash manifest.
- `downloads/all-adders.zip` and `downloads/all-multipliers.zip` contain complete families, including the standalone and combined forms. Per-language family ZIPs are also provided.
- Family download sections additionally link directly to each combined source file, so all C functions, Python functions, or RTL modules can be obtained as a single file.

Standalone Python modules expose `compute(...)` and the original class method. Combined Python modules provide a `COMPONENTS` registry keyed by RTL module ID. Standalone C functions retain their original names; shared helpers use internal linkage. Combined RTL concatenates the modules; select the desired module as top. Use either standalone or combined forms in a build to avoid duplicate definitions.

The missing `assets/codes/LFMs.h` was reconstructed from the actual C function declarations. Multiplier RTL used the reserved word `small` as a generate label; the label was renamed to `g_small` in 13 files. Uploaded copies are retained under `assets/codes/original/LIM/`, with hashes and the exact repair in [the compatibility report](result/validation/rtl-compatibility-fixes.json). The combined and standalone multiplier C downloads omit the declaration-only local header include so they are self-contained. No arithmetic expressions changed. The CPython wrapper file is not a dependency of the distributed pure Python models.

## Reproduce the checks

Requirements: Python 3 and GCC on PATH. From this directory:

```text
python tools/validate_models.py --kind adder --width 8 --lpl 1 2 3 4 5 6 7
python tools/validate_models.py --kind multiplier --width 8 --lpl 1 2 3 4 5 6 7
python tools/validate_models.py --kind adder --width 9 --lpl 8 --output result/validation/adder9-lpl8-c-python.json
python tools/validate_models.py --kind multiplier --width 8 --lpl 8 --output result/validation/multiplier8-lpl8-c-python.json
```

The evaluator compiles the original C, executes every input pair, and compares each Python output, integer aggregate, and error metric. It records source hashes, compiler flags and diagnostics, compiler target, and Python version. Validation here used MinGW GCC 6.3.0 and Python 3.12.8. C warnings are retained in the reports.

RTL validation additionally requires Icarus Verilog on PATH:

```text
python tools/validate_rtl.py --kind adder --simulator iverilog
python tools/validate_rtl.py --kind multiplier --simulator iverilog
```

For this workspace, the actual checks used the installed ModelSim SE-64 2020.4:

```text
python tools/validate_rtl.py --kind adder --simulator modelsim --tool-dir "C:/modeltech64_2020.4/win64"
python tools/validate_rtl.py --kind multiplier --simulator modelsim --tool-dir "C:/modeltech64_2020.4/win64"
```

Replace the tool directory for another installation. The testbench evaluates all ordered pairs across every requested architecture/LPL combination and checks outputs against the already validated Python models. Error reports alone do not prove every RTL output; the saved RTL reports contain separate per-configuration comparison counts.

For the additional benchmark domains, use the matching C/Python reference report:

```text
python tools/validate_rtl.py --kind adder --width 9 --lpl 8 --reference-report result/validation/adder9-lpl8-c-python.json --simulator modelsim --tool-dir "C:/modeltech64_2020.4/win64" --output result/validation/adder9-lpl8-rtl.json
python tools/validate_rtl.py --kind multiplier --width 8 --lpl 8 --reference-report result/validation/multiplier8-lpl8-c-python.json --simulator modelsim --tool-dir "C:/modeltech64_2020.4/win64" --output result/validation/multiplier8-lpl8-rtl.json
```

Regenerate model files and verify the generated C extractions:

```text
python -m pip install -r requirements-plots.txt
python tools/prepare_models.py --kind adder
python tools/prepare_models.py --kind multiplier
python tools/import_comparisons.py
python tools/check_packaged_models.py --kind adder
python tools/check_packaged_models.py --kind multiplier
python tools/catalog.py build
python tools/summarize_validation.py
```

Preparation refuses stale, failing, or incomplete C/Python results. Standalone Python method ASTs are checked against the notebook; generated C files compile independently. Packaged C files are then exhaustively compared to the original combined C; Python standalone and combined APIs are also checked on boundary and patterned inputs. The ZIP builder preserves model bytes and includes source/configuration manifests with SHA-256 hashes.

Import comparisons after preparing models: preparation replaces that family's catalog records; import restores the additional verified domains, source measurements, and plots. Matplotlib is required only for rebuilding plots. The site itself works offline with no external dependencies.

Combined RTL files were additionally compiled and exhaustively simulated at LPL=4 across all input pairs. Those reports are separate from the full LPL=1..7 individual-module checks. To reproduce them with the installed ModelSim, add `--combined models/lia/lia_all.v --lpl 4 --output result/validation/adder8-combined-rtl.json` (or the corresponding multiplier paths) to the RTL command.

## Select by error and hardware constraints

```text
python tools/catalog.py select --kind adder --width 8 --lpl 4 --max-mae 2
python tools/catalog.py select --kind multiplier --width 8 --lpl 4 --max-abs-me 0.5
```

The tables support the same constraints. Other CLI options include `--max-mse`, `--max-pe`, `--max-abs-error`, `--max-area-um2`, `--max-power-uw`, `--max-delay-ns`, and `--benchmark-group`. These select existing measured configurations; they do not synthesize new hardware. Unknown measurements cannot satisfy a numerical limit. Area and power constraints can use the supplied LPL=8 measurements. Raw reported timing cannot satisfy physical-delay constraints.

```text
python tools/catalog.py select --kind adder --width 9 --lpl 8 --max-mae 50 --max-area-um2 20 --max-power-uw 5
```

Reproducing or customizing PPA requires the exact Liberty file/corner, numerical constraints and switching activity, tool versions, and synthesis/analysis scripts. The named Nangate45/Yosys/ABC/OpenSTA/OpenROAD flow and common assumptions were supplied by the maintainer, but these detailed inputs were not; a complete command sequence for that flow cannot yet be provided. The page identifies this limitation alongside the measurements.

To evaluate a custom workload, run the chosen model and exact reference on identical inputs, export CSV columns `exact,approximate`, and run:

```text
python tools/measure_errors.py --input path/to/output-pairs.csv --output path/to/error.json
```

## Data and GitHub Pages

`data/catalog.json` contains verified configuration metadata, numerical error values, implementation paths, and provenance. See [the data contract](data/README.md). Rebuild the static tables and ZIPs after changes. `data/validation-report.json` records missing PPA and provenance conditions. `data/comparisons.json` preserves all 95 source rows and raw strings; `data/comparison-plot-points.csv` records each plotted value, rank, percentile, source file, and row. `data/comparison-import-report.json` records the negative timing values, missing report, and characterization limitations. These raw distribution plots do not establish a matched-flow performance ranking.

The site uses relative links, static crawlable table rows, semantic HTML, descriptive metadata, and visible approximate/imprecise arithmetic terminology. Set the actual public site root URL, ending in `/`, as `site.url`, and the real repository URL as `site.repository_url`. Rebuild to generate the canonical URL, Open Graph URL, and sitemap. `.nojekyll` supports direct GitHub Pages hosting. No remote deployment or repository push has been performed.

See [PUBLISHING.md](PUBLISHING.md) for the repository creation, Windows Git commands, GitHub Pages settings, and final URL configuration.

Routine tooling checks:

```text
python -m unittest discover -s tools -p "test_*.py"
node --check assets/app.js
python tools/catalog.py validate
```

Original paper: [A Comprehensive Model for Efficient Design Space Exploration of Imprecise Computational Blocks](https://doi.org/10.1145/3625555). Cite the architecture, implementation release, and measurement sources that you actually use.

For original published characterization, also consult [EvoApprox8b (DATE 2017)](https://doi.org/10.23919/DATE.2017.7926993), its [author-hosted PDF](https://www.fit.vut.cz/research/result-file/c134714/279697/paper.pdf), and [EvoApproxLib (WOSET 2019)](https://woset-workshop.github.io/PDFs/2019/a10.pdf). The original 2017 paper uses a TSMC 180 nm context, distinct from this comparison's Nangate45 flow. Both EvoApprox papers were accessible; the LIA/LIM publisher full text was not accessible during review, so no paper-specific synthesis details were transcribed. The plots retain the supplied CSV values.

The original C libraries were developed by the authors in the ICVLSI research group at Shahid Beheshti University, Tehran, Iran. Gelara is a group member, not an author of the original paper, and developed this website, the other implementation versions, validation, and Yosys/OpenROAD synthesis information and comparisons. This website is an independent project; the original-library credit does not identify it as the group's official website.
