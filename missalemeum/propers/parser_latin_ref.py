import re
from typing import Union

from exceptions import ProperNotFound
from propers.models import Proper, ParsedSource, Section
from propers.parser import ProperParser, log
from constants.common import LANGUAGE_LATIN, REFERENCE_REGEX, SECTION_REGEX, IGNORED_REFERENCES, RULE


class ProperParserLatinRef(ProperParser):

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
            proper.title = self.translations[lang].TITLES[self.proper_id]
        except KeyError:
            # Handling very rare case when proper's source exists but rank or color in the ID is invalid
            raise ProperNotFound(f"Proper {self.proper_id} not found")
        proper.description = parsed_comment['description']
        proper.tags = parsed_comment['tags']
        proper.tags.extend(self.translations[lang].PAGES.get(self.proper_id, []))
        proper.supplements = self.translations[lang].SUPPLEMENTS.get(self.proper_id, [])
        proper = self._add_preface(proper, lang)
        proper = self._filter_sections(proper)
        proper = self._amend_sections_contents(proper)
        proper = self._translate_section_titles(proper, lang)

        return proper

    def _parse_source(self, partial_path: str, lang, lookup_section=None) -> ParsedSource:
        """
        Read the file and organize the content as a list of dictionaries
        where `[Section]` becomes an `id` key and each line below - an item of a `body` list.
        Resolve references like `@Sancti/02-02:Evangelium`.
        """
        parsed_source: ParsedSource = ParsedSource()
        section_name: Union[str, None] = None
        concat_line: bool = False
        full_path: str = self._get_full_path(partial_path, lang)
        if not full_path:
            raise ProperNotFound(f'Proper `{partial_path}` not found.')
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
                    if RULE not in parsed_source.keys():
                        parsed_source.set_section(RULE, Section(RULE))
                    parsed_source.get_section(RULE).append_to_body(f"vide {ln.lstrip('@')}")
                    continue

                ln = self._normalize(ln, lang)

                if re.search(SECTION_REGEX, ln):
                    section_name: str = re.sub(SECTION_REGEX, '\\1', ln)

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

        # Rules need to be parsed after the whole source is read
        parsed_source.rules = parsed_source.parse_rules()

        # Reference in Rule section in 'vide' or 'ex' clause - load all sections
        # from the referenced file and get sections that are not explicitly defined in the current proper.
        if vide := parsed_source.rules.vide:
            if '/' in vide:
                nested_path = self._get_full_path(f'{vide}.txt', lang)
            else:
                for subdir in ('Commune', 'Tempora'):
                    nested_path = self._get_full_path(f'{subdir}/{vide}.txt', lang)
                    if nested_path:
                        break
            if not nested_path:
                raise ProperNotFound(f'Proper from vide not found {vide}.')
            parsed_source.merge(self._parse_source(nested_path, lang=lang))

        for section_name, section in parsed_source.items():
            section_body = section.get_body()
            for i, section_body_ln in enumerate(section_body):
                if REFERENCE_REGEX.match(section_body_ln):
                    try:
                        path_bit, nested_section_name, substitution = REFERENCE_REGEX.findall(ln)[0]
                    except IndexError:
                        raise
                    if path_bit:
                        # Reference to external file - parse it recursively
                        nested_path: str = self._get_full_path(f'{path_bit}.txt', lang) \
                            if path_bit else partial_path
                        if not nested_path:
                            raise ProperNotFound(f'Proper `{path_bit}.txt` not found.')
                        nested_proper: ParsedSource = self._parse_source(
                            nested_path, lang=lang, lookup_section=nested_section_name)
                        nested_section = nested_proper.get_section(nested_section_name)
                        if nested_section is not None:
                            new_section_body = section_body[:i] + nested_section.body + section_body[i + 1:]
                            new_section = Section(id_=section.id, label=section.label, body=new_section_body)
                            parsed_source.set_section(section_name, new_section)
                        elif nested_section_name in IGNORED_REFERENCES:
                            pass
                        else:
                            log.warning("Section `%s` referenced from `%s` is missing in `%s`",
                                        nested_section_name, full_path, nested_path)
                    else:
                        # Reference to the other section in current file
                        nested_section_body = parsed_source.get_section(nested_section_name).body
                        parsed_source.get_section(section_name).extend_body(nested_section_body)

        parsed_source = self._strip_newlines(parsed_source)
        parsed_source = self._resolve_conditionals(parsed_source)
        return parsed_source
