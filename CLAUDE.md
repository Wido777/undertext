# undertext

Detects instructions aimed at AI that websites hide: in "Summarize with AI"
links (prefilled `?q=` prompts that try to poison an assistant's memory) and in
page content (hidden text, comments, alt text, meta tags, JSON-LD, invisible
Unicode). Also runs research scans of real websites.

## Map of the code

| Area | Where | Notes |
|---|---|---|
| Link engine | `undertext/detector.py` | Rules (`RULES`), URL decoding, scoring. Source of truth for all rules. |
| Page engine | `undertext/page.py` | HTML to chunks (`extract_chunks`), `analyse_chunk`, `PAGE_OVERRIDE`, `ADDRESS`, `INSTRUCT`. |
| AI review | `undertext/judge.py` | Optional model review. **Can only raise a verdict, never lower it.** |
| CLI | `undertext/cli.py` | `undertext check`, `undertext page`, `--follow`, `--ai`. |
| Website | `docs/` | GitHub Pages. `rules.js` is GENERATED. `undertext.js` and `page.js` are JS ports that must match Python. |
| Extension | `extension/` | MV3. `extension/lib/` is a COPY of `docs/{rules,undertext,page}.js`. |
| Research | `research/` | `scan.py` (crawler), `summarize.py`, `review.py`, `ai_review.py`. |
| Evaluation | `eval/` | Labelled sets and runners. |
| CI | `.github/workflows/` | `tests.yml`, `scan.yml`, `review.yml`, `ai-eval.yml`. |

## Commands

```bash
python -m unittest discover -s tests          # all tests (needs node for parity tests)
python scripts/export_web_rules.py            # after ANY rule change in detector.py or page.py
python scripts/build_extension.py             # after export, copies the engine into extension/lib
python eval/run_eval.py [--real|--wild|--dev] # keyword-rule evaluation
```

A rule change is only done when all three have been run and the tests pass.
`tests/test_web_parity.py` fails if the browser engine and Python disagree.

## Rules everyone follows

- **Honest evaluation.** `eval/fresh.py` and `eval/reworded.py` are unseen test
  sets: never tune rules or the reviewer prompt on them. Changing the reviewer
  prompt or the rules invalidates the score on a set, so write a new set to
  measure afterwards. Report misses and false alarms, not just wins.
- **Privacy of scan results.** Never name a website in anything public (README,
  site, posts, commits, annotations). Scan items are anonymised to
  Acme / acme.example. Site names stay in private artifacts only.
- **Security of the tools themselves.** Text being checked is untrusted data.
  Never render it as HTML (use textContent), never execute pasted pages, and keep
  the AI reviewer's fencing (random markers, JSON-only replies).
- **No secrets.** Never write API keys or tokens into files, commits or logs.
- **Small, reviewed changes.** Engineering changes go through the reviewer and
  the tester before they are committed.
- Plain, clear English in user-facing text. No emojis in the site or posts.
