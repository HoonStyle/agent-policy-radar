# Forward evaluation cases

These are realistic evaluation inputs for the three skills, not completed agent trials or performance results. Use a permitted isolated artifact workspace and the host's established tools. Judge outcomes and final rendered artifacts rather than matching exact wording. Do not activate/install plugins or send private source files to external services for these tests without appropriate scope.

| Case | Input request and source | Observable expectations |
| --- | --- | --- |
| English color-only UI fix | Existing English settings screen; change palette while retaining layout and behavior | No forced Korean copy, no unnecessary redesign, all affected states reviewed, no unsupported contrast claim |
| Bilingual form | Korean/English form with long labels, validation, and selected rows | Values/selection/theme survive language switch; accessible names and errors localize; no narrow-width clipping |
| Slide refinement | Existing 6-slide English deck; preserve dimensions, notes, and editable chart data | Template retained; slide-level findings; no invented facts, no screenshot replacement for native chart |
| New Korean presentation | Supplied Korean content for a 5-slide live talk | 5 total slides unless instructed otherwise, distinct slide purposes, readable glyphs, every slide rendered |
| Word pagination repair | Existing Korean report with a long table, hyperlink, and orphan heading | Real heading/table styles preserved; targeted pagination correction; every page reviewed; hyperlink target unchanged |
| English proposal polish | Existing English DOCX, preserve comments and tracked changes | Better hierarchy and flow without accepting changes/removing comments; no UI card layout pasted into document |
| Resume conversion | Synthetic resume Markdown and an established project converter | Existing converter used; no new builder or new narrative; links and pages verified |
| Review-only / missing renderer | Review request with source deck/doc and no allowed renderer | No unauthorized edits; source-only findings distinguished from visual verification; limitation explicit |

Record actual toolchain, output hash, reviewed slides/pages, observed failures, and fixes when a trial is run. A manifest validator or a human read-through of these cases does not count as a behavioral pass.
