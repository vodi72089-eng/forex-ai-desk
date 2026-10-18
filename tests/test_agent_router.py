import os
import unittest
from unittest.mock import patch
from agent_router import ask_jev_compatible, ask_agent

class AgentRouterTests(unittest.TestCase):
    def test_missing_jev_config_returns_helpful_error(self):
        with patch.dict(os.environ, {"JEV_BASE_URL": "", "JEV_API_KEY": "", "JEV_MODEL": ""}, clear=False):
            reply = ask_jev_compatible("Summarize this strategy")
        self.assertFalse(reply.ok)
        self.assertIn("JEV_BASE_URL", reply.detail)

    def test_unknown_preferred_agent_falls_back_to_jev_adapter(self):
        with patch.dict(os.environ, {"JEV_BASE_URL": "", "JEV_API_KEY": "", "JEV_MODEL": ""}, clear=False):
            reply = ask_agent("test", preferred="unknown")
        self.assertFalse(reply.ok)
        self.assertEqual(reply.provider, "none")

if __name__ == "__main__":
    unittest.main()
