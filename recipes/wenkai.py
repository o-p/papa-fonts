from pathlib import Path

from fontTools.ttLib import TTFont

from common import bbox, copy_outlines, download, save

TC_VERSION = "v1.522"
SC_VERSION = "v1.522"
WEIGHTS = ["Light", "Regular", "Medium"]
VARIANTS = ["", "Mono"]
TC_RELEASE = f"https://github.com/lxgw/LxgwWenkaiTC/releases/download/{TC_VERSION}"
SC_RELEASE = f"https://github.com/lxgw/LxgwWenKai/releases/download/{SC_VERSION}"
TC_LICENSE = f"https://raw.githubusercontent.com/lxgw/LxgwWenkaiTC/{TC_VERSION}/OFL.txt"
SC_LICENSE = f"https://raw.githubusercontent.com/lxgw/LxgwWenKai/{SC_VERSION}/OFL.txt"
# 'LXGW' and '霞鶩' are Reserved Font Names of the punctuation donor
NAMES = [("LXGWWenKai", "PapaWenKai"), ("LXGW WenKai", "Papa WenKai")]


def donor(variant: str = "", weight: str = "Regular") -> TTFont:
    return TTFont(download(f"{SC_RELEASE}/LXGWWenKai{variant}-{weight}.ttf"))


def build(out: Path) -> None:
    for variant in VARIANTS:
        for weight in WEIGHTS:
            font = TTFont(download(f"{TC_RELEASE}/LXGWWenKai{variant}TC-{weight}.ttf"))
            before = bbox(font)
            copy_outlines(font, donor(variant, weight))
            save(font, out, NAMES, before, ".ttf")
    download(TC_LICENSE, out / "LICENSE-LXGWWenKaiTC.txt")
    download(SC_LICENSE, out / "LICENSE-LXGWWenKai.txt")
