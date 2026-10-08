# Agent guide

Goal: build the fonts the user wants, install them, and point their apps at them. Read `README.md` for what each recipe produces and the license rules.

## Steps

1. Ask which recipes the user wants (`sarasa`, `source-han-serif`, `wenkai`, `iansui`). The default is all of them. `source-han-serif` downloads ~140 MB and takes ~5 minutes.
2. Make sure `uv` is installed. If it is missing, ask before installing it.
3. Run `uv run --script build.py <recipes...>` from the repository root.
4. Verify the build. Each font line shows the `，` bounding box `before -> after`, and the x range must move left. Stop and report if any line errors or the x range doesn't move.
5. Install the files from `out/<recipe>/` (`*.ttf`, `*.otf`) as described in README "Install". Remove older copies of the same families first.
6. Optionally update the user's app settings, after confirming with them:
   - VS Code: `editor.fontFamily`, `terminal.integrated.fontFamily`. Put the Papa family first.
   - iTerm2: Profiles > Text > Non-ASCII Font.
   - Other terminals and editors: set the Papa family as the primary font or the CJK fallback font.
7. Have the user open `sample.txt` to check: all 8 marks `、。，．：；！？` should sit on the left of their cell.

## Rules

- Never commit, upload or publish anything in `downloads/` or `out/`.
- Font names in a new or changed recipe must not contain any upstream Reserved Font Name (see README "Licenses").
- To add a font: if its TC build already contains SC glyphs through `locl` (Source Han / Noto CJK region builds), use `remap_locl`. Otherwise find an OFL donor with the same units-per-em, the same punctuation advance width and a matching style, and use `copy_outlines`. Then add the font to the README tables.
