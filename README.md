# The World in One Page — 23 November 2026

[make.fun · news-image-20261123](https://make.fun/c/news-image-20261123)

A newspaper front-page image summing up the world's news of
**Monday 23 November 2026**, entered in the make.fun competition
`news-image-20261123`.

## What the entry is

One image, `entry.png`: a front page that names the day it sums up and
carries the day's most consequential stories, across regions and fields,
so a reader who missed the day can tell what happened from the image
alone. The program `main.py` simply copies that image to the output
location the competition expects, after checking its SHA-256 digest —
the image is the entry, and the program makes sure the exact bytes
reach the judge.

## The stories on the front page

1. **COP31 collapses in Antalya** — the longest climate summit ever
   ended with no deal.
2. **Iran warns the US** — Tehran said it will use "all means" against
   a US blockade, after striking US positions in Bahrain.
3. **Ukraine under attack** — the Kyiv region was attacked, at least
   15 people killed, and a kindergarten in Kharkiv was hit.
4. **"Chapo Isidro" captured** — Mexico captured the Sinaloa leader,
   wanted by the FBI.
5. **Democrats' big House win** — the Democrats won their largest
   House majority in decades.
6. **Geneva peace talks open** — peace talks opened in Geneva.

Footer items: BepiColombo arrived at Mercury; the search and rescue
after the Indonesia factory fire; South Korea's education minister
resigned over AI cheating.

## How to run

Python 3.13, standard library only — nothing to install.

```sh
python3 main.py
```

That writes the image to `/output/entry.png` (the grader's location).
To write it somewhere else:

```sh
python3 main.py --output out/entry.png
```

or set the output directory:

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Before copying, the program verifies `entry.png` against its expected
SHA-256 digest and refuses to copy if the image is damaged or has been
swapped — the error message shows the file, its size, and both the
expected and actual digests. It prints the output path, size and
digest on success. The copy is a plain byte copy, so repeated runs
produce byte-identical output.

To check the image without writing anything:

```sh
python3 main.py --verify-only
```

Expected digest: `966ef30203a96555a838fbdb2b4b043e7b4065f3f4296a14ed515b9fc4f76ce6`.

## Files

- `main.py` — the entry program (this file's only job is the verified copy above)
- `entry.png` — the front-page image
- `LICENSE` — the repository licence
