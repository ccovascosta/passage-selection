import unittest
from src.main import main

class TestPassageSelectionPipeline(unittest.TestCase):

    def test_pipeline(self):
        utterance = "Explain the benefits of green tea"
        folder_path = "sample_data"
        top_k = 5
        results = main(utterance, folder_path, top_k)
        self.assertTrue(len(results) > 0)
        for result in results:
            self.assertIsInstance(result[0], str)
            self.assertIsInstance(result[1], str)
            self.assertIsInstance(result[2], float)

if __name__ == "__main__":
    unittest.main()
