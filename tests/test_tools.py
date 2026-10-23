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

    def test_plain_words_can_change_uncertainty(self):
        out = preserve.compare("A tarefa pode ocorrer.", "A tarefa ocorreu.")
        self.assertTrue(out["review_required"])
        self.assertIn("modality_uncertainty", out["semantic_cues"])
        self.assertIn("não prova equivalência", out["limitations"])


class RegressionTests(unittest.TestCase):
    def test_chatbot_exclamation(self):
        names = {r.rule for r in lint.lint_text("Claro! Aqui está a resposta.", "pt")}
        self.assertIn("chatbot_open", names)

    def test_english_chatbot(self):
        names = {r.rule for r in lint.lint_text("Here's the thing: it failed.", "en")}
        self.assertIn("chatbot_open", names)

    def test_three_steps_are_allowed(self):
        text = "1. Solicite acesso.\n2. Confirme a autorização.\n3. Entre na conta."
        self.assertEqual(lint.lint_text(text, "pt"), [])

    def test_quoted_cliche_is_not_a_problem(self):
        self.assertEqual(lint.lint_text('A frase "é importante ressaltar" é redundante.', "pt"), [])

    def test_code_fences_do_not_close_on_wrong_delimiter(self):
        raw = "~~~~python\nÉ importante ressaltar\n" + chr(96) * 3 + "\nE isso muda tudo.\n~~~~"
        self.assertEqual(lint.lint_text(raw, "pt"), [])

    def test_unclosed_code_fence_stays_masked(self):
        raw = "~~~python\nÉ importante ressaltar\nE isso muda tudo."
        self.assertEqual(lint.lint_text(raw, "pt"), [])

    def test_inline_code_ignored(self):
        text = "Use " + chr(96) + "é importante ressaltar" + chr(96) + " como exemplo."
        self.assertEqual(lint.lint_text(text, "pt"), [])

    def test_invalid_language_is_rejected(self):
        with self.assertRaises(ValueError):
            lint.lint_text("Hello", "xx")

    def test_change_modal_force_must_not_disappear(self):
        result = preserve.compare("O usuário pode exportar.", "O usuário deve exportar.")
        self.assertTrue(result["review_required"])
        self.assertIn("modality_uncertainty", result["semantic_cues"])

    def test_change_negation_is_warning(self):
        result = preserve.compare("Não verificamos a etapa.", "Verificamos a etapa.")
        self.assertIn("negation_scope", result["semantic_cues"])

    def test_plan_turned_into_done_is_warning(self):
        result = preserve.compare("Será implantado depois.", "Foi implantado depois.")
        self.assertIn("operational_state", result["semantic_cues"])

    def test_no_unnecessary_alert_on_same_text(self):
        line = "Não sabemos a causa; o erro pode ocorrer amanhã."
        self.assertFalse(preserve.compare(line, line)["review_required"])

    def test_counter_handles_duplicate_numbers(self):
        res = preserve.compare("2 e 2 e 3", "2 e 3")
        self.assertEqual(res["missing_anchors"]["number"]["2"], 1)

    def test_urls_in_parentheses_not_changed(self):
        before = "[manual](https://exemplo.com/docs)"
        after = "Veja https://exemplo.com/docs."
        self.assertNotIn("url", preserve.compare(before, after)["missing_anchors"])

    def test_money_whitespace_is_cosmetic(self):
        self.assertNotIn("money", preserve.compare("R$ 120", "R$120")["missing_anchors"])

    def test_percent_whitespace_is_cosmetic(self):
        self.assertNotIn("percent", preserve.compare("12 %", "12%")["missing_anchors"])

    def test_percent_sign_change_matters(self):
        self.assertIn("percent", preserve.compare("-10%", "10%")["missing_anchors"])

    def test_cnpj_data_preserved(self):
        a = "CNPJ 12.345.678/0001-90"
        b = "CNPJ: 12.345.678/0001-90."
        self.assertFalse(preserve.compare(a, b)["review_required"])

    def test_uncertainty_equivalent_expression_false_positive_documented(self):
        res = preserve.compare("Pode ocorrer.", "É possível ocorrer.")
        self.assertTrue(res["review_required"])
        self.assertIn("Mudanças legítimas", res["limitations"])

    def test_unrelated_semantic_change_may_go_undetected(self):
        res = preserve.compare("O gato dorme.", "O gato corre.")
        self.assertFalse(res["review_required"])
        self.assertIn("ausência de alertas não valida", res["limitations"])

if __name__ == "__main__":
    unittest.main()
