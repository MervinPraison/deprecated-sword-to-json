import json


def load_checks(version):
    # path = os.path.abspath('')
    # filename = f'{path}/optional-extra-verse-checks-data.json'

    with open('optional-extra-verse-checks-data.json') as data:
        my_json = json.load(data)
        checks = my_json.get(version, {})

    return checks
