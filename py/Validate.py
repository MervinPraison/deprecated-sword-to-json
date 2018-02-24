import json
import os
from py.vars import expected_book_count, expected_chapter_count, expected_bloated_verse_count


class Validate:

    def __init__(self, version):
        self.version = version

        path = os.path.abspath('')
        filename = f'{path}/optional-extra-verse-checks-data.json'

        with open(filename) as data:
            my_json = json.load(data)
            validate = my_json.get(version, {})
        self.expected_omitted_verses = validate.get('expectedOmittedVerses')
        self.expected_eoc_differences = validate.get('expectedEndOfChapterDifferences')

    def keys(self, actual_key_count):
        expected_key_count = 1
        msg = f'{self.version} - invalid module keys count, expected {expected_key_count} but got {actual_key_count}'
        assert actual_key_count == expected_key_count, msg

    def books(self, actual_book_count):
        msg = f'{self.version} - invalid book count, expected {expected_book_count} but got {actual_book_count}'
        assert actual_book_count == expected_book_count, msg

    def chapters(self, actual_chapter_count):
        msg = f'{self.version} - invalid chapter count, expected {expected_chapter_count} but got {actual_chapter_count}'
        assert actual_chapter_count == expected_chapter_count, msg

    def verses(self, actual_verse_count, actual_eoc_differences, actual_omitted_verses):

        # TODO: Add super validation using self.expected_omitted_count AND self.expected_omitted_verses_count (add it)
        # can_validate = isinstance(self.expected_omitted_count, int)
        # if can_validate:

        actual_bloated_verse_count = actual_verse_count + len(actual_eoc_differences) + len(actual_omitted_verses)

        msg = f'{self.version} - invalid bloated verse count, expected {expected_bloated_verse_count} but got {actual_bloated_verse_count}'
        assert actual_bloated_verse_count == expected_bloated_verse_count, msg
        print(f'{self.version} - PASSED verse count check => {actual_verse_count}')
        # TODO: return False if not super validation

        can_do_extra_checks = isinstance(self.expected_omitted_verses, list) and isinstance(self.expected_eoc_differences, list)

        if not can_do_extra_checks:
            print(f'{self.version} - SKIPPED extra verse checks due to insufficient data')
            return False

        else:

            sorted_expected_omitted_verses = sorted(self.expected_omitted_verses)
            sorted_actual_omitted_verses = sorted(actual_omitted_verses)
            sorted_expected_eoc_differences = sorted(self.expected_eoc_differences)
            sorted_actual_eoc_differences = sorted(actual_eoc_differences)

            msg = f'{self.version} - invalid omitted verses, expected {sorted_expected_omitted_verses} but got {sorted_actual_omitted_verses}'
            assert sorted_actual_omitted_verses == sorted_expected_omitted_verses, msg

            msg = f'{self.version} - invalid end of chapter differences, expected {sorted_expected_eoc_differences} but got {sorted_actual_eoc_differences}'
            assert sorted_actual_eoc_differences == sorted_expected_eoc_differences, msg

            print(f'{self.version} - PASSED extra verse checks')
            return True
