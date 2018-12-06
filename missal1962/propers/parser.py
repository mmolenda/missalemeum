import importlib
import logging
import os
import re
from exceptions import InvalidInput, ProperNotFound
from typing import Tuple

from constants.common import (CUSTOM_DIVOFF_DIR, DIVOFF_DIR, EXCLUDE_SECTIONS,
                              COMMEMORATION_SECTIONS, LANGUAGE_LATIN,
                              REFERENCE_REGEX, SECTION_REGEX)
from propers.models import Proper, ProperSection

log = logging.getLogger(__name__)


class ProperParser:
    """
    ProperParser parses files from https://github.com/DivinumOfficium/divinum-officium in its proprietary format
    and represents them as a hierarchy of `propers.Proper` and `propers.ProperSection` objects.
    """

    lang: str = None
    translations: dict = {}
    prefaces: dict = {}

    @classmethod
    def parse(cls, proper_id: str, lang: str) -> Tuple[Proper, Proper]:
        proper_id: str = ':'.join(proper_id.split(':')[:2])
        cls.lang = lang
        cls.translations[cls.lang] = importlib.import_module(f'constants.{cls.lang}.translation')
        cls.translations[LANGUAGE_LATIN] = importlib.import_module(f'constants.{LANGUAGE_LATIN}.translation')
        cls.prefaces[cls.lang] = cls.parse_file('Ordo/Prefationes.txt', cls.lang)
        cls.prefaces[LANGUAGE_LATIN] = cls.parse_file('Ordo/Prefationes.txt', lang=LANGUAGE_LATIN)
        try:
            partial_path = f'{proper_id.split(":")[0].capitalize()}/{proper_id.split(":")[1]}.txt'
        except IndexError:
            raise InvalidInput("Proper ID should follow format `<flex>:<name>`, e.g. `tempora:Adv1-0`")
        try:
            proper_vernacular: Proper = cls.parse_file(partial_path, cls.lang)
            proper_latin: Proper = cls.parse_file(partial_path, LANGUAGE_LATIN)
        except FileNotFoundError as e:
            raise ProperNotFound(f'Proper `{e.filename}` not found.')
        return proper_vernacular, proper_latin

    @classmethod
    def parse_file(cls, partial_path: str, lang, lookup_section=None) -> Proper:
        """
        Read the file and organize the content as a list of dictionaries
        where `[Section]` becomes an `id` key and each line below - an item of a `body` list.
        Resolve references like `@Sancti/02-02:Evangelium`.
        """
        proper: Proper = Proper()
        section_name: str = None
        concat_line: bool = False
        full_path: str = cls._get_full_path(partial_path, lang)
        with open(full_path) as fh:
            for itr, ln in enumerate(fh):
                ln = ln.strip()

                if section_name is None and ln == '':
                    # Skipping empty lines in the beginning of the file
                    continue

                if ln.strip() == '!':
                    # Skipping lines containing exclamation mark only
                    continue

                if section_name is None and REFERENCE_REGEX.match(ln):
                    # reference outside any section as a first non-empty line - load all sections
                    # from the referenced file and continue with the sections from the current one.
                    path_bit, _, _ = REFERENCE_REGEX.findall(ln)[0]
                    # Recursively read referenced file
                    nested_path: str = cls._get_full_path(f'{path_bit}.txt', lang) if path_bit else partial_path
                    proper.merge(cls.parse_file(nested_path, lang=lang))
                    continue

                ln = cls._normalize(ln, lang)

                if re.search(SECTION_REGEX, ln):
                    section_name: str = re.sub(SECTION_REGEX, '\\1', ln)

                if not lookup_section or lookup_section == section_name:
                    if re.match(SECTION_REGEX, ln):
                        proper.set_section(section_name, ProperSection(section_name))
                    else:
                        if REFERENCE_REGEX.match(ln):
                            path_bit, nested_section_name, substitution = REFERENCE_REGEX.findall(ln)[0]
                            if path_bit:
                                # Reference to external file - parse it recursively
                                nested_path: str = cls._get_full_path(path_bit + '.txt', lang) \
                                    if path_bit else partial_path
                                nested_proper: Proper = cls.parse_file(
                                    nested_path, lang=lang, lookup_section=nested_section_name)
                                nested_section = nested_proper.get_section(nested_section_name)
                                if nested_section is not None:
                                    proper.get_section(section_name).extend_body(nested_section.body)
                                else:
                                    log.warning("Section `%s` referenced from `%s` is missing in `%s`",
                                                nested_section_name, full_path, nested_path)
                            else:
                                # Reference to the other section in current file
                                nested_section_body = proper.get_section(nested_section_name).body
                                proper.get_section(section_name).extend_body(nested_section_body)

                        else:
                            # Finally, a regular line...
                            # Line ending with `~` indicates that the next line should be treated as its continuation
                            appendln: str = ln.replace('~', ' ')
                            if section_name not in proper.keys():
                                proper.set_section(section_name, ProperSection(section_name))
                            if concat_line:
                                proper.get_section(section_name).body[-1] += appendln
                            else:
                                proper.get_section(section_name).append_to_body(appendln)
                            concat_line = True if ln.endswith('~') else False

        # Reference in Rule section in 'vide' or 'ex' clause - load all sections
        # from the referenced file and get sections that are not explicitly defined in the current proper.
        vide = proper.get_rule('vide')
        if vide:
            nested_path = cls._get_full_path(f'{vide}.txt', lang)
            proper.merge(cls.parse_file(nested_path, lang=lang))

        # Postprocessing obtained sections
        proper = cls._strip_contents(proper)
        proper = cls._resolve_conditionals(proper)
        if 'Ordo' not in partial_path and not lookup_section:
            proper = cls._add_prefaces(proper, lang)
            proper = cls._filter_sections(proper, lang)
            proper = cls._translate_section_titles(proper, lang)
        return proper

    @classmethod
    def _normalize(cls, ln, lang):
        for r, s in cls.translations[lang].transformations:
            ln = re.sub(r, s.get(lang, s.get(None)), ln)
        return ln

    @staticmethod
    def _strip_contents(proper):
        for section in proper.values():
            while section.body and not section.body[-1]:
                section.body.pop(-1)
        return proper

    @classmethod
    def _filter_sections(cls, proper, lang):
        ignore_commememoration = proper.get_rule('ignore_commemoration')
        for section_id in list(proper.keys()):
            if section_id in EXCLUDE_SECTIONS or (ignore_commememoration and section_id in COMMEMORATION_SECTIONS):
                proper.pop_section(section_id)
        return proper

    @classmethod
    def _translate_section_titles(cls, proper, lang):
        sections_ids = proper.keys()
        section_labels = {}
        section_labels.update(cls.translations[lang].section_labels)
        if 'GradualeL1' in sections_ids:
            section_labels.update(cls.translations[lang].section_labels_multi)

        for section in proper.values():
            section.set_label(section_labels.get(section.id, section.id))
        return proper

    @classmethod
    def _add_prefaces(cls, proper, lang):
        if 'Prefatio' in proper.keys():
            return proper
        preface_name = proper.get_rule('preface') or 'Communis'
        preface_item = cls.prefaces[lang].get_section(preface_name)
        if preface_item is None:
            preface_item = cls.prefaces[lang].get_section('Communis')
        proper.set_section('Prefatio', ProperSection('Prefatio', body=preface_item.body))
        return proper

    @staticmethod
    def _resolve_conditionals(proper):
        for section_name, section in proper.items():
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
                if '(deinde dicuntur)' in ln or '(sed communi Summorum Pontificum dicitur)' in ln:
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
            proper.get_section(section_name).body = new_content
        return proper

    @staticmethod
    def _get_full_path(partial_path, lang):
        full_path = os.path.join(CUSTOM_DIVOFF_DIR, 'web', 'www', 'missa', lang, partial_path)
        if not os.path.exists(full_path):
            full_path = os.path.join(DIVOFF_DIR, 'web', 'www', 'missa', lang, partial_path)
        return full_path
