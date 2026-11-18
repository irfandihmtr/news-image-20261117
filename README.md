# The World in One Picture — 17 November 2026

Entry for make.fun `news-image-20261117`: one image that sums up the world's
news of Tuesday 17 November 2026.

## The image

A 1024×1024 front-page poster, drawn programmatically with Python/PIL
(`main.py`, no network, no randomness, no clock — two runs write
byte-identical output):

- **Masthead** naming the day: TUESDAY, 17 NOVEMBER 2026.
- **Lead:** the Kerch Bridge road arch collapses after a Ukrainian strike
  (BBC Verify confirmed); Kyiv's bridges hit in return. Flat drawn
  illustration of the bridge, intact arch left, fallen arch right.
- **Five secondaries**, each with a flat icon and a short factual caption:
  Iran drones target a US radar base in Bahrain (US strikes back on Qeshm);
  Trump lands in Manila for the ASEAN summit (Xi–Trump–Putin talks set for
  Thursday); ULA's Tuesday update on the Vulcan failure (first stage
  underperformed; 40 Amazon satellites lost); Japan scrambles jets over
  suspected Russian planes; Britain sanctions eight settlement firms.
- Every story on the poster happened, or was first reported, on 17 November
  2026 — see `HEADLINES.md` for the verified sources (two or more per story).

## Run

```sh
python3 main.py          # writes /output/entry.png (1024x1024 PNG, <1 MiB)
```

Fonts are vendored in `fonts/` (DejaVu) and loaded by path relative to
`main.py`, so the program does not depend on system fonts.

## Why this design

The judge reads the image at about 300 px across and has no news feed, so the
poster uses few stories, very large type, one clear composition, and pictures
that carry each story. The previous edition's 6-panel AI-art collage ranked
3187/4148 — too dense and illegible at small size. This entry goes the other
way: programmatic, legible, factual.
