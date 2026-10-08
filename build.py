# /// script
# requires-python = ">=3.11"
# dependencies = ["fonttools", "py7zr"]
# ///
import sys

from common import OUT
from recipes import iansui, sarasa, source_han_serif, wenkai

RECIPES = {
    "sarasa": sarasa,
    "source-han-serif": source_han_serif,
    "wenkai": wenkai,
    "iansui": iansui,
}


def main() -> None:
    names = sys.argv[1:] or list(RECIPES)
    if unknown := [n for n in names if n not in RECIPES]:
        sys.exit(f"unknown recipe: {', '.join(unknown)} (choose from {', '.join(RECIPES)})")
    for name in names:
        out = OUT / name
        out.mkdir(parents=True, exist_ok=True)
        RECIPES[name].build(out)


if __name__ == "__main__":
    main()
