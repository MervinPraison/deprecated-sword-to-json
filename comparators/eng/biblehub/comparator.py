import os
import xml.etree.ElementTree
from py.loaders import load_checks


class BibleHubComparator:

    def __init__(self, version):

        checks = load_checks(version)
        self.prefer = checks.get('comparator').get('prefer')

        path = os.path.abspath('comparators/eng/biblehub')
        filename = f'{path}/bibles.xml'
        root = xml.etree.ElementTree.parse(filename).getroot()[0][0]
        self.rows = root.findall('Row')
        self.column = None
        self.row = 1
        self.version = version

        for idx, datum in enumerate(self.rows[0].iter('Data')):
            if datum.text != 'Verse' and datum.text == version:
                self.column = idx

        if self.column is None:
            raise Exception(f'{self.version} - unknown version for BibleHubComparator')

    def preferred(self, my_verse, comparator_verse, ref):

        omv = my_verse
        ocv = comparator_verse

        preferred_verse = ''

        while len(my_verse) or len(comparator_verse):

            found = False
            for prefer in self.prefer:
                # print(my_verse.startswith(prefer[0]))
                # print(comparator_verse.startswith(prefer[1]))

                allow = True
                if len(prefer) > 3:
                    allow = ref == prefer[3]

                if my_verse.startswith(prefer[0]) and comparator_verse.startswith(prefer[1]) and allow:
                    preferred_verse = preferred_verse + prefer[2]
                    my_verse = my_verse.replace(prefer[0], '', 1)
                    comparator_verse = comparator_verse.replace(prefer[1], '', 1)
                    found = True
                    break

            if not found:

                if my_verse[0] == comparator_verse[0]:
                    preferred_verse = preferred_verse + my_verse[0]
                    my_verse = my_verse[1:]
                    comparator_verse = comparator_verse[1:]

                else:

                    print('\n')
                    print(f'{self.version} - {ref}')
                    print(f'{self.version} - my verse:')

                    print(f'{self.version} - {ref}')
                    print(f'{self.version} - my verse:')
                    print(f'{self.version} - {omv}')
                    print(f'{self.version} - {my_verse}')
                    print(f'{self.version} - comparator verse:')
                    print(f'{self.version} - {ocv}')
                    print(f'{self.version} - {comparator_verse}')
                    raise Exception(f'{self.version} - BibleHubComparator error')

        # print(f'preferred_verse = {preferred_verse}')
        return preferred_verse

    def compare(self, verse):
        my_verse = verse
        comparator_verse = self.rows[self.row].findall('Cell')[self.column].find('Data').text
        ref = self.rows[self.row].findall('Cell')[0].find('Data').text
        self.row += 1
        return my_verse if my_verse == comparator_verse else self.preferred(my_verse, comparator_verse, ref)
