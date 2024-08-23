import re
from typing import Union

from exceptions import ProperNotFound
from propers.models import Proper, ParsedSource, Section
from propers.parser import ProperParser, log
from constants.common import LANGUAGE_LATIN, REFERENCE_REGEX, SECTION_REGEX, IGNORED_REFERENCES, RULE


class ProperParserLatinRef(ProperParser):

    def parse(self) -> tuple[Proper, Proper]:

        parsed_source_latin, parsed_source_vernacular = self.preparse()
        proper_latin = Proper(self.proper_id, LANGUAGE_LATIN, parsed_source_latin)
        proper_vernacular = Proper(self.proper_id, self.lang, parsed_source_vernacular)
        return proper_vernacular, proper_latin

    def preparse(self) -> tuple[ParsedSource, ParsedSource]:
        """
        Read plain file and store it as ParsedSource, do not resolve any dependencies at this point.
        """
        def _parse(lang):
            full_path: str = self._get_full_path(self._get_partial_path(), lang)
            if not full_path:
                raise ProperNotFound(f'Proper `{self.proper_id}` not found.')
            parsed_source = ParsedSource()
            section_name: Union[str, None] = None
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
                        # reference outside any section as a first non-empty line - treat as [Rule] vide
                        if RULE not in parsed_source.keys():
                            parsed_source.set_section(RULE, Section(RULE))
                        parsed_source.get_section(RULE).append_to_body(f"vide {ln.lstrip('@')}")
                        continue

                    ln = self._normalize(ln, lang)

                    if re.search(SECTION_REGEX, ln):
                        section_name: str = re.sub(SECTION_REGEX, '\\1', ln)

                    if re.match(SECTION_REGEX, ln):
                        parsed_source.set_section(section_name, Section(section_name))
                    else:
                        if section_name not in parsed_source.keys():
                            parsed_source.set_section(section_name, Section(section_name))
                        parsed_source.get_section(section_name).append_to_body(ln)
            return parsed_source

        parsed_source_latin = _parse(LANGUAGE_LATIN)
        parsed_source_vernacular = _parse(self.lang)
        parsed_source_vernacular.merge(parsed_source_latin)

        return parsed_source_latin, parsed_source_vernacular