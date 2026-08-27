import hashlib
import json
import plistlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PALETTE_PATH = ROOT / "palette" / "apollo.json"
THEME_PATH = ROOT / "Apollo.xccolortheme"
PALETTE_SHA256 = "550f8c36cf4ef6ac99551541d1fe9554f77d563fa1e7c129a6a82583321d61ef"

XCODE_26_SYNTAX_ROLES = {
    "xcode.syntax.attribute",
    "xcode.syntax.character",
    "xcode.syntax.comment",
    "xcode.syntax.comment.doc",
    "xcode.syntax.comment.doc.keyword",
    "xcode.syntax.declaration.other",
    "xcode.syntax.declaration.type",
    "xcode.syntax.identifier.class",
    "xcode.syntax.identifier.class.system",
    "xcode.syntax.identifier.constant",
    "xcode.syntax.identifier.constant.system",
    "xcode.syntax.identifier.function",
    "xcode.syntax.identifier.function.system",
    "xcode.syntax.identifier.macro",
    "xcode.syntax.identifier.macro.system",
    "xcode.syntax.identifier.type",
    "xcode.syntax.identifier.type.system",
    "xcode.syntax.identifier.variable",
    "xcode.syntax.identifier.variable.system",
    "xcode.syntax.keyword",
    "xcode.syntax.mark",
    "xcode.syntax.markup.aside.kind",
    "xcode.syntax.markup.code",
    "xcode.syntax.number",
    "xcode.syntax.plain",
    "xcode.syntax.preprocessor",
    "xcode.syntax.string",
    "xcode.syntax.url",
}


def rgba_hex(value):
    channels = [float(channel) for channel in value.split()]
    return "#" + "".join(f"{round(channel * 255):02x}" for channel in channels[:3])


class XcodeThemeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.palette_bytes = PALETTE_PATH.read_bytes()
        cls.palette = json.loads(cls.palette_bytes)
        cls.theme = plistlib.loads(THEME_PATH.read_bytes())

    def test_palette_snapshot_is_canonical(self):
        self.assertEqual(hashlib.sha256(self.palette_bytes).hexdigest(), PALETTE_SHA256)

    def test_xcode_26_syntax_role_map(self):
        syntax_colors = self.theme["DVTSourceTextSyntaxColors"]
        syntax_fonts = self.theme["DVTSourceTextSyntaxFonts"]
        self.assertEqual(set(syntax_colors), XCODE_26_SYNTAX_ROLES)
        self.assertEqual(set(syntax_fonts), XCODE_26_SYNTAX_ROLES)
        self.assertEqual(rgba_hex(syntax_colors["xcode.syntax.plain"]), self.palette["colors"]["foreground"])
        self.assertEqual(rgba_hex(syntax_colors["xcode.syntax.comment"]), self.palette["colors"]["foregroundInactive"])

    def test_editor_and_status_roles_use_exact_palette_colors(self):
        colors = self.palette["colors"]
        self.assertEqual(rgba_hex(self.theme["DVTSourceTextBackground"]), colors["background"])
        self.assertEqual(rgba_hex(self.theme["DVTSourceTextInsertionPointColor"]), colors["accent"])
        self.assertEqual(rgba_hex(self.theme["DVTScrollbarMarkerErrorColor"]), colors["danger"])
        self.assertEqual(rgba_hex(self.theme["DVTScrollbarMarkerDiffConflictColor"]), colors["danger"])
        self.assertEqual(rgba_hex(self.theme["DVTScrollbarMarkerWarningColor"]), colors["accent"])
        self.assertEqual(rgba_hex(self.theme["DVTConsoleDebuggerPromptTextColor"]), colors["success"])

    def test_restricted_bright_black_is_not_used_for_xcode_text(self):
        restricted = self.palette["colors"]["ansiBrightBlack"]
        color_values = [value for key, value in self.theme.items() if key.endswith("Color") or key == "DVTSourceTextBackground"]
        color_values.extend(self.theme["DVTSourceTextSyntaxColors"].values())
        self.assertNotIn(restricted, {rgba_hex(value) for value in color_values})


if __name__ == "__main__":
    unittest.main()
