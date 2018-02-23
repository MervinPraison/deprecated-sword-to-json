from pysword.modules import SwordModules
import argparse
import time
from py.Report import Report
from py.Validate import Validate
from pathlib import Path
from py.vars import omissible_verses
from py.vars import permissible_eoc_differences
from py.helpers import does_bible_json_exist
from py.helpers import write_bible_json

# from pprint import pprint  # pprint(vars(book))


def get_bible_json(path, overwrite):
    modules = SwordModules(path)
    found_modules = modules.parse_modules()
    keys = found_modules.keys()
    version = list(keys)[0]
    validate = Validate(version)
    report = Report(version)
    validate.keys(len(keys))

    exists_obj = does_bible_json_exist(version)
    if exists_obj['exists'] and not overwrite:
        print(f'{version} - skipping')
        return None

    bible = modules.get_bible_from_module(version)
    raw_books = bible.get_structure()._books['ot'] + bible.get_structure()._books['nt']
    validate.books(len(raw_books))

    print('==================================================')
    print(f'{version} - processing in progress, please wait')

    chapter_count = 0
    all_verses = []
    omitted_verses = []
    actual_eoc_differences = []
    books = []
    start = time.time()

    for book_idx, book in enumerate(raw_books):

        # TODO: Add more checks based on book info
        # pprint(vars(book))

        report.processed(book_idx + 1, book.osis_name, start)
        range_chapters = range(1, book.num_chapters + 1)
        chapters = []

        for chapter in range_chapters:

            raw_verses = book.get_indicies(chapter)
            verses = []

            for verseIdx, verse in enumerate(raw_verses):

                verse_ref = book.osis_name + ' ' + str(chapter) + ':' + str(verseIdx + 1)

                try:
                    text = bible.get(books=[book.name], chapters=[chapter], verses=[verseIdx + 1])
                except Exception as e:
                    if 'incorrect header' in str(e):
                        if verse_ref in omissible_verses or verse_ref in permissible_eoc_differences:
                            text = None
                        else:
                            print(f'{version} - aborting with error on {verse_ref}')
                            print(f'{version} - {str(e)}')
                            return None
                    else:
                        raise e

                # if verse_ref == 'Romans 16:25':
                #     print(f'{verse_ref} = "{text}"')

                if text is not None:
                    text = text.strip()

                if text == '':
                    text = None

                if text is None:
                    if verse_ref in omissible_verses:
                        omitted_verses.append(verse_ref)
                    elif verse_ref in permissible_eoc_differences:
                        pass
                    else:
                        raise Exception(f'{version} - text is none for {verse_ref}')

                else:

                    verse = {
                        'verse': verseIdx + 1,
                        'chapter': chapter,
                        'ref': verse_ref,
                        'text': text
                    }
                    verses.append(verse)
                    all_verses.append(verse)

            # TODO: Add testament
            chapters.append({
                'chapter': chapter,
                'name': book.osis_name + ' ' + str(chapter),
                'verses': verses
            })

        chapter_count += len(chapters)

        books.append({
            'name': book.osis_name,
            'chapters': chapters
        })

    for eoc_difference in permissible_eoc_differences:
        eoc_verse = next((x for x in all_verses if x['ref'] == eoc_difference), None)
        if eoc_verse is None:
            actual_eoc_differences.append(eoc_difference)

    report.summary(len(books), chapter_count, len(all_verses))
    report.omitted(omitted_verses)
    report.eoc(actual_eoc_differences)

    validate.chapters(chapter_count)
    passed_verses = validate.verses(len(all_verses), len(actual_eoc_differences), len(omitted_verses))

    return {
        'version': version,
        'omittedVerses': omitted_verses,
        'endOfChapterDifferences': actual_eoc_differences,
        'verseCount': len(all_verses),
        'passedVerseCountChecks': passed_verses,
        'books': books
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    overwrite = args.overwrite

    paths = Path('sword-modules').glob('**/*.zip')
    for path in paths:
        bible = get_bible_json(str(path), overwrite)
        if bible is not None:
            write_bible_json(bible)


if __name__ == '__main__':
    main()
