import unittest,json
from MatchPhrases import MatchPhrases
import time
import random
from copy import deepcopy


class TestMatchPhrases(unittest.TestCase):
    def setUp(self):
        self.match = MatchPhrases("phrases.txt")

    def tearDown(self):
        self.match = None

    def test_single_phrase_match(self):
        matched_phrases = json.loads(self.match.find_matches("I have a sore throat"))
        self.assertIn("sore throat",matched_phrases)

    def test_partial_match_is_rejected(self):
        matched_phrases = json.loads(self.match.find_matches("I have a wonderful family"))
        self.assertEqual(matched_phrases,[])

    def test_string_overlap_is_rejected(self):
        matched_phrases = json.loads(self.match.find_matches("scrofulators are my favourite band. I also like herp"))
        self.assertEqual(matched_phrases,[])

    def test_beginning_end(self):
        matched_phrases=json.loads(self.match.find_matches("cellulites is bad. I also hate herpes simplex type 2 infection"))
        self.assertEqual(len(matched_phrases), 2)

    def test_no_duplicates(self):
        matched_phrases = json.loads(self.match.find_matches("I have a sore throat . I really have a sore throat"))
        self.assertEqual(len(matched_phrases), 1)

    def test_multiple_phrases_match(self):
        matched_phrases=json.loads(self.match.find_matches("do I have cancer or just a sore throat"))
        self.assertIn("cancer",matched_phrases)
        self.assertIn("sore throat",matched_phrases)

    def test_no_match(self):
        matched_phrases=json.loads(self.match.find_matches("I feel great"))
        self.assertEqual(matched_phrases,[])

    def test_survive_special_characters(self):
        matched_phrases = json.loads(self.match.find_matches("Do you think I have Hunnington's Corèa?"))
        pass

    def test_empty_line(self):
        matched_phrases = json.loads(self.match.find_matches(""))
        self.assertEqual(matched_phrases,[])

    def test_scalable_to_long_sentence(self):
        s="*"
        for i in range(1024):
            s += ' *'
        start = time.clock()
        matched_phrases = json.loads(self.match.find_matches(s))
        parsing_time = time.clock() - start
        self.assertLess(parsing_time, 0.1)  # scalable request shouldn't take more than 0.1 s

    def test_random_word(self):
        matched_phrases = json.loads(self.match.find_matches(random.choice(self.match.phrases)))
        self.assertEqual(len(matched_phrases), 1)

    def test_scalable_to_long_wordlist(self):
        match=deepcopy(self.match)
        match.phrases += 10*match.phrases
        start = time.clock()
        matched_phrases = json.loads(match.find_matches("I have a sore throat"))
        parsing_time = time.clock() - start
        self.assertLess(parsing_time, 0.1)  # scalable request shouldn't take more than 0.1 s


if __name__ == '__main__':
    unittest.main()
