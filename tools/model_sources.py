"""Inspect supplied model sources. Never edit the uploaded originals."""
import ast
import hashlib
import json
from pathlib import Path
import re
import textwrap

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "assets/codes"


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def notebook_source(kind):
    filename = "LIAs.ipynb" if kind == "adder" else "LIMs.ipynb"
    notebook = json.loads((SOURCES / filename).read_text(encoding="utf-8-sig"))
    source = "\n\n".join(textwrap.dedent("".join(c["source"])) for c in notebook["cells"] if c["cell_type"] == "code")
    tree = ast.parse(source)
    if any(not isinstance(node, (ast.Import, ast.ImportFrom, ast.ClassDef)) for node in tree.body):
        raise ValueError(f"Review executable top-level notebook statements before loading {filename}")
    namespace = {}
    exec(compile(source, filename, "exec"), namespace)
    return source, namespace["LIAComponents" if kind == "adder" else "LIMComponents"]


def architectures(kind):
    _, cls = notebook_source(kind)
    prefix = "unsgn_LFA_" if kind == "adder" else "unsgn_LFM_"
    functions = {name: value for name, value in vars(cls).items() if name.startswith(prefix)}
    result = []
    folder = SOURCES / ("LIA" if kind == "adder" else "LIM")
    for rtl in sorted(folder.glob("*.v")):
        code = rtl.read_text(encoding="utf-8-sig")
        if kind == "adder":
            function = re.search(r"Auto-translated from LFAs\.c:\s*(\w+)", code).group(1)
        else:
            suffix = rtl.stem.removeprefix("lim_")
            function = next((name for name in functions if name.removeprefix("unsgn_LFM_").lower() == suffix), None)
        if function not in functions:
            raise ValueError(f"No notebook function corresponds to {rtl}")
        result.append({"id": rtl.stem, "kind": kind, "function": function, "rtl": rtl.relative_to(ROOT).as_posix()})
    if len(result) != len(functions):
        raise ValueError(f"Incomplete {kind} RTL/Python mapping")
    return result


def c_functions(source):
    """Return original function spans; ignore braces in comments and literals."""
    stripped = re.sub(r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'',
                      lambda m: "".join("\n" if c == "\n" else " " for c in m[0]), source, flags=re.S)
    pattern = r'\b(?:unsigned\s+)?(?:long\s+)?(?:int|long|void)\s+(\w+)\s*\([^;{}]*\)\s*\{'
    functions = {}
    for match in re.finditer(pattern, stripped):
        start, index, depth = match.start(), match.end(), 1
        while depth and index < len(stripped):
            depth += (stripped[index] == "{") - (stripped[index] == "}")
            index += 1
        if depth:
            raise ValueError(f"Unbalanced function body: {match[1]}")
        functions[match[1]] = (start, index, source[start:index])
    return functions
