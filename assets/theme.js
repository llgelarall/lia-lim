"use strict";

(() => {
  const root = document.documentElement;
  const storageKey = "lia-lim-theme";
  const preference = window.matchMedia("(prefers-color-scheme: dark)");
  let savedTheme = null;
  let printTheme = null;
  try {
    const value = localStorage.getItem(storageKey);
    if (value === "light" || value === "dark") savedTheme = value;
  } catch { /* System preference still works when storage is unavailable. */ }

  function applyTheme(theme) {
    root.dataset.theme = theme;
    const dark = theme === "dark";
    const toggle = document.getElementById("theme-toggle");
    if (toggle) {
      toggle.hidden = false;
      toggle.setAttribute("aria-pressed", String(dark));
      toggle.title = `Switch to ${dark ? "light" : "dark"} theme`;
      toggle.querySelector(".theme-state").textContent = dark ? "On" : "Off";
    }
    document.querySelectorAll("source[data-dark-plot]").forEach(source => {
      source.media = dark ? "screen" : "not all";
    });
    document.querySelectorAll("a[data-light-download][data-dark-download]").forEach(link => {
      link.href = dark ? link.dataset.darkDownload : link.dataset.lightDownload;
    });
    const browserColor = document.querySelector('meta[name="theme-color"]');
    if (browserColor) browserColor.content = dark ? "#151817" : "#fbfcfd";
  }

  const preferredTheme = () => savedTheme || (preference.matches ? "dark" : "light");
  applyTheme(preferredTheme()); // Set the theme before the stylesheet is painted.

  function initialize() {
    applyTheme(preferredTheme());
    document.getElementById("theme-toggle")?.addEventListener("click", () => {
      savedTheme = root.dataset.theme === "dark" ? "light" : "dark";
      try { localStorage.setItem(storageKey, savedTheme); } catch { /* Keep the in-page choice. */ }
      applyTheme(savedTheme);
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initialize, {once: true});
  else initialize();

  preference.addEventListener("change", () => {
    if (!savedTheme && !printTheme) applyTheme(preferredTheme());
  });
  window.addEventListener("storage", event => {
    if (event.key !== storageKey && event.key !== null) return;
    savedTheme = event.newValue === "light" || event.newValue === "dark" ? event.newValue : null;
    if (!printTheme) applyTheme(preferredTheme());
  });
  window.addEventListener("beforeprint", () => {
    printTheme = root.dataset.theme;
    applyTheme("light");
  });
  window.addEventListener("afterprint", () => {
    printTheme = null;
    applyTheme(preferredTheme());
  });
})();
