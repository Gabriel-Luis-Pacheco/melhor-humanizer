"""Corpus checks and advisory output comparisons."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "eval"))
import check_runs

class CorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = check_runs.load_jsonl(ROOT / "eval/casos.jsonl")

    def test_corpus_integrity(self):
        check_runs.validate_cases(self.cases)
        self.assertEqual(len(self.cases), 40)
        self.assertGreaterEqual(sum(c["control"] for c in self.cases), 14)

    def test_genre_diversity(self):
        self.assertGreaterEqual(len({c["genre"] for c in self.cases}), 15)

    def test_good_control_kept_no_flags(self):
        res = check_runs.evaluate(self.cases, [{"id": "R09", "output": "O céu estava azul naquele dia."}])
        self.assertEqual(res["outputs_needing_review"], 0)

    def test_new_fact_flagged(self):
        res = check_runs.evaluate(self.cases, [
            {"id": "E05", "output": "Na auditoria de julho, identificamos divergência de R$ 1.200."}])
        names = [f["kind"] for f in res["results"][0]["review_flags"]]
        self.assertIn("preservation_warning", names)

    def test_missing_required_fragment_flagged(self):
        res = check_runs.evaluate(self.cases, [{"id": "E07", "output": "A API pode falhar."}])
        self.assertIn("required_text_missing", [r["kind"] for r in res["results"][0]["review_flags"]])

    def test_overedit_control_flagged(self):
        res = check_runs.evaluate(self.cases, [{"id": "R09", "output": "Uma história totalmente diferente."}])
        self.assertIn("possible_overediting", [r["kind"] for r in res["results"][0]["review_flags"]])

    def test_candidate_labels_separate(self):
        res = check_runs.evaluate(self.cases, [{"candidate": "A", "id": "R09", "output": "O céu estava azul naquele dia."},
                                               {"candidate": "B", "id": "R09", "output": "O céu estava azul naquele dia."}])
        self.assertEqual(res["outputs_received"], {"A": 1, "B": 1})

    def test_unknown_case_rejected(self):
        with self.assertRaises(ValueError):
            check_runs.evaluate(self.cases, [{"id": "none", "output": "x"}])

    def test_duplicate_case_rejected(self):
        with self.assertRaises(ValueError):
            check_runs.evaluate(self.cases, [{"id": "R09", "output": "x"},
                                             {"id": "R09", "output": "y"}])

    def test_duplicate_corpus_id_rejected(self):
        with self.assertRaises(ValueError):
            check_runs.validate_cases(self.cases + [self.cases[0]])

    def test_broken_jsonl_is_error(self):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / "invalid.jsonl"
            file.write_text("{invalid\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "JSON inválido"):
                check_runs.load_jsonl(file)

if __name__ == "__main__":
    unittest.main()
