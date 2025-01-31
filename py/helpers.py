import json
import os
import re
from comparators.eng.biblehub.comparator import BibleHubComparator
from py.loaders import load_checks


def does_bible_json_exist(version):
    path = os.path.abspath(f'bibles/{version}')
    filename = f'{path}/{version}.json'
    return {
        'exists': os.path.exists(filename),
        'path': path,
        'filename': filename
    }


def write_bible_json(bible):
    version = bible['version']
    exists_obj = does_bible_json_exist(version)

    if not os.path.exists(exists_obj['path']):
        os.makedirs(exists_obj['path'])

    print(f'{version} - writing JSON file')
    with open(exists_obj['filename'], 'w') as f:
        json.dump(bible, f)

    if os.environ.get('PYTHON_ENV') == 'development':
        for book in bible['books']:
            for chapter in book['chapters']:
                chapter['verses'] = []

        partial_filename = re.sub('.json$', '-partial.json', exists_obj['filename'])
        with open(partial_filename, 'w') as f:
            f.write(json.dumps(bible, indent=2))


def get_comparator(version):
    checks = load_checks(version)
    str_comparator = checks.get('comparator').get('name')

    if str_comparator == 'BibleHubComparator':
        return BibleHubComparator(version)

    return None
