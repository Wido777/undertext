"""Copy the shared engine into the browser extension and package it.

    python scripts/build_extension.py          copy docs/{rules,undertext,page}.js into extension/lib/
    python scripts/build_extension.py --zip    also write one store zip per browser:
                                                 dist/undertext-extension-<version>-chrome.zip
                                                 dist/undertext-extension-<version>-firefox.zip

The extension uses exactly the same generated rules and engine as the web
checker; tests/test_extension.py fails if the copies are out of date.

extension/manifest.json works unpacked in both browsers: Chrome (121+) uses
background.service_worker and ignores background.scripts; Firefox uses
background.scripts. For the store uploads each zip gets a manifest with only
the keys that browser understands, so neither store review shows warnings:

  chrome   drops background.scripts and browser_specific_settings
  firefox  drops background.service_worker

Only an allowlist of files is packaged (see files()); the test/ demo pages,
editor backups and anything else in extension/ are left out.
"""

from __future__ import annotations

import copy as _copy
import json
import os
import shutil
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXT = os.path.join(ROOT, "extension")
SHARED = ("rules.js", "undertext.js", "page.js")
BROWSERS = ("chrome", "firefox")


def copy() -> None:
    os.makedirs(os.path.join(EXT, "lib"), exist_ok=True)
    for name in SHARED:
        shutil.copyfile(os.path.join(ROOT, "docs", name), os.path.join(EXT, "lib", name))


def load_manifest() -> dict:
    with open(os.path.join(EXT, "manifest.json"), encoding="utf-8") as fh:
        return json.load(fh)


def manifest_for(browser: str, m: dict | None = None) -> dict:
    """The manifest that goes into the zip for one browser."""
    m = _copy.deepcopy(m if m is not None else load_manifest())
    bg = m.get("background", {})
    if browser == "chrome":
        bg.pop("scripts", None)
        m.pop("browser_specific_settings", None)
    elif browser == "firefox":
        bg.pop("service_worker", None)
    else:
        raise ValueError(browser)
    return m


def files(m: dict | None = None) -> list[str]:
    """Paths (relative to extension/, "/"-separated) that are packaged, manifest excluded.

    An explicit allowlist: everything the manifest references (scripts, popup,
    icons), the stylesheet and scripts popup.html loads, and the shared engine
    in lib/. Anything else in extension/ (test pages, editor backups, notes)
    is never shipped. A missing file is an error.
    """
    import re
    m = m if m is not None else load_manifest()
    want = set()
    for cs in m.get("content_scripts", []):
        want.update(cs.get("js", []) + cs.get("css", []))
    bg = m.get("background", {})
    if bg.get("service_worker"):
        want.add(bg["service_worker"])
    want.update(bg.get("scripts", []))
    action = m.get("action", {})
    want.update(action.get("default_icon", {}).values())
    want.update(m.get("icons", {}).values())
    popup = action.get("default_popup")
    if popup:
        want.add(popup)
        with open(os.path.join(EXT, popup), encoding="utf-8") as fh:
            html = fh.read()
        want.update(re.findall(r'<(?:script|link)\b[^>]*\b(?:src|href)="([^":]+)"', html))
    want.update("lib/" + name for name in SHARED)
    missing = sorted(f for f in want if not os.path.isfile(os.path.join(EXT, f)))
    if missing:
        raise FileNotFoundError("extension files referenced but missing: " + ", ".join(missing))
    return sorted(want)


def package(browser: str) -> str:
    m = manifest_for(browser)
    os.makedirs(os.path.join(ROOT, "dist"), exist_ok=True)
    out = os.path.join(ROOT, "dist", f"undertext-extension-{m['version']}-{browser}.zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("manifest.json", json.dumps(m, indent=2) + "\n")
        for rel in files(m):
            z.write(os.path.join(EXT, rel), rel)
    return out


if __name__ == "__main__":
    copy()
    print("copied shared engine into extension/lib/")
    if "--zip" in sys.argv:
        for b in BROWSERS:
            print("wrote", os.path.relpath(package(b), ROOT))
