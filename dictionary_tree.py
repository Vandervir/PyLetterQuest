from timeit import default_timer as timer

from word_classification import WordClassification


class DictionaryTree:
    def __init__(self, letter, is_end=False, word=None):
        self.children = dict()
        self.letter = letter
        self.is_end = is_end
        self.word = word


class TreeCreator:
    def __init__(self, dictionary='dictionary.txt'):
        self.dictionary = dictionary
        self.wc = WordClassification()
        self.read_words()

    def insert(self, root, letters, word):
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
            self.insert(self.root, line, line)
        fo.close()

    def search_for_word(self, root, letters):
        if letters is None or letters.__len__() == 0:
            return
        for letter in root.children:
            if letter in letters:
                if root.children[letter].is_end:
                    self.wc.run(root.children[letter].word)
                    self.found.append(root.children[letter].word)
                left_letters = letters[:]
                left_letters.remove(letter)
                self.search_for_word(root.children[letter], left_letters)

    def search(self, letters):
        self.current_word = ''
        self.found = []
        self.wc.new_search()

        start = timer()
        self.search_for_word(self.root, sorted(letters))
        end = timer()
        print('{} finding word  {}'.format(end - start, self.wc.get_word()))
        return self.wc.get_word()

    def get_next_word(self):
        return self.wc.get_next_word()
