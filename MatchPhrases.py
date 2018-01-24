import cherrypy as http
import os
import json


class MatchPhrases:
    """
    MatchPhrases: parse sentences and identify medical phrases inside the sentence.
    The find_matches method is exposable, in order to allow a CherryPy server to expose it
    """

    def __init__(self, phrases_file):
        """
        constructor for the MatchNounChunks class. loads the phrases to match.
        :param phrases_file: file containing a list of medical phrases which will be used as a lookup dictionary
        :type phrases_file: str (filename)
        :raises AssertionError: if the file phrases_file doesn't exist
        """
        self.phrases = []  # Phrases to lookup in the input sentence
        assert (os.path.isfile(phrases_file))
        with open(phrases_file) as pfile:
            for line in pfile:
                self.phrases.append(line.strip())

    @staticmethod
    def check_match(sentence, phrase):
        """
        check whether the given sentence contains the given phrase.
        :param sentence: input sentence
        :type sentence: str
        :param phrase: phrase to search in the sentence
        :type phrase: str
        :returns whether the phrase appears in the sentence
        :rtype: bool
        """
        # leading and trailing spaces allow to check whether the phrase is at the beginning/end of the sentence.
        # it also avoid misclassification of substrings as sentences (ex. phrase 'hiv' matching "hive mind")
        return " " + phrase + " " in " " + sentence + " "

    @staticmethod
    def extend(phrases_list, new_phrase):
        """
        add new phrase to the phrases list if it's not already there / it's not a subphrase of any phrases.
        remove any subphrases of the new phrase
        :param phrases_list: set of phrases found until now
        :type phrases_list: set
        :param new_phrase: new phrase to add
        :type new_phrase: str
        """
        trash_list = []  # phrases to eliminate
        for phrase in phrases_list:
            if new_phrase in phrase:  # new_phrase is a subphrase of an already found phrase
                return
            elif phrase in new_phrase:  # new_phrase extend this phrase: remove the entry
                trash_list.append(phrase)
        for trash in trash_list:
            phrases_list.remove(trash)
        phrases_list.add(new_phrase)

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
        for phrase in self.phrases:
            if self.check_match(text, phrase):
                self.extend(found_phrases, phrase)
        return json.dumps(list(found_phrases))
