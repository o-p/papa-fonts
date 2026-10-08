from pathlib import Path

from fontTools.ttLib import TTFont

from common import bbox, copy_outlines, download, extract, save
from recipes import wenkai

VERSION = "v1.020"
ARCHIVE = f"https://github.com/ButTaiwan/iansui/releases/download/{VERSION}/iansui.zip"
LICENSE = f"https://raw.githubusercontent.com/ButTaiwan/iansui/{VERSION}/OFL.txt"
NAMES = [("Iansui-", "PapaIansui-"), ("Iansui", "Papa Iansui")]


def build(out: Path) -> None:
    font = TTFont(next(extract(download(ARCHIVE)).rglob("Iansui-Regular.ttf")))
    before = bbox(font)
    # Iansui and LXGW WenKai both derive from Klee One, so the punctuation styles match
    copy_outlines(font, wenkai.donor())
    save(font, out, NAMES, before, ".ttf")
    download(LICENSE, out / "LICENSE-Iansui.txt")
    download(wenkai.SC_LICENSE, out / "LICENSE-LXGWWenKai.txt")
