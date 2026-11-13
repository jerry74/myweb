import json
import os
import re
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date, timedelta
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
        self.assertIn(':root[data-style="coastal-breeze"]', stylesheet)
        self.assertIn(':root[data-theme="dark"][data-style="coastal-breeze"]', stylesheet)
        self.assertNotIn(':root[data-style="heritage-ink"]', stylesheet)
        self.assertNotIn(':root[data-style="travel-toon-cards"]', stylesheet)
        self.assertLess(len(stylesheet), 40_000)
        self.assertIn("--hero-background: radial-gradient", stylesheet)
        self.assertIn("--timeline-card-background: color-mix", stylesheet)
        self.assertIn("--day-tab-active-shadow", stylesheet)
        self.assertIn("prefers-reduced-motion", stylesheet)

        manifest = json.loads((self.project_root / "20270403/manifest.webmanifest").read_text(encoding="utf-8"))
        self.assertEqual(manifest["background_color"], "#edf8fa")
        self.assertEqual(manifest["theme_color"], "#087e9b")

        root_page = (self.project_root / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="./20270403/" data-trip="20270403"', root_page)
        self.assertIn("--card-accent: #087e9b", root_page)
        self.assertNotIn("`/20270403/`", root_page)

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
        registry = runpy.run_path(str(SCRIPT))["STYLE_PROFILES"]
        for index, (style, profile) in enumerate(registry.items()):
            with self.subTest(style=style):
                start = date(2028, 1, 1) + timedelta(days=index)
                trip_id = f"{start:%Y%m%d}-style{index}"
                self.run_cli(
                    "create",
                    "--id",
                    trip_id,
                    "--name",
                    f"{style} 行程",
                    "--start-date",
                    start.isoformat(),
                    "--end-date",
                    start.isoformat(),
                    "--style",
                    style,
                )
                self.run_cli("verify", "--id", trip_id)
                site_root = self.project_root / f"{start:%Y%m%d}"
                page = (site_root / "index.html").read_text(encoding="utf-8")
                stylesheet = (site_root / "styles.css").read_text(encoding="utf-8")
                manifest = json.loads((site_root / "manifest.webmanifest").read_text(encoding="utf-8"))
                self.assertIn(f'data-style="{style}"', page)
                self.assertRegex(profile["theme_color"], r"^#[0-9a-f]{6}$")
                self.assertEqual(manifest["theme_color"], profile["theme_color"])
                self.assertEqual(manifest["background_color"], profile["background_color"])
                self.assertEqual(set(re.findall(r'data-style="([^"]+)"', stylesheet)), {style})
                if style != "editorial-wayfinder":
                    self.assertIn(f':root[data-theme="dark"][data-style="{style}"]', stylesheet)

    def create_kyoto(self, *extra: str) -> Path:
        self.run_cli(
            "create",
            "--id",
            "20270403-kyoto",
            "--name",
            "2027 京都親子行程",
            "--start-date",
            "2027-04-03",
            "--end-date",
            "2027-04-05",
            *extra,
        )
        return self.project_root / "data/trips/20270403-kyoto.yaml"

    def write_source(self, source: Path, data: dict) -> None:
        source.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8", newline="\n")

    def run_repo_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env={**os.environ, "PYTHONUTF8": "1"},
        )

    def test_create_defaults_short_name_and_uses_destination_timezone(self) -> None:
        source = self.create_kyoto("--timezone", "+09:00", "--departure-time", "07:45")
        trip = yaml.safe_load(source.read_text(encoding="utf-8"))["trip"]
        self.assertEqual(trip["shortName"], "2027 京都親子行程")
        self.assertEqual(trip["departureAt"], "2027-04-03T07:45:00+09:00")
        self.assertEqual(trip["endAt"], "2027-04-05T23:59:59+09:00")

        result = self.run_cli(
            "create", "--id", "20270501-osaka", "--name", "大阪", "--start-date", "2027-05-01",
            "--end-date", "2027-05-02", "--timezone", "JST", expect_success=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("--timezone", result.stderr)

    def test_build_rerenders_page_and_home_card_after_rename(self) -> None:
        source = self.create_kyoto()
        data = yaml.safe_load(source.read_text(encoding="utf-8"))
        data["trip"]["name"] = "京都櫻花散步"
        data["trip"]["shortName"] = "京都櫻花"
        data["trip"]["style"] = "sakura-promenade"
        self.write_source(source, data)

        self.run_cli("build", "--id", "20270403-kyoto")
        self.run_cli("verify", "--id", "20270403-kyoto")

        page = (self.project_root / "20270403/index.html").read_text(encoding="utf-8")
        self.assertIn("<title>京都櫻花散步</title>", page)
        stylesheet = (self.project_root / "20270403/styles.css").read_text(encoding="utf-8")
        self.assertEqual(set(re.findall(r'data-style="([^"]+)"', stylesheet)), {"sakura-promenade"})
        root_page = (self.project_root / "index.html").read_text(encoding="utf-8")
        self.assertIn("京都櫻花散步", root_page)
        self.assertNotIn("2027 京都親子行程", root_page)
        self.assertEqual(root_page.count('data-trip="20270403"'), 1)

    def test_build_explains_yaml_mistakes_with_paths(self) -> None:
        source = self.create_kyoto()
        text = source.read_text(encoding="utf-8").replace("time: '14:00'", "time: 14:00", 1)
        text = text.replace("weekday: 六", "weekday: 日", 1)
        source.write_text(text, encoding="utf-8", newline="\n")
        before = (self.project_root / "20270403/data.generated.json").read_bytes()

        result = self.run_cli("build", "--id", "20270403-kyoto", expect_success=False)

        self.assertEqual(result.returncode, 2)
        self.assertIn("days[0].schedule[1].time", result.stderr)
        self.assertIn("'14:00'", result.stderr)
        self.assertIn("days[0].weekday", result.stderr)
        self.assertEqual((self.project_root / "20270403/data.generated.json").read_bytes(), before)

    def test_verify_strict_blocks_placeholder_content(self) -> None:
        self.create_kyoto()
        relaxed = self.run_cli("verify", "--id", "20270403-kyoto")
        self.assertIn("待補", relaxed.stderr)

        strict = self.run_cli("verify", "--id", "20270403-kyoto", "--strict", expect_success=False)
        self.assertEqual(strict.returncode, 2)
        self.assertIn("待補", strict.stderr)

    def test_styles_command_filters_by_keyword(self) -> None:
        result = self.run_repo_cli("styles", "海島")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("coastal-breeze", result.stdout)
        self.assertNotIn("neon-metro", result.stdout)

    def test_gallery_renders_every_style_from_the_full_template(self) -> None:
        out_dir = self.project_root / "gallery"
        result = self.run_repo_cli("gallery", "--out", str(out_dir))
        self.assertEqual(result.returncode, 0, result.stderr)
        registry = runpy.run_path(str(SCRIPT))["STYLE_PROFILES"]
        page = (out_dir / "index.html").read_text(encoding="utf-8")
        for style in registry:
            self.assertIn(f'"id": "{style}"', page)
        stylesheet = (out_dir / "sample/styles.css").read_text(encoding="utf-8")
        self.assertEqual(set(re.findall(r':root\[data-style="([^"]+)"\]', stylesheet)), set(registry))
        app = (out_dir / "sample/app.js").read_text(encoding="utf-8")
        self.assertIn("previewStyle", app)
        self.assertIn("previewTheme", app)

    def test_new_style_scaffolds_registry_css_and_docs(self) -> None:
        design = self.project_root / "design-system/triphelper-next"
        shutil.copytree(ROOT / "design-system/triphelper-next/styles", design / "styles")
        shutil.copy2(ROOT / "design-system/triphelper-next/styles.json", design / "styles.json")
        shutil.copy2(ROOT / "design-system/triphelper-next/MASTER.md", design / "MASTER.md")
        shutil.copytree(ROOT / "templates/trip-pwa", self.project_root / "templates/trip-pwa")

        self.run_cli(
            "new-style", "--id", "harbor-lights", "--label", "港灣燈火", "--base", "coastal-breeze",
            "--fits", "港口夜景", "--theme-color", "#1A5F8A",
        )

        registry = json.loads((design / "styles.json").read_text(encoding="utf-8"))
        entry = registry["styles"][-1]
        self.assertEqual(entry["id"], "harbor-lights")
        self.assertEqual(entry["themeColor"], "#1a5f8a")
        stylesheet = (self.project_root / "templates/trip-pwa/styles.css").read_text(encoding="utf-8")
        self.assertIn(':root[data-style="harbor-lights"]', stylesheet)
        self.assertIn(':root[data-theme="dark"][data-style="harbor-lights"]', stylesheet)
        self.assertIn("--primitive-primary: #1a5f8a;", stylesheet)
        self.assertTrue((design / "styles/harbor-lights.md").is_file())
        self.assertIn("| `harbor-lights` | 港灣燈火 |", (design / "MASTER.md").read_text(encoding="utf-8"))

        duplicate = self.run_cli("new-style", "--id", "harbor-lights", "--label", "重複", expect_success=False)
        self.assertEqual(duplicate.returncode, 2)

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

        master = (ROOT / "design-system/triphelper-next/MASTER.md").read_text(encoding="utf-8")
        master_styles = set(re.findall(r'^\| `([^`]+)` \|', master, flags=re.MULTILINE))
        skill = (ROOT / ".codex/skills/trip-page-creator/SKILL.md").read_text(encoding="utf-8")
        static_previews = preview_styles - {"live"}

        self.assertEqual(light_styles, registry)
        self.assertEqual(dark_styles, registry - {"editorial-wayfinder"})
        self.assertEqual(doc_styles, registry)
        self.assertEqual(master_styles, registry)
        # Static screenshots are optional now that `gallery` renders every style live,
        # but the catalog, README and image folders must still agree with each other.
        self.assertLessEqual(static_previews, registry)
        self.assertEqual(catalog_styles, static_previews)
        self.assertEqual(readme_styles, static_previews)
        self.assertNotRegex(skill, r"(?m)^- `[a-z-]+`：", "SKILL.md 不應再手抄風格清單，請改用 styles 指令")

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
            "desert-caravan",
            "nordic-fjord",
            "carnival-parade",
            "forest-fairytale",
            "cosmic-camp",
            "treasure-island",
        }
        for style in illustrated_styles:
            block = re.search(rf':root\[data-style="{re.escape(style)}"\]\s*\{{(.*?)\n\}}', stylesheet, flags=re.DOTALL)
            self.assertIsNotNone(block, style)
            self.assertIn("--hero-scene-background:", block.group(1))
            self.assertIn("--hero-orbit-background:", block.group(1))

        expected_images = {"mobile-light.png", "desktop-light.png", "mobile-dark.png"}
        for style in static_previews:
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
