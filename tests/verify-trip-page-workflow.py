import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "trip-page.py"


class TripPageWorkflowTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(prefix="triphelper-page-")
        self.project_root = Path(self.temp_dir.name)
        shutil.copy2(ROOT / "index.html", self.project_root / "index.html")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_cli(self, *args: str, expect_success: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), *args, "--project-root", str(self.project_root)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env={**os.environ, "PYTHONUTF8": "1"},
        )
        if expect_success and result.returncode != 0:
            self.fail(f"CLI failed ({result.returncode}):\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
        return result

    def test_create_generates_complete_data_driven_pwa(self) -> None:
        self.run_cli(
            "create",
            "--id",
            "20270403-kyoto",
            "--name",
            "2027 京都親子行程",
            "--short-name",
            "京都行程",
            "--start-date",
            "2027-04-03",
            "--end-date",
            "2027-04-05",
            "--summary",
            "三天兩夜的京都散步與親子體驗。",
        )

        expected_paths = [
            "data/trips/20270403-kyoto.yaml",
            "trips/20270403-kyoto.md",
            "20270403/index.html",
            "20270403/styles.css",
            "20270403/app.js",
            "20270403/data.generated.json",
            "20270403/data.fallback.js",
            "20270403/manifest.webmanifest",
            "20270403/service-worker.js",
            "20270403/icons/icon.svg",
        ]
        for relative_path in expected_paths:
            self.assertTrue((self.project_root / relative_path).is_file(), relative_path)

        generated = json.loads((self.project_root / "20270403/data.generated.json").read_text(encoding="utf-8"))
        self.assertEqual(generated["trip"]["id"], "20270403-kyoto")
        self.assertEqual(len(generated["days"]), 3)

        page = (self.project_root / "20270403/index.html").read_text(encoding="utf-8")
        self.assertIn('data-ui="trip-wayfinder"', page)
        self.assertIn("2027 京都親子行程", page)
        self.assertNotIn("沖繩", page)

        stylesheet = (self.project_root / "20270403/styles.css").read_text(encoding="utf-8")
        self.assertIn("--color-cobalt", stylesheet)
        self.assertIn("prefers-reduced-motion", stylesheet)

        root_page = (self.project_root / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="./20270403/"', root_page)

    def test_build_refreshes_all_data_artifacts_and_verify_accepts_them(self) -> None:
        self.run_cli(
            "create",
            "--id",
            "20270403-kyoto",
            "--name",
            "2027 京都親子行程",
            "--short-name",
            "京都行程",
            "--start-date",
            "2027-04-03",
            "--end-date",
            "2027-04-05",
        )
        source = self.project_root / "data/trips/20270403-kyoto.yaml"
        trip = yaml.safe_load(source.read_text(encoding="utf-8"))
        trip["days"][0]["title"] = "抵達京都，沿鴨川散步"
        source.write_text(yaml.safe_dump(trip, allow_unicode=True, sort_keys=False), encoding="utf-8", newline="\n")
        old_service_worker = (self.project_root / "20270403/service-worker.js").read_text(encoding="utf-8")

        self.run_cli("build", "--id", "20270403-kyoto")
        self.run_cli("verify", "--id", "20270403-kyoto")

        generated = json.loads((self.project_root / "20270403/data.generated.json").read_text(encoding="utf-8"))
        self.assertEqual(generated["days"][0]["title"], "抵達京都，沿鴨川散步")
        fallback = (self.project_root / "20270403/data.fallback.js").read_text(encoding="utf-8")
        self.assertIn("抵達京都，沿鴨川散步", fallback)
        new_service_worker = (self.project_root / "20270403/service-worker.js").read_text(encoding="utf-8")
        self.assertNotEqual(new_service_worker, old_service_worker)

    def test_create_refuses_to_overwrite_an_existing_trip(self) -> None:
        create_args = (
            "create",
            "--id",
            "20270403-kyoto",
            "--name",
            "2027 京都親子行程",
            "--short-name",
            "京都行程",
            "--start-date",
            "2027-04-03",
            "--end-date",
            "2027-04-05",
        )
        self.run_cli(*create_args)
        source = self.project_root / "data/trips/20270403-kyoto.yaml"
        before = source.read_bytes()

        result = self.run_cli(*create_args, expect_success=False)

        self.assertEqual(result.returncode, 2)
        self.assertIn("拒絕覆寫既有行程", result.stderr)
        self.assertEqual(source.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
