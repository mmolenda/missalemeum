import re
from trans import trans


def parse_section(text):
    """
    "*Ps 50:9*\nPokrop mnie, Panie, hyzopem, a będę oczyszczony.\n*Ps 50:3*\nZmiłuj się nade mną" ->
    "<em>Ps 50:9</em><br>Pokrop mnie, Panie, hyzopem, a będę oczyszczony.<br><em>Ps 50:3</em><br>Zmiłuj się nade mną"
    :param text:
    :return:
    """
    return re.sub('\*([^\*]+)\*', '<em>\\1</em>', text.replace('\n', '<br>'))


def slugify(text):
    """
    "Antyfona na Komunię" -> "antyfona-na-komunie"
    :param text:
    :return:
    """
    return trans(text).replace(' ', '-').lower()

