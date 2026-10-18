"""The store zips contain what the manifest needs, and the extension keeps the
promises made in the privacy policy (no permissions, no network, no storage)."""

import json
import os
import re
import sys
import tempfile
import unittest
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXT = os.path.join(ROOT, "extension")


def _build_extension():
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import build_extension as be
    return be


def _referenced_files(m: dict) -> set[str]:
    refs = set()
    for cs in m.get("content_scripts", []):
        refs.update(cs.get("js", []))
        refs.update(cs.get("css", []))
    bg = m.get("background", {})
    if "service_worker" in bg:
        refs.add(bg["service_worker"])
    refs.update(bg.get("scripts", []))
    refs.add(m["action"]["default_popup"])
    refs.update(m["action"].get("default_icon", {}).values())
    refs.update(m.get("icons", {}).values())
    return refs


class StoreZips(unittest.TestCase):
    def test_zips_are_complete_and_browser_specific(self):
        be = _build_extension()
        old_root = be.ROOT
        with tempfile.TemporaryDirectory() as tmp:
            be.ROOT = tmp                      # write dist/ into a temp dir, read sources from extension/
            try:
                for browser in be.BROWSERS:
                    path = be.package(browser)
                    version = be.load_manifest()["version"]
                    self.assertEqual(os.path.basename(path), f"promptlink-extension-{version}-{browser}.zip")
                    with zipfile.ZipFile(path) as z:
                        names = z.namelist()
                        self.assertIsNone(z.testzip())
                        m = json.loads(z.read("manifest.json"))
                    self.assertEqual(m, be.manifest_for(browser))
                    self.assertEqual(names.count("manifest.json"), 1)
                    self.assertFalse([n for n in names if "\\" in n], "zip paths must use /")
                    self.assertFalse([n for n in names if n.startswith("test/")], "demo pages must not ship")
                    self.assertFalse([n for n in names if os.path.basename(n).startswith(".")])
                    missing = _referenced_files(m) - set(names)
                    self.assertFalse(missing, f"{browser} zip is missing files the manifest uses: {missing}")
                    # popup.html's own scripts and stylesheet must ship too.
                    with open(os.path.join(EXT, "popup.html"), encoding="utf-8") as fh:
                        popup = fh.read()
                    for ref in re.findall(r'(?:src|href)="([^":]+)"', popup):
                        self.assertIn(ref, names, f"popup.html uses {ref}")
            finally:
                be.ROOT = old_root


class PrivacyPromises(unittest.TestCase):
    def _js(self):
        out = {}
        for base, _, names in os.walk(EXT):
            if os.path.relpath(base, EXT).split(os.sep)[0] == "test":
                continue
            for n in names:
                if n.endswith(".js"):
                    with open(os.path.join(base, n), encoding="utf-8") as fh:
                        out[os.path.relpath(os.path.join(base, n), EXT)] = fh.read()
        return out

    def test_no_network_storage_or_injection_apis(self):
        banned = [r"\bfetch\s*\(", r"XMLHttpRequest", r"sendBeacon", r"\bWebSocket\b", r"EventSource",
                  r"localStorage", r"sessionStorage", r"indexedDB", r"\.storage\.", r"\.scripting\.",
                  r"\.cookies\.", r"\.innerHTML\b", r"\.outerHTML\s*=", r"insertAdjacentHTML", r"\beval\s*\(",
                  r"new\s+Function\s*\("]
        for path, src in self._js().items():
            for pat in banned:
                self.assertIsNone(re.search(pat, src), f"{path} uses {pat}")

    def test_docs_do_not_claim_removed_permissions(self):
        with open(os.path.join(EXT, "manifest.json"), encoding="utf-8") as fh:
            m = json.load(fh)
        self.assertNotIn("permissions", m)
        for doc in ("docs/privacy.html", "README.md"):
            with open(os.path.join(ROOT, doc), encoding="utf-8") as fh:
                text = fh.read()
            self.assertNotIn("activeTab", text, f"{doc} still mentions activeTab")
        with open(os.path.join(ROOT, "docs", "privacy.html"), encoding="utf-8") as fh:
            self.assertNotIn("local files", fh.read(), "privacy.html still says it runs on local files")


if __name__ == "__main__":
    unittest.main()
