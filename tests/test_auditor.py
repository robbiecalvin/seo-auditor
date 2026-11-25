import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace
from seo_auditor.auditor import SEOAuditor

BASE = "https://example.com"
PAGES = {
    BASE: '<title>Fixture title</title><meta name="description" content="Fixture description"><h1>Home</h1><img src="missing.png"><a href="/second">Next</a><a href="/missing">Missing</a>',
    BASE + "/second": '<title>Fixture title</title><meta name="description" content="Fixture description"><h1>Second</h1><img src="ok.png" alt="Example">',
}

def get(url, **kwargs):
    return SimpleNamespace(status_code=200 if url in PAGES else 404, text=PAGES.get(url, ""))

def head(url, **kwargs):
    return SimpleNamespace(status_code=200 if url in PAGES else 404)

class AuditorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        # Freeze domain extraction to the synthetic fixture; no public suffix download.
        extract = patch("seo_auditor.auditor.tldextract.extract", return_value=SimpleNamespace(domain="example"))
        extract.start()
        self.addCleanup(extract.stop)
        for name, fn in (("get", get), ("head", head)):
            mock = patch("seo_auditor.auditor.requests." + name, side_effect=fn)
            mock.start()
            self.addCleanup(mock.stop)
        self.auditor = SEOAuditor(BASE, output_dir=self.temp.name)
        self.auditor.crawl()

    def test_crawl_and_status(self):
        self.assertEqual(self.auditor.visited, {BASE, BASE + "/second", BASE + "/missing"})
        self.assertEqual([p["Status Code"] for p in self.auditor.page_data], [200, 200, 404])

    def test_metadata_and_images(self):
        page = self.auditor.page_data[0]
        self.assertEqual(page["Title"], "Fixture title")
        self.assertEqual(page["Meta Description"], "Fixture description")
        self.assertEqual(page["H1 Tags"], 1)
        self.assertEqual(page["Missing ALT Images"], 1)

    def test_broken_links(self):
        self.assertEqual(self.auditor.page_data[0]["Broken Links List"], [BASE + "/missing"])

    def test_duplicates(self):
        self.assertEqual(self.auditor.duplicate_check["title"]["Fixture title"], [BASE, BASE + "/second"])
        self.assertEqual(len(self.auditor.duplicate_check["meta"]["Fixture description"]), 2)

    def test_reports(self):
        csv_path, html_path = self.auditor.save_report()
        with open(csv_path, newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["Title"], "Fixture title")
        self.assertIn("Fixture title", Path(html_path).read_text(encoding="utf-8"))
