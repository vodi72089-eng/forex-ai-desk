import unittest
from strategy_analyzer import review_strategy, build_ai_prompt

class StrategyAnalyzerTests(unittest.TestCase):
    def test_detects_common_strategy_terms(self):
        result = review_strategy("Entry on H1, stop loss 20 pips, take profit 40 pips, risk management.")
        for key in ("entrée", "stop loss", "take profit", "timeframe", "gestion du risque"):
            self.assertTrue(result["checks"][key], key)
    def test_empty_text_warns(self):
        result = review_strategy("")
        self.assertGreater(len(result["warnings"]), 0)
        self.assertEqual(result["word_count"], 0)
    def test_prompt_limits_document_length(self):
        prompt = build_ai_prompt("x" * 30000)
        self.assertLess(len(prompt), 25000)
        self.assertIn("aucun ordre de trading", prompt.lower())

if __name__ == "__main__":
    unittest.main()
