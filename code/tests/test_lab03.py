import tempfile
import unittest
from pathlib import Path

from lab03_vlm_ui.agent import CockpitUIAgent


class CockpitUITests(unittest.TestCase):
    def test_normal_action_is_simulated(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            agent = CockpitUIAgent(audit_path=Path(directory) / "audit.jsonl")
            event = agent.simulate("unused.svg", "打开空调")
            self.assertEqual(event["status"], "simulated")
            self.assertEqual(event["plan"]["target_id"], "ac_toggle")

    def test_critical_action_requires_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            agent = CockpitUIAgent(audit_path=Path(directory) / "audit.jsonl")
            pending = agent.simulate("unused.svg", "切换运动模式")
            self.assertEqual(pending["status"], "confirmation_required")
            confirmed = agent.simulate("unused.svg", "切换运动模式", confirmed=True)
            self.assertEqual(confirmed["status"], "simulated")

    def test_unknown_action_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            agent = CockpitUIAgent(audit_path=Path(directory) / "audit.jsonl")
            event = agent.simulate("unused.svg", "打开车窗")
            self.assertEqual(event["status"], "refused")


if __name__ == "__main__":
    unittest.main()
