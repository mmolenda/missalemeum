from copy import copy
from typing import ItemsView, KeysView, List, Union, ValuesView

from constants.common import VISIBLE_SECTIONS, GRADUALE, TRACTUS, GRADUALE_PASCHAL, COMMEMORATED_ORATIO, \
    COMMEMORATED_SECRETA, COMMEMORATED_POSTCOMMUNIO, POSTCOMMUNIO, SECRETA, ORATIO, COMMEMORATION
from exceptions import ProperNotFound


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

    def merge(self, proper: 'ParsedSource') -> None:
        for k, v in proper.items():
            if k not in self._container.keys():
                self._container[k] = v


class Proper(ParsedSource):
    """
    Class representing a Proper for given observance.
    """
    title: str = None
    description: str = None
    rank: int = None
    additional_info: List[str] = []
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

    def serialize(self) -> List[dict]:
        list_ = [v.serialize() for k, v in self._container.items()]
        return sorted(list_, key=lambda x: VISIBLE_SECTIONS.index(x['id']))

    def get_rule(self, rule_name: str) -> Union[None, str]:
        """
        Extract certain rules from sections [Rank] and [Rule]:
            * `Prefatio=.*` -> ID of preface for given observance
            * `vide .*`, `ex .*` -> global reference to other observance

        e.g.
        [Rank]
        Prefatio=Maria=veneratione;

        translates into `{'preface': 'Maria', 'vide': None}`

        """
        rules = {'preface': None, 'vide': None}

        rules_src = []
        for s in ('Rank', 'Rule'):
            section = self.get_section(s)
            if section is not None:
                for line in section.get_body():
                    rules_src.extend([i.strip() for i in line.split(';')])

        if rules_src:
            preface = [i for i in rules_src if i.startswith('Prefatio') and '=' in i]
            if preface:
                rules['preface'] = preface[-1].split('=')[1]

            vide = [i for i in rules_src if i.startswith('vide ') or i.startswith('ex ')]
            if vide:
                rules['vide'] = vide[0].split(' ')[-1].split(';')[0]

        return rules.get(rule_name)

    def add_commemorations(self, commemorations: List['Proper']):
        for commemoration in commemorations:
            self.description += f"\n{self.commemorations_names_translations[COMMEMORATION]} {commemoration.title}."
            if commemoration.description:
                self.description += f"\n\n{commemoration.description}"
            for commemorated_section_name, source_section_name in (
                    (COMMEMORATED_ORATIO, ORATIO),
                    (COMMEMORATED_SECRETA, SECRETA),
                    (COMMEMORATED_POSTCOMMUNIO, POSTCOMMUNIO)
            ):
                commemorated_section = commemoration.get_section(source_section_name)
                commemorated_section.body.insert(0, f"* {self.commemorations_names_translations[COMMEMORATION]} "
                                                    f"{commemoration.title} *")
                commemorated_section.id = commemorated_section_name
                commemorated_section.label = self.commemorations_names_translations[commemorated_section_name]
                self.set_section(commemorated_section_name, commemorated_section)

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

    def __init__(self, preface: str = None,
                 inter_readings_section: str = None,
                 strip_alleluia: bool = False):
        # inter_readings_section == None - show all sections defined in the source
        assert inter_readings_section in (None, GRADUALE, TRACTUS, GRADUALE_PASCHAL)
        self.preface = preface
        self.inter_readings_section = inter_readings_section
        self.strip_alleluia = strip_alleluia
