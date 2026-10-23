"use strict";

(() => {
  const byId = (id) => document.getElementById(id);
  let records;
  try {
    records = JSON.parse(byId("catalog-data").textContent).components;
  } catch {
    return; // Static single-LPL tables and downloads remain usable.
  }
  const isNumber = (value) => typeof value === "number" && Number.isFinite(value);
  const kinds = ["adder", "multiplier"];
  const state = new Map();

  function metric(record, key) {
    const error = record.error || {};
    if (key === "abs_me") return isNumber(error.me) ? Math.abs(error.me) : null;
    if (key === "wce") return isNumber(error.min) && isNumber(error.max) ? Math.max(Math.abs(error.min), Math.abs(error.max)) : null;
    if (key === "timing") return isNumber(record.reported_timing_ns) ? record.reported_timing_ns : record.ppa?.delay;
    return ["area", "power", "delay"].includes(key) ? record.ppa?.[key] : error[key];
  }

  function setTab(kind, focus = false) {
    for (const current of kinds) {
      const selected = current === kind;
      const button = byId(`tab-${current}`);
      button.setAttribute("aria-selected", String(selected));
      button.tabIndex = selected ? 0 : -1;
      byId(`panel-${current}`).hidden = !selected;
    }
    if (focus) byId(`tab-${kind}`).focus();
  }

  function updateLevels(kind, preferred) {
    const select = byId(`${kind}-lpl`);
    const previous = preferred ?? select.value;
    const width = Number(byId(`${kind}-width`).value);
    const levels = [...new Set(records.filter((r) => r.kind === kind && r.width === width).map((r) => r.lpl).filter((v) => v !== null && v !== undefined))].sort((a, b) => a - b);
    const selected = levels.includes(Number(previous)) ? Number(previous) : levels.includes(4) ? 4 : levels[0];
    select.replaceChildren(...(levels.length ? levels.map((level) => new Option(String(level), String(level), level === selected, level === selected)) : [new Option("No LPL supplied", "")]));
  }

  function withinLimit(record, key, input) {
    if (!input.value.trim()) return true;
    const limit = Number(input.value), value = metric(record, key);
    return Number.isFinite(limit) && limit >= 0 && isNumber(value) && value <= limit;
  }

  function draw(kind) {
    const get = (suffix) => byId(`${kind}-${suffix}`);
    const width = Number(get("width").value), level = Number(get("lpl").value);
    const query = get("query").value.trim().toLowerCase();
    const available = records.filter((r) => r.kind === kind && r.width === width && r.lpl === level);
    const filtered = available.filter((r) =>
      `${r.id} ${r.architecture} ${JSON.stringify(r.parameters || {})}`.toLowerCase().includes(query) &&
      withinLimit(r, get("error-metric").value, get("max-error")) &&
      withinLimit(r, "area", get("max-area")) && withinLimit(r, "power", get("max-power")) &&
      withinLimit(r, "delay", get("max-delay"))
    ).sort((a, b) => {
      const key = get("sort").value;
      if (key !== "id") {
        const av = metric(a, key), bv = metric(b, key);
        if (!isNumber(av) && isNumber(bv)) return 1;
        if (isNumber(av) && !isNumber(bv)) return -1;
        if (isNumber(av) && isNumber(bv) && av !== bv) return av - bv;
      }
      return a.id.localeCompare(b.id);
    });
    const rowMap = state.get(kind).rows;
    const nodes = filtered.map((r) => rowMap.get(r.id)).filter(Boolean);
    if (!nodes.length) {
      const row = document.createElement("tr");
      const cell = document.createElement("td");
      cell.colSpan = 14;
      cell.className = "empty-state";
      cell.textContent = available.length ? "No configurations match these limits. Adjust the filters or reset this table." : "No configurations are supplied for this width and LPL.";
      row.append(cell);
      nodes.push(row);
    }
    byId(`rows-${kind}`).replaceChildren(...nodes);
    get("count").textContent = available.length ? `${filtered.length} of ${available.length} configurations · ${width}-bit operands · LPL ${level}` : "No configurations available";
  }

  for (const kind of kinds) {
    const template = byId(`records-${kind}`);
    const rows = new Map([...template.content.querySelectorAll("tr[data-record-id]")].map((row) => [row.dataset.recordId, row]));
    state.set(kind, {rows, width: byId(`${kind}-width`).value, level: byId(`${kind}-lpl`).value});
    const form = byId(`filters-${kind}`);
    form.addEventListener("submit", (event) => event.preventDefault());
    form.addEventListener("input", (event) => {
      if (event.target.id === `${kind}-width`) updateLevels(kind);
      draw(kind);
    });
    form.addEventListener("reset", () => setTimeout(() => {
      byId(`${kind}-width`).value = state.get(kind).width;
      updateLevels(kind, state.get(kind).level);
      draw(kind);
    }, 0));
    byId(`tab-${kind}`).addEventListener("click", () => setTab(kind));
    byId(`tab-${kind}`).addEventListener("keydown", (event) => {
      if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
      event.preventDefault();
      const next = event.key === "Home" ? "adder" : event.key === "End" ? "multiplier" : kinds[(kinds.indexOf(kind) + 1) % kinds.length];
      setTab(next, true);
    });
    updateLevels(kind);
    draw(kind);
  }
  setTab(location.hash.includes("multiplier") ? "multiplier" : "adder");
  window.addEventListener("hashchange", () => {
    if (location.hash.includes("multiplier")) setTab("multiplier");
    else if (location.hash.includes("adder")) setTab("adder");
  });
})();
