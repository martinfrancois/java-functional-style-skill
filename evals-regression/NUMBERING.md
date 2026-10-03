Regression scenarios keep the number they had in `evals-reference/`. They are safety coverage,
run with context only, and are not part of lift discovery or the public score.

Moved on 2026-09-20 after hosted run `01a0bfa2-c49e-7178-a1a1-910db1b92785` (Tessl default solver)
scored both variants at 100/100:

- `01-to-map-function-identity-mapper`
- `02-remove-identity-map-stage`
- `03-extract-block-callback-helper`
- `05-checked-boundary-plain-branch`
- `06-do-not-force-functional-style`
- `08-track-name-normalizers`
- `10-bike-station-fallbacks`
- `11-trail-permit-reader`

With-context rerun against the final runtime bundle on 2026-09-21: all eight at 100/100 in run
`01a0c1de-cc4b-70ef-a074-106a34a465c5`.

Rerun against the PR #18 runtime text on 2026-10-03 (default solver `deepseek-v4.1-flash`), run
`01a10393-bc00-74b2-9943-a40df1e48b69`: seven at 100/100 and `06` at 99/100, where the scorer took
one point from "Keeps review focused" for a side note on `Stream.toList()` mutability. The
isolated rerun of `06` (`01a1039a-85bd-75c7-9345-f5ccab25e382`) scored 100/100.
