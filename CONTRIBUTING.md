# Contributing

Anyone building a MailerCloud customer document can propose a change. The owner (Technical Operations at MailerCloud) approves it. The full policy is in [`docs/governance.md`](docs/governance.md); this is the short version.

## Before you start

- This repository is **public**. Never commit client names, customer figures, account lists, screenshots of customer documents or deck configs for real clients. Use fictional examples (`Example Client`, `Account A`).
- Check the brand guide at <https://www.mailercloud.com/brand-assets> first. Where it speaks, it wins.

## Making a change

1. Open an issue using the *Change request* template, naming the document that needs the change.
2. Branch from `main`: `feature/<short-name>` or `fix/<short-name>`.
3. Edit the source, not the output:
   - values in `tokens/tokens.json` (three tiers: primitive, semantic, component; every token has a usage note);
   - guidance in `docs/`;
   - component previews in `components/<Name>/preview.html`.
4. Run `python scripts/build_tokens.py` and `python scripts/check_contrast.py`. Commit the regenerated files.
5. If you add a colour pair, add it to `scripts/contrast_pairs.json`.
6. Rebuild one existing document (the deck kit example is enough) to prove nothing else moved.
7. Update `CHANGELOG.md` and, for a release, `VERSION` and the `version` in `tokens/tokens.json`.
8. Open a pull request using the template. The owner reviews against the checklist in the template.

## Versioning

Semantic versioning on the whole system: **patch** for a corrected value or wording, **minor** for a new token, component or pattern, **major** for a change that alters the look of documents already sent. Tag releases `v3.0.0`, `v3.1.0` and so on.

## Token naming

Lowercase, hyphen-separated, role first (`text-`, `surface-`, `border-`, `status-`, `chart-`). Semantic and component tokens refer to primitives with an alias such as `"{ink}"`. Deprecate a token for one release before removing it, and say in its usage note what replaces it.
