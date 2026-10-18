import tempfile
import unittest
from pathlib import Path
from paper_trading import PaperLedger, calculate_position_risk

class PaperTradingTests(unittest.TestCase):
    def test_risk_amount(self):
        self.assertEqual(calculate_position_risk(1000, 1, 1.1, 1.09)["risk_amount"], 10.0)
    def test_risk_above_two_percent_rejected(self):
        with self.assertRaises(ValueError):
            calculate_position_risk(1000, 3, 1.1, 1.09)
    def test_paper_trade_persists(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = PaperLedger(Path(tmp) / "trades.json")
            ledger.add("EURUSD", "BUY", 1.1, 1.09, 1.12, 1)
            self.assertEqual(len(ledger.list_all()), 1)
    def test_invalid_buy_levels_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = PaperLedger(Path(tmp) / "trades.json")
            with self.assertRaises(ValueError):
                ledger.add("EURUSD", "BUY", 1.1, 1.12, 1.13, 1)

if __name__ == "__main__":
    unittest.main()
