"""Static, accessible family tables and comparison figures for the website."""
import html
import json


def esc(value):
    return html.escape(str(value),quote=True)


def default_setting(records):
    benchmark=next((r for r in records if r.get("source_comparison")),None)
    if benchmark:
        return benchmark["width"],benchmark["lpl"]
    if not records:
        return None,None
    width=min(r["width"] for r in records)
    levels=sorted({r["lpl"] for r in records if r["width"]==width and r.get("lpl") is not None})
    return width,4 if 4 in levels else levels[0] if levels else None


def family_panels(data,links,downloads,row_html):
    panels=[]
    for kind,title in (("adder","LIA adders"),("multiplier","LIM multipliers")):
        records=[r for r in data["components"] if r["kind"]==kind]
        width,level=default_setting(records)
        selected=[r for r in records if r["width"]==width and r.get("lpl")==level]
        widths=sorted({r["width"] for r in records})
        levels=sorted({r["lpl"] for r in records if r["width"]==width and r.get("lpl") is not None})
        width_options=''.join(f'<option value="{v}"{" selected" if v==width else ""}>{v}-bit operands</option>' for v in widths) or '<option value="">No widths supplied</option>'
        level_options=''.join(f'<option value="{v}"{" selected" if v==level else ""}>{v}</option>' for v in levels) or '<option value="">No LPL supplied</option>'
        body='\n'.join(row_html(r,links[r["id"]]) for r in selected) or '<tr><td colspan="14" class="empty-state"><strong>No released configurations in this checkout.</strong></td></tr>'
        all_rows='\n'.join(row_html(r,links[r["id"]]) for r in records)
        count=f'{len(selected)} configurations shown · N={width}, LPL={level}' if selected else 'No configurations available'
        panels.append(f'''<div id="panel-{kind}" class="family-panel" role="tabpanel" aria-labelledby="tab-{kind}" tabindex="0" data-kind="{kind}">
  <div class="family-heading"><h2>{title}</h2>{downloads[kind]}</div>
  <p class="objective-legend">Vertical badges identify the ME, MAE, MSE, or PE design targets in the original function names. The MAE/PE adder carries both badges. Targets describe design intent; Pareto optimality depends on the evaluated workload and constraints.</p>
  <form id="filters-{kind}" class="filters family-filters" role="search" aria-label="Filter {title}">
    <label>Operand width<select id="{kind}-width">{width_options}</select></label>
    <label>LPL<select id="{kind}-lpl">{level_options}</select></label>
    <label class="search-label">Component or architecture<input id="{kind}-query" type="search" placeholder="Search {kind}s" autocomplete="off"></label>
    <label>Sort by<select id="{kind}-sort"><option value="id">Component</option><option value="mae">MAE, ascending</option><option value="mse">MSE, ascending</option><option value="pe">PE, ascending</option><option value="area">Area, ascending</option><option value="power">Power, ascending</option><option value="timing">Reported timing, ascending</option></select></label>
    <details class="constraint-controls"><summary>Set error and hardware limits</summary><div class="limits">
      <label>Error criterion<select id="{kind}-error-metric"><option value="mae">MAE</option><option value="mse">MSE</option><option value="pe">PE (fraction)</option><option value="abs_me">Absolute ME</option><option value="wce">Worst absolute error</option></select></label>
      <label>Maximum error<input id="{kind}-max-error" type="number" min="0" step="any" placeholder="No limit"></label>
      <label>Maximum area (µm²)<input id="{kind}-max-area" type="number" min="0" step="any" placeholder="No limit"></label>
      <label>Maximum power (µW)<input id="{kind}-max-power" type="number" min="0" step="any" placeholder="No limit"></label>
      <label>Maximum physical delay (ns)<input id="{kind}-max-delay" type="number" min="0" step="any" placeholder="Unverified"></label>
    </div><p class="small muted">Unknown measurements cannot satisfy a limit. Raw reported timing has no confirmed path definition and is excluded from physical-delay constraints.</p></details>
    <div class="filter-footer"><p id="{kind}-count" role="status" aria-live="polite">{count}</p><button type="reset" class="text-button">Reset this table</button></div>
  </form>
  <div class="table-scroll" tabindex="0" role="region" aria-label="{title} measurements; scroll horizontally for all columns">
    <table class="component-table" id="table-{kind}">
      <caption class="sr-only">{title}: one operand width and one LPL setting, error metrics, reported hardware cost, downloads and provenance.</caption>
      <thead><tr><th scope="col" rowspan="2">Component / architecture</th><th scope="col" rowspan="2">Width</th><th scope="col" rowspan="2">LPL</th><th scope="colgroup" colspan="6">Numerical error</th><th scope="colgroup" colspan="3">Reported hardware cost</th><th scope="col" rowspan="2">Source code</th><th scope="col" rowspan="2">Provenance</th></tr>
        <tr><th scope="col">ME</th><th scope="col">MSE</th><th scope="col">MAE</th><th scope="col">PE</th><th scope="col">Max error</th><th scope="col">Min error</th><th scope="col">Area<small>µm²</small></th><th scope="col">Power<small>µW</small></th><th scope="col">Timing †<small>ns, as reported</small></th></tr></thead>
      <tbody id="rows-{kind}">{body}</tbody>
      <tfoot><tr><td colspan="14" id="metrics-{kind}" class="table-footnotes">
        <p><strong>Numerical error.</strong> For e = approximate − exact: ME = mean(e), MSE = mean(e²), MAE = mean(|e|), PE = fraction(e ≠ 0). Min/max are signed extrema; worst absolute error = max(|min|, |max|). Error uses output units; MSE uses output units²; PE is a fraction from 0 to 1.</p>
        <p><strong>PPA.</strong> Area and power retain the source CSV’s µm² and total µW at the supplied benchmark settings. The maintainer reports Yosys/ABC mapping to Nangate45 and pre-layout OpenSTA within OpenROAD with identical timing, loading, and switching-activity assumptions; see the <a href="#benchmark-methodology">comparison methodology</a>. Tool versions, corner, numerical constraints/activity, and timing-path definition were not supplied. † Timing retains <code>delay_ns</code> verbatim; negative values are not physical propagation delays. Missing measurements are shown as a dash.</p>
        <p>One width and LPL are shown at a time. Numerical metrics were checked exhaustively against C; <a href="result/validation/index.html">reports and full-precision values</a> record the tested domain. CSV signed errors were converted from exact − approximate and checked against C; PPA values were not copied to other LPLs. <a href="data/comparison-import-report.json">Import findings</a>.</p>
      </td></tr></tfoot>
    </table>
  </div>
  <template id="records-{kind}"><table><tbody>{all_rows}</tbody></table></template>
</div>''')
    return '\n'.join(panels)


def comparison_plots(data):
    if not data:
        return '<p class="muted">No comparison dataset supplied.</p>'
    output=[]
    labels={"area":"Area","power":"Power","timing":"Reported timing"}
    for benchmark in data["benchmarks"]:
        figures=[]
        for metric in ("area","power","timing"):
            chart=benchmark["plots"][metric]
            counts=', '.join(f'{library}: n={n}' for library,n in chart["counts"].items())
            dark_source=f'<source data-dark-plot media="screen and (prefers-color-scheme: dark)" srcset="{esc(chart["dark_svg"])}">' if chart.get("dark_svg") else ''
            download_attributes=lambda fmt: f'data-light-download="{esc(chart[fmt])}" data-dark-download="{esc(chart.get("dark_"+fmt,chart[fmt]))}"'
            figures.append(f'''<figure class="comparison-figure"><picture>{dark_source}<img src="{esc(chart['svg'])}" alt="{esc(labels[metric])}: {esc(benchmark['description'])}; {esc(counts)}; values sorted independently within each library" width="430" height="300" loading="lazy"></picture><figcaption>{esc(labels[metric])} · <a href="{esc(chart['svg'])}" {download_attributes('svg')} download aria-label="{esc(benchmark['library'])} {metric} plot as SVG">SVG</a> / <a href="{esc(chart['png'])}" {download_attributes('png')} download aria-label="{esc(benchmark['library'])} {metric} plot as PNG">PNG</a></figcaption></figure>''')
        excluded=sorted({e["module"] for chart in benchmark["plots"].values() for e in chart["exclusions"]})
        missing=f' Missing PPA measurements: {esc(", ".join(excluded))}; omitted from the relevant curves.' if excluded else ''
        negative=any(row["values"]["timing"] is not None and row["values"]["timing"]<0 for row in benchmark["rows"])
        timing_note=' Negative timing values are retained; their physical meaning is unresolved.' if negative else ' The timing-path definition was not supplied.'
        output.append(f'''<article class="comparison-group"><h3>{esc(benchmark['description'])}</h3><div class="comparison-grid">{''.join(figures)}</div><p class="small muted"><a href="{esc(benchmark['source_file'])}" download>Source comparison CSV</a>.{missing}{timing_note}</p></article>''')
    return '\n'.join(output)
