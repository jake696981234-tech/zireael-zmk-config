#!/usr/bin/env python3
"""Validate and render the Dao keymap reference with keymap-drawer."""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

import yaml


ROOT = Path(__file__).resolve().parents[1]
KEYMAP = ROOT / "config" / "dao.keymap"
DAO_DTSI = ROOT / "modules" / "dao" / "boards" / "dao" / "dao.dtsi"
GUIDE = ROOT / "LAYER_ACCESS_GUIDE.md"
DOCS = ROOT / "docs" / "keymap"
DRAW_CONFIG = DOCS / "keymap-drawer.config.yaml"
NORMALIZED_YAML = DOCS / "dao-keymap.yaml"
PRIMARY_SVG = DOCS / "dao-primary.svg"
SECONDARY_SVG = DOCS / "dao-secondary.svg"

LAYERS = ("BASE", "NAV", "MOUSE", "MEDIA", "NUM", "SYM", "FUN", "GAME", "BT")
PRIMARY_LAYERS = ("BASE", "NAV", "NUM", "SYM")
SECONDARY_LAYERS = ("FUN", "MEDIA", "MOUSE", "GAME", "BT")
THUMB_POSITIONS = tuple(range(36, 42))
FALLBACKS = {
    0: "Tab",
    11: "Backspace",
    12: "Ctrl",
    23: "Enter",
    24: "Shift",
    35: "Delete",
}

LABELS = {
    "TAB": "Tab",
    "ESC": "Esc",
    "BSPC": "Backspace",
    "ENTER": "Enter",
    "SPACE": "Space",
    "DEL": "Delete",
    "INS": "Insert",
    "HOME": "Home",
    "UP": "Up",
    "END": "End",
    "LEFT": "Left",
    "DOWN": "Down",
    "RIGHT": "Right",
    "PG UP": "Page Up",
    "PG DN": "Page Down",
    "LCTRL": "Ctrl",
    "RCTRL": "RCtrl",
    "LSHFT": "Shift",
    "RSHFT": "RShift",
    "LALT": "Alt",
    "RALT": "RAlt",
    "LGUI": "GUI",
    "RGUI": "RGUI",
    "PSCRN": "Print Screen",
    "SLCK": "Scroll Lock",
    "PAUSE BREAK": "Pause",
    "APP": "App",
}

EXPECTED_TRANSFORM = (
    tuple((0, column) for column in range(6))
    + tuple((0, column) for column in range(11, 5, -1))
    + tuple((1, column) for column in range(6))
    + tuple((1, column) for column in range(11, 5, -1))
    + tuple((2, column) for column in range(6))
    + tuple((2, column) for column in range(11, 5, -1))
    + ((3, 3), (3, 4), (3, 5), (3, 11), (3, 10), (3, 9))
)


def fail(message: str) -> None:
    raise RuntimeError(message)


def run_keymap_drawer(*arguments: str) -> None:
    command = [sys.executable, "-m", "keymap_drawer", "-c", str(DRAW_CONFIG), *arguments]
    subprocess.run(command, cwd=ROOT, check=True)


def flatten(rows: list[list[Any]]) -> list[Any]:
    return [key for row in rows for key in row]


def validate_sources() -> None:
    for source in (KEYMAP, DAO_DTSI, GUIDE, DRAW_CONFIG):
        if not source.is_file():
            fail(f"Required source is missing: {source.relative_to(ROOT)}")

    dtsi = DAO_DTSI.read_text(encoding="utf-8")
    transform_match = re.search(
        r"default_transform:.*?\bmap\s*=\s*<(.*?)>;",
        dtsi,
        flags=re.DOTALL,
    )
    if not transform_match:
        fail("Could not find default_transform map in dao.dtsi")

    transform = tuple(
        (int(row), int(column))
        for row, column in re.findall(r"RC\(\s*(\d+)\s*,\s*(\d+)\s*\)", transform_match.group(1))
    )
    if transform != EXPECTED_TRANSFORM:
        fail("Dao default_transform no longer matches the documented 42-key physical order")
    if len(transform) != 42 or tuple(range(len(transform) - 6, len(transform))) != THUMB_POSITIONS:
        fail("Dao geometry must contain 42 positions with thumbs at positions 36-41")


def parse_keymap(destination: Path) -> dict[str, Any]:
    run_keymap_drawer(
        "parse",
        "--columns",
        "12",
        "--zmk-keymap",
        str(KEYMAP),
        "--layer-names",
        *LAYERS,
        "--output",
        str(destination),
    )
    parsed = yaml.safe_load(destination.read_text(encoding="utf-8"))
    if not isinstance(parsed, dict):
        fail("keymap-drawer produced an invalid keymap document")
    return parsed


def validate_parsed(parsed: dict[str, Any]) -> None:
    layers = parsed.get("layers")
    if not isinstance(layers, dict) or tuple(layers) != LAYERS:
        fail(f"Expected layers in this order: {', '.join(LAYERS)}")

    for name, rows in layers.items():
        if not isinstance(rows, list) or any(not isinstance(row, list) for row in rows):
            fail(f"Layer {name} is not arranged as rows")
        if [len(row) for row in rows] != [12, 12, 12, 6]:
            fail(f"Layer {name} must have rows of 12, 12, 12, and 6 bindings")
        if len(flatten(rows)) != 42:
            fail(f"Layer {name} does not contain exactly 42 bindings")

    base_bindings = flatten(layers["BASE"])
    expected_home_row = {
        13: {"t": "A", "h": "LGUI"},
        14: {"t": "R", "h": "LALT"},
        15: {"t": "S", "h": "LCTRL"},
        16: {"t": "T", "h": "LSHFT"},
        19: {"t": "N", "h": "LSHFT"},
        20: {"t": "E", "h": "LCTRL"},
        21: {"t": "I", "h": "LALT"},
        22: {"t": "O", "h": "LGUI"},
    }
    for position, expected in expected_home_row.items():
        if base_bindings[position] != expected:
            fail(f"BASE home-row tap/hold binding changed at position {position}")

    base_thumbs = base_bindings[36:42]
    expected_base_thumbs = [
        {"t": "ESC", "h": "MEDIA"},
        {"t": "TAB", "h": "MOUSE"},
        {"t": "SPACE", "h": "NAV"},
        {"t": "BSPC", "h": "NUM"},
        {"t": "ENTER", "h": "SYM"},
        {"t": "DEL", "h": "FUN"},
    ]
    if base_thumbs != expected_base_thumbs:
        fail("BASE thumb tap/hold bindings no longer match positions 36-41")

    combos = parsed.get("combos")
    if not isinstance(combos, list) or len(combos) != 1:
        fail("Expected exactly one combo in the active keymap")
    combo = combos[0]
    if combo.get("p") != [36, 41] or combo.get("k") != "BT":
        fail("The sole combo must hold positions 36 and 41 to enter BT")
    if combo.get("l") != ["BASE", "GAME"]:
        fail("The BT combo must be active on BASE and GAME")


def normalized_label(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    return LABELS.get(value, value)


def normalize_binding(binding: Any, position: int, layer: str) -> Any:
    if isinstance(binding, str):
        normalized: Any = normalized_label(binding)
    elif isinstance(binding, dict):
        if binding.get("type") == "trans":
            if position not in FALLBACKS:
                fail(f"Unexpected transparent binding on {layer} at position {position}")
            return {"t": FALLBACKS[position], "type": "fallback"}
        normalized = {
            key: normalized_label(value) if key in {"t", "h", "s"} else value
            for key, value in binding.items()
        }
    else:
        fail(f"Unsupported binding on {layer} at position {position}: {binding!r}")

    labels = normalized.values() if isinstance(normalized, dict) else (normalized,)
    for label in labels:
        if isinstance(label, str) and re.match(r"^&[A-Za-z_]", label):
            fail(f"Unmapped ZMK behavior on {layer} at position {position}: {label}")
    return normalized


def normalize(parsed: dict[str, Any]) -> dict[str, Any]:
    parsed["layout"] = {
        "ortho_layout": {"split": True, "rows": 3, "columns": 6, "thumbs": 3}
    }
    for layer, rows in parsed["layers"].items():
        position = 0
        for row_index, row in enumerate(rows):
            normalized_row = []
            for binding in row:
                normalized_row.append(normalize_binding(binding, position, layer))
                position += 1
            rows[row_index] = normalized_row

    parsed["combos"][0]["k"] = {"t": "BT", "h": "36 + 41"}
    parsed["combos"][0]["a"] = "bottom"
    parsed["combos"][0]["o"] = 0.35
    return parsed


def write_normalized(parsed: dict[str, Any]) -> None:
    content = "# Generated by tools/render_keymap.py; do not edit by hand.\n"
    content += yaml.safe_dump(parsed, sort_keys=False, allow_unicode=True, width=1000)
    NORMALIZED_YAML.write_text(content, encoding="utf-8", newline="\n")


def render(output: Path, layers: tuple[str, ...]) -> None:
    document = yaml.safe_load(NORMALIZED_YAML.read_text(encoding="utf-8"))
    document["layers"] = {layer: document["layers"][layer] for layer in layers}
    for combo in document.get("combos", []):
        combo["l"] = [layer for layer in combo.get("l", []) if layer in layers]
    with tempfile.TemporaryDirectory(prefix="dao-keymap-draw-") as temporary_directory:
        selected_yaml = Path(temporary_directory) / "selected.yaml"
        selected_yaml.write_text(
            yaml.safe_dump(document, sort_keys=False, allow_unicode=True, width=1000),
            encoding="utf-8",
            newline="\n",
        )
        run_keymap_drawer(
            "draw",
            str(selected_yaml),
            "--output",
            str(output),
        )


def validate_svg(path: Path, expected_layers: tuple[str, ...]) -> None:
    try:
        root = ElementTree.parse(path).getroot()
    except ElementTree.ParseError as error:
        fail(f"Invalid SVG generated at {path.relative_to(ROOT)}: {error}")
    if root.tag != "{http://www.w3.org/2000/svg}svg":
        fail(f"Generated file is not an SVG: {path.relative_to(ROOT)}")

    text_elements = [element for element in root.iter() if element.tag.endswith("text")]
    text = " ".join(element.text or "" for element in text_elements)
    headings = tuple(
        element.attrib["id"]
        for element in text_elements
        if element.attrib.get("class") == "label" and "id" in element.attrib
    )
    if headings != expected_layers:
        fail(f"{path.name} has layer headings {headings}, expected {expected_layers}")

    layer_groups = {
        element.attrib["class"].removeprefix("layer-"): element
        for element in root.iter()
        if element.tag.endswith("g") and element.attrib.get("class", "").startswith("layer-")
    }
    for layer in expected_layers:
        rendered_positions = {
            int(match.group(1))
            for element in layer_groups[layer].iter()
            if element.tag.endswith("g")
            for match in [re.search(r"\bkeypos-(\d+)\b", element.attrib.get("class", ""))]
            if match
        }
        if rendered_positions != set(range(42)):
            fail(f"{path.name} does not render all positions 0-41 on {layer}")

    rendered_combos = [
        element
        for element in root.iter()
        if element.tag.endswith("g") and "combopos-0" in element.attrib.get("class", "").split()
    ]
    if len(rendered_combos) != 1:
        fail(f"{path.name} must render the BT combo exactly once")
    if re.search(r"&amp;[A-Za-z_]|&[A-Za-z_]", text):
        fail(f"{path.name} contains an unmapped raw behavior")


def main() -> None:
    validate_sources()
    DOCS.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="dao-keymap-") as temporary_directory:
        parsed = parse_keymap(Path(temporary_directory) / "parsed.yaml")
    validate_parsed(parsed)
    write_normalized(normalize(parsed))
    render(PRIMARY_SVG, PRIMARY_LAYERS)
    render(SECONDARY_SVG, SECONDARY_LAYERS)
    validate_svg(PRIMARY_SVG, PRIMARY_LAYERS)
    validate_svg(SECONDARY_SVG, SECONDARY_LAYERS)
    print("Validated 9 layers, 42 bindings per layer, Dao positions 0-41, and BT combo 36+41.")
    print(f"Wrote {PRIMARY_SVG.relative_to(ROOT)}")
    print(f"Wrote {SECONDARY_SVG.relative_to(ROOT)}")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1) from error
