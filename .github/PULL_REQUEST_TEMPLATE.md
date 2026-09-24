## What changed and why

<!-- One or two sentences. Name the document that needed it. -->

## Checklist (owner reviews against this)

- [ ] Source edited (`tokens/tokens.json`, `docs/`, `components/`), not only generated files
- [ ] `python scripts/build_tokens.py` run and the regenerated files committed
- [ ] `python scripts/check_contrast.py` and `--coverage` pass; any new colour pair added to `scripts/contrast_pairs.json`
- [ ] `python scripts/check_usage.py` passes: no colour, type size, radius or spacing step written as a literal
- [ ] Every new token has a usage note; semantic or component tokens alias a primitive
- [ ] Palette, type and logo agree with the brand guide (https://www.mailercloud.com/brand-assets)
- [ ] One existing document rebuilt (deck kit example) and nothing else moved
- [ ] No client names, customer figures or real client configs anywhere in the change
- [ ] `CHANGELOG.md` updated; version bumped if this is a release
