# -*- coding: utf-8 -*-

"""
TODO:
* eundem/eundem w plikach zrodlowych
"""
import contextlib
import importlib
import re
import os
from collections import OrderedDict
import logging
import sys

from constants import REFERENCE_REGEX, SECTION_REGEX, THIS_DIR
from exceptions import InvalidInput

log = logging.getLogger()


class DivoffFormatter(object):

    locale = None
    translation = None
    prefationes_a = None
    prefationes_b = None
    footnotes = []

    @classmethod
    def run(cls, proper_id: str, locale: str):
        collect = []
        log.info("Starting the process")
        log.debug("Reading Ordo/Prefationes.txt")
        cls.locale = locale
        cls.translation = importlib.import_module(f'missal1962.resources.{cls.locale}.translation')
        cls.prefaces_vernacular = cls.parse_file('Ordo/Prefationes.txt', cls.translation.divoff_lang)
        cls.prefaces_latin = cls.parse_file('Ordo/Prefationes.txt', lang=cls.translation.divoff_lang_latin)
        try:
            partial_path = f'{proper_id.split(":")[0].capitalize()}/{proper_id.split(":")[1]}.txt'
        except IndexError:
            raise InvalidInput("Proper ID should follow format `<flex>:<name>`, e.g. `tempora:Adv1-0`")
        log.debug("Parsing file `%s`", partial_path)
        contents_vernacular = cls.parse_file(partial_path, cls.translation.divoff_lang)
        contents_latin = cls.parse_file(partial_path, cls.translation.divoff_lang_latin)
        return contents_vernacular, contents_latin

    @classmethod
    def parse_file(cls, partial_path, lang, lookup_section=None):
        """
        Read the file and organize the content as ordered dictionary
        where `[Section]` becomes a key and each line below - an item of related
        list. Resolve references like `@Sancti/02-02:Evangelium`.
        """
        d = OrderedDict()
        section = None
        concat_line = False
        full_path = cls._get_full_path(partial_path, lang)
        with open(full_path) as fh:
            for itr, ln in enumerate(fh):
                ln = ln.strip()

                if section is None and ln == '':
                    # Skipping empty lines in the beginning of the file
                    continue

                if section is None and REFERENCE_REGEX.match(ln):
                    # reference outside any section as a first non-empty line - load all sections
                    # from the referenced file and continue with the sections from the current one.
                    path_bit, _, _ = REFERENCE_REGEX.findall(ln)[0]
                    # Recursively read referenced file
                    nested_path = cls._get_full_path(path_bit + '.txt', lang) if path_bit else partial_path
                    d = cls.parse_file(nested_path, lang=lang)
                    continue

                ln = cls._normalize(ln, lang)

                if re.search(SECTION_REGEX, ln):
                    section = re.sub(SECTION_REGEX, '\\1', ln)

                if not lookup_section or lookup_section == section:
                    if re.match(SECTION_REGEX, ln):
                        d[section] = []
                    else:
                        if REFERENCE_REGEX.match(ln):
                            path_bit, nested_section, substitution = REFERENCE_REGEX.findall(ln)[0]
                            if path_bit:
                                # Reference to external file - parse it recursively
                                nested_path = cls._get_full_path(path_bit + '.txt', lang) if path_bit else partial_path
                                nested_content = cls.parse_file(nested_path, lang=lang, lookup_section=nested_section)
                                try:
                                    d[section].extend(nested_content[nested_section])
                                except KeyError:
                                    log.warning("Section `%s` referenced from `%s` is missing in `%s`",
                                                nested_section, full_path, nested_path)
                            else:
                                # Reference to the other section in current file
                                d[section].extend(d[nested_section])
                        else:
                            # Finally, a regular line...
                            # Line ending with `~` indicates that next line
                            # should be treated as its continuation
                            appendln = ln.replace('~', ' ')
                            if concat_line:
                                d[section][-1] += appendln
                            else:
                                d[section].append(appendln)
                            concat_line = True if ln.endswith('~') else False
        d = cls._strip_contents(d)
        d = cls._resolve_conditionals(d)
        return d

    @classmethod
    def _normalize(cls, ln, lang):
        for r, s in cls.translation.transformations:
            ln = re.sub(r, s.get(lang, s.get(None)), ln)
        return ln

    @staticmethod
    def _strip_contents(d):
        for section, content in d.items():
            while content and not content[-1]:
                content.pop(-1)
        return d

    @staticmethod
    def _get_full_path(partial_path, lang):
        if os.path.exists(partial_path):
            return partial_path
        full_path = os.path.join(THIS_DIR, 'resources', 'divinum-officium-custom', 'web', 'www', 'missa', lang, partial_path)
        if not os.path.exists(full_path):
            full_path = os.path.join(THIS_DIR, 'resources', 'divinum-officium', 'web', 'www', 'missa', lang, partial_path)
        return full_path

    @staticmethod
    def _resolve_conditionals(d):
        for section, content in d.items():
            new_content = []
            omit = False
            itercontent = iter(content)
            for i, ln in enumerate(itercontent):
                if '(sed rubrica 1960 dicuntur)' in ln:
                    # delete previous line; do not append current one
                    del new_content[i - 1]
                    continue
                if '(rubrica 1570 aut rubrica 1910 aut rubrica divino afflatu dicitur)' in ln:
                    # skip next line; do not append current one
                    next(itercontent)
                    continue
                if '(deinde dicuntur)' in ln:
                    # start skipping lines from now on
                    omit = True
                    continue
                if '(sed rubrica 1955 aut rubrica 1960 haec versus omittuntur)' in ln:
                    # stop skipping lines from now on
                    omit = False
                    continue
                if omit:
                    continue
                new_content.append(ln)
            d[section] = new_content
        return d
