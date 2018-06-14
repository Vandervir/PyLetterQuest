import itertools
from timeit import default_timer as timer

class DictionaryTree:
    def __init__(self, letter, is_end=False, word=None):
        self.children = dict()
        self.letter = letter
        self.is_end = is_end
        self.word = word


class TreeCreator:
    def __init__(self, dictionary='dictionary.txt', database='database.db'):
        self.dictionary = dictionary
        self.read_words()

    def insert(self, root, letters, word=None):
        if word is None:
            word = letters
        letter = letters[:1]
        left_letters = letters[1:]
        if not root.children.has_key(letter):
            root.children[letter] = DictionaryTree(letter)

        if left_letters.__len__() == 0:
            root.children[letter].is_end = True
            root.children[letter].word = word
            return
        self.insert(root.children[letter], left_letters, word)

    def read_words(self):
        self.root = DictionaryTree(None)
        fo = open(self.dictionary, "r")
        for line in fo.readlines():
            line = line.strip()
            sorted_letters = ''.join(sorted(line))
            # print(sorted_letters)
            self.insert(self.root, sorted_letters, line)
        fo.close()

    def search_for_word(self, root, letters):
        letter = letters[:1]
        left_letters = letters[1:]
        if root.is_end is True:
            self.word_classification(root.word)
        for l in self.root.children:
            if l == letter and left_letters.__len__() > 0 and root.children.has_key(letter):
                self.search_for_word(root.children[letter], left_letters)

    def word_classification(self, word):
        if self.current_word.__len__() < word.__len__():
            self.current_word = word

    def search(self, letters):
        # sorted_letters = ''.join(sorted(letters))
        i = 0
        self.current_word = ''
        self.found = dict()

        start = timer()
        for r in reversed(range(2, letters.__len__() + 1)):
            for a in itertools.combinations(letters, r):
                sl = ''.join(sorted(a))
                res = self.search_for_word(self.root, sl)
                if res is not None:
                    print(res)

        end = timer()
        print('{} finding word  {}'.format(end - start, self.current_word))
        return self.current_word
