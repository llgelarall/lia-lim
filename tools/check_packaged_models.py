"""Check distributed C extractions against original C across the validated domain."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile

from model_sources import ROOT, architectures, c_functions, sha256


def check(kind,compiler):
    family="lia" if kind=="adder" else "lim"
    manifest_path=ROOT/f"models/{family}/model-manifest.json"
    manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
    reference=json.loads((ROOT/manifest["c_python_report"]).read_text(encoding="utf-8"))
    items=architectures(kind)
    domains=[{"width":8,"lpl":list(range(1,8))},*manifest.get("additional_validated_domains",[])]
    for path,digest in manifest["generated_sha256"].items():
        if sha256(ROOT/path)!=digest:
            raise ValueError(f"Packaged file changed since generation: {path}")
    for path,digest in manifest["source_sha256"].items():
        if sha256(ROOT/path)!=digest:
            raise ValueError(f"Original source changed since generation: {path}")
    combined=ROOT/f"models/{family}/{family}_all.c"
    original_bytes=(ROOT/reference["baseline"]).read_bytes()
    if kind=="multiplier":
        original_bytes=re.sub(rb'^#include[ \t]+"LFMs\.h"[^\r\n]*\r?\n',b'',original_bytes,flags=re.M)
    if combined.read_bytes()!=original_bytes:
        raise ValueError("Combined C differs from baseline")
    py_source=(ROOT/f"models/{family}/{family}_all.py").read_text(encoding="utf-8")
    compiled_ns={}
    exec(compile(py_source,f"{family}_all.py","exec"),compiled_ns)
    c_source=(ROOT/reference["baseline"]).read_text(encoding="utf-8")
    functions=c_functions(c_source)
    declarations=[]
    with tempfile.TemporaryDirectory(prefix="lia-lim-package-check-") as temp:
        folder=Path(temp)
        objects=[]
        for item in items:
            name=item["function"]
            declaration=functions[name][2].split("{",1)[0].strip()
            declarations.extend([declaration+";",declaration.replace(name,"packaged_"+name)+";"])
            obj=folder/f'{item["id"]}.o'
            source=ROOT/f"models/{family}/c/{item['id']}.c"
            result=subprocess.run([compiler,"-std=c99","-O2",f"-D{name}=packaged_{name}","-c",str(source),"-o",str(obj)],capture_output=True,text=True)
            if result.returncode:
                raise ValueError(result.stderr)
            objects.append(str(obj))
            ns={}
            exec(compile((ROOT/f"models/{family}/python/{item['id']}.py").read_text(encoding="utf-8"),item["id"],"exec"),ns)
            for domain in domains:
                width=domain["width"]
                size=1<<width
                for lpl in domain["lpl"]:
                    for a in range(size):
                        for b in (0,1,size//2-1,size//2,size-2,size-1,a,size-1-a):
                            args=(a,b,width,lpl) if kind=="adder" else (a,b,width,width,lpl)
                            if ns["compute"](*args)!=compiled_ns["COMPONENTS"][item["id"]](*args):
                                raise ValueError(f"Packaged Python mismatch: {item['id']} {args}")
        calls=[]
        for item in items:
            args="a,b,width,lpl" if kind=="adder" else "a,b,width,width,lpl"
            name=item["function"]
            calls.append(f'if({name}({args})!=packaged_{name}({args})) mismatches++; comparisons++;')
        loops=[]
        for domain in domains:
            for level in domain["lpl"]:
                width=domain["width"]
                loops.append(f'{{ unsigned int width={width}, lpl={level}; for(unsigned int a=0;a<{1<<width};a++) for(unsigned int b=0;b<{1<<width};b++){{\n'+"\n".join(calls)+'\n}}\n')
        driver=folder/"check.c"
        driver.write_text('#include <stdio.h>\n'+"\n".join(declarations)+'\nint main(void){unsigned long long mismatches=0,comparisons=0;\n'+"\n".join(loops)+'\nprintf("%llu %llu\\n",comparisons,mismatches);return mismatches?1:0;}\n',encoding="utf-8")
        executable=folder/"check.exe"
        result=subprocess.run([compiler,"-std=c99","-O2",str(driver),str(combined),*objects,"-lm","-o",str(executable)],capture_output=True,text=True)
        if result.returncode:
            raise ValueError(result.stderr)
        result=subprocess.run([str(executable)],capture_output=True,text=True,check=True)
        comparisons,mismatches=map(int,result.stdout.strip().split())
    report={"kind":kind,"status":"passed" if not mismatches else "failed","c_exhaustive_comparisons":comparisons,"c_mismatches":mismatches,
            "domains":[{"width":d["width"],"lpl":d["lpl"]} for d in domains],
            "python_checks":"Standalone method ASTs preserved; packaged Python agrees with the combined registry for every a in each domain and b at zero, one, midpoint boundaries, maximum boundaries, a, and its complement, for every listed LPL.",
            "combined_rtl":"Each original module is concatenated verbatim, with source labels; original modules separately underwent exhaustive simulation.",
            "manifest":manifest_path.relative_to(ROOT).as_posix(),"manifest_sha256":sha256(manifest_path),"evaluator":"tools/check_packaged_models.py","evaluator_sha256":sha256(__file__)}
    output=ROOT/f"result/validation/{kind}8-packaged.json"
    output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(f"{kind}: {comparisons:,} packaged C comparisons, {mismatches} mismatches; Python variants and source hashes pass.",flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind",choices=("adder","multiplier"),required=True)
    parser.add_argument("--compiler",default="gcc")
    args=parser.parse_args()
    try:
        check(args.kind,args.compiler)
    except (ValueError,OSError,subprocess.SubprocessError) as exc:
        parser.exit(1,f"ERROR: {exc}\n")


if __name__=="__main__":
    main()
