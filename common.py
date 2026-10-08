import urllib.request
import zipfile
from pathlib import Path

import py7zr
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

PUNCT = "、。，．：；！？"
ROOT = Path(__file__).parent
DL = ROOT / "downloads"
OUT = ROOT / "out"
NAME_IDS = (1, 3, 4, 6, 16, 21)


def download(url: str, dest: Path | None = None) -> Path:
    path = dest or DL / url.rsplit("/", 1)[1]
    if not path.exists():
        print(f"download {url}")
        path.parent.mkdir(parents=True, exist_ok=True)
        part = path.with_name(path.name + ".part")
        urllib.request.urlretrieve(url, part)
        part.rename(path)
    return path


def extract(archive: Path) -> Path:
    target = archive.with_suffix("")
    if not target.exists():
        part = target.with_name(target.name + ".part")
        if archive.suffix == ".7z":
            with py7zr.SevenZipFile(archive) as z:
                z.extractall(part)
        else:
            with zipfile.ZipFile(archive) as z:
                z.extractall(part)
        part.rename(target)
    return target


def copy_outlines(base: TTFont, donor: TTFont, chars: str = PUNCT) -> None:
    """Replace base's glyphs for `chars` with donor's outlines (TrueType only)."""
    assert "glyf" in base and "glyf" in donor
    assert base["head"].unitsPerEm == donor["head"].unitsPerEm
    donor_set = donor.getGlyphSet()
    for ch in chars:
        dst = base.getBestCmap()[ord(ch)]
        src = donor.getBestCmap()[ord(ch)]

        # Decompose so the glyph never references components missing from base
        rec = DecomposingRecordingPen(donor_set)
        donor_set[src].draw(rec)
        pen = TTGlyphPen(None)
        rec.replay(pen)
        glyph = pen.glyph()
        glyph.recalcBounds(base["glyf"])

        adv = donor["hmtx"][src][0]
        if adv != base["hmtx"][dst][0]:
            raise ValueError(f"advance mismatch {ch}: {adv} vs {base['hmtx'][dst][0]}")
        base["glyf"][dst] = glyph
        base["hmtx"][dst] = (adv, getattr(glyph, "xMin", 0))
        if "vmtx" in base and "vmtx" in donor:
            base["vmtx"][dst] = donor["vmtx"][src]


def remap_locl(font: TTFont, lang: str, script: str = "hani", chars: str = PUNCT) -> None:
    """Point cmap at the glyphs the font's own `locl` feature uses for `lang`."""
    gsub = font["GSUB"].table
    rec = next(s for s in gsub.ScriptList.ScriptRecord if s.ScriptTag == script)
    langsys = next(l.LangSys for l in rec.Script.LangSysRecord if l.LangSysTag.strip() == lang)
    mapping = {}
    for fi in langsys.FeatureIndex:
        feature = gsub.FeatureList.FeatureRecord[fi]
        if feature.FeatureTag != "locl":
            continue
        for li in feature.Feature.LookupListIndex:
            for sub in gsub.LookupList.Lookup[li].SubTable:
                sub = getattr(sub, "ExtSubTable", sub)
                mapping.update(getattr(sub, "mapping", {}))

    cmap = font.getBestCmap()
    for ch in chars:
        target = mapping[cmap[ord(ch)]]
        for table in font["cmap"].tables:
            if ord(ch) in getattr(table, "cmap", {}):
                table.cmap[ord(ch)] = target


def rename(font: TTFont, pairs: list[tuple[str, str]]) -> str:
    """Rewrite English family/PS names with the first matching pair; drop localized ones.

    Localized names are dropped rather than prefixed, since some (e.g. 霞鶩) are Reserved Font Names.
    Returns the new PostScript name.
    """

    def sub(s: str) -> str:
        for old, new in pairs:
            if old in s:
                return s.replace(old, new, 1)
        raise ValueError(f"no rename rule matches {s!r}")

    table = font["name"]
    for rec in list(table.names):
        if rec.nameID not in NAME_IDS:
            continue
        english = (rec.platformID, rec.langID) in ((3, 0x409), (1, 0))
        if english:
            rec.string = sub(rec.toUnicode())
        else:
            table.names.remove(rec)

    if "CFF " in font:
        cff = font["CFF "].cff
        cff.fontNames = [sub(n) for n in cff.fontNames]
        top = cff.topDictIndex[0]
        for attr in ("FullName", "FamilyName"):
            if hasattr(top, attr):
                setattr(top, attr, sub(getattr(top, attr)))
        for fd in getattr(top, "FDArray", []):
            fd.FontName = sub(fd.FontName)

    if "DSIG" in font:
        del font["DSIG"]
    return table.getDebugName(6)


def bbox(font: TTFont, ch: str = "，") -> str:
    gs = font.getGlyphSet()
    pen = BoundsPen(gs)
    gs[font.getBestCmap()[ord(ch)]].draw(pen)
    x0, y0, x1, y1 = pen.bounds
    return f"x {x0:.0f}..{x1:.0f} y {y0:.0f}..{y1:.0f}"


def save(font: TTFont, out: Path, pairs: list[tuple[str, str]], before: str, ext: str) -> None:
    ps = rename(font, pairs)
    path = out / f"{ps}{ext}"
    font.save(path)
    print(f"{path.name}  ，: {before} -> {bbox(font)}")
