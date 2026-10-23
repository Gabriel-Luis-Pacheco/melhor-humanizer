"""Checks for conservative, transparent and non-destructive tools."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import lint
import preserve

class LintTests(unittest.TestCase):
    def test_detects_genuine_pt_filler(self):
        rows = lint.lint_text("É importante ressaltar que o projeto foi entregue.\n"
                              "E isso muda tudo.", "pt")
        self.assertEqual({r.rule for r in rows}, {"empty_preamble", "generic_ending"})

    def test_quoted_example_is_not_flagged(self):
        rows = lint.lint_text('A expressão "é importante ressaltar" aparece no relatório.', "pt")
        self.assertEqual(rows, [])

    def test_code_and_markdown_are_not_scanned(self):
        text = "---\nname: sample\ndescription: É importante ressaltar\n---\n"
        text += "~~~txt\nÉ importante ressaltar\n~~~\n"
        text += chr(96) * 3 + "python\nE isso muda tudo.\n" + chr(96) * 3 + "\n"
        text += "> E isso muda tudo.\n# É importante ressaltar"
        self.assertEqual(lint.lint_text(text, "pt"), [])

    def test_good_human_prose_stays_clean(self):
        text = "Bah, fiz duas tentativas e ainda não deu certo. Amanhã volto nisso."
        self.assertEqual(lint.lint_text(text, "pt"), [])

    def test_one_dash_is_not_flagged(self):
        self.assertEqual(lint.lint_text("A resposta — que chegou ontem — foi curta.", "pt"), [])

    def test_human_list_is_not_suspicious_without_label_bold(self):
        self.assertEqual(lint.lint_text("- Anote a data.\n- Envie o arquivo.\n- Guarde o recibo.", "pt"), [])

    def test_english_rule(self):
        rows = lint.lint_text("Here's the thing: it was delayed.", "en")
        self.assertEqual(rows[0].rule, "chatbot_open")

class PreservationTests(unittest.TestCase):
    def test_keeps_all_anchors(self):
        text = "Em 02/10/2026, R$ 1.200,50 (12%) constava em https://exemplo.com."
        result = preserve.compare(text, text)
        self.assertFalse(result["review_required"])

    def test_detects_new_and_missing(self):
        a = "Em 02/10/2026, o valor foi R$ 120."
        b = "Em 03/10/2026, o valor foi R$ 150."
        out = preserve.compare(a, b)
        self.assertTrue(out["review_required"])
        self.assertIn("date", out["missing_anchors"])
        self.assertIn("money", out["added_anchors"])

    def test_cnpj_kept_when_punctuation_changes(self):
        a = "CNPJ: 12.345.678/0001-90"
        b = "O CNPJ é 12.345.678/0001-90."
        out = preserve.compare(a, b)
        self.assertFalse(out["review_required"])

    def test_urls_are_preserved(self):
        out = preserve.compare("Acesse https://exemplo.com/arquivo.", "Acesse https://outro.com/arquivo.")
        self.assertTrue(out["review_required"])
        self.assertIn("url", out["missing_anchors"])

    def test_plain_words_not_claimed_verified(self):
        out = preserve.compare("A tarefa pode ocorrer.", "A tarefa ocorreu.")
        self.assertFalse(out["review_required"])
        self.assertIn("não fatos", out["limitations"])

if __name__ == "__main__":
    unittest.main()
