import dataclasses
import re
from copy import copy
from typing import ItemsView, KeysView, List, Union, ValuesView

from constants.common import VISIBLE_SECTIONS, GRADUALE, TRACTUS, GRADUALE_PASCHAL, COMMEMORATED_ORATIO, \
    COMMEMORATED_SECRETA, COMMEMORATED_POSTCOMMUNIO, POSTCOMMUNIO, SECRETA, ORATIO, COMMEMORATION, RULE, RANK, \
    TOP_LEVEL_REF
from exceptions import ProperNotFound


@dataclasses.dataclass
class Rules:
    # global reference to other source file
    vide: str = None
    # name of the preface
    preface: str = None
    # optional substitute string for the preface that will be put instead of
    # the string between two asterisks in the preface body.
    # For example prefaces about B.V.M. have variable part depending on the feast.
    preface_mod: str = None
    # if present, no data will be taken from the source;
    # used for compatibility in case of commemorations that are already included in
    # main observance's source
    ignore: bool = False

    def merge(self, other_rules: Union[None, 'Rules']) -> None:
        if other_rules:
            self.preface = self.preface or other_rules.preface
            self.preface_mod = self.preface_mod or other_rules.preface_mod


class ParsedSource:
    """
    Class representing parsed plain data file in Divinum Officium format, such as

     Ordo/Prefationes.txt
        [Adv]
        !de Adventu
        v. Vere dignum et justum est, æquum et salutáre...

        [Nat]
        !de Nativitate Domini
        v. Vere dignum et justum est, æquum et salutáre....

     Sancti/01-27.txt
        [Rank]
        S. Joannis Chrysostomi Episcopi Confessoris Ecclesiæ Doctoris;;Duplex;;3;;vide C4a

        [Name]
        Joannes Chrisostome

        [Rule]
        vide C4a

        [Introitus]
        !Eccli 15:5
        v. In médio Ecclésiæ apéruit os ejus: et implévit eum Dóminus spíritu sapiéntiæ~

    Internally it keeps the data in a dict of sections where each key is a section's ID and the value
    is a `Section` object keeping actual content of the section.
    """
    _container: dict = None

    def __init__(self) -> None:
        self._container = {}
        self.rules: Union[Rules, None] = None

    def has_section(self, section_id: str):
        try:
            body = self._container[section_id].body
        except KeyError:
            return False
        else:
            return any([i.strip() for i in body])

    def get_section(self, section_id: str) -> Union[None, 'Section']:
        return self._container.get(section_id)

    def set_section(self, section_name: str, section: 'Section') -> None:
        self._container[section_name] = section

    def pop_section(self, section_id: str) -> Union[None, 'Section']:
        try:
            body = self._container[section_id]
        except KeyError:
            return
        else:
            del self._container[section_id]
            return body

    def keys(self) -> KeysView[str]:
        return self._container.keys()

    def values(self) -> ValuesView['Section']:
        return self._container.values()

    def items(self) -> ItemsView[str, 'Section']:
        return self._container.items()

    def merge(self, other_proper: 'ParsedSource') -> None:
        if self.rules:
            self.rules.merge(other_proper.rules)
        for k, v in other_proper.items():
            if not self.has_section(k):
                self._container[k] = v

    def parse_rules(self) -> Rules:
        """
        Extract certain rules from sections [Rank] and [Rule]:
            * `Prefatio=.*=.*` -> ID of preface for given observance and optional modifier
            * `vide .*`, `ex .*` -> global reference to other observance

        e.g.
        [Rank]
        Prefatio=Maria=veneratione;

        translates into:
          vide=None
          prefatio=Maria
          prefatio_mod=veneratione

        """
        rules = Rules()

        rules_src = []
        for s in (TOP_LEVEL_REF, RANK, RULE):
            section = self.get_section(s)
            if section is not None:
                for line in section.get_body():
                    rules_src.extend([i.strip() for i in line.split(';')])

        if rules_src:
            # There might be a different preface for 1960 and earlier issue of the missal, for example:
            # Pent02-0 has `Prefatio=Nat` and `Prefatio1960=Trinitate`, that's why we sort to get 1960 last
            if preface := sorted([i.strip(';') for i in rules_src if i.startswith('Prefatio')], reverse=True):
                _, name, *mod = preface[-1].split('=')
                rules.preface = name
                if mod:
                    rules.preface_mod = mod[0]

            if vide := [i for i in rules_src if i.startswith('vide ') or i.startswith('ex ')]:
                rules.vide = vide[0].split(' ')[-1].split(';')[0]
            if [i for i in rules_src if i.startswith('ignore')]:
                rules.ignore = True

        return rules


class Proper(ParsedSource):
    """
    Class representing a Proper for given observance.
    """
    title: str = None
    description: str = None
    rank: int = None
    tags: List[str] = []
    supplements = []
    commemorations_names_translations = {
        COMMEMORATION: None,
        COMMEMORATED_ORATIO: None,
        COMMEMORATED_SECRETA: None,
        COMMEMORATED_POSTCOMMUNIO: None,
    }

    def __init__(self, id_: str, lang: str, parsed_source: ParsedSource = None) -> None:
        super(Proper, self).__init__()
        self.id = id_
        self.lang = lang
        try:
            _, _, rank, color = id_.split(':')
            self.rank = int(rank)
        except ValueError:
            raise ProperNotFound(f"Proper {id_} not found")
        self.colors = list(color)
        if parsed_source is not None:
            self._container = copy(parsed_source._container)
            self.rules = parsed_source.rules

    def serialize(self) -> List[dict]:
        list_ = [v.serialize() for k, v in self._container.items()]
        return sorted(list_, key=lambda x: VISIBLE_SECTIONS.index(x['id']))

    def add_commemorations(self, commemorations: List['Proper']):
        for i, commemoration in enumerate(commemorations):
            if commemoration.rules.ignore:
                continue
            if commemoration.description:
                self.description += (f"\n{self.commemorations_names_translations[COMMEMORATION]} "
                                     f"{commemoration.title}.\n\n{commemoration.description}")
            for source_section_name, target_section_name, add_comm_title in (
                    (ORATIO, COMMEMORATED_ORATIO, True),
                    (SECRETA, COMMEMORATED_SECRETA, True),
                    (POSTCOMMUNIO, COMMEMORATED_POSTCOMMUNIO, True),
                    (COMMEMORATED_ORATIO, COMMEMORATED_ORATIO, False),
                    (COMMEMORATED_SECRETA, COMMEMORATED_SECRETA, False),
                    (COMMEMORATED_POSTCOMMUNIO, COMMEMORATED_POSTCOMMUNIO, False)
            ):
                if source_section := commemoration.get_section(source_section_name):
                    target_section = self.get_section(target_section_name) or Section(
                        id_=target_section_name,
                        label=self.commemorations_names_translations[target_section_name]
                    )
                    if add_comm_title:
                        target_section.append_to_body(f"*{self.commemorations_names_translations[COMMEMORATION]} "
                                                      f"{commemoration.title}*")
                    try:
                        target_section.extend_body(source_section.body)
                    except AttributeError:
                        raise
                    self.set_section(target_section_name, target_section)

    def __repr__(self):
        return f'Proper<{self.id}>'


class Section:
    id: str = None
    label: str = None
    body: List[str] = None

    def __init__(self, id_: str, body: list=None, label: str=None) -> None:
        self.id = id_
        self.body = body if body is not None else []
        self.label = label if label is not None else id_

    def get_body(self) -> List[str]:
        return self.body

    def set_label(self, label: str) -> None:
        self.label = label

    def extend_body(self, body_part: list) -> None:
        self.body.extend(body_part)

    def append_to_body(self, body_part: str) -> None:
        self.body.append(body_part)

    def substitute_reference(self, reference: str, body_part: list[str]) -> None:
        for i, ln in enumerate(self.body):
            if ln == reference:
                self.body = self.body[:i] + body_part + self.body[i + 1:]

    def substitute_in_preface(self, from_: re.Pattern, to_: str):
        """
        As prefaces after the normalisation have both the title and a string
        that can be potentially substituted (depending on feast) marked in the same way,
        we explicitly omit the first line.

        [Maria]
        *de Beata Maria Virgine*
        v. Vere dignum et justum est (...) Et te in *Festivitáte* beátæ Maríæ
                                                    ^^^^^^^^^^^^^
                                                    only do substitution here
        """
        for i, line in enumerate(self.body[1:], start=1):
            self.body[i] = re.sub(from_, to_, line)

    def serialize(self) -> dict:
        return {'id': self.id, 'label': self.label, 'body': '\n'.join(self.body)}

    def __str__(self):
        body_short = ' '.join(self.body)[:32]
        return f'{self.id} ({self.label}) {body_short}'

    def __repr__(self):
        return f'Section<{self.label}>'


class ProperConfig:
    """
    This class is used to override certain aspects of the proper existing in the proper's source file
    """
    preface = None
    inter_readings_section = None
    strip_alleluia = False
    strip_tract = False

    def __init__(self, preface: str = None,
                 inter_readings_section: str = None,
                 strip_alleluia: bool = False,
                 strip_tract: bool = False):
        # inter_readings_section == None - show all sections defined in the source
        assert inter_readings_section in (None, GRADUALE, TRACTUS, GRADUALE_PASCHAL)
        self.preface = preface
        self.inter_readings_section = inter_readings_section
        self.strip_alleluia = strip_alleluia
        self.strip_tract = strip_tract
