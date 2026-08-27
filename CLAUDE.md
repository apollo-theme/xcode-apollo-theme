# Repository guidance

This standalone repository publishes Apollo for Xcode. `palette/apollo.json` is the exact canonical snapshot and `Apollo.xccolortheme` is generated and committed.

## Architecture

- `palette/apollo.json`: source palette snapshot; do not hand-edit generated colors.
- `scripts/generate.py`: deterministic stdlib-only Xcode plist generator. The top-level editor/markup/console keys and all 28 syntax roles follow the installed Xcode 26 schema.
- `Apollo.xccolortheme`: generated native Xcode font-and-color theme.
- `tests/test_theme.py`: schema coverage, palette mappings, status colors, and restricted-color checks.
- `scripts/check.py`: regeneration, tests, plist parsing, and macOS `plutil` lint.

## Commands

```sh
python3 scripts/generate.py
python3 scripts/generate.py --check
python3 scripts/check.py
python3 -m unittest tests.test_theme.XcodeThemeTests.test_xcode_26_syntax_role_map -v
plutil -lint Apollo.xccolortheme  # macOS
```

Preserve the full role map and readable semantic hierarchy. Never edit Xcode preferences or install automatically. `#665c54` is ANSI-only and must not appear in this Xcode theme.
