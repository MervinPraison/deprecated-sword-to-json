import json
import os
from py.vars import expected_book_count
from py.vars import expected_chapter_count
from py.vars import expected_bloated_verse_count


class Validate:

    def __init__(self, version):
        self.version = version

        path = os.path.abspath('py')
        filename = f'{path}/validate.json'

        with open(filename) as data:
            my_json = json.load(data)
            validate = my_json.get(version, {})
        self.expected_omitted_count = validate.get('expectedOmittedCount')

    def keys(self, actual_key_count):
        expected_key_count = 1
        msg = f'{self.version} - invalid module keys count, expected {expected_key_count} but got {actual_key_count}'
        assert actual_key_count == expected_key_count, msg

    def books(self, actual_book_count):
        msg = f'{self.version} - invalid book count, expected {expected_book_count} but got {actual_book_count}'
        assert actual_book_count == expected_book_count, msg

    def chapters(self, actual_chapter_count):
        msg = f'{self.version} - invalid chapter count, expected {expected_chapter_count} ' \
              f'but got {actual_chapter_count}'
        assert actual_chapter_count == expected_chapter_count, msg

    def verses(self, actual_verse_count, actual_eoc_differences_count, actual_omitted_verses_count):

        # TODO: Add super validation using self.expected_omitted_count AND self.expected_omitted_verses_count (add it)
        # can_validate = isinstance(self.expected_omitted_count, int)
        # if can_validate:

        actual_bloated_verse_count = actual_verse_count + actual_eoc_differences_count + actual_omitted_verses_count

        msg = f'{self.version} - invalid bloated verse count, expected {expected_bloated_verse_count} ' \
              f'but got {actual_bloated_verse_count}'
        assert actual_bloated_verse_count == expected_bloated_verse_count, msg
        print(f'{self.version} - PASSED verse count check => {actual_verse_count}')
        # TODO: return False if not super validation
        return True

        # else:
        #     print(f'{self.version} - WARNING: insufficient data to perform verse count check')
        #     return False
