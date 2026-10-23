"""Import the supplied comparison CSVs, validate error signs, and plot raw PPA."""
from __future__ import annotations

import copy
import csv
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from model_sources import ROOT, sha256

BENCHMARKS = (
    ("adder", "LIA", 9, "EvoApprox-8+MSB", "9-bit LIA, LPL=8 vs. EvoApprox 8-bit + MSB"),
    ("multiplier", "LIM", 8, "EvoApprox", "8-bit LIM, LPL=8 vs. EvoApprox 8-bit"),
)
METRICS = {"area": ("area_um2", "Area (µm²)", "um2"),
           "power": ("total_uw", "Power (µW)", "uW"),
           "timing": ("delay_ns", "Reported timing (ns)", "ns")}


def numeric(value):
    if value is None or not str(value).strip():
        return None
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"Nonfinite source value: {value}")
    return number


def normalized_errors(row):
    # Independently established below against the original C outputs.
    return {"me": -float(row["ME"]), "mse": float(row["MSE"]),
            "mae": float(row["MAE"]), "pe": float(row["PE"]),
            "max": -float(row["MIN"]), "min": -float(row["MAX"])}


def validate_row(row, width):
    """Check source arithmetic relationships without assuming model correctness."""
    metrics = {key: numeric(row[key]) for key in ("ME", "MSE", "MAE", "PE", "MIN", "MAX", "MAX_ABS")}
    if any(value is None for value in metrics.values()):
        raise ValueError("Missing source error measurement")
    if int(row["vectors"]) != 1 << (2 * width):
        raise ValueError("CSV vector count differs from the stated operand domain")
    if not 0 <= metrics["PE"] <= 1 or metrics["MSE"] < 0 or metrics["MAE"] < 0:
        raise ValueError("Invalid error probability or nonnegative error metric")
    if metrics["MIN"] > metrics["MAX"] or not metrics["MIN"] <= metrics["ME"] <= metrics["MAX"]:
        raise ValueError("Inconsistent signed error bounds")
    if not math.isclose(metrics["MAX_ABS"], max(abs(metrics["MIN"]), abs(metrics["MAX"])), rel_tol=1e-10, abs_tol=1e-10):
        raise ValueError("MAX_ABS disagrees with signed extrema")
    if metrics["MAE"] + 1e-9 < abs(metrics["ME"]) or metrics["MSE"] + 1e-8 < metrics["MAE"] ** 2:
        raise ValueError("Inconsistent error moments")
    if not math.isclose(metrics["PE"] * 100, numeric(row["PE_percent"]), abs_tol=1e-8):
        raise ValueError("PE fraction and percentage disagree")


def plot(benchmark, metric, output_folder):
    column, label, unit = METRICS[metric]
    points, counts, exclusions, series = [], {}, [], []
    for library in (benchmark["library"], benchmark["reference_library"]):
        candidates = [r for r in benchmark["rows"] if r["library"] == library]
        included = sorted((r for r in candidates if r["values"][metric] is not None), key=lambda r: (r["values"][metric], r["module"]))
        counts[library] = len(included)
        for row in candidates:
            if row["values"][metric] is None:
                exclusions.append({"module": row["module"], "library": library,
                                   "source_row": row["source_row"], "reason": f"Missing {column}"})
        xs = [100*i/(len(included)-1) if len(included)>1 else 0 for i in range(len(included))]
        ys = [row["values"][metric] for row in included]
        series.append((library,xs,ys))
        for rank, (percentile, row) in enumerate(zip(xs, included)):
            points.append({"metric": metric, "source_column": column, "unit": unit,
                           "library": library, "module": row["module"], "rank": rank,
                           "percentile": percentile, "value": row["values"][metric],
                           "source_file": benchmark["source_file"], "source_row": row["source_row"]})
    stem=f'{benchmark["kind"]}-{metric}'
    result={"counts": counts, "exclusions": exclusions, "source_column": column,
            "units": unit, "points": points}
    base={"font.family":"sans-serif", "font.sans-serif":["DejaVu Sans","Arial","Helvetica","sans-serif"],
          "font.size":8,"axes.titlesize":10,"axes.labelsize":8,"legend.fontsize":7,"svg.fonttype":"none",
          "figure.facecolor":"#fbfcfd","axes.facecolor":"#ffffff","savefig.facecolor":"#fbfcfd",
          "text.color":"#18242c","axes.labelcolor":"#18242c","xtick.color":"#66747d",
          "ytick.color":"#66747d","axes.edgecolor":"#66747d","grid.color":"#b9cedd",
          "legend.facecolor":"#ffffff","legend.edgecolor":"#b9cedd"}
    dark={"figure.facecolor":"#151817","axes.facecolor":"#202523","savefig.facecolor":"#151817",
          "text.color":"#eef2ef","axes.labelcolor":"#eef2ef","xtick.color":"#aeb8b2",
          "ytick.color":"#aeb8b2","axes.edgecolor":"#83aaa5","grid.color":"#4b625f",
          "legend.facecolor":"#202523","legend.edgecolor":"#4b625f"}
    for theme,style,colors in (("light",{},("#537f9a","#725b16")),("dark",dark,("#83aaa5","#e2cd91"))):
        with plt.rc_context({**base,**style}):
            fig,axis=plt.subplots(figsize=(4.3,3.0),layout="constrained")
            for (library,xs,ys),color in zip(series,colors):
                axis.plot(xs,ys,marker="o",markersize=2.8,linewidth=1.5,color=color,label=f"{library} (n={len(ys)})")
            axis.set_title(label)
            axis.set_xlabel("Within-library percentile, sorted by value")
            axis.set_ylabel(label)
            axis.set_xlim(-3,103)
            axis.set_xticks([0,25,50,75,100])
            axis.grid(True,alpha=.25)
            axis.legend(loc="best",framealpha=.9)
            suffix="-dark" if theme=="dark" else ""
            for fmt in ("svg","png"):
                path=output_folder/f"{stem}{suffix}.{fmt}"
                fig.savefig(path,**({"metadata":{"Date":None}} if fmt=="svg" else {"dpi":180}))
                result[("dark_" if theme=="dark" else "")+fmt]=path.relative_to(ROOT).as_posix()
            plt.close(fig)
    return result


def main():
    catalog_path=ROOT/"data/catalog.json"
    catalog=json.loads(catalog_path.read_text(encoding="utf-8"))
    methodology_path=ROOT/"data/benchmark-methodology.json"
    methodology=json.loads(methodology_path.read_text(encoding="utf-8"))
    flow=methodology["flow"]
    # Repeated imports replace only this importer’s benchmark rows.
    catalog["components"]=[r for r in catalog["components"] if not r.get("source_comparison")]
    for record in catalog["components"]:
        record["provenance"]["notes"]=[note.replace("No PPA reports supplied. Parameterized templates are available; only N=8, LPL=1..7 are characterized here.","No PPA report was supplied for this width/LPL. Base error characterization covers N=8, LPL=1..7; other domains require their own validation reports.") for note in record["provenance"].get("notes",[])]
    originals={r["architecture"]:r for r in catalog["components"]}
    dataset={"benchmarks":[], "issues":[], "method": "Each library is sorted independently for each metric; percentile=100*rank/(n-1), with rank starting at zero. No interpolation, absolute-value conversion, or missing-value imputation."}
    dataset.update(methodology_source=methodology_path.relative_to(ROOT).as_posix(),methodology_sha256=sha256(methodology_path))
    figures=ROOT/"assets/plots"
    figures.mkdir(parents=True,exist_ok=True)
    all_points=[]
    for kind, library, width, reference, description in BENCHMARKS:
        source=ROOT/f"assets/excels/{library}_final_comparison.csv"
        validation_path=ROOT/f"result/validation/{kind}{width}-lpl8-c-python.json"
        rtl_path=ROOT/f"result/validation/{kind}{width}-lpl8-rtl.json"
        validation=json.loads(validation_path.read_text(encoding="utf-8"))
        rtl=json.loads(rtl_path.read_text(encoding="utf-8"))
        if validation["status"]!="passed" or rtl["status"]!="passed":
            raise ValueError("Benchmark model checks must pass before importing measurements")
        domain=next(d for d in methodology["verified_functional_domains"] if d["family"]==library)
        if domain["operand_bits"]!=width or domain["lpl"]!=8 or domain["ordered_pairs_per_architecture"]!=1<<(2*width):
            raise ValueError("Methodology input count does not match the operand width")
        if domain["report"]!=rtl_path.relative_to(ROOT).as_posix() or rtl["width"]!=width or any(r["pairs_checked"]!=domain["ordered_pairs_per_architecture"] or r["mismatches"]!=0 for r in rtl["configurations"]):
            raise ValueError("Methodology verification claim differs from the saved RTL results")
        canonical={r["id"]:r["c"]["metrics"] for r in validation["configurations"]}
        with source.open(encoding="utf-8-sig",newline="") as stream:
            raw=list(csv.DictReader(stream))
        benchmark={"id":f"{kind}-n{width}-lpl8", "kind":kind, "library":library,
                   "reference_library":reference, "operand_width":width, "lpl":8,
                   "description":description, "source_file":source.relative_to(ROOT).as_posix(),
                   "source_sha256":sha256(source), "error_sign_in_source":"exact-approximate (established by exhaustive original C comparison for LIA/LIM rows)",
                   "conditions":{"source":dataset["methodology_source"],
                                 "toolchain":"Yosys with ABC technology mapping; OpenSTA within OpenROAD, as reported by the maintainer; tool versions not supplied",
                                 "standard_cell_library":flow["standard_cell_library"],"stage":flow["stage"],
                                 "common_assumptions":flow["common_assumptions"],
                                 "unrecorded_details":flow["unrecorded_details"],
                                 "timing_definition":"not recorded; delay_ns retained as reported timing, without conversion to physical propagation delay"},
                   "functional_validation":domain, "rows":[], "plots":{}}
        seen=set()
        for source_row,row in enumerate(raw,2):
            if row["module"] in seen:
                raise ValueError(f"Duplicate module in {source}: {row['module']}")
            seen.add(row["module"])
            if row["library"] not in (library,reference):
                raise ValueError(f"Unexpected library in {source}: {row['library']}")
            values={metric:numeric(row[column]) for metric,(column,_,_) in METRICS.items()}
            if any(values[k] is not None and values[k]<0 for k in ("area","power")):
                raise ValueError("Area/power cannot be negative")
            benchmark["rows"].append({"library":row["library"],"module":row["module"],"source_row":source_row,"values":values,"raw":row})
            if values["timing"] is not None and values["timing"]<0:
                dataset["issues"].append({"source_file":benchmark["source_file"],"row":source_row,"module":row["module"],"field":"delay_ns","value":values["timing"],"issue":"Negative reported timing; cannot be treated as a physical propagation delay without the underlying timing report."})
            if row["PPA_status"]!="OK" or any(v is None for v in values.values()):
                dataset["issues"].append({"source_file":benchmark["source_file"],"row":source_row,"module":row["module"],"issue":"Missing or incomplete PPA report; omit absent values from plots."})
            validate_row(row,width)
            if row["library"]!=library:
                continue
            converted=normalized_errors(row)
            if any(not math.isclose(converted[k],canonical[row["module"]][k],rel_tol=1e-10,abs_tol=1e-10) for k in converted):
                raise ValueError(f"CSV/C metric mismatch: {library} {row['module']}")
            if int(row["vectors"])!=1<<(2*width):
                raise ValueError("CSV vector count differs from the independently tested domain")
            record=copy.deepcopy(originals[row["module"]])
            record.update(id=f'{row["module"]}-u{width}-lpl8',width=width,lpl=8,
                          source_comparison=benchmark["id"], error=canonical[row["module"]],
                          ppa={"area":values["area"],"power":values["power"],"delay":None},
                          reported_timing_ns=values["timing"])
            record["parameters"].update(N=width,LPL=8,output_bits=width+1 if kind=="adder" else 2*width)
            record["provenance"]["source_files"] += [benchmark["source_file"],dataset["methodology_source"],validation_path.relative_to(ROOT).as_posix(),rtl_path.relative_to(ROOT).as_posix()]
            record["provenance"]["error"]={"sign":"approximate-exact","units":"integer-output","pe_unit":"fraction","domain":{"a":[0,(1<<width)-1],"b":[0,(1<<width)-1],"signed":False,"exact_reference":"a+b" if kind=="adder" else "a*b","output_bits":width+1 if kind=="adder" else 2*width},"coverage":"exhaustive ordered pairs","distribution":"uniform; one equal weight per ordered input pair","count":1<<(2*width),"toolchain":validation["toolchain"]}
            record["provenance"]["ppa"]={"units":{"area":"um2","power":"uW","delay":"ns"},"platform":"Nangate45 standard-cell library (maintainer-reported)","corner":"not recorded","voltage_v":"not recorded","temperature_c":"not recorded","constraints":"Identical timing and loading assumptions across architectures (maintainer-reported); numerical constraints and loads not supplied","activity":"Identical switching-activity assumptions across architectures (maintainer-reported); activity values, source, and operating frequency not supplied","toolchain":"Yosys with ABC technology mapping; OpenSTA within OpenROAD; pre-layout (maintainer-reported); versions not recorded","area_definition":"source column area_um2; exact report field not supplied","power_definition":"pre-layout OpenSTA/OpenROAD power (maintainer-reported); source total_uw; underlying component reports unavailable","delay_definition":"pre-layout OpenSTA/OpenROAD timing (maintainer-reported); path/slack definition not supplied; delay_ns retained separately and canonical physical delay is null"}
            record["provenance"]["notes"]=[f"{benchmark['source_file']}, CSV row {source_row}, module={row['module']}. {description}.","CSV signed errors use exact-approximate; ME is negated and extrema converted as min=-source MAX, max=-source MIN. MSE/MAE/PE unchanged. Converted values agree with exhaustive C outputs; Python and RTL agree too.","CSV area_um2 and total_uw are retained as reported. delay_ns is displayed separately as reported timing. Negative values are not converted to absolute values or physical delay.","The maintainer reports a common Yosys/ABC Nangate45 synthesis flow and pre-layout OpenSTA within OpenROAD, with identical timing, loading, and switching-activity assumptions. See data/benchmark-methodology.json. Numerical settings, versions, and original reports were not supplied, so this flow was not independently reproduced. Source PPA_status and verification flags remain in data/comparisons.json."]
            catalog["components"].append(record)
        for metric in METRICS:
            result=plot(benchmark,metric,figures)
            all_points.extend(result.pop("points"))
            benchmark["plots"][metric]=result
        dataset["benchmarks"].append(benchmark)
        # Document the newly checked runtime parameters in the shared downloads.
        family="lia" if kind=="adder" else "lim"
        readme=ROOT/f"models/{family}/README.md"
        text=readme.read_text(encoding="utf-8")
        text=text.split("\n## Additional benchmark validation\n",1)[0]
        text=text.replace("Only N=8 and LPL=1..7 are published as validated configurations here. Other template widths/levels have not been established by this validation.","Base validation covers N=8 and LPL=1..7. Additional benchmark validation is recorded below; other settings remain unverified.")
        text=text.replace("No measured area, power, or delay is supplied with these models.","Hardware measurement availability is specific to each configuration; see the catalog provenance.")
        text+=f"\n## Additional benchmark validation\n\nUnsigned N={width}, LPL=8 also passed exhaustive original C/Python/RTL agreement: {1<<(2*width):,} ordered input pairs per architecture. Reports: `{validation_path.relative_to(ROOT).as_posix()}` and `{rtl_path.relative_to(ROOT).as_posix()}`. The parameterized arithmetic implementations are unchanged. Area and power are imported from `{benchmark['source_file']}`; reported timing has no confirmed propagation-delay definition.\n"
        readme.write_text(text,encoding="utf-8",newline="\n")
        manifest_path=ROOT/f"models/{family}/model-manifest.json"
        manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["additional_validated_domains"]=[{"width":width,"lpl":[8],"pairs_per_architecture":1<<(2*width),"c_python_report":validation_path.relative_to(ROOT).as_posix(),"rtl_report":rtl_path.relative_to(ROOT).as_posix()}]
        manifest["generated_sha256"][readme.relative_to(ROOT).as_posix()]=sha256(readme)
        manifest_path.write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    dataset["limitations"]=["The common Yosys/ABC Nangate45 and pre-layout OpenSTA/OpenROAD flow, including identical timing/loading/activity assumptions, is maintainer-reported. Scripts, tool versions, exact corner, voltage, temperature, and numerical constraints/activity were not supplied.","Negative adder timing values are plotted verbatim and identified as unresolved reported timing, rather than physical propagation delay.","EvoApprox model code and timing/power reports were not supplied here; its CSV verification flags are source-reported and have not been independently rerun.","Power curves use reported total_uw, without reconstructing totals from rounded components.","Original-paper synthesis results are separate characterization contexts; no paper measurements were substituted into these CSV plots."]
    (ROOT/"data/comparisons.json").write_text(json.dumps(dataset,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    catalog_path.write_text(json.dumps(catalog,indent=2)+"\n",encoding="utf-8")
    with (ROOT/"data/comparison-plot-points.csv").open("w",encoding="utf-8",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(all_points[0]))
        writer.writeheader();writer.writerows(all_points)
    checked=sum(bool(r.get("source_comparison")) for r in catalog["components"])
    total_rows=sum(len(b["rows"]) for b in dataset["benchmarks"])
    report={"source_files":{b["source_file"]:b["source_sha256"] for b in dataset["benchmarks"]},"source_rows_checked":total_rows,"canonical_error_conversions_verified":checked,"benchmark_rows_added":checked,"plot_count":6,"issues":dataset["issues"],"limitations":dataset["limitations"]}
    report["source_files"][dataset["methodology_source"]]=dataset["methodology_sha256"]
    (ROOT/"data/comparison-import-report.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(f"Imported {total_rows} CSV rows; added {checked} independently checked LPL=8 configurations; generated six plots and {len(all_points)} traceable plot points.")


if __name__=="__main__":
    main()
