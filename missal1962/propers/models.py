import json
from typing import ItemsView, KeysView, List, Union, ValuesView

from constants.common import VISIBLE_SECTIONS


class Proper:
    """
    Class representing a Proper for given observance.

    Internally it keeps the data in a dict of sections where each key is a section's ID and the value
    is a `ProperSection` object keeping actual content of the section.
    """
    _container: dict = None

    def __init__(self, id_: str) -> None:
        self.id = id_
        self._container = {}

    def serialize(self) -> List[dict]:
        list_ = [v.serialize() for k, v in self._container.items() if k in VISIBLE_SECTIONS]
        return sorted(list_, key=lambda x: VISIBLE_SECTIONS.index(x['id']))

    def get_section(self, section_id: str) -> Union[None, 'ProperSection']:
        return self._container.get(section_id)

    def set_section(self, section_name: str, section: 'ProperSection') -> None:
        self._container[section_name] = section

    def pop_section(self, section_id: str) -> Union[None, 'ProperSection']:
        try:
            body = self._container[section_id]
        except KeyError:
            return
        else:
            del self._container[section_id]
            return body

    def keys(self) -> KeysView[str]:
        return self._container.keys()

    def values(self) -> ValuesView['ProperSection']:
        return self._container.values()

    def items(self) -> ItemsView[str, 'ProperSection']:
        return self._container.items()

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
        for s in ('Rule', 'Rank'):
            section = self.get_section(s)
            if section is not None:
                rules_src.extend(section.get_body())

        if rules_src:
            preface = [i for i in rules_src if i.startswith('Prefatio=')]
            if preface:
                rules['preface'] = preface[0].split('=')[1]

            vide = [i for i in rules_src if i.startswith('vide ') or i.startswith('ex ')]
            if vide:
                vide = vide[0].split(' ')[-1].split(';')[0]
                if '/' not in vide:
                    vide = f'Commune/{vide}'
                rules['vide'] = vide

        return rules.get(rule_name)

    def merge(self, proper: 'Proper') -> None:
        for k, v in proper.items():
            if k not in self._container.keys():
                self._container[k] = v


class ProperSection:
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
