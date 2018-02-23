import json
import os


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
