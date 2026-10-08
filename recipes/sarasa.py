from pathlib import Path

from fontTools.ttLib import TTFont

from common import bbox, copy_outlines, download, extract, save

VERSION = "1.0.42"
STYLES = ["Term", "TermSlab"]
RELEASE = f"https://github.com/be5invis/Sarasa-Gothic/releases/download/v{VERSION}"
LICENSE = f"https://raw.githubusercontent.com/be5invis/Sarasa-Gothic/v{VERSION}/LICENSE"
NAMES = [("Sarasa-", "PapaSarasa-"), ("Sarasa", "Papa Sarasa")]


def build(out: Path) -> None:
    for style in STYLES:
        tc = extract(download(f"{RELEASE}/Sarasa{style}TC-TTF-{VERSION}.7z"))
        sc = extract(download(f"{RELEASE}/Sarasa{style}SC-TTF-{VERSION}.7z"))
        for path in sorted(tc.rglob("*.ttf")):
            font = TTFont(path)
            before = bbox(font)
            copy_outlines(font, TTFont(next(sc.rglob(path.name.replace("TC", "SC", 1)))))
            save(font, out, NAMES, before, ".ttf")
    download(LICENSE, out / "LICENSE-Sarasa.txt")
