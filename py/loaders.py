import json
from pathlib import Path


def load_checks(version):
    # path = os.path.abspath('')
    # filename = f'{path}/optional-extra-verse-checks-data.json'

    with open('optional-extra-verse-checks-data.json') as data:
        my_json = json.load(data)
        checks = my_json.get(version, {})

    return checks


def load_psalms_check(version):
    paths = Path('psalms').glob(f'**/{version}.json')
    paths = list(paths)
    path = paths[0] if len(paths) else None
    psalms = None

    if path is not None:
        with open(path) as data:
            psalms = json.load(data)

    return psalms
