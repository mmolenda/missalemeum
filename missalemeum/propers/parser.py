import logging
import os
import re
from typing import Tuple, Union

import utils as utils
from exceptions import InvalidInput, ProperNotFound

from constants import TRANSLATION
from constants import common as cc
from constants.common import (DIVOFF_DIR, LANGUAGE_LATIN, DIVOFF_LANG_MAP,
                              REFERENCE_REGEX,
                              SECTION_REGEX, EXCLUDE_SECTIONS_IDX, ASTERISK, PATTERN_COMMEMORATION,
                              PREFATIO_COMMUNIS,
                              VISIBLE_SECTIONS, TRACTUS, GRADUALE, GRADUALE_PASCHAL, PATTERN_ALLELUIA,
                              PREFATIO_OMIT,
                              OBSERVANCES_WITHOUT_OWN_PROPER, PATTERN_TRACT, IGNORED_REFERENCES, PREFATIO,
                              PATTERN_PREFATIO_SUBSTITUTION, RULE, TOP_LEVEL_REF)
from propers.models import Proper, Section, ProperConfig, ParsedSource

log = logging.getLogger(__name__)


class ProperParser:
    """
    ProperParser parses files from https://github.com/DivinumOfficium/divinum-officium in its proprietary format
    and represents them as a hierarchy of `propers.models.Proper` and `propers.model.Section` objects.
    """

    def __init__(self, proper_id: str, lang: str, config: ProperConfig = None):
        self.proper_id: str = proper_id
        self.lang = lang
        self.config = config or ProperConfig()
        self.translations: dict = {}
        self.prefaces: dict = {}
        self.translations[self.lang] = TRANSLATION[self.lang]
        self.translations[LANGUAGE_LATIN] = TRANSLATION[LANGUAGE_LATIN]

    def proper_exists(self) -> bool:
        return not utils.match_first(self.proper_id, OBSERVANCES_WITHOUT_OWN_PROPER) \
               and ((self._get_full_path(self._get_partial_path(), self.lang) is not None) or
                    (self._get_full_path(self._get_partial_path(), LANGUAGE_LATIN) is not None))

    def parse(self) -> Tuple[Proper, Proper]:
        self.prefaces[self.lang] = self._parse_source('Ordo/Prefationes.txt', self.lang)
        self.prefaces[LANGUAGE_LATIN] = self._parse_source('Ordo/Prefationes.txt', lang=LANGUAGE_LATIN)
        partial_path = self._get_partial_path()
        try:
            proper_vernacular: Proper = self._parse_proper_source(partial_path, self.lang)
            proper_latin: Proper = self._parse_proper_source(partial_path, LANGUAGE_LATIN)
        except FileNotFoundError as e:
            raise ProperNotFound(f'Proper `{e.filename}` not found.')
        return proper_vernacular, proper_latin

    def _parse_proper_source(self, partial_path: str, lang, lookup_section=None) -> Proper:
        """
        Read the file and organize the content as a list of dictionaries
        where `[Section]` becomes an `id` key and each line below - an item of a `body` list.
        Resolve references like `@Sancti/02-02:Evangelium`.
        """
        parsed_source: ParsedSource = self._parse_source(partial_path, lang, lookup_section)
        proper = Proper(self.proper_id, lang, parsed_source)

        # Moving data from "Comment" section up as direct properties of a Proper object
        parsed_comment: dict = self._parse_comment(proper.pop_section('Comment'))
        try:
            proper.title = self.translations[lang].TITLES[self.config.title_id or self.proper_id]
        except KeyError:
            # Handling very rare case when proper's source exists but rank or color in the ID is invalid
            raise ProperNotFound(f"Proper {self.config.title_id or self.proper_id} not found")
        proper.description = parsed_comment['description']
        proper.tags = parsed_comment['tags']
        proper.tags.extend(self.translations[lang].PAGES.get(self.proper_id, []))
        proper.supplements = self.translations[lang].SUPPLEMENTS.get(self.proper_id, [])
        proper = self._add_preface(proper, lang)
        proper = self._filter_sections(proper)
        proper = self._amend_sections_contents(proper)
        proper = self._translate_section_titles(proper, lang)
        return proper

    def _parse_source(self, partial_path: str, lang, coming_from: str = None, lookup_section=None) -> ParsedSource:
        """
        Read the file and organize the content as a list of dictionaries
        where `[Section]` becomes an `id` key and each line below - an item of a `body` list.
        """
        log.debug("Parsing source %s%s/%s %s",
                  f"{lang}/{coming_from} -> " if coming_from else "",
                  lang,
                  partial_path,
                  f"lookup={lookup_section}" if lookup_section else ""
                  )

        if lang == LANGUAGE_LATIN:
            parsed_source = self._read_source(partial_path, LANGUAGE_LATIN, lookup_section)
        else:
            try:
                parsed_source = self._read_source(partial_path, lang, lookup_section)
                parsed_source_latin = self._read_source(partial_path, LANGUAGE_LATIN, lookup_section)
                parsed_source.merge(parsed_source_latin)
            except ProperNotFound:
                parsed_source = self._read_source(partial_path, LANGUAGE_LATIN, lookup_section)

        parsed_source = self._resolve_conditionals(parsed_source)
        parsed_source.rules = parsed_source.parse_rules()
        # Reference in Rule section in 'vide' or 'ex' clause - load all sections
        # from the referenced file and get sections that are not explicitly defined in the current proper.
        if vide := parsed_source.rules.vide:
            # Avoiding infinite loops when:
            # 1. There's self reference, for example Commune/C10.txt has 'vide C10'
            # 2. Source proper points to target proper which again points to the source proper,
            #    for example: C7a points to Graduale in C7ap and C7ap has vide C7a
            vide_partial_path = f'{vide}.txt'
            if not vide_partial_path in partial_path and not vide_partial_path in (coming_from or ''):
                for nested_path in (vide_partial_path, f'Commune/{vide_partial_path}', f'Tempora/{vide_partial_path}'):
                    nested_path_full = self._get_full_path(nested_path, lang)
                    if nested_path_full:
                        break
                else:
                    raise ProperNotFound(f'Proper from vide not found: ({lang}) {coming_from} -> {vide}.')
                parsed_source.merge(self._parse_source(nested_path, lang=lang, coming_from=partial_path))

        parsed_source = self._resolve_references(parsed_source, partial_path, lang, coming_from)
        parsed_source = self._strip_newlines(parsed_source)
        return parsed_source

    def _read_source(self, partial_path: str, lang: str, lookup_section: Union[str, None] = None) -> ParsedSource:
        parsed_source: ParsedSource = ParsedSource()
        section_name: Union[str, None] = None
        concat_line: bool = False
        full_path: str = self._get_full_path(partial_path, lang)
        if not full_path:
            raise ProperNotFound(f'Proper `{lang}/{partial_path}` not found.')
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
                    top_level_ref_section = Section(TOP_LEVEL_REF, [f"vide {ln.lstrip('@')}"])
                    parsed_source.set_section(TOP_LEVEL_REF, top_level_ref_section)
                    continue

                ln = self._normalize(ln, lang)

                if re.search(SECTION_REGEX, ln):
                    section_name: str = self._parse_section_name(ln)

                if not lookup_section or lookup_section == section_name:
                    if re.match(SECTION_REGEX, ln):
                        parsed_source.set_section(section_name, Section(section_name))
                    else:
                        # Finally, a regular line...
                        # Line ending with `~` indicates that the next line should be treated as its continuation
                        appendln: str = ln.replace('~', ' ')
                        if section_name not in parsed_source.keys():
                            parsed_source.set_section(section_name, Section(section_name))
                        if concat_line:
                            parsed_source.get_section(section_name).body[-1] += appendln
                        else:
                            parsed_source.get_section(section_name).append_to_body(appendln)
                        concat_line = True if ln.endswith('~') else False
        return parsed_source

    def _resolve_references(self, parsed_source: ParsedSource, partial_path: str, lang, coming_from: str = None) -> ParsedSource:
        for section_name, section in parsed_source.items():
            section_body = section.get_body()
            for i, section_body_ln in enumerate(section_body):
                if REFERENCE_REGEX.match(section_body_ln):
                    path_bit, nested_section_name, substitutions = REFERENCE_REGEX.findall(section_body_ln)[0]
                    if not nested_section_name:
                        nested_section_name = section_name
                    if path_bit:
                        # Reference to external file - parse it recursively
                        nested_path: str = f"{path_bit}.txt"
                        nested_proper: ParsedSource = self._parse_source(
                            nested_path, lang=lang, coming_from=partial_path, lookup_section=nested_section_name)
                        nested_section = nested_proper.get_section(nested_section_name)
                        if nested_section is not None:
                            nested_section_body = nested_section.body
                            if substitutions:
                                for substitution in re.split(r"\bs/", substitutions):
                                    if not substitution:
                                        continue
                                    try:
                                        sub_from, sub_to, _ = substitution.split("/")
                                        for i, line in enumerate(nested_section_body):
                                            nested_section_body[i] = re.sub(sub_from, sub_to, line)
                                    except Exception as e:
                                        log.warning("Can't make substitution for pattern `%s` in `%s:%s`. "
                                                    "Referenced from `%s`. %s",
                                                    substitutions, nested_path, nested_section_name, coming_from, e)
                            section.substitute_reference(section_body_ln, nested_section_body)
                        elif nested_section_name in IGNORED_REFERENCES:
                            section.substitute_reference(section_body_ln, [""])
                        else:
                            log.warning("Section `%s` referenced from `%s/%s` is missing in `%s`",
                                        nested_section_name, lang, partial_path, nested_path)
                    else:
                        # Reference to the other section in current file
                        nested_section_body = parsed_source.get_section(nested_section_name).body
                        section.substitute_reference(section_body_ln, nested_section_body)
        return parsed_source

    @staticmethod
    def _parse_comment(comment: Union[None, Section]) -> dict:
        parsed_comment = {
            "title": None,
            "description": "",
            "rank": None,
            "tags": []
        }
        if comment is None:
            return parsed_comment
        for ln in comment.get_body():
            if ln.startswith('#'):
                parsed_comment['title'] = re.split("[–—-]", ln.strip("#"), 1)[-1].strip()
            elif ln.strip().startswith('*') and ln.endswith('*'):
                info_item = ln.replace('*', '')
                try:
                    parsed_comment['rank'] = int(info_item.split(' ')[0])
                except ValueError:
                    if PATTERN_COMMEMORATION in info_item.lower():
                        parsed_comment['rank'] = 4
                    else:
                        parsed_comment['tags'].append(info_item)
            else:
                parsed_comment['description'] += ln + '\n'
        return parsed_comment

    def _normalize(self, ln, lang):
        for from_, to_ in self.translations[lang].TRANSFORMATIONS:
            ln = re.sub(from_, to_, ln)
        return ln.strip()

    @staticmethod
    def _parse_section_name(ln: str) -> str:
        """
        In most cases section name looks like `[Rank]`, but sometimes in one proper there can
        be several sections with the same name, but related to different issues of the missal, e.g.
        `[Rank] (rubrica 1960)`
        `[Ultima Evangelium](sed non rubrica 1960)`
        Sections proper to 1962 issue are parsed as normal ones, e.g. `[Rank] (rubrica 1960)` -> `[Rank]`.
        Sections from other issues or ones explicitly excluded from 1962 are parsed like
          `[Rank] (rubrica 1570)` -> `[Rank (rubrica 1570)]` so they will be excluded later.
        """
        #
        #
        #
        name, modifier = re.findall(SECTION_REGEX, ln)[0]
        name = name.strip()
        if "sed non rubrica 196" in modifier:
            return f"{name} {modifier}"
        if not modifier or "(" not in modifier or "rubrica 196" in modifier:
            return name
        return f"{name} {modifier}"

    @staticmethod
    def _strip_newlines(proper):
        for section in proper.values():
            while section.body and not section.body[-1]:
                section.body.pop(-1)
        return proper

    def _filter_sections(self, proper):

        def not_visible(section_id):
            return section_id not in VISIBLE_SECTIONS

        def is_excluded(proper_id, section_id):
            return bool({proper_id, ASTERISK}.intersection(EXCLUDE_SECTIONS_IDX.get(section_id, set())))

        def get_excluded_inter_readings_sections(config, proper):
            if config.inter_readings_section == GRADUALE and proper.get_section(GRADUALE) is not None:
                return [GRADUALE_PASCHAL, TRACTUS]
            elif config.inter_readings_section == GRADUALE_PASCHAL:
                if proper.get_section(GRADUALE_PASCHAL) is not None:
                    return [GRADUALE, TRACTUS]
                else:
                    return [TRACTUS]
            elif config.inter_readings_section == TRACTUS:
                if proper.get_section(TRACTUS) is not None:
                    return [GRADUALE, GRADUALE_PASCHAL]
                else:
                    return [GRADUALE_PASCHAL]
            return []

        sections_to_remove = set()
        for section_id in list(proper.keys()):
            if not_visible(section_id) or is_excluded(proper.id, section_id):
                sections_to_remove.add(section_id)
        sections_to_remove.update(get_excluded_inter_readings_sections(self.config, proper))

        for section_id in sections_to_remove:
            proper.pop_section(section_id)

        return proper

    def _amend_sections_contents(self, proper):
        gradual = proper.get_section(GRADUALE)
        if gradual is not None:
            if self.config.strip_alleluia is True:
                for i, line in enumerate(gradual.body):
                    gradual.body[i] = re.sub(PATTERN_ALLELUIA, "", line)
            if self.config.strip_tract is True:
                new_body = []
                for line in gradual.body:
                    if re.search(PATTERN_TRACT, line):
                        break
                    new_body.append(line)
                gradual.body = new_body
        return proper

    def _translate_section_titles(self, proper, lang):
        proper.commemorations_names_translations = self.translations[lang].COMMEMORATIONS
        sections_ids = proper.keys()
        section_labels = {}
        section_labels.update(self.translations[lang].SECTION_LABELS)
        if 'GradualeL1' in sections_ids:
            section_labels.update(self.translations[lang].SECTION_LABELS_MULTI)

        for section in proper.values():
            section.set_label(section_labels.get(section.id, section.id))
        return proper

    def _add_preface(self, proper, lang):
        preface_name = self.config.preface or proper.rules.preface
        if preface_name == PREFATIO_OMIT or (preface_name is None and PREFATIO in proper.keys()):
            return proper
        preface_item: Section = self.prefaces[lang].get_section(preface_name)
        if preface_item is None:
            preface_item = self.prefaces[lang].get_section(PREFATIO_COMMUNIS)

        if preface_mod := proper.rules.preface_mod:
            repl = preface_mod
        else:
            repl = '\\1'
        preface_item.substitute_in_preface(PATTERN_PREFATIO_SUBSTITUTION, repl)
        proper.set_section(PREFATIO, Section(PREFATIO, body=preface_item.body))
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
                if '(deinde dicuntur)' in ln:
                    # start skipping lines from now on
                    omit = True
                    continue
                if '(sed rubrica 1955 aut rubrica 1960' in ln and 'versus omittuntur)' in ln:
                    # stop skipping lines from now on
                    omit = False
                    continue
                if 'communi summorum pontificum' in ln.lower() or '(sed rubrica 195 aut rubrica 196)' in ln.lower():
                    # From this line on we want only what follows this line, and possibly the header
                    first_line = new_content[0] if new_content and new_content[0].startswith("*") else None
                    if first_line:
                        new_content = [first_line]
                    else:
                        new_content = []
                    continue
                if omit:
                    continue
                if '(dicitur)' in ln:
                    continue
                new_content.append(ln)
            proper.get_section(section_name).body = new_content
        return proper

    @staticmethod
    def _get_full_path(partial_path, lang):
        full_path = os.path.join(cc.CUSTOM_DIVOFF_DIR, 'web', 'www', 'missa', DIVOFF_LANG_MAP[lang], partial_path)
        if os.path.exists(full_path):
            log.debug("%s/%s comes from custom DivinumOfficium dir", lang, partial_path)
        else:
            full_path = os.path.join(DIVOFF_DIR, 'web', 'www', 'missa', DIVOFF_LANG_MAP[lang], partial_path)
            if not os.path.exists(full_path):
                return None
        return full_path

    def _get_partial_path(self):
        try:
            return f'{self.proper_id.split(":")[0].capitalize()}/{self.proper_id.split(":")[1]}.txt'
        except IndexError:
            raise InvalidInput("Proper ID should follow format `<flex>:<name>`, e.g. `tempora:Adv1-0`")
