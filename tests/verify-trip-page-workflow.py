import json
import os
import re
import runpy
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
            "--style",
            "coastal-breeze",
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
        self.assertEqual(generated["trip"]["style"], "coastal-breeze")
        self.assertEqual(len(generated["days"]), 3)

        page = (self.project_root / "20270403/index.html").read_text(encoding="utf-8")
        self.assertIn('data-ui="trip-wayfinder"', page)
        self.assertIn('data-style="coastal-breeze"', page)
        self.assertIn("2027 京都親子行程", page)
        self.assertNotIn("沖繩", page)

        stylesheet = (self.project_root / "20270403/styles.css").read_text(encoding="utf-8")
        self.assertIn("--primitive-primary", stylesheet)
        self.assertIn(':root[data-style="heritage-ink"]', stylesheet)
        self.assertIn(':root[data-style="berry-picnic"]', stylesheet)
        self.assertIn(':root[data-style="doodle-notebook"]', stylesheet)
        self.assertIn(':root[data-style="travel-toon-cards"]', stylesheet)
        self.assertIn("--hero-background: radial-gradient", stylesheet)
        self.assertIn("--timeline-card-background: color-mix", stylesheet)
        self.assertIn("--day-tab-active-shadow", stylesheet)
        self.assertIn("prefers-reduced-motion", stylesheet)

        manifest = json.loads((self.project_root / "20270403/manifest.webmanifest").read_text(encoding="utf-8"))
        self.assertEqual(manifest["background_color"], "#edf8fa")
        self.assertEqual(manifest["theme_color"], "#087e9b")

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

    def test_each_supported_style_creates_and_verifies(self) -> None:
        styles = {
            "editorial-wayfinder": ("20280101-editorial", "#2457d6"),
            "coastal-breeze": ("20280102-coastal", "#087e9b"),
            "alpine-field-notes": ("20280103-alpine", "#2f6845"),
            "neon-metro": ("20280104-metro", "#6038d5"),
            "heritage-ink": ("20280105-heritage", "#76523b"),
            "candy-postcard": ("20280106-candy", "#9d2c67"),
            "cloud-storybook": ("20280107-cloud", "#2369a8"),
            "sticker-playground": ("20280108-sticker", "#cf2862"),
            "berry-picnic": ("20280109-berry", "#7f2d4f"),
            "comic-panel": ("20280110-comic", "#b7242a"),
            "cel-adventure": ("20280111-cel", "#147d82"),
            "retro-toon": ("20280112-retro", "#146b70"),
            "doodle-notebook": ("20280113-doodle", "#245a86"),
            "travel-toon-cards": ("20280114-toon", "#0f766e"),
            "aurora-frost": ("20280115-aurora", "#18547a"),
            "savanna-safari": ("20280116-safari", "#81510f"),
            "ancient-odyssey": ("20280117-ancient", "#825316"),
            "tokyo-pulse": ("20280118-tokyo", "#075d80"),
            "coral-dive": ("20280119-coral", "#0b7182"),
            "sakura-promenade": ("20280120-sakura", "#9d3e5b"),
            "tropical-lagoon": ("20280121-lagoon", "#08717d"),
            "golden-boulevard": ("20280122-golden", "#925008"),
            "alpine-railway": ("20280123-railway", "#2c6f46"),
            "sunset-street-food": ("20280124-street-food", "#9d3d2a"),
        }
        registry = runpy.run_path(str(SCRIPT))["STYLE_PROFILES"]
        self.assertEqual(set(registry), set(styles))
        for style, (trip_id, theme_color) in styles.items():
            with self.subTest(style=style):
                date_prefix = trip_id[:8]
                iso_date = f"{date_prefix[:4]}-{date_prefix[4:6]}-{date_prefix[6:]}"
                self.run_cli(
                    "create",
                    "--id",
                    trip_id,
                    "--name",
                    f"{style} 行程",
                    "--short-name",
                    "測試行程",
                    "--start-date",
                    iso_date,
                    "--end-date",
                    iso_date,
                    "--style",
                    style,
                )
                self.run_cli("verify", "--id", trip_id)
                site_root = self.project_root / date_prefix
                page = (site_root / "index.html").read_text(encoding="utf-8")
                stylesheet = (site_root / "styles.css").read_text(encoding="utf-8")
                manifest = json.loads((site_root / "manifest.webmanifest").read_text(encoding="utf-8"))
                self.assertIn(f'data-style="{style}"', page)
                self.assertEqual(manifest["theme_color"], theme_color)
                self.assertEqual(manifest["background_color"], registry[style]["background_color"])
                self.assertIn(f':root[data-style="{style}"]', stylesheet)
                if style != "editorial-wayfinder":
                    self.assertIn(f':root[data-theme="dark"][data-style="{style}"]', stylesheet)

    def test_style_registry_design_docs_and_previews_stay_in_sync(self) -> None:
        registry = set(runpy.run_path(str(SCRIPT))["STYLE_PROFILES"])
        stylesheet = (ROOT / "templates/trip-pwa/styles.css").read_text(encoding="utf-8")
        light_styles = set(re.findall(r':root\[data-style="([^"]+)"\]\s*\{', stylesheet))
        dark_styles = set(re.findall(r':root\[data-theme="dark"\]\[data-style="([^"]+)"\]\s*\{', stylesheet))
        doc_styles = {path.stem for path in (ROOT / "design-system/triphelper-next/styles").glob("*.md")}
        preview_root = ROOT / "design-system/triphelper-next/previews"
        preview_styles = {path.name for path in preview_root.iterdir() if path.is_dir()}
        catalog = (preview_root / "index.html").read_text(encoding="utf-8")
        catalog_styles = set(re.findall(r'<span class="style-id">([^<]+)</span>', catalog))
        preview_readme = (preview_root / "README.md").read_text(encoding="utf-8")
        readme_styles = set(re.findall(r'^\| `([^`]+)` \|', preview_readme, flags=re.MULTILINE))

        self.assertEqual(len(registry), 24)
        self.assertEqual(light_styles, registry)
        self.assertEqual(dark_styles, registry - {"editorial-wayfinder"})
        self.assertEqual(doc_styles, registry)
        self.assertEqual(preview_styles, registry)
        self.assertEqual(catalog_styles, registry)
        self.assertEqual(readme_styles, registry)

        illustrated_styles = {
            "aurora-frost",
            "savanna-safari",
            "ancient-odyssey",
            "tokyo-pulse",
            "coral-dive",
            "sakura-promenade",
            "tropical-lagoon",
            "golden-boulevard",
            "alpine-railway",
            "sunset-street-food",
        }
        for style in illustrated_styles:
            block = re.search(rf':root\[data-style="{re.escape(style)}"\]\s*\{{(.*?)\n\}}', stylesheet, flags=re.DOTALL)
            self.assertIsNotNone(block, style)
            self.assertIn("--hero-scene-background:", block.group(1))
            self.assertIn("--hero-orbit-background:", block.group(1))

        expected_images = {"mobile-light.png", "desktop-light.png", "mobile-dark.png"}
        for style in registry:
            with self.subTest(preview=style):
                self.assertEqual({path.name for path in (preview_root / style).glob("*.png")}, expected_images)
        for relative_path in re.findall(r'(?:href|src)="\.\/([^"#?]+\.png)"', catalog):
            self.assertTrue((preview_root / relative_path).is_file(), relative_path)

    def test_build_updates_style_markers_and_manifest(self) -> None:
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
        trip["trip"]["style"] = "heritage-ink"
        source.write_text(yaml.safe_dump(trip, allow_unicode=True, sort_keys=False), encoding="utf-8", newline="\n")

        self.run_cli("build", "--id", "20270403-kyoto")
        self.run_cli("verify", "--id", "20270403-kyoto")

        page = (self.project_root / "20270403/index.html").read_text(encoding="utf-8")
        manifest = json.loads((self.project_root / "20270403/manifest.webmanifest").read_text(encoding="utf-8"))
        generated = json.loads((self.project_root / "20270403/data.generated.json").read_text(encoding="utf-8"))
        self.assertIn('data-style="heritage-ink"', page)
        self.assertEqual(manifest["theme_color"], "#76523b")
        self.assertEqual(generated["trip"]["style"], "heritage-ink")

    def test_build_defaults_legacy_trip_without_style_without_rewriting_source(self) -> None:
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
        del trip["trip"]["style"]
        source.write_text(yaml.safe_dump(trip, allow_unicode=True, sort_keys=False), encoding="utf-8", newline="\n")
        before = source.read_bytes()

        self.run_cli("build", "--id", "20270403-kyoto")
        self.run_cli("verify", "--id", "20270403-kyoto")

        page = (self.project_root / "20270403/index.html").read_text(encoding="utf-8")
        manifest = json.loads((self.project_root / "20270403/manifest.webmanifest").read_text(encoding="utf-8"))
        self.assertEqual(source.read_bytes(), before)
        self.assertIn('data-style="editorial-wayfinder"', page)
        self.assertEqual(manifest["theme_color"], "#2457d6")


if __name__ == "__main__":
    unittest.main()
