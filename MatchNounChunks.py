import cherrypy as http
import os
import json
from bisect import bisect_left
import spacy


class MatchNounChunks:
    """
    MatchNounChunks: parse sentences and identify medical phrases inside the sentence.
    The find_matches method is exposable, in order to allow a CherryPy server to expose it
    """

    def __init__(self, phrases_file):
        """
        constructor for the MatchNounChunks class. loads the phrases to match and instantiates SpaCy
        :param phrases_file: file containing a list of medical phrases which will be used as a lookup dictionary
        :type phrases_file: str
        :raises AssertionError: if the file phrases_file doesn't exist
        """
        self.phrases = []  # Phrases to lookup in the input sentence
        assert(os.path.isfile(phrases_file))
        with open(phrases_file) as pfile:
            for line in pfile:
                self.phrases.append(line.strip())
        self.phrases+=10*self.phrases
        self.phrases.sort()
        self.spacy_inst = spacy.load("en")

    def check_match(self, noun_chunk):
        """
        check whether the given noun-chunk appears in the phrases list.
        the list is read using binary search to reduce time complexity of the check from O(n) to O(log n)
        :param noun_chunk: noun-chunk to check
        :type noun_chunk: str
        :returns whether the noun chunk appears in the phrases list
        """
        # Locate the leftmost value exactly equal to x
        i = bisect_left(self.phrases, noun_chunk)
        if i != len(self.phrases) and self.phrases[i] == noun_chunk:
            return True
        return False

    @http.expose
    def find_matches(self, text):
        """
        find the noun chunks in the sentence matching any of the phrases in the phrases list
        :param text: input sentence to parse
        :type text: str
        :returns json-encoded list of matched phrases
        :rtype: str (json)
        """
        found_phrases = set()
        doc = self.spacy_inst(text)
        for np in doc.noun_chunks:
            if self.check_match(np.text):
                found_phrases.add(np.text)
        return json.dumps(list(found_phrases))
