import os
import re
import xml.etree.ElementTree
from py.loaders import load_checks, load_psalms_check


class BibleHubComparator:

    def __init__(self, version):

        self.psalms = load_psalms_check(version)
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
                    print(f'{self.version} - {omv}')
                    print(f'{self.version} - {my_verse}')
                    print(f'{self.version} - comparator verse:')
                    print(f'{self.version} - {ocv}')
                    print(f'{self.version} - {comparator_verse}')
                    raise Exception(f'{self.version} - BibleHubComparator error')

        # print(f'preferred_verse = {preferred_verse}')
        return preferred_verse

    def compare_psalm(self, my_verse, comparator_verse, ref, psalm):

        omv = my_verse
        ocv = comparator_verse
        verse_zero = psalm[0].lower()
        verse_one = psalm[1].lower()

        for prefer in self.prefer:
            # print(my_verse.startswith(prefer[0]))
            # print(comparator_verse.startswith(prefer[1]))

            allow = True
            if len(prefer) > 3:
                allow = ref == prefer[3]

            if allow:
                my_verse = my_verse.replace(prefer[0], prefer[2])
                comparator_verse = comparator_verse.replace(prefer[1], prefer[2])

        my_verse = my_verse.lower()
        comparator_verse = comparator_verse.lower()

        if verse_one in my_verse and verse_one in comparator_verse and (verse_zero in my_verse or verse_zero in comparator_verse):
            # TODO - Return both verses
            return verse_one
        else:
            print('\n')
            print(f'{self.version} - {ref}')
            print(f'{self.version} - my verse:')
            print(f'{self.version} - {omv}')
            print(f'{self.version} - comparator verse:')
            print(f'{self.version} - {ocv}')
            print(f'{self.version} - verse zero:')
            print(f'{self.version} - {psalm[0]}')
            print(f'{self.version} - verse one:')
            print(f'{self.version} - {psalm[1]}')
            raise Exception(f'{self.version} - BibleHubComparator psalm error')

    def compare(self, verse):
        my_verse = verse
        comparator_verse = self.rows[self.row].findall('Cell')[self.column].find('Data').text
        ref = self.rows[self.row].findall('Cell')[0].find('Data').text
        self.row += 1

        chapter = re.findall('(\d+):', ref)[0]
        psalm = self.psalms.get(chapter)

        if ref.startswith('Ps') and ref.endswith(':1') and psalm is not None:
            return self.compare_psalm(my_verse, comparator_verse, ref, psalm)
        elif my_verse == comparator_verse:
            return my_verse
        else:
            return self.preferred(my_verse, comparator_verse, ref)
