"""Exhaustively compare uploaded Python models with the independent C baseline.

Example: python tools/validate_models.py --kind adder --width 8 --lpl 1 2 3 4 5 6 7
This evaluates all ordered input pairs 0..255, plus reports the 0..127 subset.
"""
from __future__ import annotations

import argparse
import array
from fractions import Fraction
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

from model_sources import ROOT, SOURCES, architectures, notebook_source, sha256


class Aggregates:
    def __init__(self):
        self.count = self.total = self.absolute = self.squared = self.different = 0
        self.minimum = self.maximum = None

    def add(self, error):
        self.count += 1
        self.total += error
        self.absolute += abs(error)
        self.squared += error * error
        self.different += error != 0
        self.minimum = error if self.minimum is None else min(self.minimum, error)
        self.maximum = error if self.maximum is None else max(self.maximum, error)

    def result(self):
        numerators = {"me": self.total, "mse": self.squared, "mae": self.absolute, "pe": self.different}
        return {"count": self.count,
                "metrics": {**{k: v / self.count for k, v in numerators.items()}, "max": self.maximum, "min": self.minimum},
                "exact_ratios": {k: str(Fraction(v, self.count)) for k, v in numerators.items()},
                "integer_sums": {"signed": self.total, "absolute": self.absolute, "squared": self.squared, "different": self.different}}


def driver_source(kind, items, baseline):
    if kind == "adder":
        typedef = "typedef unsigned int (*model_fn)(unsigned int,unsigned int,unsigned int,unsigned int);"
        names = [item["function"] for item in items]
        call = "models[id](a,b,width,lpl)"
    else:
        typedef = "typedef unsigned long int (*model_fn)(unsigned long int,unsigned long int,int,int,int);"
        baseline_text = baseline.read_text(encoding="utf-8-sig")
        names = [item["function"] if item["function"] + "(" in baseline_text.replace(" ", "") else "py_" + item["function"] for item in items]
        call = "models[id](a,b,width,width,lpl)"
    return f'''#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#ifdef _WIN32
#include <io.h>
#include <fcntl.h>
#endif
#include "{baseline.as_posix()}"
{typedef}
model_fn models[] = {{{','.join(names)}}};
int main(int argc,char **argv) {{
  if(argc!=4) return 2;
  unsigned int id=atoi(argv[1]),width=atoi(argv[2]),lpl=atoi(argv[3]);
  if(width<1 || width>12 || id>={len(items)}) return 2;
#ifdef _WIN32
  _setmode(_fileno(stdout),_O_BINARY);
#endif
  for(unsigned int a=0;a<(1u<<width);a++)
    for(unsigned int b=0;b<(1u<<width);b++) {{
      uint32_t result=(uint32_t)({call});
      if(fwrite(&result,sizeof(result),1,stdout)!=1) return 3;
    }}
  return 0;
}}
'''


def validate_kind(kind, width, levels, compiler, output):
    baseline = SOURCES / ("LFAs.c" if kind == "adder" else "LFMs.c")
    if not baseline.is_file():
        raise ValueError(f"Missing independent C baseline: {baseline.relative_to(ROOT)}; a header declaration is not an implementation")
    items = architectures(kind)
    _, cls = notebook_source(kind)
    notebook = SOURCES / ("LIAs.ipynb" if kind == "adder" else "LIMs.ipynb")
    report = {"kind": kind, "width": width, "lpl_values": levels, "input_domain": f"all ordered pairs of unsigned integers 0..{(1 << width)-1}",
              "subset_domain": f"all ordered pairs 0..{(1 << (width-1))-1}", "sign": "approximate-exact", "normalization": "none; PE is a fraction",
              "baseline": baseline.relative_to(ROOT).as_posix(), "baseline_sha256": sha256(baseline), "python_source": notebook.relative_to(ROOT).as_posix(), "python_source_sha256": sha256(notebook),
              "toolchain": {"python": platform.python_version(), "compiler": subprocess.check_output([compiler, "--version"], text=True).splitlines()[0],
                            "compiler_target": subprocess.check_output([compiler, "-dumpmachine"], text=True).strip(), "compiler_flags": ["-std=c99", "-O2", "-Wall", "-Wextra", "-lm"]},
              "evaluator": "tools/validate_models.py", "evaluator_sha256": sha256(__file__), "configurations": [], "status": "running"}
    output.parent.mkdir(parents=True, exist_ok=True)
    def save():
        output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="lia-lim-validation-") as workspace:
        folder = Path(workspace)
        driver = folder / "baseline_driver.c"
        executable = folder / ("baseline.exe" if sys.platform == "win32" else "baseline")
        driver.write_text(driver_source(kind, items, baseline), encoding="utf-8")
        compiled = subprocess.run([compiler, "-std=c99", "-O2", "-Wall", "-Wextra", str(driver), "-lm", "-o", str(executable)], capture_output=True, text=True)
        report["compiler_diagnostics"] = compiled.stderr
        if compiled.returncode:
            raise ValueError(f"C baseline compilation failed:\n{compiled.stderr}")
        for index, item in enumerate(items):
            fn = getattr(cls, item["function"])
            for lpl in levels:
                c_result = subprocess.run([str(executable), str(index), str(width), str(lpl)], capture_output=True)
                expected_bytes = (1 << (2 * width)) * 4
                entry = {**item, "lpl": lpl, "width": width, "mismatches": 0, "examples": []}
                if c_result.returncode or len(c_result.stdout) != expected_bytes:
                    entry.update(status="baseline-failed", message=c_result.stdout[:500].decode("utf-8", errors="replace"), exit_code=c_result.returncode)
                else:
                    values = array.array("I")
                    values.frombytes(c_result.stdout)
                    if sys.byteorder != "little":
                        values.byteswap()
                    c_stats, py_stats, c_subset, py_subset = (Aggregates() for _ in range(4))
                    first_exception = None
                    size = 1 << width
                    for pair, expected in enumerate(values):
                        a, b = divmod(pair, size)
                        exact = a+b if kind == "adder" else a*b
                        c_stats.add(expected-exact)
                        in_subset = a < size//2 and b < size//2
                        if in_subset:
                            c_subset.add(expected-exact)
                        try:
                            actual = fn(a,b,width,lpl) if kind == "adder" else fn(a,b,width,width,lpl)
                            if not isinstance(actual, int):
                                raise TypeError(f"Noninteger output: {actual!r}")
                            py_stats.add(actual-exact)
                            if in_subset:
                                py_subset.add(actual-exact)
                            if actual != expected:
                                entry["mismatches"] += 1
                                if len(entry["examples"]) < 8:
                                    entry["examples"].append({"a":a,"b":b,"c":expected,"python":actual,"exact":exact})
                        except (Exception, SystemExit) as exc:
                            first_exception = {"a":a,"b":b,"type":type(exc).__name__,"message":str(exc)}
                            break
                    entry["c"] = c_stats.result()
                    entry["c_subset"] = c_subset.result()
                    if first_exception:
                        entry.update(status="python-failed", exception=first_exception)
                    else:
                        entry["python"] = py_stats.result()
                        entry["python_subset"] = py_subset.result()
                        entry["status"] = "passed" if entry["mismatches"] == 0 and entry["c"] == entry["python"] and entry["c_subset"] == entry["python_subset"] else "mismatch"
                report["configurations"].append(entry)
                save()
                print(f'{item["id"]} N={width} LPL={lpl}: {entry["status"]}; {entry["mismatches"]} mismatches', flush=True)
    report["status"] = "passed" if all(c["status"] == "passed" for c in report["configurations"]) else "failed"
    report["total_pairs"] = sum(c.get("c", {}).get("count", 0) for c in report["configurations"])
    save()
    return report["status"] == "passed"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", choices=("adder", "multiplier"), required=True)
    parser.add_argument("--width", type=int, default=8)
    parser.add_argument("--lpl", type=int, nargs="+", default=list(range(1,8)))
    parser.add_argument("--compiler", default=shutil.which("gcc"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    max_level = args.width if args.kind == "multiplier" else args.width - 1
    if not args.compiler or not 2 <= args.width <= 12 or any(not 1 <= n <= max_level for n in args.lpl):
        parser.error("GCC and 2 <= width <= 12 are required; use 1 <= LPL < width for adders or 1 <= LPL <= width for multipliers")
    output = args.output or ROOT / f"result/validation/{args.kind}{args.width}-c-python.json"
    try:
        return 0 if validate_kind(args.kind, args.width, args.lpl, args.compiler, output) else 1
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
