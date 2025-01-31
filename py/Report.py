import math
import sys
import time
from py.vars import expected_book_count


class Report:

    def __init__(self, version):
        self.version = version

    def processed(self, book_idx, book_name, start):
        elapsed = str(math.floor(time.time() - start)).zfill(3)
        str_book_idx = str(book_idx).zfill(2)
        str_book_name = book_name.ljust(6)
        bar = '|' + '#' * (book_idx - 1) + ' ' * (expected_book_count - book_idx) + '|'
        msg = f'{self.version} - {str_book_idx} {str_book_name} {bar} {elapsed} sec'
        sys.stdout.write('\r' + msg)
        sys.stdout.flush()

    def summary(self, books, chapters, verses):
        print()
        print(f'{self.version} - processing complete with {books} books {chapters} chapters {verses} verses')

    def omitted(self, omitted):
        if len(omitted):
            print(f'{self.version} - {len(omitted)} omitted verses found:')
            print(omitted)
        else:
            print(f'{self.version} - no omitted verses found')

    def eoc(self, eoc):
        if len(eoc):
            print(f'{self.version} - {len(eoc)} end of chapter differences found:')
            print(eoc)
        else:
            print(f'{self.version} - no end of chapter differences found')
