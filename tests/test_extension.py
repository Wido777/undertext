"""The browser extension ships the same engine as the web checker."""

import json
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ExtensionUpToDate(unittest.TestCase):
    def test_engine_copies_match(self):
        for name in ("rules.js", "promptlink.js", "page.js"):
            with open(os.path.join(ROOT, "docs", name), encoding="utf-8") as a, \
                 open(os.path.join(ROOT, "extension", "lib", name), encoding="utf-8") as b:
                self.assertEqual(a.read(), b.read(), f"extension/lib/{name} is stale: run python scripts/build_extension.py")

    def test_manifest(self):
        with open(os.path.join(ROOT, "extension", "manifest.json"), encoding="utf-8") as fh:
            m = json.load(fh)
        from promptlink import __version__
        self.assertEqual(m["version"], __version__)
        # No API permissions at all: no activeTab, tabs, storage, scripting or network.
        self.assertNotIn("permissions", m)
        for f in m["content_scripts"][0]["js"] + [m["background"]["service_worker"], m["action"]["default_popup"]]:
            self.assertTrue(os.path.exists(os.path.join(ROOT, "extension", f)), f)
        self.assertLessEqual(len(m["description"]), 132)          # Chrome Web Store limit
        for size in ("16", "32", "48", "128"):
            self.assertTrue(os.path.exists(os.path.join(ROOT, "extension", m["icons"][size])), size)
        # Content script only on normal web pages: no file://, no <all_urls>, no host_permissions.
        self.assertEqual(sorted(m["content_scripts"][0]["matches"]), ["http://*/*", "https://*/*"])
        self.assertNotIn("host_permissions", m)
        self.assertNotIn("optional_permissions", m)
        self.assertNotIn("optional_host_permissions", m)

    def test_store_manifests(self):
        import sys
        sys.path.insert(0, os.path.join(ROOT, "scripts"))
        import build_extension as be
        chrome, firefox = be.manifest_for("chrome"), be.manifest_for("firefox")
        # Chrome: service worker only, no Firefox-only keys.
        self.assertEqual(chrome["background"], {"service_worker": "background.js"})
        self.assertNotIn("browser_specific_settings", chrome)
        # Firefox: event page scripts and the add-on id.
        self.assertEqual(firefox["background"], {"scripts": ["background.js"]})
        self.assertIn("gecko", firefox["browser_specific_settings"])
        for m in (chrome, firefox):
            for key in ("permissions", "host_permissions", "optional_permissions", "optional_host_permissions"):
                self.assertNotIn(key, m)
        gecko = firefox["browser_specific_settings"]["gecko"]
        self.assertEqual(gecko["data_collection_permissions"], {"required": ["none"]})
        self.assertGreaterEqual(int(gecko["strict_min_version"].split(".")[0]), 128)   # 127 and older reject the key above
        packaged = be.files()
        self.assertFalse([f for f in packaged if f.startswith("test/")], "demo pages must not ship")
        self.assertFalse([f for f in packaged if f.endswith(("~", ".bak", ".swp", ".DS_Store", ".md"))], packaged)
        for f in ("background.js", "content.js", "popup.html", "popup.js", "popup.css", "lib/rules.js",
                  "lib/promptlink.js", "lib/page.js", "icons/icon128.png"):
            self.assertIn(f, packaged)

    def test_no_risky_apis(self):
        """The extension's own scripts never store, send, inject or render page data as HTML."""
        import glob
        import re
        banned = [r"\bchrome\.storage\b", r"\bbrowser\.storage\b", r"\bapi\.storage\b", r"executeScript",
                  r"\bscripting\.", r"\bfetch\s*\(", r"XMLHttpRequest", r"\.innerHTML\b", r"\.outerHTML\s*=",
                  r"insertAdjacentHTML", r"\beval\s*\(", r"new\s+Function\b", r"WebSocket", r"sendBeacon"]
        files = sorted(glob.glob(os.path.join(ROOT, "extension", "*.js")))
        self.assertTrue(files)
        for path in files:
            with open(path, encoding="utf-8") as fh:
                src = fh.read()
            for pat in banned:
                self.assertIsNone(re.search(pat, src), f"{os.path.basename(path)} uses {pat}")


if __name__ == "__main__":
    unittest.main()
