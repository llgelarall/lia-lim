"""Repair the reserved generate label 'small', preserving uploaded RTL copies."""
import json
from model_sources import ROOT, SOURCES, sha256


def main():
    repairs=[]
    for path in sorted((SOURCES/"LIM").glob("*.v")):
        before=path.read_bytes()
        old,new=b"end else begin : small",b"end else begin : g_small"
        original=SOURCES/"original/LIM"/path.name
        if old in before:
            if before.count(old)!=1:
                raise ValueError(f"Unexpected label occurrence count: {path}")
            original.parent.mkdir(parents=True,exist_ok=True)
            if original.exists() and original.read_bytes()!=before:
                raise ValueError(f"Original RTL backup already differs: {original}")
            original.write_bytes(before)
            path.write_bytes(before.replace(old,new))
        if original.is_file():
            if original.read_bytes().replace(old,new)!=path.read_bytes():
                raise ValueError("RTL differs from its upload beyond the declared label-only repair")
            repairs.append({"source":path.relative_to(ROOT).as_posix(),"original":original.relative_to(ROOT).as_posix(),
                            "original_sha256":sha256(original),"repaired_sha256":sha256(path),
                            "change":"Generate block label small renamed to g_small; no arithmetic expressions changed."})
    report={"repairs":repairs,"reason":"small is a reserved Verilog drive-strength keyword and cannot be used as an unescaped generate label."}
    (ROOT/"result/validation/rtl-compatibility-fixes.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(f"Verified {len(repairs)} label-only RTL repairs; uploaded originals retained in assets/codes/original/LIM/.")


if __name__=="__main__":
    main()
