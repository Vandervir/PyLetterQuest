import itertools
import os
import sqlite3
import string
from timeit import default_timer as timer

from sqlbuilder.smartsql import Q, T, compile


class Database:
    DATABASE_NAME = 'database.db'

    def __exit__(self, *args):
        self.conn.close()

    def check_database_file(self):
        if not os.path.exists(self.DATABASE_NAME):
            print('-= Generating database =-')
            DbCreator(database=self.DATABASE_NAME)
            print('-=         Done.       =-')

    def __init__(self):
        self.query = None
        self.null_conditions = None
        self.letters_counter = None
        self.letters_list = None
        self.table = dict()
        self.create_table_reference()
        self.check_database_file()
        self.conn = sqlite3.connect(self.DATABASE_NAME)

        self.cur = self.conn.cursor()

    def get_random_word(self):
        self.cur.execute('SELECT word, word_length FROM dictionary ORDER BY RANDOM() LIMIT 1')
        return self.cur.fetchone()

    def try_find_words(self, letters, length, skip_letters):
        # query  ='SELECT word, word_length FROM dictionary WHERE word like \'{}\' and word_length = {}'.format(letters, length)
        query  ='SELECT word, word_length FROM dictionary WHERE word like \'{}\''.format(letters)
        for letter in skip_letters:
            query += ' AND word not like \'%{}%\''.format(letter)
        self.cur.execute(query + ' LIMIT 1000')
        return self.cur.fetchall()

    @staticmethod
    def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]

    def get_table_by_name(self, char):
        pass

    def base_query(self, conditions):
        return compile(Q().tables(self.get_tables()).fields(self.get_fields()).where(conditions))

    def add_null_condition(self, condition_to_add):
        if self.null_conditions is None:
            self.null_conditions = condition_to_add
        else:
            self.null_conditions = self.null_conditions & condition_to_add

    def prepare_null_conditions(self, letters):
        self.letters_counter = dict()
        self.letters_list = []
        for char in string.ascii_lowercase:
            count = letters.count(char.upper())
            if count > 0:
                self.letters_counter[char] = count
                self.letters_list.append(char)
            else:
                self.letters_counter[char] = False
                self.add_null_condition(self.table[char].number.is_(None))

    def execute_main_condition(self):
        for r in reversed(range(2, self.letters_list.__len__() + 1)):
            for a in itertools.combinations(self.letters_list, r):
                start = timer()
                conditions = self.null_conditions
                smaller_query = None
                for val in a:
                    smaller_query = self.connect_conditions(
                        smaller_query,
                        self.table[val].number - self.letters_counter[val] <= 0,
                        'AND'
                    )
                for val in self.diff(self.letters_list, a):
                    smaller_query = self.connect_conditions(
                        smaller_query,
                        self.table[val].number.is_(None),
                        'AND'
                    )

                conditions = self.connect_conditions(conditions, smaller_query, 'AND', force_braces=True)
                result = self.execute_query(conditions)
                end = timer()
                print('{} finding word length: {} from: {}'.format(end - start, r, a))
                if result:
                    return next(iter(result), None)
        raise Exception('Shuffle tiles')

    def create_table_reference(self):
        self.table['a'] = T.letter_a
        self.table['b'] = T.letter_b
        self.table['c'] = T.letter_c
        self.table['d'] = T.letter_d
        self.table['e'] = T.letter_e
        self.table['f'] = T.letter_f
        self.table['g'] = T.letter_g
        self.table['h'] = T.letter_h
        self.table['i'] = T.letter_i
        self.table['j'] = T.letter_j
        self.table['k'] = T.letter_k
        self.table['l'] = T.letter_l
        self.table['m'] = T.letter_m
        self.table['n'] = T.letter_n
        self.table['o'] = T.letter_o
        self.table['p'] = T.letter_p
        self.table['q'] = T.letter_q
        self.table['r'] = T.letter_r
        self.table['s'] = T.letter_s
        self.table['t'] = T.letter_t
        self.table['u'] = T.letter_u
        self.table['v'] = T.letter_v
        self.table['w'] = T.letter_w
        self.table['x'] = T.letter_x
        self.table['y'] = T.letter_y
        self.table['z'] = T.letter_z
        pass

    def get_tables(self):
        return T.dictionary + self.table['a'].on(
            T.dictionary.id == self.table['a'].dict_id) + self.table['b'].on(
            T.dictionary.id == self.table['b'].dict_id) + self.table['c'].on(
            T.dictionary.id == self.table['c'].dict_id) + self.table['d'].on(
            T.dictionary.id == self.table['d'].dict_id) + self.table['e'].on(
            T.dictionary.id == self.table['e'].dict_id) + self.table['f'].on(
            T.dictionary.id == self.table['f'].dict_id) + self.table['g'].on(
            T.dictionary.id == self.table['g'].dict_id) + self.table['h'].on(
            T.dictionary.id == self.table['h'].dict_id) + self.table['i'].on(
            T.dictionary.id == self.table['i'].dict_id) + self.table['j'].on(
            T.dictionary.id == self.table['j'].dict_id) + self.table['k'].on(
            T.dictionary.id == self.table['k'].dict_id) + self.table['l'].on(
            T.dictionary.id == self.table['l'].dict_id) + self.table['m'].on(
            T.dictionary.id == self.table['m'].dict_id) + self.table['n'].on(
            T.dictionary.id == self.table['n'].dict_id) + self.table['o'].on(
            T.dictionary.id == self.table['o'].dict_id) + self.table['p'].on(
            T.dictionary.id == self.table['p'].dict_id) + self.table['q'].on(
            T.dictionary.id == self.table['q'].dict_id) + self.table['r'].on(
            T.dictionary.id == self.table['r'].dict_id) + self.table['s'].on(
            T.dictionary.id == self.table['s'].dict_id) + self.table['t'].on(
            T.dictionary.id == self.table['t'].dict_id) + self.table['u'].on(
            T.dictionary.id == self.table['u'].dict_id) + self.table['v'].on(
            T.dictionary.id == self.table['v'].dict_id) + self.table['w'].on(
            T.dictionary.id == self.table['w'].dict_id) + self.table['x'].on(
            T.dictionary.id == self.table['x'].dict_id) + self.table['y'].on(
            T.dictionary.id == self.table['y'].dict_id) + self.table['z'].on(
            T.dictionary.id == self.table['z'].dict_id)

    @staticmethod
    def get_fields():
        return T.dictionary.word, T.dictionary.word_length

    def execute_query(self, conditions):
        query = self.base_query(conditions)

        self.cur.execute(query[0] % tuple(query[1]))
        return self.cur.fetchall()

    def find_longest_word(self, letters):
        self.prepare_null_conditions(letters)
        return self.execute_main_condition()

    # noinspection PyRedundantParentheses
    @staticmethod
    def connect_conditions(condition, new_thing, connector, force_braces=False):
        if condition is None:
            return new_thing

        if connector == 'OR':
            if force_braces:
                return condition | (new_thing)
            return condition | new_thing
        else:
            if force_braces:
                return condition & (new_thing)
            return condition & new_thing


class DbCreator:
    dictionary = 'raw_words.txt'
    cursor = ''

    def __init__(self, dictionary='dictionary.txt', database='database.db'):
        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()
        self.dictionary = dictionary
        self.create_table()
        self.read_words()
        self.conn.close()

    def create_table(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS dictionary (id INTEGER PRIMARY KEY, word_length INTEGER NOT "
            "NULL, word TEXT NOT NULL);"
        )
        self.cursor.execute(
            "CREATE INDEX IF NOT EXISTS `idx_dict_id` ON `dictionary`(`id` ASC);"
        )

        for char in string.ascii_lowercase:
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS letter_{} (id INTEGER PRIMARY KEY, dict_id INTEGER NOT NULL, "
                "number INTEGER NOT NULL);".format(char)
            )
            self.cursor.execute(
                "CREATE INDEX IF NOT EXISTS `idx_letter_{}` ON `letter_{}`(`dict_id` ASC);".format(char, char)
            )
            self.cursor.execute(
                "CREATE INDEX IF NOT EXISTS `idx_number_{}` ON `letter_{}`(`number` ASC);".format(char, char)
            )
        self.conn.commit()

    def split_to_dict(self, dict_id, word):
        for char in string.ascii_uppercase:
            if word.count(char) == 0:
                continue
            self.cursor.execute(
                "INSERT INTO letter_{} (dict_id, number) values (?,?)".format(char.lower()),
                (dict_id, word.count(char),)
            )

    def read_words(self):
        fo = open(self.dictionary, "r")

        for line in fo.readlines():
            line = line.strip()
            self.cursor.execute("INSERT INTO dictionary (word_length, word) values (?,?)",
                                (line.__len__(), line,))
            self.split_to_dict(self.cursor.lastrowid, line)

        self.conn.commit()
        fo.close()
