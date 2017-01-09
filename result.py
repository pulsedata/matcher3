'''
Welcome to Matcher 3
(c) PulseData/ftxrc 2016

This matches the pristine, virgin PR.gov into usable ones.
'''

# from sys import argv

class Result:
    """ The Matcher result store. """
    def __init__(self):
        """ Initialize the Result store. """
        # Low accuracy (manual review)
        self._high = []
        # Medium-tier accuracy (30% or high Leveinstein)
        self._medium = []
        # High-confidence results (1:1 or close)
        self._low = []

    def insert(self, confidence, payload):
        """ Categorize and insert depending on the confidence score. """
        if confidence >= 90:
            # High-confidence
            self._high.append(payload)
        elif confidence < 90 and confidence >= 30:
            self._medium.append(payload)
        elif confidence < 30:
            self._low.append(payload)

    @property
    def high(self):
        return self._high

    @property
    def medium(self):
        return self._medium
    
    @property
    def low(self):
        return self._low
    
    @property
    def all(self):
        return self.high + self.medium + self.low

