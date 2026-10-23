"""Validate and publish verified component metadata without changing model files."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
from pathlib import Path
import re
import sys
from urllib.parse import quote, urlparse
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ERROR_KEYS = ("me", "mse", "mae", "pe", "max", "min")
PPA_KEYS = ("area", "power", "delay")
LANGUAGES = {"c": "C", "python": "Python", "rtl": "RTL"}
RESULT_DIRS = ("result/adder8-lia-vs-evo", "result/multiplier8-lim-vs-evo")


def dump(value):
    return json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"


def local_file(root, value):
    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError("Use a nonempty site-relative path with forward slashes")
    if any(part in (".", "..") for part in value.split("/")):
        raise ValueError(f"Use a normalized path without dot segments: {value}")
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError(f"Missing file or path outside the website: {value}")
    if Path(value).is_absolute() or re.match(r"^[A-Za-z]:", value):
        raise ValueError(f"Absolute paths are not publishable: {value}")
    return path


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def metric(record, key):
    error = record.get("error", {})
    if key == "abs_me":
        return abs(error["me"]) if number(error.get("me")) else None
    if key == "wce":
        return max(abs(error["min"]), abs(error["max"])) if all(number(error.get(k)) for k in ("min", "max")) else None
    return record.get("ppa" if key in PPA_KEYS else "error", {}).get(key)


def group_context(record):
    """A group must share operation/domain and all recorded benchmark conditions."""
    p = record.get("provenance", {})
    if not isinstance(p, dict):
        p = {}
    return dump({"kind": record.get("kind"), "width": record.get("width"),
                 "signed": record.get("signed"), "error": p.get("error"), "ppa": p.get("ppa")})


def validate(data, root=ROOT):
    errors, warnings = [], []
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        return {"errors": ["Expected an object with schema_version: 1"], "warnings": [], "configurations": 0}
    records = data.get("components")
    if not isinstance(records, list):
        return {"errors": ["components must be an array"], "warnings": [], "configurations": 0}
    if not records:
        warnings.append("No component implementations or measurements supplied; the catalog is empty.")
    site = data.get("site", {})
    if not isinstance(site, dict):
        errors.append("site must be an object")
        site = {}
    for key in ("url", "repository_url"):
        value = site.get(key)
        if not value:
            warnings.append(f"site.{key} is missing.")
        elif not isinstance(value, str) or urlparse(value).scheme not in ("http", "https") or not urlparse(value).netloc:
            errors.append(f"site.{key} must be an absolute HTTP(S) URL")
        elif key == "url" and (not value.endswith("/") or urlparse(value).query or urlparse(value).fragment):
            errors.append("site.url must end in / and contain no query string or fragment")
    for folder in (() if (root/"data/comparisons.json").is_file() else RESULT_DIRS):
        if not (root / folder).is_dir() or not any((root / folder).rglob("*.*")):
            warnings.append(f"Result collection is absent or empty: {folder}/")
    libraries = data.get("libraries", {})
    if not isinstance(libraries, dict):
        errors.append("libraries must be an object")
        libraries = {}
    for kind, library in libraries.items():
        if kind not in ("adder", "multiplier") or not isinstance(library, dict):
            errors.append(f"Invalid integrated library: {kind}")
            continue
        paths = [library[k] for k in LANGUAGES if library.get(k)]
        support = library.get("support", [])
        if not isinstance(support, list):
            errors.append(f"libraries.{kind}.support must be an array")
            support = []
        for path in paths + support:
            try:
                local_file(root, path)
            except ValueError as exc:
                errors.append(str(exc))
    ids, groups = set(), {}
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"components[{index}] must be an object")
            continue
        ident = record.get("id", "")
        label = str(ident) or f"components[{index}]"
        fail = lambda message: errors.append(f"{label}: {message}")
        warn = lambda message: warnings.append(f"{label}: {message}")
        if not isinstance(ident, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", ident):
            fail("id must be a unique filename-safe string")
        elif ident.casefold() in ids:
            fail("duplicate ID (case-insensitive)")
        else:
            ids.add(ident.casefold())
        if record.get("kind") not in ("adder", "multiplier"):
            fail("kind must be adder or multiplier")
        if not isinstance(record.get("architecture"), str) or not record["architecture"].strip():
            fail("architecture is required")
        if type(record.get("width")) is not int or record["width"] < 1:
            fail("width must be a positive integer (equal-width operands)")
        if not isinstance(record.get("signed"), bool):
            fail("signed must explicitly be true or false")
        if record.get("lpl") is not None and (type(record["lpl"]) is not int or record["lpl"] < 0):
            fail("lpl must be a nonnegative integer or null; supported ranges must come from the implementation")
        if record.get("lpl") is None:
            warn("LPL is unspecified; confirm whether it is not applicable or missing")
        if record.get("reported_timing_ns") is not None and not number(record["reported_timing_ns"]):
            fail("reported_timing_ns must be a finite number or null")
        if not isinstance(record.get("parameters", {}), dict):
            fail("parameters must be an object")
        implementations = record.get("implementations", {})
        if not isinstance(implementations, dict):
            fail("implementations must be an object")
            implementations = {}
        for language in implementations:
            if language not in LANGUAGES:
                fail(f"unknown implementation language: {language}")
        for language in LANGUAGES:
            paths = implementations.get(language, [])
            if not isinstance(paths, list) or any(not isinstance(p, str) for p in paths):
                fail(f"implementations.{language} must be an array of file paths")
                continue
            if not paths:
                warn(f"{LANGUAGES[language]} implementation unavailable")
            for path in paths:
                try:
                    local_file(root, path)
                except ValueError as exc:
                    fail(str(exc))
        p = record.get("provenance", {})
        if not isinstance(p, dict):
            fail("provenance must be an object")
            p = {}
        sources = p.get("source_files", [])
        if not isinstance(sources, list):
            fail("provenance.source_files must be an array")
            sources = []
        for source in sources:
            try:
                local_file(root, source)
            except ValueError as exc:
                fail(str(exc))
        for section, keys in (("error", ERROR_KEYS), ("ppa", PPA_KEYS)):
            values = record.get(section, {})
            if not isinstance(values, dict):
                fail(f"{section} must be an object")
                continue
            for key, value in values.items():
                if key not in keys:
                    fail(f"unknown {section} metric: {key}")
                elif value is not None and not number(value):
                    fail(f"{section}.{key} must be a finite number or null")
                elif number(value) and key in (*PPA_KEYS, "mae", "mse") and value < 0:
                    fail(f"{section}.{key} cannot be negative")
                elif number(value) and key == "pe" and not 0 <= value <= 1:
                    fail("PE must be a fraction in [0, 1]")
            missing = [k for k in keys if values.get(k) is None]
            if missing:
                warn(f"missing {section} measurements: {', '.join(missing)}")
            if any(number(values.get(k)) for k in keys):
                if not sources:
                    fail("measurements require provenance.source_files")
                context = p.get(section, {})
                if not isinstance(context, dict):
                    fail(f"provenance.{section} must be an object")
                    continue
                required = (("sign", "units", "pe_unit", "domain", "coverage", "distribution", "count", "toolchain") if section == "error" else
                            ("units", "platform", "corner", "voltage_v", "temperature_c", "constraints", "activity", "toolchain", "area_definition", "power_definition", "delay_definition"))
                for field in required:
                    if context.get(field) is None or context.get(field) == "" or context.get(field) == {}:
                        fail(f"measured {section} requires provenance.{section}.{field}; use an explicit 'not recorded' string for unknown conditions")
                    elif isinstance(context[field], str) and context[field].lower().startswith(("unknown", "not recorded")):
                        warn(f"{section}.{field}: {context[field]}")
                if section == "error":
                    if context.get("sign") != "approximate-exact" or context.get("units") != "integer-output" or context.get("pe_unit") != "fraction":
                        fail("error conventions must be approximate-exact, integer-output, and PE as fraction; convert and document the source explicitly")
                    if type(context.get("count")) is not int or context["count"] < 1:
                        fail("error count must be a positive integer")
                elif context.get("units") != {"area": "um2", "power": "uW", "delay": "ns"}:
                    fail("PPA units must be {area: um2, power: uW, delay: ns}; document source conversions")
        e = record.get("error", {})
        if isinstance(e, dict):
            if all(number(e.get(k)) for k in ("min", "max")) and e["min"] > e["max"]:
                fail("minimum error exceeds maximum error")
            if all(number(e.get(k)) for k in ("me", "min", "max")) and not e["min"] - 1e-9 <= e["me"] <= e["max"] + 1e-9:
                fail("ME is outside the signed error range")
            if all(number(e.get(k)) for k in ("me", "mae")) and abs(e["me"]) > e["mae"] + 1e-9:
                fail("absolute ME exceeds MAE")
            if all(number(e.get(k)) for k in ("mae", "mse")) and e["mae"] ** 2 > e["mse"] + 1e-9 * max(1, abs(e["mse"])):
                fail("MAE squared exceeds MSE")
        group = record.get("benchmark_group")
        if group is not None and not isinstance(group, str):
            fail("benchmark_group must be a string or null")
        elif group:
            context = group_context(record)
            if group in groups and groups[group] != context:
                fail(f"benchmark group '{group}' mixes operations, domains, or benchmark conditions")
            groups[group] = context
            if not isinstance(p.get("error"), dict) or not isinstance(p.get("ppa"), dict) or "not recorded" in context.lower() or "unknown" in context.lower():
                fail("a comparable benchmark group requires explicit error and PPA conditions without unknown fields")
        else:
            warn("no verified benchmark_group; physical-flow equivalence is not established")
    return {"configurations": len(records), "errors": errors, "warnings": warnings,
            "verification": "Schema, files, units, and basic metric consistency checked. Source measurements still require review against original reports."}


def text(value):
    return html.escape(str(value), quote=True)


def fmt(value):
    return '<span class="dash" title="Not supplied">—</span>' if value is None else format(value, ".8g")


OBJECTIVE_LABELS = {"ME": "signed mean error", "MAE": "mean absolute error",
                    "MSE": "mean squared error", "PE": "error probability"}


def design_objectives(record):
    """Use the original C function's criterion tokens, never measured minima."""
    function = record.get("parameters", {}).get("c_function", "")
    return list(dict.fromkeys(token for token in function.split("_") if token in OBJECTIVE_LABELS))


def row_html(record, links):
    objectives = design_objectives(record)
    badges = ''.join(f'<span class="criterion-badge criterion-{key.lower()}" role="img" aria-label="Design target: {text(OBJECTIVE_LABELS[key])} ({key})" title="Design target: {text(OBJECTIVE_LABELS[key])} ({key})"><span aria-hidden="true">{key}</span></span>' for key in objectives)
    function = record.get("parameters", {}).get("c_function", "")
    short_name = function.removeprefix("unsgn_LFA_21_21_").removeprefix("unsgn_LFM_") if function else f'{record["architecture"]} · {record["kind"]}'
    cells = [f'<td><div class="component-name"><span class="objective-badges">{badges}</span><span class="component-label"><span class="component-id">{text(record["id"])}</span><span class="cell-sub component-function" title="{text(function)}">{text(short_name)}</span></span></div></td>',
             f'<td>{record["width"]} × {record["width"]}<span class="cell-sub">{"signed" if record["signed"] else "unsigned"}</span></td>',
             f'<td>{fmt(record.get("lpl"))}</td>']
    for k in (*ERROR_KEYS, *PPA_KEYS):
        raw_timing=record.get("reported_timing_ns") if k=="delay" else None
        displayed=fmt(raw_timing) + '<sup title="Reported timing; propagation-delay definition unverified">†</sup>' if raw_timing is not None else fmt(metric(record,k))
        cells.append(f'<td class="number">{displayed}</td>')
    models = "".join(f'<a href="{text(links[k])}" download>{label}</a>' if k in links else f'<span class="dash" title="No file supplied">{label}</span>' for k, label in LANGUAGES.items())
    cells.append(f'<td><div class="model-links">{models}</div></td>')
    p = record.get("provenance", {})
    details = f'<dt>Architecture and configuration</dt><dd>{text(record["architecture"])}; width={record["width"]}; LPL={text(record.get("lpl"))}; parameters={text(json.dumps(record.get("parameters", {}), ensure_ascii=False))}</dd>'
    if objectives:
        details += '<dt>Design targets from the original function name</dt><dd>' + text(', '.join(f'{key}: {OBJECTIVE_LABELS[key]}' for key in objectives)) + '; these labels describe design intent, not established Pareto optimality.</dd>'
    details += '<dt>Source files</dt><dd>' + ("<br>".join(f'<a href="{text(quote(s, safe="/"))}">{text(s)}</a>' for s in p.get("source_files", [])) or 'Not supplied') + '</dd>'
    for label, value in (("Error conditions", p.get("error")), ("PPA conditions", p.get("ppa")), ("Benchmark group", record.get("benchmark_group")), ("Notes / conversions", p.get("notes"))):
        details += f'<dt>{label}</dt><dd>{text(json.dumps(value, ensure_ascii=False) if value is not None else "Not supplied")}</dd>'
    cells.append(f'<td><details class="provenance"><summary>View sources</summary><dl>{details}</dl></details></td>')
    return f'<tr data-record-id="{text(record["id"])}">' + "".join(cells) + '</tr>'


def archive(root, relative, records, language=None, extras=None):
    entries = []
    paths = set()
    for record in records:
        implementations = {k: v for k, v in record.get("implementations", {}).items() if v and (language is None or k == language)}
        if implementations:
            entries.append({**record, "implementations": implementations})
            paths.update(path for files in implementations.values() for path in files)
    if not entries:
        return None
    paths.update(extras or [])
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    contents = {f"sources/{p}": local_file(root, p).read_bytes() for p in sorted(paths)}
    manifest = {"configurations": entries, "integrated_sources_and_support": extras or [], "path_prefix": "sources/", "sha256": {p: hashlib.sha256(contents[f"sources/{p}"]).hexdigest() for p in sorted(paths)}}
    contents["MANIFEST.json"] = dump(manifest).encode("utf-8")
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for name, content in sorted(contents.items()):
            entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o644 << 16
            bundle.writestr(entry, content)
    return relative


def replace_block(document, name, body):
    pattern = rf"(<!-- BEGIN {re.escape(name)} -->).*?(<!-- END {re.escape(name)} -->)"
    result, count = re.subn(pattern, lambda m: f"{m[1]}\n{body}\n            {m[2]}", document, flags=re.S)
    if count != 1:
        raise ValueError(f"Expected one generated block: {name}")
    return result


def build(data, root=ROOT):
    records, links, families = data["components"], {}, {}
    for record in records:
        links[record["id"]] = {}
        for language, paths in record.get("implementations", {}).items():
            if len(paths) == 1:
                links[record["id"]][language] = quote(paths[0], safe="/")
            elif paths:
                links[record["id"]][language] = archive(root, f'downloads/components/{record["id"]}-{language}.zip', [record], language)
    for kind, title, plural in (("adder", "LIA adders", "adders"), ("multiplier", "LIM multipliers", "multipliers")):
        subset = [r for r in records if r["kind"] == kind]
        library = data.get("libraries", {}).get(kind, {})
        support = library.get("support", [])
        complete = archive(root, f"downloads/all-{plural}.zip", subset, extras=[library[k] for k in LANGUAGES if library.get(k)] + support)
        action = f'<a class="bundle-link" href="{complete}" download>All {plural} (.zip)</a>' if complete else f'<span class="download-unavailable">All {plural} (.zip) — unavailable</span>'
        per_language = []
        for language, label in LANGUAGES.items():
            url = archive(root, f"downloads/all-{plural}-{language}.zip", subset, language, extras=([library[language]] if library.get(language) else []) + support)
            per_language.append(f'<a href="{url}" download>{label} (.zip)</a>' if url else f'{label} — unavailable')
        integrated = ' · '.join(f'<a href="{text(quote(library[k], safe="/"))}" download aria-label="All {plural} as one {label} file">{label}</a>' if library.get(k) else f'{label} — unavailable' for k, label in LANGUAGES.items())
        families[kind]=f'<div class="family-downloads">{action}<span class="language-downloads">Single files: {integrated}</span><details class="language-archives"><summary>Language ZIPs</summary><span>{" · ".join(per_language)}</span></details></div>'
    page_path = root / "index.html"
    page = page_path.read_text(encoding="utf-8")
    if '<!-- BEGIN FAMILY PANELS -->' in page:
        from site_render import family_panels,comparison_plots
        page=replace_block(page,"FAMILY PANELS",family_panels(data,links,families,row_html))
        comparisons_path=root/"data/comparisons.json"
        comparisons=json.loads(comparisons_path.read_text(encoding="utf-8")) if comparisons_path.is_file() else None
        page=replace_block(page,"COMPARISON PLOTS",comparison_plots(comparisons))
    else:
        rows = "\n".join(row_html(r, links[r["id"]]) for r in records) if records else '<tr><td colspan="14" class="empty-state"><strong>No released configurations in this checkout.</strong></td></tr>'
        page = replace_block(page, "COMPONENT ROWS", rows)
        page = replace_block(page, "BUNDLE DOWNLOADS", "\n".join(families.values()))
    coverage = []
    for folder, label in zip(RESULT_DIRS, ("8-bit adders · LIA vs. EvoApproxLib", "8-bit multipliers · LIM vs. EvoApproxLib")):
        files = sorted(p for p in (root / folder).rglob("*") if p.is_file())
        count = len(files)
        coverage.append(f'<div><dt>{label}</dt><dd><code>{folder}/</code><span>{str(count) + " files supplied; see row provenance" if count else "Not supplied"}</span></dd></div>')
    if '<!-- BEGIN RESULT COVERAGE -->' in page:
        page = replace_block(page, "RESULT COVERAGE", '<dl class="result-locations">' + ''.join(coverage) + '</dl>')
    embedded = json.dumps(data, ensure_ascii=False, allow_nan=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    page = replace_block(page, "CATALOG DATA", f'<script type="application/json" id="catalog-data">{embedded}</script>')
    count_text = f'{len(records)} configurations available'
    page = re.sub(r'(<p id="count"[^>]*>).*?(</p>)', lambda m: m[1] + count_text + m[2], page)
    status = ('<strong>Data availability.</strong> Component sources and characterization results have not been added yet.' if not records else f'<strong>Data availability.</strong> {len(records)} catalog entries. Availability and benchmark conditions are recorded per configuration; missing measurements remain blank.')
    page = re.sub(r'(<p class="data-notice" id="data-status">).*?(</p>)', lambda m: m[1] + status + m[2], page)
    url = data.get("site", {}).get("url")
    canonical = f'<link rel="canonical" href="{text(url)}">\n<meta property="og:url" content="{text(url)}">' if url else '<!-- Canonical URL pending: configure site.url in data/catalog.json. -->'
    page = replace_block(page, "SITE URL", canonical)
    page_path.write_text(page, encoding="utf-8")
    if url:
        (root / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{text(url)}</loc></url></urlset>\n', encoding="utf-8")
    elif (root / "sitemap.xml").is_file():
        (root / "sitemap.xml").unlink()


def nonnegative(value):
    parsed = float(value)
    if not math.isfinite(parsed) or parsed < 0:
        raise argparse.ArgumentTypeError("Expected a finite, nonnegative number")
    return parsed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "build", "select"))
    parser.add_argument("--catalog", type=Path, default=ROOT / "data/catalog.json")
    parser.add_argument("--kind", choices=("adder", "multiplier"))
    parser.add_argument("--width", type=int)
    parser.add_argument("--lpl", type=int)
    parser.add_argument("--benchmark-group")
    limits = {"mae": "mae", "mse": "mse", "pe": "pe", "abs-me": "abs_me", "abs-error": "wce", "area-um2": "area", "power-uw": "power", "delay-ns": "delay"}
    for flag in limits:
        parser.add_argument(f"--max-{flag}", type=nonnegative)
    args = parser.parse_args()
    try:
        data = json.loads(args.catalog.read_text(encoding="utf-8"))
        report = validate(data)
        if args.command != "select":
            (ROOT / "data/validation-report.json").write_text(dump(report), encoding="utf-8")
        for message in report["errors"]:
            print(f"ERROR: {message}", file=sys.stderr)
        for message in report["warnings"][:10]:
            print(f"NOTE: {message}", file=sys.stderr)
        if len(report["warnings"]) > 10:
            print(f"NOTE: {len(report['warnings'])-10} further availability notes; see data/validation-report.json after validate/build.", file=sys.stderr)
        if report["errors"]:
            return 1
        if args.command == "select":
            matches = []
            for record in data["components"]:
                if any(value is not None and record.get(key) != value for key, value in (("kind", args.kind), ("width", args.width), ("lpl", args.lpl), ("benchmark_group", args.benchmark_group))):
                    continue
                if all((limit := getattr(args, "max_" + flag.replace("-", "_"))) is None or (number(value := metric(record, key)) and value <= limit) for flag, key in limits.items()):
                    matches.append(record)
            print(dump(matches), end="")
        elif args.command == "build":
            build(data)
            print(f"Built static catalog and available downloads for {len(data['components'])} configurations.")
        else:
            print(f"Valid catalog: {report['configurations']} configurations, {len(report['warnings'])} availability notes.")
        return 0
    except (ValueError, OSError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
