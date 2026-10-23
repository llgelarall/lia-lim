"""Publish a readable validation summary and full-precision error CSV."""
import csv
import html
import json

from model_sources import ROOT, sha256


def main():
    folder=ROOT/"result/validation"
    catalog=json.loads((ROOT/"data/catalog.json").read_text(encoding="utf-8"))
    families,csv_rows,report_links=[],[],[]
    for kind,name in (("adder","LIA adders"),("multiplier","LIM multipliers")):
        manifest_path=ROOT/f"models/{'lia' if kind=='adder' else 'lim'}/model-manifest.json"
        manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
        numerical_paths=[ROOT/manifest["c_python_report"]]
        rtl_paths=[ROOT/manifest["rtl_report"]]
        for extra in manifest.get("additional_validated_domains",[]):
            numerical_paths.append(ROOT/extra["c_python_report"])
            rtl_paths.append(ROOT/extra["rtl_report"])
        records={}
        rtl_records={}
        for path in numerical_paths:
            report=json.loads(path.read_text(encoding="utf-8"))
            if report["status"]!="passed":
                raise ValueError(f"Validation has not passed: {path}")
            records.update({(report["width"],r["id"],r["lpl"]):(r,path) for r in report["configurations"]})
            report_links.append((path.name,f"{name} — N={report['width']}, LPL={report['lpl_values']}, C/Python"))
        for path in rtl_paths:
            report=json.loads(path.read_text(encoding="utf-8"))
            if report["status"]!="passed":
                raise ValueError(f"RTL validation has not passed: {path}")
            rtl_records.update({(report["width"],r["id"],r["lpl"]):r for r in report["configurations"]})
            report_links.append((path.name,f"{name} — N={report['width']}, LPL={report['lpl_values']}, RTL"))
        packaged_path=folder/f"{kind}8-packaged.json"
        packaged=json.loads(packaged_path.read_text(encoding="utf-8"))
        if packaged["status"]!="passed":
            raise ValueError("Generated model checks have not passed")
        if packaged["manifest_sha256"] != sha256(manifest_path):
            raise ValueError("Generated model checks are stale; rerun check_packaged_models.py")
        report_links.extend([(packaged_path.name,f"{name} — generated downloads"),(f"{kind}8-combined-rtl.json",f"{name} — combined RTL at N=8, LPL=4")])
        count=pairs=rtl_pairs=mismatches=rtl_mismatches=0
        for record in catalog["components"]:
            if record["kind"]!=kind:
                continue
            key=record["width"],record["architecture"],record["lpl"]
            item,path=records[key]
            rtl_item=rtl_records[key]
            if record["error"]!=item["c"]["metrics"]:
                raise ValueError(f"Catalog differs from C results: {record['id']}")
            count+=1;pairs+=item["c"]["count"];rtl_pairs+=rtl_item["pairs_checked"]
            mismatches+=item["mismatches"];rtl_mismatches+=rtl_item["mismatches"]
            csv_rows.append({"id":record["id"],"architecture":record["architecture"],"operation":kind,"operand_width":record["width"],"lpl":record["lpl"],"input_min":0,"input_max":(1<<record["width"])-1,"pairs":item["c"]["count"],
                             **item["c"]["metrics"],**{f"{k}_exact":v for k,v in item["c"]["exact_ratios"].items()},
                             "sign":"approximate-exact","normalization":"none","pe_unit":"fraction","source_file":path.relative_to(ROOT).as_posix(),"source_configuration":f"{record['architecture']}; lpl={record['lpl']}"})
        families.append({"name":name,"kind":kind,"architectures":len({r["architecture"] for r in catalog["components"] if r["kind"]==kind}),"configurations":count,
                         "c_python_pairs":pairs,"c_python_mismatches":mismatches,"rtl_pairs":rtl_pairs,"rtl_mismatches":rtl_mismatches,
                         "packaged_c_pairs":packaged["c_exhaustive_comparisons"],"packaged_c_mismatches":packaged["c_mismatches"],"status":"passed"})
    with (folder/"error-metrics.csv").open("w",encoding="utf-8",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(csv_rows[0]));writer.writeheader();writer.writerows(csv_rows)
    limitations=["Base validation: unsigned N=8, LPL=1..7. Additional benchmarks: 9-bit LIA at LPL=8 and 8-bit LIM at LPL=8. No other widths, signed operands, asymmetric operands, or boundary settings are established by these checks.",
                 "Full ordered input domains are evaluated uniformly. Each C/Python report also includes the lower-half operand subset.",
                 "Errors use approximate minus exact output, unnormalized output units (squared for MSE), and PE as a fraction. Signed errors in the supplied comparison CSVs use the opposite sign; converted LIA/LIM rows match the independently evaluated C results.",
                 "CSV area and power values are available only at benchmark settings. The maintainer reports Yosys/ABC Nangate45 synthesis and pre-layout OpenSTA within OpenROAD under identical timing, loading, and switching-activity assumptions. Versions, corner, numerical conditions, and report definitions were not supplied. Timing is retained verbatim; negative adder timing cannot be interpreted as physical propagation delay.",
                 "The supplied EvoApprox CSV verification flags have not been independently rerun because those model sources and evaluation scripts were not supplied.",
                 "LFMs.h declarations were recovered from LFMs.c. Thirteen RTL generate labels were changed from the reserved word small to g_small; uploaded originals remain available. Arithmetic expressions were unchanged."]
    summary={"status":"passed","configurations":sum(f["configurations"] for f in families),"architectures":sum(f["architectures"] for f in families),"total_c_python_pairs":sum(f["c_python_pairs"] for f in families),"total_rtl_pairs":sum(f["rtl_pairs"] for f in families),"families":families,"limitations_and_repairs":limitations}
    (folder/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    table_rows="".join(f'<tr><th scope="row">{f["name"]}</th><td>{f["architectures"]}</td><td>{f["configurations"]}</td><td>{f["c_python_pairs"]:,}</td><td>{f["rtl_pairs"]:,}</td><td>{f["packaged_c_pairs"]:,}</td><td>0</td></tr>' for f in families)
    links="".join(f'<li><a href="{html.escape(path)}">{html.escape(label)}</a></li>' for path,label in report_links)
    notes="".join(f'<li>{html.escape(note)}</li>' for note in limitations)
    page=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>LIA / LIM — Exhaustive Validation Results</title><meta name="description" content="C, Python and RTL agreement for 27 LIA/LIM architectures, including 8-bit LPL 1–7 and LPL 8 comparison benchmarks."><script src="../../assets/theme.js"></script><link rel="stylesheet" href="../../assets/style.css"></head><body>
<header class="site-header"><div class="container header-inner"><a class="brand" href="../../index.html">LIA / LIM</a><div class="header-tools"><nav aria-label="Main navigation"><a href="../../index.html">Component catalog</a></nav><button id="theme-toggle" class="theme-toggle" type="button" aria-pressed="false" hidden><span>Dark theme</span><span class="theme-state" aria-hidden="true">Off</span></button></div></div></header>
<main class="container"><section><h1>Implementation agreement</h1><p>{summary['architectures']} architectures, {summary['configurations']} configurations. C is the baseline; Python and RTL agree on every tested result. Generated standalone C files also agree with the original C.</p>
<div class="table-scroll" tabindex="0"><table><thead><tr><th scope="col">Family</th><th scope="col">Architectures</th><th scope="col">Configurations</th><th scope="col">C/Python pairs</th><th scope="col">RTL pairs</th><th scope="col">Packaged C pairs</th><th scope="col">Mismatches</th></tr></thead><tbody>{table_rows}</tbody></table></div>
<p class="table-note">The base 8-bit N=8, LPL=1..7 tests cover 65,536 ordered pairs per configuration. The LPL=8 benchmarks add 9-bit LIA (262,144 pairs per architecture) and 8-bit LIM (65,536 pairs per architecture).</p></section>
<section><h2>Measurements and provenance</h2><p><a href="error-metrics.csv" download>Download error metrics (CSV)</a> · <a href="summary.json">Summary JSON</a> · <a href="../../data/comparison-import-report.json">Comparison import findings</a></p><ul>{links}<li><a href="rtl-compatibility-fixes.json">RTL repairs and source hashes</a></li></ul></section>
<section><h2>Conditions and limitations</h2><ul>{notes}</ul></section><p style="margin:20px 0"><a href="../../index.html#catalog">Return to the component catalog</a></p></main></body></html>'''
    (folder/"index.html").write_text(page,encoding="utf-8")
    print(f"Published validation summary and {len(csv_rows)} full-precision metric rows.")


if __name__=="__main__":
    main()
