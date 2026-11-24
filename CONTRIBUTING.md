# Contributing to DailyToolsOps

Start with the [roadmap](docs/ROADMAP.md) and [issues](https://github.com/AnkitParekh007/DailyToolsOps/issues). Discuss scope before large changes. Do not include private data, credentials or unlicensed third-party assets.

For a resource pack, include README.md, INSTRUCTIONS.md, VERSION, manifest.json, install.py, pack.py, concrete templates or runnable examples and relevant tests. Register it in catalog.json. Keep installs preview-first and non-overwriting. Document actual compatibility and limitations; do not label templates as runnable agents.

Run from repository root:

```sh
python3 dailytools.py validate
python3 -m unittest discover -s tests -v
python3 scripts/build_site.py _site
```

Open a focused PR referencing the issue, with actual test results and known limitations. Do not bypass failing CI. Avoid unrelated changes. Review repository licensing before distributing derivatives.
