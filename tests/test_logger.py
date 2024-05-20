import datetime
import unittest
import shutil

from sc2_evals.agents.openai.logger import Logger
from sc2_evals.agents.models import ModelInfo, Model


class TestLogger(unittest.TestCase):

    def test_logger(self):
        model_info = ModelInfo(Model.GPT_35_TURBO_0125)
        logger = Logger("testdir", model_info, "game")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        self.assertEqual(logger._dir, f"testdir/game/{timestamp}/gpt_35_turbo_0125")
        shutil.rmtree("testdir")


if __name__ == "__main__":
    unittest.main()
