import sys

from bs4 import BeautifulSoup


def fix_xml(in_path, out_path):
    """Programmatic entry point to fix_xml.

    :param in_path: path to input xml file
    :param out_path: path to output fixed xml file
    """
    with open(in_path, 'r', encoding='utf-8') as infile:
        soup: BeautifulSoup = Fixer(infile, 'xml')
    with open(out_path, 'w', encoding='utf-8') as outfile:
        outfile.write(str(soup))


class Fixer(BeautifulSoup):
    NESTABLE_TAGS: dict = {
        'suite': ['robot', 'suite', 'statistics'],
        'doc': ['suite', 'test', 'kw'],
        'metadata': ['suite'],
        'item': ['metadata'],
        'status': ['suite', 'test', 'kw'],
        'test': ['suite'],
        'tags': ['test'],
        'tag': ['tags'],
        'kw': ['suite', 'test', 'kw'],
        'msg': ['kw', 'errors'],
        'arguments': ['kw'],
        'arg': ['arguments'],
        'statistics': ['robot'],
        'errors': ['robot']
    }

    __close_on_open = None

    def handle_starttag(self, name, namespace, nsprefix, attrs, sourceline=None, sourcepos=None, namespaces=None):
        if name == 'robot':
            attrs = [(key, value) if key != 'generator' else ('generator', 'robotfix_xml.py') for key, value in
                     attrs.items()]
        if name == 'kw' and ('type', 'teardown') in attrs:
            while self.tagStack[-1].name not in ['test', 'suite']:
                self.handle_endtag(self.tagStack[-1].name)
        if self.__close_on_open:
            self.handle_endtag(self.__close_on_open)
            self.__close_on_open = None
        super().handle_starttag(name, namespace, nsprefix, attrs, sourceline=sourceline, sourcepos=sourcepos,
                                namespaces=namespaces)

    def handle_endtag(self, name, nsprefix=None):
        super().handle_endtag(name, nsprefix=nsprefix)
        if name == 'status':
            self.__close_on_open = self.tagStack[-1].name
        else:
            self.__close_on_open = None


if __name__ == '__main__':
    try:
        fix_xml(*sys.argv[1:])
    except TypeError:
        print(__doc__)
    else:
        print(sys.argv[2])
