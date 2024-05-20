import unittest

from sc2_evals.agents.openai.message_param import system_message

class TestAgent(unittest.TestCase):

    def test_message_params(self):
        message = system_message("test")
        self.assertEqual(message, {"role": "system", "content": "test"})

if __name__ == "__main__":
    unittest.main()
