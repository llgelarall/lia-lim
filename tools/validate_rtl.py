"""Exhaustively check RTL outputs after the independent C/Python validation passes."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from model_sources import ROOT, SOURCES, architectures, notebook_source, sha256


def run(kind, width, levels, tool_dir, simulator, output, combined=None, reference=None):
    baseline_path = reference or ROOT / f"result/validation/{kind}{width}-c-python.json"
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    if baseline["status"] != "passed" or baseline["python_source_sha256"] != sha256(ROOT / baseline["python_source"]) or baseline["baseline_sha256"] != sha256(ROOT / baseline["baseline"]):
        raise ValueError("A passing, current C/Python validation report is required before checking RTL")
    items = architectures(kind)
    configs = [(item, lpl) for item in items for lpl in levels]
    proven={(entry["id"],entry["lpl"]) for entry in baseline["configurations"] if entry["status"]=="passed"}
    if any((item["id"],lpl) not in proven for item,lpl in configs):
        raise ValueError("Requested RTL configurations must first pass the C/Python comparison")
    _, cls = notebook_source(kind)
    funcs = [getattr(cls, item["function"]) for item, _ in configs]
    out_width = width+1 if kind == "adder" else 2*width
    report = {"kind": kind, "width": width, "lpl_values": levels,
              "status": "running", "reference_report": baseline_path.relative_to(ROOT).as_posix(), "reference_report_sha256": sha256(baseline_path),
              "evaluator": "tools/validate_rtl.py", "evaluator_sha256": sha256(__file__),
              "configurations": [{"id": item["id"], "lpl": lpl, "pairs_checked": 0, "mismatches": 0, "examples": []} for item,lpl in configs],
              "rtl_sources": {str(path.relative_to(ROOT).as_posix()): sha256(path) for path in ([combined] if combined else [ROOT/item["rtl"] for item in items])}}
    with tempfile.TemporaryDirectory(prefix="lia-lim-rtl-") as temp:
        workspace = Path(temp)
        testbench = workspace / "tb.v"
        lines = ["module tb;", f"reg [{width-1}:0] a,b;", f"wire [{out_width-1}:0] results[0:{len(configs)-1}];", "integer fd,aa,bb,j;"]
        for index,(item,lpl) in enumerate(configs):
            lines.append(f'{item["id"]} #(.N({width}),.LPL({lpl})) dut_{index}(a,b,results[{index}]);')
        lines += ['initial begin', 'fd=$fopen("outputs.txt","w");', 'if(fd==0) $fatal(1,"Cannot open outputs.txt");',
                  f'for(aa=0;aa<{1<<width};aa=aa+1) begin', f'for(bb=0;bb<{1<<width};bb=bb+1) begin',
                  'a=aa;b=bb;#1;', f'for(j=0;j<{len(configs)};j=j+1) $fwrite(fd,"%h ",results[j]);', '$fwrite(fd,"\\n");',
                  'end', 'end', '$fclose(fd);', '$finish;', 'end', 'endmodule']
        testbench.write_text("\n".join(lines)+"\n", encoding="utf-8")
        paths = [str(combined)] if combined else [str(ROOT/item["rtl"]) for item in items]
        def command(argv):
            completed = subprocess.run(argv,cwd=workspace,capture_output=True,text=True,timeout=240)
            report.setdefault("commands",[]).append({"command": [str(v) for v in argv], "returncode": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr})
            if completed.returncode:
                raise ValueError(f"RTL tool failed: {argv[0]}\n{completed.stdout}\n{completed.stderr}")
        def tool(name):
            resolved=str(tool_dir/(name+".exe")) if tool_dir else shutil.which(name)
            if not resolved:
                raise ValueError(f"Required RTL tool is unavailable: {name}; install it or pass --tool-dir")
            return resolved
        if simulator == "modelsim":
            report["toolchain"] = subprocess.check_output([tool("vsim"),"-version"],text=True).strip()
            command([tool("vlib"),"work"])
            command([tool("vlog"),"-quiet","-work","work",*paths,str(testbench)])
            command([tool("vsim"),"-c","-quiet","-lib","work","tb","-do","run -all; quit -f"])
        else:
            report["toolchain"] = subprocess.check_output([tool("iverilog"),"-V"],text=True,stderr=subprocess.STDOUT).splitlines()[0]
            command([tool("iverilog"),"-g2012","-s","tb","-o","sim",*paths,str(testbench)])
            command([tool("vvp"),"sim"])
        size = 1 << width
        pair = 0
        with (workspace/"outputs.txt").open(encoding="utf-8") as stream:
            for pair,line in enumerate(stream,1):
                if pair > size*size:
                    raise ValueError("RTL testbench emitted too many input pairs")
                a,b=divmod(pair-1,size)
                values=line.split()
                if len(values)!=len(configs):
                    raise ValueError("Incomplete RTL output row")
                for column,(item,lpl) in enumerate(configs):
                    fn=funcs[column]
                    expected=fn(a,b,width,lpl) if kind=="adder" else fn(a,b,width,width,lpl)
                    try:
                        actual=int(values[column],16)
                    except ValueError:
                        actual=values[column]
                    entry=report["configurations"][column]
                    entry["pairs_checked"]+=1
                    if actual!=expected:
                        entry["mismatches"]+=1
                        if len(entry["examples"])<5:
                            entry["examples"].append({"a":a,"b":b,"c_python":expected,"rtl":actual})
                if pair%16384==0:
                    print(f"{kind} RTL: {pair}/{size*size} input pairs × {len(configs)} configurations checked",flush=True)
        if pair!=size*size:
            raise ValueError("Incomplete exhaustive RTL simulation")
    for entry in report["configurations"]:
        entry["status"]="passed" if not entry["mismatches"] else "mismatch"
    report["status"]="passed" if all(c["status"]=="passed" for c in report["configurations"]) else "failed"
    report["total_pairs"]=sum(c["pairs_checked"] for c in report["configurations"])
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(f"{kind} RTL validation: {report['status']}; {sum(c['mismatches'] for c in report['configurations'])} mismatches",flush=True)
    return report["status"]=="passed"


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind",choices=("adder","multiplier"),required=True)
    parser.add_argument("--width",type=int,default=8)
    parser.add_argument("--lpl",nargs="+",type=int,default=list(range(1,8)))
    parser.add_argument("--simulator",choices=("modelsim","iverilog"),default="iverilog")
    parser.add_argument("--tool-dir",type=Path)
    parser.add_argument("--combined",type=Path)
    parser.add_argument("--output",type=Path)
    parser.add_argument("--reference-report",type=Path)
    args=parser.parse_args()
    max_level=args.width if args.kind=="multiplier" else args.width-1
    if not 2<=args.width<=12 or any(not 1<=n<=max_level for n in args.lpl):
        parser.error("Use 2 <= width <= 12; LPL < width for adders, LPL <= width for multipliers")
    try:
        return 0 if run(args.kind,args.width,args.lpl,args.tool_dir,args.simulator,args.output or ROOT/f"result/validation/{args.kind}{args.width}-rtl.json",args.combined.resolve() if args.combined else None,args.reference_report.resolve() if args.reference_report else None) else 1
    except (ValueError,OSError,subprocess.SubprocessError) as exc:
        parser.exit(1,f"ERROR: {exc}\n")


if __name__=="__main__":
    raise SystemExit(main())
