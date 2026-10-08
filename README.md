# Papa Fonts

Build scripts that take the Traditional Chinese (TC) version of open-licensed CJK fonts and move the fullwidth punctuation `、。，．：；！？` from the centre of the em box to the left, the Simplified Chinese (SC) way.

This repository contains **no font files**. `build.py` downloads the official upstream releases and writes the modified fonts to `out/` on your machine.

## Why SC punctuation

| Convention | `、。，．` | `：；！？` |
|---|---|---|
| Taiwan (MOE standard, all TC fonts) | centred | centred |
| Japanese | bottom-left corner | centred |
| Simplified Chinese (GB) | bottom-left corner | left half |

The SC convention is the closest to handwriting: a pause mark sits right after the character it follows, and every one of the 8 marks leans the same way. Only the punctuation changes. Every character keeps its TC glyph form.

## Fonts

| Recipe | Output family | TC base | Punctuation source | Method |
|---|---|---|---|---|
| `sarasa` | Papa Sarasa Term TC, Papa Sarasa Term Slab TC | [Sarasa Gothic](https://github.com/be5invis/Sarasa-Gothic) Term / Term Slab TC | Sarasa Gothic SC, same style and weight | copy outlines |
| `source-han-serif` | Papa Han Serif TC | [Source Han Serif](https://github.com/adobe-fonts/source-han-serif) TC | the same font: its own `locl` SC glyphs | remap cmap |
| `wenkai` | Papa WenKai TC, Papa WenKai Mono TC | [LXGW WenKai TC](https://github.com/lxgw/LxgwWenkaiTC) | [LXGW WenKai](https://github.com/lxgw/LxgwWenKai), same variant and weight | copy outlines |
| `iansui` | Papa Iansui | [Iansui 芫荽](https://github.com/ButTaiwan/iansui) | LXGW WenKai Regular. Both derive from Klee One, so the shapes match | copy outlines |

Upstream versions are pinned in each `recipes/*.py`.

## Licenses

All upstream fonts are licensed under the [SIL Open Font License 1.1](https://openfontlicense.org). The outputs are Modified Versions under the same license.

| Upstream | Reserved Font Names | How the outputs comply |
|---|---|---|
| Sarasa Gothic | `Source` (inherited from Adobe) | family names keep `Sarasa` and never use `Source` |
| Source Han Serif | `Source` | renamed to `Papa Han Serif`, including the CFF internal names |
| LXGW WenKai | `LXGW`, `霞鶩`, `霞鹜`, `落霞孤鶩`, `落霞孤鹜` | renamed to `Papa WenKai`. Both the WenKai TC and Iansui outputs contain LXGW WenKai glyphs |
| LXGW WenKai TC | none | (as above) |
| Iansui | none | prefixed with `Papa` |

Localized (non-English) family names are dropped instead of being translated, because some of them are Reserved Font Names.

Each `out/<recipe>/` directory gets the upstream license text of every font used in that recipe. If you share the built fonts, OFL 1.1 requires that you:

- ship those license files with the fonts,
- keep the fonts under OFL 1.1,
- not sell them on their own,
- not use any Reserved Font Name.

This project is not affiliated with or endorsed by any upstream author.

## Build

Requires [uv](https://docs.astral.sh/uv/).

```sh
uv run --script build.py                 # all recipes
uv run --script build.py sarasa wenkai   # selected recipes
```

- Downloads are cached in `downloads/` and can take a few GB.
- Each built font prints the bounding box of `，` before and after. The x range should move from around the centre (~400..600 of 1000) to the left.
- Hinting is dropped from the replaced glyphs only. macOS ignores hinting anyway.

`sample.txt` contains public-domain text (the opening of *Romance of the Three Kingdoms*) that uses all 8 marks, for checking the result.

## Install

Remove any older Papa builds first. Font caches are known to hold on to large CJK fonts.

- macOS: open the files in Font Book, or copy them to `~/Library/Fonts/`
- Linux: copy them to `~/.local/share/fonts/`, then run `fc-cache -f`
- Windows: right-click the file and choose *Install for all users*

Restart the apps that use the fonts.
