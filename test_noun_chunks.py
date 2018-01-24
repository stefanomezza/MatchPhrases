import unittest,json
from MatchNounChunks import MatchNounChunks
import time
import random
from copy import deepcopy


class TestMatchPhrases(unittest.TestCase):
    def setUp(self):
        self.match = MatchNounChunks("phrases.txt")

    def tearDown(self):
        self.match = None

    def test_single_phrase_match(self):
        matched_phrases = json.loads(self.match.find_matches("I have sore throat"))
        self.assertIn("sore throat",matched_phrases)

    def test_partial_match_is_rejected(self):
        matched_phrases = json.loads(self.match.find_matches("I have a wonderful family"))
        self.assertEqual(matched_phrases,[])

    def test_no_duplicates(self):
        matched_phrases = json.loads(self.match.find_matches("I have sore throat . I really have sore throat"))
        self.assertEqual(len(matched_phrases), 1)

    def test_random_word(self):
        matched_phrases = json.loads(self.match.find_matches(random.choice(self.match.phrases)))
        self.assertEqual(len(matched_phrases), 1)

    def test_multiple_phrases_match(self):
        matched_phrases=json.loads(self.match.find_matches("do I have cancer or do I have sore throat"))
        self.assertIn("cancer",matched_phrases)
        self.assertIn("sore throat",matched_phrases)

    def test_no_match(self):
        matched_phrases=json.loads(self.match.find_matches("I feel great"))
        self.assertEqual(matched_phrases,[])

    def test_article(self):
        matched_phrases = json.loads(self.match.find_matches("I have a sore throat"))
        self.assertIn("sore throat",matched_phrases)
        self.assertNotIn("throat",matched_phrases)

    def test_survive_special_characters(self):
        matched_phrases = json.loads(self.match.find_matches("Do you think I have Hunnington's Corèa?"))
        pass

    def test_scalable_to_long_sentence(self):
        s="*"
        for i in range(1024):
            s += ' *'
        start = time.clock()
        matched_phrases = json.loads(self.match.find_matches(s))
        parsing_time = time.clock() - start
        self.assertLess(parsing_time, 0.1)  # server request shouldn't take more than 0.1 s

    def test_scalable_to_long_wordlist(self):
        match=deepcopy(self.match)
        match.phrases += 10*match.phrases
        start = time.clock()
        matched_phrases = json.loads(match.find_matches("I have a sore throat"))
        parsing_time = time.clock() - start
        self.assertLess(parsing_time, 0.1)  # server request shouldn't take more than 0.1 s

if __name__ == '__main__':
    unittest.main()
