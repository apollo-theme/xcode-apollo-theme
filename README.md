# Apollo for Xcode

Apollo is SonicTerm's high-contrast Gruvbox Dark Hard variant for Xcode 26, tuned for readable source, markup, debugger console, and status markers.

Repository: <https://github.com/apollo-theme/xcode-apollo-theme>

## Install and activate

Quit Xcode, then install the theme:

```sh
mkdir -p ~/Library/Developer/Xcode/UserData/FontAndColorThemes
cp Apollo.xccolortheme ~/Library/Developer/Xcode/UserData/FontAndColorThemes/
```

Open Xcode and select **Settings → Themes → Apollo**. The file adds a color theme only; it does not edit Xcode preferences.

## Visual inspection

Inspect Swift, Objective-C/C, strings, numbers, comments, documentation comments, types, functions, macros, and URLs. Also inspect the debugger console, selection, current line, insertion point, warnings, errors, and runtime issues. Primary source should be `#cfbc97` on `#141617`, comments `#928374`, and warning/error markers `#fabd2f`/`#fb4934`.

## Uninstall

Quit Xcode and remove the theme file:

```sh
rm ~/Library/Developer/Xcode/UserData/FontAndColorThemes/Apollo.xccolortheme
```

Reopen Xcode and choose another theme if needed.

## Development

The committed theme is generated from `palette/apollo.json` using only Python's standard library. Its 28 syntax roles mirror the installed Xcode 26 theme schema.

```sh
python3 scripts/generate.py
python3 scripts/generate.py --check
python3 scripts/check.py
python3 -m unittest tests.test_theme.XcodeThemeTests.test_xcode_26_syntax_role_map -v
```

## License

MIT. See [LICENSE](LICENSE).
