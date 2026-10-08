from pathlib import Path

from fontTools.ttLib import TTFont

from common import bbox, download, extract, remap_locl, save

VERSION = "2.003R"
ARCHIVE = f"https://github.com/adobe-fonts/source-han-serif/releases/download/{VERSION}/10_SourceHanSerifTC.zip"
LICENSE = f"https://raw.githubusercontent.com/adobe-fonts/source-han-serif/{VERSION}/LICENSE.txt"
# 'Source' is a Reserved Font Name
NAMES = [("SourceHanSerif", "PapaHanSerif"), ("Source Han Serif", "Papa Han Serif")]


def build(out: Path) -> None:
    for path in sorted(extract(download(ARCHIVE)).rglob("*.otf")):
        font = TTFont(path)
        before = bbox(font)
        remap_locl(font, "ZHS")
        save(font, out, NAMES, before, ".otf")
    download(LICENSE, out / "LICENSE-SourceHanSerif.txt")
