import logging
import os
import re

import importlib
from typing import Tuple

from constants import LANGUAGE_LATIN, REFERENCE_REGEX, SECTION_REGEX, EXCLUDE_SECTIONS, EXCLUDE_SECTIONS_TITLES, \
    THIS_DIR
from exceptions import InvalidInput
from models import ProperSectionContainer, ProperSection


log = logging.getLogger(__name__)


class ProperParser:
    """
    ProperParser parses files from https://github.com/DivinumOfficium/divinum-officium in its proprietary format
    and represents them as a hierarchy of `models.ProperSectionContainer` and `models.ProperSection` objects.
    """

    lang = None
    translations = {}
    prefaces = {}

    @classmethod
    def run(cls, proper_id: str, lang: str) -> Tuple[ProperSectionContainer, ProperSectionContainer]:
        log.info("Starting the process")
        log.debug("Reading Ordo/Prefationes.txt")
        cls.lang = lang
        cls.translations[cls.lang] = importlib.import_module(f'missal1962.resources.{cls.lang}.translation')
        cls.translations[LANGUAGE_LATIN] = importlib.import_module(f'missal1962.resources.{LANGUAGE_LATIN}.translation')
        cls.prefaces[cls.lang] = cls.parse_file('Ordo/Prefationes.txt', cls.lang)
        cls.prefaces[LANGUAGE_LATIN] = cls.parse_file('Ordo/Prefationes.txt', lang=LANGUAGE_LATIN)
        try:
            partial_path = f'{proper_id.split(":")[0].capitalize()}/{proper_id.split(":")[1]}.txt'
        except IndexError:
            raise InvalidInput("Proper ID should follow format `<flex>:<name>`, e.g. `tempora:Adv1-0`")
        log.debug("Parsing file `%s`", partial_path)
        container_vernacular: ProperSectionContainer = cls.parse_file(partial_path, cls.lang)
        container_latin: ProperSectionContainer = cls.parse_file(partial_path, LANGUAGE_LATIN)
        return container_vernacular, container_latin

    @classmethod
    def parse_file(cls, partial_path, lang, lookup_section=None):
        """
        Read the file and organize the content as a list of dictionaries
        where `[Section]` becomes an `id` key and each line below - an item of a `body` list.
        Resolve references like `@Sancti/02-02:Evangelium`.
        """
        section_container = ProperSectionContainer()
        section_name = None
        concat_line = False
        full_path = cls._get_full_path(partial_path, lang)
        with open(full_path) as fh:
            for itr, ln in enumerate(fh):
                ln = ln.strip()

                if section_name is None and ln == '':
                    # Skipping empty lines in the beginning of the file
                    continue

                if section_name is None and REFERENCE_REGEX.match(ln):
                    # reference outside any section as a first non-empty line - load all sections
                    # from the referenced file and continue with the sections from the current one.
                    path_bit, _, _ = REFERENCE_REGEX.findall(ln)[0]
                    # Recursively read referenced file
                    nested_path = cls._get_full_path(path_bit + '.txt', lang) if path_bit else partial_path
                    section_container = cls.parse_file(nested_path, lang=lang)
                    continue

                ln = cls._normalize(ln, lang)

                if re.search(SECTION_REGEX, ln):
                    section_name = re.sub(SECTION_REGEX, '\\1', ln)

                if not lookup_section or lookup_section == section_name:
                    if re.match(SECTION_REGEX, ln):
                        section_container.append(ProperSection(section_name))
                    else:
                        if REFERENCE_REGEX.match(ln):
                            path_bit, nested_section_name, substitution = REFERENCE_REGEX.findall(ln)[0]
                            if path_bit:
                                # Reference to external file - parse it recursively
                                nested_path = cls._get_full_path(path_bit + '.txt', lang) if path_bit else partial_path
                                nested_content = cls.parse_file(nested_path, lang=lang, lookup_section=nested_section_name)
                                try:
                                    section_container[-1].extend_body(nested_content[0].body)
                                except KeyError:
                                    log.warning("Section `%s` referenced from `%s` is missing in `%s`",
                                                nested_section_name, full_path, nested_path)
                            else:
                                # Reference to the other section in current file
                                nested_section_body = section_container.get_section(nested_section_name).body
                                section_container[-1].extend_body(nested_section_body)

                        else:
                            # Finally, a regular line...
                            # Line ending with `~` indicates that next line
                            # should be treated as its continuation
                            appendln = ln.replace('~', ' ')
                            if concat_line:
                                section_container[-1].body[-1] += appendln
                            else:
                                section_container[-1].append_to_body(appendln)
                            concat_line = True if ln.endswith('~') else False
        section_container = cls._strip_contents(section_container)
        section_container = cls._resolve_conditionals(section_container)
        if 'Ordo' not in partial_path and not lookup_section:
            section_container = cls._add_prefaces(section_container, lang)
            section_container = cls._translate_section_titles(section_container, lang)
        return section_container

    @classmethod
    def _normalize(cls, ln, lang):
        for r, s in cls.translations[lang].transformations:
            ln = re.sub(r, s.get(lang, s.get(None)), ln)
        return ln

    @staticmethod
    def _strip_contents(sections):
        for section in sections:
            while section.body and not section.body[-1]:
                section.body.pop(-1)
        return sections

    @classmethod
    def _translate_section_titles(cls, sections, lang):
        sections_ids = [i.id for i in sections]
        section_labels = {}
        section_labels.update(cls.translations[lang].section_labels)
        if 'GradualeL1' in sections_ids:
            section_labels.update(cls.translations[lang].section_labels_multi)

        for section in sections:
            if section.id in EXCLUDE_SECTIONS + EXCLUDE_SECTIONS_TITLES:
                continue
            section.set_label(section_labels[section.id])
        return sections

    @classmethod
    def _add_prefaces(cls, sections, lang):
        preface_id = 'Trinitate'
        for section in sections:
            if section.id == 'Rule':
                rule_preface = [i for i in section.body if i.startswith('Prefatio=')]
                if rule_preface:
                    preface_id = rule_preface[0].split('=')[1]
                    break
        sections_ids = [i.id for i in sections]
        communion_index = sections_ids.index('Communio')
        preface_item = [i for i in cls.prefaces[lang] if i.id == preface_id][0]
        sections.insert(communion_index, ProperSection('Prefatio', body=preface_item.body))
        return sections

    @staticmethod
    def _resolve_conditionals(sections):
        for itr, section in enumerate(sections):
            new_content = []
            omit = False
            iter_body = iter(section.body)
            for i, ln in enumerate(iter_body):
                if '(sed rubrica 1960 dicuntur)' in ln:
                    # delete previous line; do not append current one
                    del new_content[i - 1]
                    continue
                if '(rubrica 1570 aut rubrica 1910 aut rubrica divino afflatu dicitur)' in ln:
                    # skip next line; do not append current one
                    next(iter_body)
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
            sections[itr].body = new_content
        return sections

    @staticmethod
    def _get_full_path(partial_path, lang):
        if os.path.exists(partial_path):
            return partial_path
        full_path = os.path.join(THIS_DIR, 'resources', 'divinum-officium-custom', 'web', 'www', 'missa', lang, partial_path)
        if not os.path.exists(full_path):
            full_path = os.path.join(THIS_DIR, 'resources', 'divinum-officium', 'web', 'www', 'missa', lang, partial_path)
        return full_path