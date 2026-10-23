"""Create standalone/combined downloads only after original C/Python checks pass."""
from __future__ import annotations

import argparse
import ast
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import textwrap

from model_sources import ROOT, SOURCES, architectures, c_functions, notebook_source, sha256


def write(path, content):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(content,encoding="utf-8",newline="\n")


def prepare(kind, compiler):
    report_path = ROOT/f"result/validation/{kind}8-c-python.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    if report["status"]!="passed" or any(c["status"]!="passed" for c in report["configurations"]):
        raise ValueError(f"{kind}: original C/Python validation has not passed")
    if report.get("width")!=8 or set(report.get("lpl_values",[]))!=set(range(1,8)):
        raise ValueError("Publishing requires the full unsigned 8-bit LPL 1..7 validation")
    if sha256(ROOT/report["baseline"])!=report["baseline_sha256"] or sha256(ROOT/report["python_source"])!=report["python_source_sha256"]:
        raise ValueError("Uploaded model changed since validation; rerun the exhaustive checks")
    rtl_report_path = ROOT/f"result/validation/{kind}8-rtl.json"
    rtl_report = json.loads(rtl_report_path.read_text(encoding="utf-8")) if rtl_report_path.is_file() else None
    if rtl_report and (rtl_report["status"]!="passed" or rtl_report["reference_report_sha256"]!=sha256(report_path)):
        raise ValueError("RTL validation failed or is stale")
    if rtl_report and any(sha256(ROOT/p)!=digest for p,digest in rtl_report["rtl_sources"].items()):
        raise ValueError("RTL changed since validation")
    family = "lia" if kind=="adder" else "lim"
    class_name = "LIAComponents" if kind=="adder" else "LIMComponents"
    destination = ROOT/f"models/{family}"
    items = architectures(kind)
    expected={(item["id"],lpl) for item in items for lpl in range(1,8)}
    actual={(entry["id"],entry["lpl"]) for entry in report["configurations"]}
    if actual!=expected or len(actual)!=len(report["configurations"]):
        raise ValueError("Incomplete or duplicated C/Python configuration coverage")
    source, cls = notebook_source(kind)
    tree = ast.parse(source)
    class_node = next(n for n in tree.body if isinstance(n,ast.ClassDef))
    lines = source.splitlines(keepends=True)
    methods = {n.name: n for n in class_node.body if isinstance(n,ast.FunctionDef)}
    architecture_names = {item["function"] for item in items}
    helper_names = [name for name in methods if name not in architecture_names]
    c_source = (ROOT/report["baseline"]).read_text(encoding="utf-8-sig")
    functions = c_functions(c_source)
    missing = architecture_names-functions.keys()
    if missing:
        raise ValueError(f"C function definitions missing: {sorted(missing)}")
    c_preamble = c_source
    for start,end,_ in sorted(functions.values(),reverse=True):
        c_preamble = c_preamble[:start]+c_preamble[end:]
    # The original multiplier header only declares these functions. Standalone
    # and single-file downloads carry their definitions and need no local include.
    c_preamble = re.sub(r'^\s*#include\s+"LFMs\.h"[^\n]*\n', '', c_preamble, flags=re.M)
    c_helpers = ["static "+body for name,(_,_,body) in functions.items() if name not in architecture_names]
    source_hashes = {report["baseline"]:report["baseline_sha256"],report["python_source"]:report["python_source_sha256"]}
    if kind=="multiplier":
        source_hashes["assets/codes/LFMs.h"]=sha256(SOURCES/"LFMs.h")
    outputs = []
    implementations = {}
    for item in items:
        ident, name = item["id"],item["function"]
        selected = helper_names+[name]
        methods_text = "\n\n".join("".join(lines[methods[n].lineno-1:methods[n].end_lineno]) for n in selected)
        python_path = destination/f"python/{ident}.py"
        call = "compute(a,b,8,lpl)" if kind=="adder" else "compute(a,b,8,8,lpl)"
        write(python_path,f'"""{ident}: extracted without arithmetic changes from {report["python_source"]}.\nValidated domain: unsigned N=8, LPL=1..7.\nCall {call}.\n"""\nimport sys\n\nclass {class_name}:\n{methods_text}\n\n{name} = {class_name}.{name}\ncompute = {name}\n')
        c_path = destination/f"c/{ident}.c"
        write(c_path,f'/* {ident}: standalone extraction from {report["baseline"]}.\n * Arithmetic function bodies preserved; private helpers have internal linkage.\n * Validated domain: unsigned N=8, LPL=1..7. Link with -lm.\n */\n'+c_preamble+"\n\n"+"\n\n".join(c_helpers)+"\n\n"+functions[name][2]+"\n")
        # A standalone file must retain the original function AST and compile independently.
        extracted = ast.parse(python_path.read_text(encoding="utf-8"))
        generated_class = next(n for n in extracted.body if isinstance(n,ast.ClassDef))
        for node in generated_class.body:
            if isinstance(node,ast.FunctionDef) and ast.dump(node,include_attributes=False)!=ast.dump(methods[node.name],include_attributes=False):
                raise ValueError(f"Python extraction changed function {node.name}")
        checked = subprocess.run([compiler,"-std=c99","-fsyntax-only",str(c_path)],capture_output=True,text=True)
        if checked.returncode:
            raise ValueError(f"Standalone C compile failed: {ident}\n{checked.stderr}")
        ns={}
        exec(compile(python_path.read_text(encoding="utf-8"),str(python_path),"exec"),ns)
        for lpl in range(1,8):
            for a,b in ((0,0),(0,255),(255,0),(255,255),(127,128),(85,170)):
                args=(a,b,8,lpl) if kind=="adder" else (a,b,8,8,lpl)
                if ns["compute"](*args)!=getattr(cls,name)(*args):
                    raise ValueError(f"Standalone Python smoke check failed: {ident}")
        outputs.extend([c_path,python_path])
        source_hashes[item["rtl"]]=sha256(ROOT/item["rtl"])
        implementations[ident]={"c":[c_path.relative_to(ROOT).as_posix()],"python":[python_path.relative_to(ROOT).as_posix()],"rtl":[item["rtl"]]}
    all_c=destination/f"{family}_all.c"
    all_py=destination/f"{family}_all.py"
    all_rtl=destination/f"{family}_all.v"
    combined_bytes=(ROOT/report["baseline"]).read_bytes()
    if kind=="multiplier":
        combined_bytes=re.sub(rb'^#include[ \t]+"LFMs\.h"[^\r\n]*\r?\n',b'',combined_bytes,flags=re.M)
    all_c.write_bytes(combined_bytes)
    aliases="\n".join(f'{item["function"]} = {class_name}.{item["function"]}' for item in items)
    registry="\n".join(f'    "{item["id"]}": {item["function"]},' for item in items)
    write(all_py,f'"""All {family.upper()} software models. Original notebook arithmetic retained.\nUse COMPONENTS[architecture_id](...) or the original class methods.\n"""\n'+source+"\n\n"+aliases+"\n\nCOMPONENTS = {\n"+registry+"\n}\n")
    all_rtl.write_bytes(b"// Combined modules; select the desired module as synthesis/simulation top.\n"+b"\n\n".join(f'// Source: {item["rtl"]}\n'.encode("utf-8")+(ROOT/item["rtl"]).read_bytes() for item in items))
    readme=destination/"README.md"
    signature="(a, b, width, lpl)" if kind=="adder" else "(a, b, width_a, width_b, lpl)"
    write(readme,f'''# {family.upper()} model downloads

The uploaded original C and notebook implementations passed exhaustive equality checks for unsigned 8-bit operands, LPL 1 through 7. Each configuration covers all 65,536 ordered pairs from 0 through 255, including a separately reported 0 through 127 subset. This establishes implementation agreement, not an error-optimality claim.

- `c/`: one self-contained C file per architecture. Public function names match the original C. Compile with C99 and link `-lm` when needed. Helpers have internal linkage so different standalone files can be linked together.
- `python/`: one self-contained Python file per architecture; call `compute{signature}` or the original class method.
- `{family}_all.c`: all C architectures in one self-contained file. The original multiplier's declaration-only local header include is omitted; arithmetic function bodies are preserved.
- `{family}_all.py`: all Python architectures in one file; `COMPONENTS` maps each RTL architecture ID to its callable.
- `{family}_all.v`: all original RTL modules in one file; choose the desired module as top. All modules use parameters `N` and `LPL`.

Use either the combined implementation or the standalone files in a build. Combining both representations duplicates the same public functions/modules. LIA results retain N+1 bits; LIM results retain 2*N bits. For LIM, the software argument VBL corresponds to RTL LPL.

Base validation covers N=8 and LPL=1..7. Additional benchmark validation, when available, is recorded below; other settings remain unverified. Keep each configuration's parameters when downloading a shared parameterized file. Hardware measurement availability is specific to each configuration; see the catalog provenance.

Original sources and hashes, the architecture/function mapping, and generated file hashes are recorded in `model-manifest.json`. Error metrics and exact rational aggregates are in the website's `result/validation/` reports. No arithmetic algorithm was changed during splitting or combination.
''')
    outputs.extend([all_c,all_py,all_rtl,readme])
    manifest_path=destination/"model-manifest.json"
    manifest={"family":family,"source_sha256":source_hashes,"validated_domain":{"width":8,"lpl":list(range(1,8)),"operands":[0,255]},
              "c_python_report":report_path.relative_to(ROOT).as_posix(),"rtl_report":rtl_report_path.relative_to(ROOT).as_posix() if rtl_report else None,
              "architectures":items,"generated_sha256":{p.relative_to(ROOT).as_posix():sha256(p) for p in outputs},
              "packaging_checks":"Standalone Python method ASTs match notebook methods; C files compile independently; Python edge cases pass."}
    write(manifest_path,json.dumps(manifest,indent=2)+"\n")
    catalog_path=ROOT/"data/catalog.json"
    catalog=json.loads(catalog_path.read_text(encoding="utf-8"))
    catalog["components"]=[r for r in catalog["components"] if r["kind"]!=kind]
    for result in report["configurations"]:
        ident,lpl=result["id"],result["lpl"]
        item=next(item for item in items if item["id"]==ident)
        source_files=[report_path.relative_to(ROOT).as_posix(),report["baseline"],report["python_source"],item["rtl"],manifest_path.relative_to(ROOT).as_posix()]
        if kind=="multiplier":
            source_files.append("assets/codes/LFMs.h")
            source_files.append("result/validation/rtl-compatibility-fixes.json")
        if rtl_report:
            source_files.append(rtl_report_path.relative_to(ROOT).as_posix())
        catalog["components"].append({"id":f"{ident}-u8-lpl{lpl}","architecture":ident,"kind":kind,"width":8,"signed":False,"lpl":lpl,
            "parameters":{"N":8,"LPL":lpl,"output_bits":9 if kind=="adder" else 16,"c_function":item["function"],"python_function":f"{class_name}.{item['function']}","rtl_top":ident},
            "implementations":implementations[ident],"error":result["c"]["metrics"],"ppa":{"area":None,"power":None,"delay":None},"benchmark_group":None,
            "provenance":{"source_files":source_files,"error":{"sign":"approximate-exact","units":"integer-output","pe_unit":"fraction",
                "domain":{"a":[0,255],"b":[0,255],"signed":False,"exact_reference":"a+b" if kind=="adder" else "a*b","output_bits":9 if kind=="adder" else 16},
                "coverage":"exhaustive ordered pairs","distribution":"uniform; one equal weight per input pair","count":65536,"toolchain":report["toolchain"]},
                "notes":[f"Source report: configurations entry id={ident}, lpl={lpl}; use c.metrics. C/Python outputs and exact aggregate ratios match, including the 0..127 subset.",
                         "RTL outputs also match on all tested pairs." if rtl_report else "RTL has not yet been simulated against the C/Python baseline.",
                         "No PPA report was supplied for this width/LPL. Base error characterization covers N=8, LPL=1..7; other domains require their own validation reports."]}})
    catalog.setdefault("libraries",{})[kind]={"c":all_c.relative_to(ROOT).as_posix(),"python":all_py.relative_to(ROOT).as_posix(),"rtl":all_rtl.relative_to(ROOT).as_posix(),
                                              "support":[readme.relative_to(ROOT).as_posix(),manifest_path.relative_to(ROOT).as_posix()]}
    write(catalog_path,json.dumps(catalog,indent=2)+"\n")
    print(f"Prepared {len(items)} standalone {kind} models in C/Python, combined C/Python/RTL files, and {len(report['configurations'])} measured catalog entries.")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind",choices=("adder","multiplier"),required=True)
    parser.add_argument("--compiler",default="gcc")
    args=parser.parse_args()
    try:
        prepare(args.kind,args.compiler)
        return 0
    except (ValueError,OSError,subprocess.SubprocessError) as exc:
        parser.exit(1,f"ERROR: {exc}\n")


if __name__=="__main__":
    raise SystemExit(main())
