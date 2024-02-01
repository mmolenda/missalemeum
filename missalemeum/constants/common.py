import os
import re
from collections import defaultdict

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
RESOURCES_DIR = os.path.join(THIS_DIR, '..', '..', 'resources')
DIVOFF_DIR = os.path.join(RESOURCES_DIR, 'divinum-officium')
CUSTOM_DIVOFF_DIR = os.path.join(RESOURCES_DIR, 'divinum-officium-custom')
PROPERS_DIR = os.path.join(RESOURCES_DIR, 'propers')
ORDO_DIR = os.path.join(RESOURCES_DIR, 'ordo')
SUPPLEMENT_DIR = os.path.join(RESOURCES_DIR, 'supplement')

SUNDAY = 6
LANGUAGE_LATIN = 'la'
LANGUAGE_ENGLISH = 'en'
LANGUAGES = {'en': 'English', 'pl': 'Polski'}
DIVOFF_LANG_MAP = {'la': 'Latin'}
DIVOFF_LANG_MAP.update(LANGUAGES)
TYPE_TEMPORA = 'tempora'
TYPE_SANCTI = 'sancti'
PREFATIO_COMMUNIS = 'Communis'
PREFATIO_TRINITATE = 'Trinitate'
PREFATIO_PASCHAL = 'Pasch'
PREFATIO_APOSTOLIS = 'Apostolis'
PREFATIO_NAT = 'Nat'
PREFATIO_EPI = 'Epi'
PREFATIO_OMIT = 'prefatio_omit'
PREFATIO_LENT = 'Quad'
PREFATIO_ASCENSION = 'Asc'

ASTERISK = '*'
PATTERN_TEMPORA = re.compile(r'^tempora:.*')
PATTERN_ADVENT = re.compile(r'^tempora:Adv\d')
PATTERN_ADVENT_SUNDAY = re.compile(r'^tempora:Adv\d-0')
PATTERN_ADVENT_FERIA = re.compile(r'tempora:Adv\d-[1-6]')
PATTERN_ADVENT_FERIA_BETWEEN_17_AND_23 = re.compile(r'tempora:Adv\d-[1-6]:2')
PATTERN_ADVENT_FERIA_BEFORE_17 = re.compile(r'tempora:Adv\d-[1-6]:3')
PATTERN_POST_EPIPHANY_SUNDAY = re.compile(r'^tempora:Epi\d-0')
PATTERN_PRE_LENTEN = re.compile(r'^tempora:Quadp\d')
PATTERN_LENT = re.compile(r'^tempora:Quad(p3-[3-6]|\d)')
PATTERN_LENT_PREFATIO = re.compile(r'^tempora:Quad(p3-[3-6]|[1-4]-\d)')
PATTERN_EASTER = re.compile(r'^tempora:Pasc\d')
PATTERN_EASTER_PREFATIO = re.compile(r'^tempora:Pasc([0-4]|5-0|5-1|5-2|5-3)')
PATTERN_ASCENSION_PREFATIO = re.compile(r'^tempora:Pasc(5-4|5-5|5-6|6-0|6-1|6-2|6-3|6-4|6-5)')
PATTERN_LENT_SUNDAY = re.compile(r'^tempora:Quad\d-0.*')
PATTERN_TEMPORA_SUNDAY = re.compile(r'^tempora:.*-0r*:\d:\w{1,2}$')
PATTERN_TEMPORA_SUNDAY_CLASS_1 = re.compile(r'^tempora:.*-0r*:1:\w{1,2}$')
PATTERN_TEMPORA_SUNDAY_CLASS_2 = re.compile(r'^tempora:(.*-0r*:2|Nat1-0):\w$')
PATTERN_TEMPORA_CLASS_1 = re.compile(r'^tempora:.*:1:\w$')
PATTERN_TEMPORA_CLASS_2 = re.compile(r'^tempora:.*:2:\w$')
PATTERN_TEMPORA_CLASS_3 = re.compile(r'^tempora:.*:3:\w$')
PATTERN_TEMPORA_CLASS_4 = re.compile(r'^tempora:.*:4:\w$')
PATTERN_SANCTI = re.compile(r'^sancti:')
PATTERN_SANCTI_CLASS_1 = re.compile(r'^sancti:.*:1:\w$')
PATTERN_SANCTI_CLASS_2 = re.compile(r'^sancti:.*:2:\w$')
PATTERN_SANCTI_CLASS_3 = re.compile(r'^sancti:.*:3:\w$')
PATTERN_SANCTI_CLASS_3_LOCAL = re.compile(r'^sancti:.*(?:' + r"|".join(LANGUAGES.keys()) + r'):3:\w$')
PATTERN_SANCTI_CLASS_4 = re.compile(r'^sancti:.*:4c?:\w$')
PATTERN_SANCTI_CLASS_1_OR_2 = re.compile(r'^sancti:.*:[12]:\w$')
PATTERN_CLASS_1 = re.compile(r'^[a-z]+:.*:1:\w$')
PATTERN_CLASS_2 = re.compile(r'^[a-z]+:.*:2:\w$')
PATTERN_CLASS_3 = re.compile(r'^[a-z]+:.*:3:\w$')
PATTERN_COMMEMORATION = 'wspomnienie'
PATTERN_ALLELUIA = re.compile(r'allel[uú][ij]a.*', re.IGNORECASE)
PATTERN_TRACT = re.compile(r'.*tra[ck]t.*', re.IGNORECASE)
PATTERN_PREFATIO_SUBSTITUTION = re.compile(r'\*(.*)\*')
INTROIT = 'Introitus'
ORATIO = 'Oratio'
LECTIO = 'Lectio'
TRACTUS = 'Tractus'
GRADUALE = 'Graduale'
GRADUALE_PASCHAL = 'GradualeP'
EVANGELIUM = 'Evangelium'
OFFERTORIUM = 'Offertorium'
SECRETA = 'Secreta'
COMMUNIO = 'Communio'
POSTCOMMUNIO = 'Postcommunio'
COMMEMORATION = 'Commemoratio'
COMMEMORATED_ORATIO = 'Commemoratio Oratio'
COMMEMORATED_SECRETA = 'Commemoratio Secreta'
COMMEMORATED_POSTCOMMUNIO = 'Commemoratio Postcommunio'
PREFATIO = 'Prefatio'
TEMPORA_RANK_MAP = (
    {"pattern": PATTERN_ADVENT_FERIA, "month": 12, "day": 17, "rank": 2},
    {"pattern": PATTERN_ADVENT_FERIA, "month": 12, "day": 18, "rank": 2},
    {"pattern": PATTERN_ADVENT_FERIA, "month": 12, "day": 19, "rank": 2},
    {"pattern": PATTERN_ADVENT_FERIA, "month": 12, "day": 20, "rank": 2},
    {"pattern": PATTERN_ADVENT_FERIA, "month": 12, "day": 21, "rank": 2},
    {"pattern": PATTERN_ADVENT_FERIA, "month": 12, "day": 22, "rank": 2},
    {"pattern": PATTERN_ADVENT_FERIA, "month": 12, "day": 23, "rank": 2},
)
WEEKDAY_MAPPING = {
    '0': 6,
    '1': 0,
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '10-DU': 6  # The Feast of Christ the King, last Sunday of October.
}


# Sections that will be visible on serialization; they'll be also ordered according to this list
VISIBLE_SECTIONS = [
    'Comment',
    # Atypical sections
    # 02-02, feast of the Purification of the B.V.M.
    'De Benedictione Candelarum',
    'De Distributione Candelarum',
    'De Processione',
    # Quad6-0r, Dominica II Passionis seu in Palmis
    'Benedictio Palmorum',
    'De distributione ramorum',
    'De lectione Evangelica',
    'De processione cum ramis benedictis',
    'Hymnus ad Christum Regem',
    # Quad6-5r, Feria Sexta in Parasceve
    'Lectiones',
    'Passio',
    'Oratio Fidelium',
    'Crucis Adoratione',
    'CommunioQ',
    # Quad6-5r, Sabbato Sancto
    'Benedictio ignis',
    'De benedictione cerei Paschalis',
    'De solemni processione',
    'De praeconio paschali',
    'De lectionibus',
    'De prima parte Litaniarum',
    'De benedictione aquae baptismalis',
    'De renovatione promissionum baptismatis',
    'De altera parte Litaniarum',
    'De Missa solemni Vigiliae paschalis',
    # Feria IV Cinerum
    'Benedictio cinerum',
    # Common sections
    INTROIT,
    ORATIO,
    'LectioL1',
    'GradualeL1',
    'OratioL1',
    'LectioL2',
    'GradualeL2',
    'OratioL2',
    'LectioL3',
    'GradualeL3',
    'OratioL3',
    'LectioL4',
    'GradualeL4',
    'OratioL4',
    'LectioL5',
    'GradualeL5',
    'OratioL5',
    COMMEMORATED_ORATIO,
    LECTIO,
    GRADUALE,
    GRADUALE_PASCHAL,
    TRACTUS,
    'Sequentia',
    EVANGELIUM,
    'Maundi',  # Quad6-4r, Feria Quinta in Coena Domini
    OFFERTORIUM,
    # 'OffertoriumP',  Ignoring for now
    SECRETA,
    COMMEMORATED_SECRETA,
    PREFATIO,
    'Pro Laudibus',  # Quad6-5r, Sabbato Sancto
    'Communicantes',
    COMMUNIO,
    # 'CommunioP',  Ignoring for now
    POSTCOMMUNIO,
    COMMEMORATED_POSTCOMMUNIO,
    'Conclusio',  # Quad6-5r, Sabbato Sancto
    'Super populum',
    'Post Missam',  # Quad6-4r, Feria Quinta in Coena Domini
    'Denudatione altaris'  # Quad6-4r, Feria Quinta in Coena Domini
]

# References to the sections that do not exist in the source files and are ignored
# on purpose as they make sense in the context of Divinum Officium, but not in Missalemeum
IGNORED_REFERENCES = ['Oratio Gregem', 'Secreta Gregem', 'Postcommunio Gregem', 'Munda Cor Passionis']

FERIA = ':feria:4:w'
# TEMPORA - days whose dates are not fixed, but are calculated (in most cases depending on Easter Sunday)
TEMPORA_EPI1_0 = 'tempora:Epi1-0:2:w'    # Feast of the Holy Family
TEMPORA_EPI1_0A = 'tempora:Epi1-0a:2:w'  # First Sunday after Epiphany
TEMPORA_EPI1_1 = 'tempora:Epi1-1:4:w'    # Monday after 1st week of Epiphany
TEMPORA_EPI1_2 = 'tempora:Epi1-2:4:w'    # Tuesday after 1st week of Epiphany
TEMPORA_EPI1_3 = 'tempora:Epi1-3:4:w'    # Wednesday after 1st week of Epiphany
TEMPORA_EPI1_4 = 'tempora:Epi1-4:4:w'    # Thursday after 1st week of Epiphany
TEMPORA_EPI1_5 = 'tempora:Epi1-5:4:w'    # Friday after 1st week of Epiphany
TEMPORA_EPI1_6 = 'tempora:Epi1-6:4:w'    # Saturday after 1st week of Epiphany
TEMPORA_EPI2_0 = 'tempora:Epi2-0:2:g'    # Sunday after 2nd week of Epiphany
TEMPORA_EPI2_1 = 'tempora:Epi2-1:4:g'    # Monday after 2nd week of Epiphany
TEMPORA_EPI2_2 = 'tempora:Epi2-2:4:g'
TEMPORA_EPI2_3 = 'tempora:Epi2-3:4:g'
TEMPORA_EPI2_4 = 'tempora:Epi2-4:4:g'
TEMPORA_EPI2_5 = 'tempora:Epi2-5:4:g'
TEMPORA_EPI2_6 = 'tempora:Epi2-6:4:g'
TEMPORA_EPI3_0 = 'tempora:Epi3-0:2:g'
TEMPORA_EPI3_1 = 'tempora:Epi3-1:4:g'
TEMPORA_EPI3_2 = 'tempora:Epi3-2:4:g'
TEMPORA_EPI3_3 = 'tempora:Epi3-3:4:g'
TEMPORA_EPI3_4 = 'tempora:Epi3-4:4:g'
TEMPORA_EPI3_5 = 'tempora:Epi3-5:4:g'
TEMPORA_EPI3_6 = 'tempora:Epi3-6:4:g'
TEMPORA_EPI4_0 = 'tempora:Epi4-0:2:g'
TEMPORA_EPI4_1 = 'tempora:Epi4-1:4:g'
TEMPORA_EPI4_2 = 'tempora:Epi4-2:4:g'
TEMPORA_EPI4_3 = 'tempora:Epi4-3:4:g'
TEMPORA_EPI4_4 = 'tempora:Epi4-4:4:g'
TEMPORA_EPI4_5 = 'tempora:Epi4-5:4:g'
TEMPORA_EPI4_6 = 'tempora:Epi4-6:4:g'
TEMPORA_EPI5_0 = 'tempora:Epi5-0:2:g'
TEMPORA_EPI5_1 = 'tempora:Epi5-1:4:g'
TEMPORA_EPI5_2 = 'tempora:Epi5-2:4:g'
TEMPORA_EPI5_3 = 'tempora:Epi5-3:4:g'
TEMPORA_EPI5_4 = 'tempora:Epi5-4:4:g'
TEMPORA_EPI5_5 = 'tempora:Epi5-5:4:g'
TEMPORA_EPI5_6 = 'tempora:Epi5-6:4:g'
TEMPORA_EPI6_0 = 'tempora:Epi6-0:2:g'
TEMPORA_EPI6_1 = 'tempora:Epi6-1:4:g'
TEMPORA_EPI6_2 = 'tempora:Epi6-2:4:g'
TEMPORA_EPI6_3 = 'tempora:Epi6-3:4:g'
TEMPORA_EPI6_4 = 'tempora:Epi6-4:4:g'
TEMPORA_EPI6_5 = 'tempora:Epi6-5:4:g'
TEMPORA_EPI6_6 = 'tempora:Epi6-6:4:g'

TEMPORA_QUADP1_0 = 'tempora:Quadp1-0:2:v'  # Septuagesima Sunday
TEMPORA_QUADP1_1 = 'tempora:Quadp1-1:4:v'
TEMPORA_QUADP1_2 = 'tempora:Quadp1-2:4:v'
TEMPORA_QUADP1_3 = 'tempora:Quadp1-3:4:v'
TEMPORA_QUADP1_4 = 'tempora:Quadp1-4:4:v'
TEMPORA_QUADP1_5 = 'tempora:Quadp1-5:4:v'
TEMPORA_QUADP1_6 = 'tempora:Quadp1-6:4:v'
TEMPORA_QUADP2_0 = 'tempora:Quadp2-0:2:v'  # Sexagesima Sunday
TEMPORA_QUADP2_1 = 'tempora:Quadp2-1:4:v'
TEMPORA_QUADP2_2 = 'tempora:Quadp2-2:4:v'
TEMPORA_QUADP2_3 = 'tempora:Quadp2-3:4:v'
TEMPORA_QUADP2_4 = 'tempora:Quadp2-4:4:v'
TEMPORA_QUADP2_5 = 'tempora:Quadp2-5:4:v'
TEMPORA_QUADP2_6 = 'tempora:Quadp2-6:4:v'
TEMPORA_QUADP3_0 = 'tempora:Quadp3-0:2:v'  # Quinquagesima Sunday
TEMPORA_QUADP3_1 = 'tempora:Quadp3-1:4:v'
TEMPORA_QUADP3_2 = 'tempora:Quadp3-2:4:v'

TEMPORA_QUADP3_3 = 'tempora:Quadp3-3:1:v'  # Ash Wednesday
TEMPORA_QUADP3_4 = 'tempora:Quadp3-4:3:v'
TEMPORA_QUADP3_5 = 'tempora:Quadp3-5:3:v'
TEMPORA_QUADP3_6 = 'tempora:Quadp3-6:3:v'
TEMPORA_QUAD1_0 = 'tempora:Quad1-0:1:v'  # Sunday in 1st week of Lent
TEMPORA_QUAD1_1 = 'tempora:Quad1-1:3:v'  # Monday in 1st week of Lent
TEMPORA_QUAD1_2 = 'tempora:Quad1-2:3:v'  # Tuesday in 1st week of Lent
TEMPORA_QUAD1_3 = 'tempora:Quad1-3:2:v'  # Ember Wednesday of Lent
TEMPORA_QUAD1_4 = 'tempora:Quad1-4:3:v'  # Thursday in 1st week of Lent
TEMPORA_QUAD1_5 = 'tempora:Quad1-5:2:v'  # Ember Friday of Lent
TEMPORA_QUAD1_6 = 'tempora:Quad1-6:2:v'  # Ember Saturday of Lent
TEMPORA_QUAD2_0 = 'tempora:Quad2-0:1:v'  # Sunday in 2nd week of Lent
TEMPORA_QUAD2_1 = 'tempora:Quad2-1:3:v'  # Monday in 2nd week of Lent
TEMPORA_QUAD2_2 = 'tempora:Quad2-2:3:v'
TEMPORA_QUAD2_3 = 'tempora:Quad2-3:3:v'
TEMPORA_QUAD2_4 = 'tempora:Quad2-4:3:v'
TEMPORA_QUAD2_5 = 'tempora:Quad2-5:3:v'
TEMPORA_QUAD2_6 = 'tempora:Quad2-6:3:v'
TEMPORA_QUAD3_0 = 'tempora:Quad3-0:1:v'
TEMPORA_QUAD3_1 = 'tempora:Quad3-1:3:v'
TEMPORA_QUAD3_2 = 'tempora:Quad3-2:3:v'
TEMPORA_QUAD3_3 = 'tempora:Quad3-3:3:v'
TEMPORA_QUAD3_4 = 'tempora:Quad3-4:3:v'
TEMPORA_QUAD3_5 = 'tempora:Quad3-5:3:v'
TEMPORA_QUAD3_6 = 'tempora:Quad3-6:3:v'
TEMPORA_QUAD4_0 = 'tempora:Quad4-0:1:pv'
TEMPORA_QUAD4_1 = 'tempora:Quad4-1:3:v'
TEMPORA_QUAD4_2 = 'tempora:Quad4-2:3:v'
TEMPORA_QUAD4_3 = 'tempora:Quad4-3:3:v'
TEMPORA_QUAD4_4 = 'tempora:Quad4-4:3:v'
TEMPORA_QUAD4_5 = 'tempora:Quad4-5:3:v'
TEMPORA_QUAD4_6 = 'tempora:Quad4-6:3:v'
TEMPORA_QUAD5_0 = 'tempora:Quad5-0:1:v'  # 1st Passion Sunday
TEMPORA_QUAD5_1 = 'tempora:Quad5-1:3:v'
TEMPORA_QUAD5_2 = 'tempora:Quad5-2:3:v'
TEMPORA_QUAD5_3 = 'tempora:Quad5-3:3:v'
TEMPORA_QUAD5_4 = 'tempora:Quad5-4:3:v'
TEMPORA_QUAD5_5 = 'tempora:Quad5-5Feria:3:v'
TEMPORA_QUAD5_5C = 'tempora:Quad5-5Feriac:4:w'
TEMPORA_QUAD5_6 = 'tempora:Quad5-6:3:v'
TEMPORA_QUAD6_0 = 'tempora:Quad6-0r:1:rv'  # 2nd Passion Sunday (Palm Sunday)
TEMPORA_QUAD6_1 = 'tempora:Quad6-1:1:v'
TEMPORA_QUAD6_2 = 'tempora:Quad6-2:1:v'
TEMPORA_QUAD6_3 = 'tempora:Quad6-3:1:v'
TEMPORA_QUAD6_4 = 'tempora:Quad6-4r:1:w'  # Maundy Thursday
TEMPORA_QUAD6_5 = 'tempora:Quad6-5r:1:bv'  # Good Friday
TEMPORA_QUAD6_6 = 'tempora:Quad6-6r:1:vw'  # Holy Saturday
#
TEMPORA_PASC0_0 = 'tempora:Pasc0-0:1:w'  # Resurrection Sunday
TEMPORA_PASC0_1 = 'tempora:Pasc0-1:1:w'
TEMPORA_PASC0_2 = 'tempora:Pasc0-2:1:w'
TEMPORA_PASC0_3 = 'tempora:Pasc0-3:1:w'
TEMPORA_PASC0_4 = 'tempora:Pasc0-4:1:w'
TEMPORA_PASC0_5 = 'tempora:Pasc0-5:1:w'
TEMPORA_PASC0_6 = 'tempora:Pasc0-6:1:w'
TEMPORA_PASC1_0 = 'tempora:Pasc1-0:1:w'  # Low Sunday
TEMPORA_PASC1_1 = 'tempora:Pasc1-1:4:w'
TEMPORA_PASC1_2 = 'tempora:Pasc1-2:4:w'
TEMPORA_PASC1_3 = 'tempora:Pasc1-3:4:w'
TEMPORA_PASC1_4 = 'tempora:Pasc1-4:4:w'
TEMPORA_PASC1_5 = 'tempora:Pasc1-5:4:w'
TEMPORA_PASC1_6 = 'tempora:Pasc1-6:4:w'
TEMPORA_PASC2_0 = 'tempora:Pasc2-0:2:w'
TEMPORA_PASC2_1 = 'tempora:Pasc2-1:4:w'
TEMPORA_PASC2_2 = 'tempora:Pasc2-2:4:w'
TEMPORA_PASC2_3 = 'tempora:Pasc2-3Feria:4:w'
TEMPORA_PASC2_4 = 'tempora:Pasc2-4Feria:4:w'
TEMPORA_PASC2_5 = 'tempora:Pasc2-5Feria:4:w'
TEMPORA_PASC2_6 = 'tempora:Pasc2-6Feria:4:w'
TEMPORA_PASC3_0 = 'tempora:Pasc3-0r:2:w'
TEMPORA_PASC3_1 = 'tempora:Pasc3-1Feria:4:w'
TEMPORA_PASC3_2 = 'tempora:Pasc3-2Feria:4:w'
TEMPORA_PASC3_3 = 'tempora:Pasc3-3Feria:4:w'
TEMPORA_PASC3_4 = 'tempora:Pasc3-4:4:w'
TEMPORA_PASC3_5 = 'tempora:Pasc3-5:4:w'
TEMPORA_PASC3_6 = 'tempora:Pasc3-6:4:w'
TEMPORA_PASC4_0 = 'tempora:Pasc4-0:2:w'
TEMPORA_PASC4_1 = 'tempora:Pasc4-1:4:w'
TEMPORA_PASC4_2 = 'tempora:Pasc4-2:4:w'
TEMPORA_PASC4_3 = 'tempora:Pasc4-3:4:w'
TEMPORA_PASC4_4 = 'tempora:Pasc4-4:4:w'
TEMPORA_PASC4_5 = 'tempora:Pasc4-5:4:w'
TEMPORA_PASC4_6 = 'tempora:Pasc4-6:4:w'
TEMPORA_PASC5_0 = 'tempora:Pasc5-0:2:w'
TEMPORA_PASC5_1 = 'tempora:Pasc5-1:4:v'
TEMPORA_PASC5_2 = 'tempora:Pasc5-2:4:w'
TEMPORA_PASC5_3 = 'tempora:Pasc5-3:2:w'  # Vigil of Ascension
#
TEMPORA_PASC5_4 = 'tempora:Pasc5-4:1:w'  # Ascension
TEMPORA_PASC5_5 = 'tempora:Pasc5-5:4:w'
TEMPORA_PASC5_6 = 'tempora:Pasc5-6:4:w'
TEMPORA_PASC6_0 = 'tempora:Pasc6-0:2:w'
TEMPORA_PASC6_1 = 'tempora:Pasc6-1:4:w'
TEMPORA_PASC6_2 = 'tempora:Pasc6-2:4:w'
TEMPORA_PASC6_3 = 'tempora:Pasc6-3:4:w'
TEMPORA_PASC6_4 = 'tempora:Pasc6-4r:4:w'
TEMPORA_PASC6_5 = 'tempora:Pasc6-5:4:w'
TEMPORA_PASC6_6 = 'tempora:Pasc6-6:1:r'  # Vigil of Pentecost
#
TEMPORA_PASC7_0 = 'tempora:Pasc7-0:1:r'  # Pentecost
TEMPORA_PASC7_1 = 'tempora:Pasc7-1:1:r'  # Whit Monday
TEMPORA_PASC7_2 = 'tempora:Pasc7-2:1:r'
TEMPORA_PASC7_3 = 'tempora:Pasc7-3:1:r'  # Ember Wednesday in Octave of Pentecost
TEMPORA_PASC7_4 = 'tempora:Pasc7-4:1:r'
TEMPORA_PASC7_5 = 'tempora:Pasc7-5:1:r'  # Ember Friday in Octave of Pentecost
TEMPORA_PASC7_6 = 'tempora:Pasc7-6:1:r'  # Ember Saturday in Octave of Pentecost
TEMPORA_PENT01_0A = 'tempora:Pent01-0a:2:g'  # 1st Sunday after Pentecost
TEMPORA_PENT01_0 = 'tempora:Pent01-0r:1:w'  # Trinity Sunday
TEMPORA_PENT01_1 = 'tempora:Pent01-1:4:g'
TEMPORA_PENT01_2 = 'tempora:Pent01-2:4:g'
TEMPORA_PENT01_3 = 'tempora:Pent01-3:4:g'
TEMPORA_PENT01_4 = 'tempora:Pent01-4:1:w'  # Corpus Christi
TEMPORA_PENT01_5 = 'tempora:Pent01-5:4:g'
TEMPORA_PENT01_6 = 'tempora:Pent01-6:4:g'
TEMPORA_PENT02_0 = 'tempora:Pent02-0r:2:g'  # Sunday in 2nd week after Pentecost
TEMPORA_PENT02_1 = 'tempora:Pent02-1:4:g'  # Monday in 2nd week after Pentecost
TEMPORA_PENT02_2 = 'tempora:Pent02-2:4:g'  # Tuesday in 2nd week after Pentecost
TEMPORA_PENT02_3 = 'tempora:Pent02-3:4:g'  # Wednesday in 2nd week after Pentecost
TEMPORA_PENT02_4 = 'tempora:Pent02-4:4:g'  # Thursday in 2nd week after Pentecost
TEMPORA_PENT02_5 = 'tempora:Pent02-5:1:w'  # Feast of the Sacred Heart
TEMPORA_PENT02_6 = 'tempora:Pent02-6Feria:4:g'  # Saturday in 2nd week after Pentecost
TEMPORA_PENT03_0 = 'tempora:Pent03-0r:2:g'  # Sunday in 3rd week after Pentecost
TEMPORA_PENT03_1 = 'tempora:Pent03-1Feria:4:g'
TEMPORA_PENT03_2 = 'tempora:Pent03-2Feria:4:g'
TEMPORA_PENT03_3 = 'tempora:Pent03-3Feria:4:g'
TEMPORA_PENT03_4 = 'tempora:Pent03-4Feria:4:g'
TEMPORA_PENT03_5 = 'tempora:Pent03-5Feria:4:g'
TEMPORA_PENT03_6 = 'tempora:Pent03-6:4:g'
TEMPORA_PENT04_0 = 'tempora:Pent04-0:2:g'
TEMPORA_PENT04_1 = 'tempora:Pent04-1:4:g'
TEMPORA_PENT04_2 = 'tempora:Pent04-2:4:g'
TEMPORA_PENT04_3 = 'tempora:Pent04-3:4:g'
TEMPORA_PENT04_4 = 'tempora:Pent04-4:4:g'
TEMPORA_PENT04_5 = 'tempora:Pent04-5:4:g'
TEMPORA_PENT04_6 = 'tempora:Pent04-6:4:g'
TEMPORA_PENT05_0 = 'tempora:Pent05-0:2:g'
TEMPORA_PENT05_1 = 'tempora:Pent05-1:4:g'
TEMPORA_PENT05_2 = 'tempora:Pent05-2:4:g'
TEMPORA_PENT05_3 = 'tempora:Pent05-3:4:g'
TEMPORA_PENT05_4 = 'tempora:Pent05-4:4:g'
TEMPORA_PENT05_5 = 'tempora:Pent05-5:4:g'
TEMPORA_PENT05_6 = 'tempora:Pent05-6:4:g'
TEMPORA_PENT06_0 = 'tempora:Pent06-0:2:g'
TEMPORA_PENT06_1 = 'tempora:Pent06-1:4:g'
TEMPORA_PENT06_2 = 'tempora:Pent06-2:4:g'
TEMPORA_PENT06_3 = 'tempora:Pent06-3:4:g'
TEMPORA_PENT06_4 = 'tempora:Pent06-4:4:g'
TEMPORA_PENT06_5 = 'tempora:Pent06-5:4:g'
TEMPORA_PENT06_6 = 'tempora:Pent06-6:4:g'
TEMPORA_PENT07_0 = 'tempora:Pent07-0:2:g'
TEMPORA_PENT07_1 = 'tempora:Pent07-1:4:g'
TEMPORA_PENT07_2 = 'tempora:Pent07-2:4:g'
TEMPORA_PENT07_3 = 'tempora:Pent07-3:4:g'
TEMPORA_PENT07_4 = 'tempora:Pent07-4:4:g'
TEMPORA_PENT07_5 = 'tempora:Pent07-5:4:g'
TEMPORA_PENT07_6 = 'tempora:Pent07-6:4:g'
TEMPORA_PENT08_0 = 'tempora:Pent08-0:2:g'
TEMPORA_PENT08_1 = 'tempora:Pent08-1:4:g'
TEMPORA_PENT08_2 = 'tempora:Pent08-2:4:g'
TEMPORA_PENT08_3 = 'tempora:Pent08-3:4:g'
TEMPORA_PENT08_4 = 'tempora:Pent08-4:4:g'
TEMPORA_PENT08_5 = 'tempora:Pent08-5:4:g'
TEMPORA_PENT08_6 = 'tempora:Pent08-6:4:g'
TEMPORA_PENT09_0 = 'tempora:Pent09-0:2:g'
TEMPORA_PENT09_1 = 'tempora:Pent09-1:4:g'
TEMPORA_PENT09_2 = 'tempora:Pent09-2:4:g'
TEMPORA_PENT09_3 = 'tempora:Pent09-3:4:g'
TEMPORA_PENT09_4 = 'tempora:Pent09-4:4:g'
TEMPORA_PENT09_5 = 'tempora:Pent09-5:4:g'
TEMPORA_PENT09_6 = 'tempora:Pent09-6:4:g'
TEMPORA_PENT10_0 = 'tempora:Pent10-0:2:g'
TEMPORA_PENT10_1 = 'tempora:Pent10-1:4:g'
TEMPORA_PENT10_2 = 'tempora:Pent10-2:4:g'
TEMPORA_PENT10_3 = 'tempora:Pent10-3:4:g'
TEMPORA_PENT10_4 = 'tempora:Pent10-4:4:g'
TEMPORA_PENT10_5 = 'tempora:Pent10-5:4:g'
TEMPORA_PENT10_6 = 'tempora:Pent10-6:4:g'
TEMPORA_PENT11_0 = 'tempora:Pent11-0:2:g'
TEMPORA_PENT11_1 = 'tempora:Pent11-1:4:g'
TEMPORA_PENT11_2 = 'tempora:Pent11-2:4:g'
TEMPORA_PENT11_3 = 'tempora:Pent11-3:4:g'
TEMPORA_PENT11_4 = 'tempora:Pent11-4:4:g'
TEMPORA_PENT11_5 = 'tempora:Pent11-5:4:g'
TEMPORA_PENT11_6 = 'tempora:Pent11-6:4:g'
TEMPORA_PENT12_0 = 'tempora:Pent12-0:2:g'
TEMPORA_PENT12_1 = 'tempora:Pent12-1:4:g'
TEMPORA_PENT12_2 = 'tempora:Pent12-2:4:g'
TEMPORA_PENT12_3 = 'tempora:Pent12-3:4:g'
TEMPORA_PENT12_4 = 'tempora:Pent12-4:4:g'
TEMPORA_PENT12_5 = 'tempora:Pent12-5:4:g'
TEMPORA_PENT12_6 = 'tempora:Pent12-6:4:g'
TEMPORA_PENT13_0 = 'tempora:Pent13-0:2:g'
TEMPORA_PENT13_1 = 'tempora:Pent13-1:4:g'
TEMPORA_PENT13_2 = 'tempora:Pent13-2:4:g'
TEMPORA_PENT13_3 = 'tempora:Pent13-3:4:g'
TEMPORA_PENT13_4 = 'tempora:Pent13-4:4:g'
TEMPORA_PENT13_5 = 'tempora:Pent13-5:4:g'
TEMPORA_PENT13_6 = 'tempora:Pent13-6:4:g'
TEMPORA_PENT14_0 = 'tempora:Pent14-0:2:g'
TEMPORA_PENT14_1 = 'tempora:Pent14-1:4:g'
TEMPORA_PENT14_2 = 'tempora:Pent14-2:4:g'
TEMPORA_PENT14_3 = 'tempora:Pent14-3:4:g'
TEMPORA_PENT14_4 = 'tempora:Pent14-4:4:g'
TEMPORA_PENT14_5 = 'tempora:Pent14-5:4:g'
TEMPORA_PENT14_6 = 'tempora:Pent14-6:4:g'
TEMPORA_PENT15_0 = 'tempora:Pent15-0:2:g'
TEMPORA_PENT15_1 = 'tempora:Pent15-1:4:g'
TEMPORA_PENT15_2 = 'tempora:Pent15-2:4:g'
TEMPORA_PENT15_3 = 'tempora:Pent15-3:4:g'
TEMPORA_PENT15_4 = 'tempora:Pent15-4:4:g'
TEMPORA_PENT15_5 = 'tempora:Pent15-5:4:g'
TEMPORA_PENT15_6 = 'tempora:Pent15-6:4:g'
TEMPORA_PENT16_0 = 'tempora:Pent16-0:2:g'
TEMPORA_PENT16_1 = 'tempora:Pent16-1:4:g'
TEMPORA_PENT16_2 = 'tempora:Pent16-2:4:g'
TEMPORA_PENT16_3 = 'tempora:Pent16-3:4:g'
TEMPORA_PENT16_4 = 'tempora:Pent16-4:4:g'
TEMPORA_PENT16_5 = 'tempora:Pent16-5:4:g'
TEMPORA_PENT16_6 = 'tempora:Pent16-6:4:g'
TEMPORA_PENT17_0 = 'tempora:Pent17-0:2:g'
TEMPORA_PENT17_1 = 'tempora:Pent17-1:4:g'
TEMPORA_PENT17_2 = 'tempora:Pent17-2:4:g'
TEMPORA_PENT17_3 = 'tempora:Pent17-3:4:g'
TEMPORA_PENT17_4 = 'tempora:Pent17-4:4:g'
TEMPORA_PENT17_5 = 'tempora:Pent17-5:4:g'
TEMPORA_PENT17_6 = 'tempora:Pent17-6:4:g'
TEMPORA_PENT18_0 = 'tempora:Pent18-0:2:g'
TEMPORA_PENT18_1 = 'tempora:Pent18-1:4:g'
TEMPORA_PENT18_2 = 'tempora:Pent18-2:4:g'
TEMPORA_PENT18_3 = 'tempora:Pent18-3:4:g'
TEMPORA_PENT18_4 = 'tempora:Pent18-4:4:g'
TEMPORA_PENT18_5 = 'tempora:Pent18-5:4:g'
TEMPORA_PENT18_6 = 'tempora:Pent18-6:4:g'
TEMPORA_PENT19_0 = 'tempora:Pent19-0:2:g'
TEMPORA_PENT19_1 = 'tempora:Pent19-1:4:g'
TEMPORA_PENT19_2 = 'tempora:Pent19-2:4:g'
TEMPORA_PENT19_3 = 'tempora:Pent19-3:4:g'
TEMPORA_PENT19_4 = 'tempora:Pent19-4:4:g'
TEMPORA_PENT19_5 = 'tempora:Pent19-5:4:g'
TEMPORA_PENT19_6 = 'tempora:Pent19-6:4:g'
TEMPORA_PENT20_0 = 'tempora:Pent20-0:2:g'
TEMPORA_PENT20_1 = 'tempora:Pent20-1:4:g'
TEMPORA_PENT20_2 = 'tempora:Pent20-2:4:g'
TEMPORA_PENT20_3 = 'tempora:Pent20-3:4:g'
TEMPORA_PENT20_4 = 'tempora:Pent20-4:4:g'
TEMPORA_PENT20_5 = 'tempora:Pent20-5:4:g'
TEMPORA_PENT20_6 = 'tempora:Pent20-6:4:g'
TEMPORA_PENT21_0 = 'tempora:Pent21-0:2:g'
TEMPORA_PENT21_1 = 'tempora:Pent21-1:4:g'
TEMPORA_PENT21_2 = 'tempora:Pent21-2:4:g'
TEMPORA_PENT21_3 = 'tempora:Pent21-3:4:g'
TEMPORA_PENT21_4 = 'tempora:Pent21-4:4:g'
TEMPORA_PENT21_5 = 'tempora:Pent21-5:4:g'
TEMPORA_PENT21_6 = 'tempora:Pent21-6:4:g'
TEMPORA_PENT22_0 = 'tempora:Pent22-0:2:g'
TEMPORA_PENT22_1 = 'tempora:Pent22-1:4:g'
TEMPORA_PENT22_2 = 'tempora:Pent22-2:4:g'
TEMPORA_PENT22_3 = 'tempora:Pent22-3:4:g'
TEMPORA_PENT22_4 = 'tempora:Pent22-4:4:g'
TEMPORA_PENT22_5 = 'tempora:Pent22-5:4:g'
TEMPORA_PENT22_6 = 'tempora:Pent22-6:4:g'
TEMPORA_PENT23_0 = 'tempora:Pent23-0:2:g'
TEMPORA_PENT23_1 = 'tempora:Pent23-1:4:g'
TEMPORA_PENT23_2 = 'tempora:Pent23-2:4:g'
TEMPORA_PENT23_3 = 'tempora:Pent23-3:4:g'
TEMPORA_PENT23_4 = 'tempora:Pent23-4:4:g'
TEMPORA_PENT23_5 = 'tempora:Pent23-5:4:g'
TEMPORA_PENT23_6 = 'tempora:Pent23-6:4:g'

TEMPORA_PENT_3 = 'tempora:093-3:2:v'  # Ember Wednesday in September
TEMPORA_PENT_5 = 'tempora:093-5:2:v'  # Ember Friday in September
TEMPORA_PENT_6 = 'tempora:093-6:2:v'  # Ember Saturday in September

TEMPORA_PENT24_0 = 'tempora:Pent24-0:2:g'
TEMPORA_PENT24_1 = 'tempora:Pent24-1:4:g'
TEMPORA_PENT24_2 = 'tempora:Pent24-2:4:g'
TEMPORA_PENT24_3 = 'tempora:Pent24-3:4:g'
TEMPORA_PENT24_4 = 'tempora:Pent24-4:4:g'
TEMPORA_PENT24_5 = 'tempora:Pent24-5:4:g'
TEMPORA_PENT24_6 = 'tempora:Pent24-6:4:g'

TEMPORA_ADV1_0 = 'tempora:Adv1-0:1:v'  # Sunday in 1st week of Advent
TEMPORA_ADV1_1 = 'tempora:Adv1-1:3:v'  # Monday in 1st week of Advent
TEMPORA_ADV1_2 = 'tempora:Adv1-2:3:v'  # Tuesday in 1st week of Advent
TEMPORA_ADV1_3 = 'tempora:Adv1-3:3:v'  # Wednesday in 1st week of Advent
TEMPORA_ADV1_4 = 'tempora:Adv1-4:3:v'  # Thursday in 1st week of Advent
TEMPORA_ADV1_5 = 'tempora:Adv1-5:3:v'  # Friday in 1st week of Advent
TEMPORA_ADV1_6 = 'tempora:Adv1-6:3:v'  # Saturday in 1st week of Advent
TEMPORA_ADV2_0 = 'tempora:Adv2-0:1:v'
TEMPORA_ADV2_1 = 'tempora:Adv2-1:3:v'
TEMPORA_ADV2_2 = 'tempora:Adv2-2:3:v'
TEMPORA_ADV2_3 = 'tempora:Adv2-3:3:v'
TEMPORA_ADV2_4 = 'tempora:Adv2-4:3:v'
TEMPORA_ADV2_5 = 'tempora:Adv2-5:3:v'
TEMPORA_ADV2_6 = 'tempora:Adv2-6:3:v'
TEMPORA_ADV3_0 = 'tempora:Adv3-0:1:pv'
TEMPORA_ADV3_1 = 'tempora:Adv3-1:3:v'
TEMPORA_ADV3_2 = 'tempora:Adv3-2:3:v'
TEMPORA_ADV3_3 = 'tempora:Adv3-3:2:v'  # Ember Wednesday in Advent
TEMPORA_ADV3_4 = 'tempora:Adv3-4:3:v'
TEMPORA_ADV3_5 = 'tempora:Adv3-5:2:v'  # Ember Friday in Advent
TEMPORA_ADV3_6 = 'tempora:Adv3-6:2:v'  # Ember Saturday in Advent
TEMPORA_ADV4_0 = 'tempora:Adv4-0:1:v'
TEMPORA_ADV4_1 = 'tempora:Adv4-1:3:v'
TEMPORA_ADV4_2 = 'tempora:Adv4-2:3:v'
TEMPORA_ADV4_3 = 'tempora:Adv4-3:3:v'
TEMPORA_ADV4_4 = 'tempora:Adv4-4:3:v'
TEMPORA_ADV4_5 = 'tempora:Adv4-5:3:v'
TEMPORA_NAT1_0 = 'tempora:Nat1-0:2:w'  # Sunday in the Octave of Nativity
TEMPORA_NAT1_1 = 'tempora:Nat1-1:2:w'  # Ordinary day in the Octave of Nativity
TEMPORA_NAT2_0 = 'tempora:Nat2-0:2:w'  # Feast of the Holy Name of Jesus

TEMPORA_C_10A = 'commune:C10a:4:v'  # B. M. V. Saturdays in Advent
TEMPORA_C_10B = 'commune:C10b:4:w'  # B. M. V. Saturdays between Nativity and Purification
TEMPORA_C_10C = 'commune:C10c:4:w'  # B. M. V. Saturdays between Feb 2 and Wednesday in Holy Week
TEMPORA_C_10PASC = 'commune:C10Pasc:4:w'  # B. M. V. Saturdays in Easter period
TEMPORA_C_10T = 'commune:C10t:4:w'  # B. M. V. Saturdays between Trinity Sunday and Saturday before 1st Sunday of Advent

# SANCTI - days which have fixed date
SANCTI_10_DU = 'sancti:10-DU:1:w'  # Feast of Christ the King; last Sunday of October
SANCTI_01_01 = 'sancti:01-01:1:w'  # Octave of the Nativity
SANCTI_01_05 = 'sancti:01-05:4:r'  # commemoratio S. Telesphori
SANCTI_01_06 = 'sancti:01-06:1:w'  # Epiphany
SANCTI_01_11 = 'sancti:01-11:4:r'  # commemoratio S. Hyginus
SANCTI_01_13 = 'sancti:01-13:2:w'  # Baptism of the Lord
SANCTI_01_14 = 'sancti:01-14:3:w'  # S. Hilarii
SANCTI_01_14C = 'sancti:01-14c:4:r'  # commemoratio S. Felicis
SANCTI_01_15 = 'sancti:01-15:3:w'
SANCTI_01_15C = 'sancti:01-15c:4:w'  # Pro S. Mauro Abbate
SANCTI_01_16 = 'sancti:01-16:3:r'
SANCTI_01_17 = 'sancti:01-17:3:w'
SANCTI_01_18 = 'sancti:01-18r:4:w'
SANCTI_01_19 = 'sancti:01-19:4:r'
SANCTI_01_19C = 'sancti:01-19c:4:r'  # Pro S. Canuto Regi Mart.
SANCTI_01_20 = 'sancti:01-20:3:r'
SANCTI_01_21 = 'sancti:01-21:3:r'
SANCTI_01_22 = 'sancti:01-22:3:r'
SANCTI_01_23 = 'sancti:01-23:3:w'
SANCTI_01_23C = 'sancti:01-23c:4:r'  # Pro S. Emerentianæ Virg. et Mart.
SANCTI_01_24 = 'sancti:01-24:3:r'
SANCTI_01_25 = 'sancti:01-25r:3:w'
SANCTI_01_25C = 'sancti:01-25c:4:w'  # Pro S. Petro
SANCTI_01_26 = 'sancti:01-26:3:r'
SANCTI_01_27 = 'sancti:01-27:3:w'
SANCTI_01_28 = 'sancti:01-28:3:w'
SANCTI_01_28C = 'sancti:01-28c:4:r'
SANCTI_01_29 = 'sancti:01-29:3:w'
SANCTI_01_30 = 'sancti:01-30:3:r'
SANCTI_01_31 = 'sancti:01-31:3:w'

SANCTI_02_01 = 'sancti:02-01:3:r'
SANCTI_02_02 = 'sancti:02-02:2:w'  # Feast of the Purification of the Blessed Virgin Mary
SANCTI_02_03 = 'sancti:02-03:4:r'
SANCTI_02_04 = 'sancti:02-04:3:w'
SANCTI_02_05 = 'sancti:02-05:3:r'
SANCTI_02_06 = 'sancti:02-06:3:w'
SANCTI_02_06C = 'sancti:02-06c:4:r'  # św. Doroty
SANCTI_02_07 = 'sancti:02-07:3:w'
SANCTI_02_08 = 'sancti:02-08:3:w'
SANCTI_02_09 = 'sancti:02-09:3:w'
SANCTI_02_09C = 'sancti:02-09c:4:r'  # św Apolonii
SANCTI_02_10 = 'sancti:02-10:3:w'
SANCTI_02_11 = 'sancti:02-11:3:w'
SANCTI_02_12 = 'sancti:02-12:3:w'
SANCTI_02_14 = 'sancti:02-14:4:r'
SANCTI_02_15 = 'sancti:02-15:4:r'
SANCTI_02_18 = 'sancti:02-18:4:r'
SANCTI_02_22 = 'sancti:02-22:2:w'  # Feast of the Chair of Saint Peter
SANCTI_02_22C = 'sancti:02-22c:4:r'  # St. Paul
SANCTI_02_23 = 'sancti:02-23r:3:w'
SANCTI_02_24 = 'sancti:02-24:2:r'  # St. Matthias, Apostle
SANCTI_02_27 = 'sancti:02-27:3:w'

SANCTI_03_04 = 'sancti:03-04:3:w'
SANCTI_03_06 = 'sancti:03-06:3:r'
SANCTI_03_07 = 'sancti:03-07:3:w'
SANCTI_03_08 = 'sancti:03-08:3:w'
SANCTI_03_09 = 'sancti:03-09:3:w'
SANCTI_03_10 = 'sancti:03-10:3:r'
SANCTI_03_12 = 'sancti:03-12:3:w'
SANCTI_03_15PL = 'sancti:03-15pl:3:w'
SANCTI_03_17 = 'sancti:03-17:3:w'
SANCTI_03_18 = 'sancti:03-18:3:w'
SANCTI_03_19 = 'sancti:03-19:1:w'  # Saint Joseph's Day
SANCTI_03_21 = 'sancti:03-21:3:w'
SANCTI_03_24 = 'sancti:03-24:3:w'
SANCTI_03_25 = 'sancti:03-25:1:w'  # Annunciation
SANCTI_03_27 = 'sancti:03-27:3:w'
SANCTI_03_28 = 'sancti:03-28:3:w'

SANCTI_04_02 = 'sancti:04-02:3:w'
SANCTI_04_04 = 'sancti:04-04:3:w'
SANCTI_04_05 = 'sancti:04-05:3:w'
SANCTI_04_11 = 'sancti:04-11:3:w'
SANCTI_04_13 = 'sancti:04-13:3:r'
SANCTI_04_14 = 'sancti:04-14:3:r'
SANCTI_04_17 = 'sancti:04-17:4:r'
SANCTI_04_21 = 'sancti:04-21:3:w'
SANCTI_04_22 = 'sancti:04-22:3:r'
SANCTI_04_23 = 'sancti:04-23:4:r'
SANCTI_04_23PL = 'sancti:04-23pl:1:r'
SANCTI_04_24 = 'sancti:04-24:3:r'
SANCTI_04_25 = 'sancti:04-25:2:r'  # St. Mark, Evangelist
SANCTI_04_25C = 'sancti:04-25c:4:r'  #
SANCTI_04_26 = 'sancti:04-26:3:r'
SANCTI_04_27 = 'sancti:04-27:3:w'
SANCTI_04_28 = 'sancti:04-28:3:w'
SANCTI_04_29 = 'sancti:04-29:3:r'
SANCTI_04_30 = 'sancti:04-30:3:w'

SANCTI_05_01 = 'sancti:05-01r:1:w'  # St. Joseph the Worker
SANCTI_05_02 = 'sancti:05-02:3:w'
SANCTI_05_03 = 'sancti:05-03r:4:r'
SANCTI_05_03PL = 'sancti:05-03pl:1:w'
SANCTI_05_04 = 'sancti:05-04:3:w'
SANCTI_05_04PL = 'sancti:05-04pl:3:r'  # St. Florian / PL
SANCTI_05_05 = 'sancti:05-05:3:w'
SANCTI_05_07 = 'sancti:05-07:3:r'
SANCTI_05_08PL = 'sancti:05-08pl:1:r'
SANCTI_05_09 = 'sancti:05-09:3:w'
SANCTI_05_10 = 'sancti:05-10:3:w'
SANCTI_05_11 = 'sancti:05-11r:2:r'  # SS. Philip and James, Apostles
SANCTI_05_12 = 'sancti:05-12:3:r'
SANCTI_05_13 = 'sancti:05-13:3:w'
SANCTI_05_14 = 'sancti:05-14:4:r'
SANCTI_05_15 = 'sancti:05-15:3:w'
SANCTI_05_16 = 'sancti:05-16:4:w'
SANCTI_05_16PL = 'sancti:05-16pl:3:w'
SANCTI_05_17 = 'sancti:05-17:3:w'
SANCTI_05_18 = 'sancti:05-18:3:r'
SANCTI_05_19 = 'sancti:05-19:3:w'
SANCTI_05_20 = 'sancti:05-20:3:w'
SANCTI_05_24PL = 'sancti:05-24pl:2:w'
SANCTI_05_25 = 'sancti:05-25:3:w'
SANCTI_05_26 = 'sancti:05-26:3:w'
SANCTI_05_27 = 'sancti:05-27:3:w'
SANCTI_05_28 = 'sancti:05-28:3:w'
SANCTI_05_29 = 'sancti:05-29:3:w'
SANCTI_05_30 = 'sancti:05-30:4:r'
SANCTI_05_31 = 'sancti:05-31:2:w'  # Mary the Queen

SANCTI_06_01 = 'sancti:06-01:3:w'
SANCTI_06_02 = 'sancti:06-02:4:r'
SANCTI_06_04 = 'sancti:06-04:3:w'
SANCTI_06_05 = 'sancti:06-05:3:r'
SANCTI_06_06 = 'sancti:06-06:3:w'
SANCTI_06_09 = 'sancti:06-09:4:r'
SANCTI_06_10 = 'sancti:06-10:3:w'
SANCTI_06_10PL = 'sancti:06-10pl:3:w'
SANCTI_06_11 = 'sancti:06-11:3:r'
SANCTI_06_12 = 'sancti:06-12:3:r'
SANCTI_06_13 = 'sancti:06-13:3:w'
SANCTI_06_14 = 'sancti:06-14:3:w'
SANCTI_06_15 = 'sancti:06-15:4:w'
SANCTI_06_15PL = 'sancti:06-15pl:3:w'
SANCTI_06_17 = 'sancti:06-17r:3:w'
SANCTI_06_18 = 'sancti:06-18:3:r'
SANCTI_06_19 = 'sancti:06-19:3:r'
SANCTI_06_20 = 'sancti:06-20:4:r'
SANCTI_06_21 = 'sancti:06-21:3:w'
SANCTI_06_22 = 'sancti:06-22:3:w'
SANCTI_06_23 = 'sancti:06-23:2:v'  # Vigil of st. John Baptist
SANCTI_06_24 = 'sancti:06-24:1:w'  # St. John Baptist
SANCTI_06_25 = 'sancti:06-25:3:w'
SANCTI_06_26 = 'sancti:06-26r:3:r'
SANCTI_06_28 = 'sancti:06-28r:2:v'  # Vigil of ss. Peter and Paul
SANCTI_06_29 = 'sancti:06-29:1:r'  # Ss. Peter and Paul
SANCTI_06_30 = 'sancti:06-30:3:r'

SANCTI_07_01 = 'sancti:07-01:1:r'  # Feast of the Most Precious Blood
SANCTI_07_02 = 'sancti:07-02:2:w'  # Feast of the Visitation of the Blessed Virgin Mary
SANCTI_07_03 = 'sancti:07-03r:3:r'
SANCTI_07_05 = 'sancti:07-05:3:w'
SANCTI_07_07 = 'sancti:07-07:3:w'
SANCTI_07_08 = 'sancti:07-08:3:w'
SANCTI_07_10 = 'sancti:07-10:3:r'
SANCTI_07_11 = 'sancti:07-11:4:r'
SANCTI_07_12 = 'sancti:07-12:3:r'
SANCTI_07_13PL = 'sancti:07-13pl:3:w'
SANCTI_07_14 = 'sancti:07-14:3:w'
SANCTI_07_15 = 'sancti:07-15:3:w'
SANCTI_07_15PL = 'sancti:07-15pl:3:r'
SANCTI_07_16 = 'sancti:07-16:4:w'
SANCTI_07_17 = 'sancti:07-17:4:w'
SANCTI_07_18 = 'sancti:07-18:3:r'
SANCTI_07_18PL = 'sancti:07-18pl:3:r'
SANCTI_07_19 = 'sancti:07-19:3:w'
SANCTI_07_20 = 'sancti:07-20:3:r'
SANCTI_07_20PL = 'sancti:07-20pl:3:w'
SANCTI_07_21 = 'sancti:07-21r:3:w'
SANCTI_07_22 = 'sancti:07-22:3:w'
SANCTI_07_23 = 'sancti:07-23:3:w'
SANCTI_07_24 = 'sancti:07-24r:4:r'
SANCTI_07_24PL = 'sancti:07-24pl:3:w'
SANCTI_07_25 = 'sancti:07-25:2:r'  # St. James, Apostle
SANCTI_07_26 = 'sancti:07-26:2:w'  # St. Anna, Mary's Mother
SANCTI_07_27 = 'sancti:07-27:4:r'
SANCTI_07_28 = 'sancti:07-28:3:r'
SANCTI_07_29 = 'sancti:07-29:3:r'
SANCTI_07_30 = 'sancti:07-30:4:r'
SANCTI_07_31 = 'sancti:07-31:3:w'

SANCTI_08_01 = 'sancti:08-01r:4:r'
SANCTI_08_02 = 'sancti:08-02:3:r'
SANCTI_08_04 = 'sancti:08-04:3:w'
SANCTI_08_05 = 'sancti:08-05:3:w'
SANCTI_08_06 = 'sancti:08-06:2:r'  # Transfiguration
SANCTI_08_07 = 'sancti:08-07:3:r'
SANCTI_08_08 = 'sancti:08-08r:3:r'
SANCTI_08_09 = 'sancti:08-09t:3:r'  # Vigil of st. Laurent
SANCTI_08_10 = 'sancti:08-10:2:r'  # St. Laurent
SANCTI_08_11 = 'sancti:08-11:4:r'
SANCTI_08_12 = 'sancti:08-12:3:w'
SANCTI_08_13 = 'sancti:08-13:4:r'
SANCTI_08_14 = 'sancti:08-14:2:w'  # Vigil of Assumption of Mary
SANCTI_08_15 = 'sancti:08-15r:1:w'  # Assumption of Mary
SANCTI_08_16 = 'sancti:08-16:2:w'  # St. Joachim
SANCTI_08_17 = 'sancti:08-17:3:w'
SANCTI_08_18 = 'sancti:08-18r:4:w'
SANCTI_08_19 = 'sancti:08-19:3:w'
SANCTI_08_20 = 'sancti:08-20:3:w'
SANCTI_08_21 = 'sancti:08-21:3:w'
SANCTI_08_22 = 'sancti:08-22:2:w'  # Immaculate Heart of Mary
SANCTI_08_23 = 'sancti:08-23:3:w'
SANCTI_08_24 = 'sancti:08-24:2:r'  # St. Bartholomew, Apostle
SANCTI_08_25 = 'sancti:08-25:3:w'
SANCTI_08_26 = 'sancti:08-26:4:r'
SANCTI_08_26PL = 'sancti:08-26pl:1:w'
SANCTI_08_27 = 'sancti:08-27:3:w'
SANCTI_08_28 = 'sancti:08-28:3:r'
SANCTI_08_29 = 'sancti:08-29:3:r'
SANCTI_08_30 = 'sancti:08-30:3:r'
SANCTI_08_31 = 'sancti:08-31:3:w'

SANCTI_09_01 = 'sancti:09-01:4:w'
SANCTI_09_01PL = 'sancti:09-01pl:3:w'
SANCTI_09_02 = 'sancti:09-02:3:w'
SANCTI_09_03 = 'sancti:09-03r:3:w'
SANCTI_09_05 = 'sancti:09-05:3:w'
SANCTI_09_07PL = 'sancti:09-07pl:3:r'
SANCTI_09_08 = 'sancti:09-08:2:w'  # Nativity of Mary
SANCTI_09_09 = 'sancti:09-09:4:r'
SANCTI_09_10 = 'sancti:09-10:3:w'
SANCTI_09_11 = 'sancti:09-11:4:r'
SANCTI_09_12 = 'sancti:09-12:3:w'
SANCTI_09_14 = 'sancti:09-14:2:r'  # Exaltation of the Cross
SANCTI_09_15 = 'sancti:09-15:2:w'  # The Seven Dolors of the Blessed Virgin Mary
SANCTI_09_16 = 'sancti:09-16:3:r'
SANCTI_09_17 = 'sancti:09-17:4:w'
SANCTI_09_18 = 'sancti:09-18r:3:w'
SANCTI_09_19 = 'sancti:09-19:3:r'
SANCTI_09_20 = 'sancti:09-20:4:r'
SANCTI_09_21 = 'sancti:09-21:2:r'  # St. Matthew, Apostle and Evangelist
SANCTI_09_22 = 'sancti:09-22:3:w'
SANCTI_09_23 = 'sancti:09-23:3:r'
SANCTI_09_24 = 'sancti:09-24:4:w'
SANCTI_09_25PL = 'sancti:09-25pl:3:w'
SANCTI_09_26 = 'sancti:09-26:4:r'
SANCTI_09_27 = 'sancti:09-27:3:r'
SANCTI_09_28 = 'sancti:09-28:3:r'
SANCTI_09_29 = 'sancti:09-29:1:w'  # St. Michael the Archangel
SANCTI_09_30 = 'sancti:09-30r:3:w'

SANCTI_10_01 = 'sancti:10-01:4:w'
SANCTI_10_01PL = 'sancti:10-01pl:3:w'
SANCTI_10_02 = 'sancti:10-02:3:w'
SANCTI_10_03 = 'sancti:10-03:3:w'
SANCTI_10_04 = 'sancti:10-04:3:w'
SANCTI_10_05 = 'sancti:10-05:4:r'
SANCTI_10_06 = 'sancti:10-06:3:w'
SANCTI_10_07 = 'sancti:10-07r:2:w'  # Our Lady of the Rosary
SANCTI_10_08 = 'sancti:10-08r:3:w'
SANCTI_10_09 = 'sancti:10-09:3:w'
SANCTI_10_09PL = 'sancti:10-09pl:3:w'
SANCTI_10_10 = 'sancti:10-10:3:w'
SANCTI_10_10PL = 'sancti:10-10pl:4:w'
SANCTI_10_11 = 'sancti:10-11:2:w'  # Maternity of the Blessed Virgin Mary
SANCTI_10_13 = 'sancti:10-13:3:w'
SANCTI_10_14 = 'sancti:10-14:3:r'
SANCTI_10_15 = 'sancti:10-15:3:w'
SANCTI_10_16 = 'sancti:10-16:3:w'
SANCTI_10_17 = 'sancti:10-17:3:w'
SANCTI_10_18 = 'sancti:10-18:2:r'  # St. Luke, Evangelist
SANCTI_10_19 = 'sancti:10-19:3:w'
SANCTI_10_20 = 'sancti:10-20:3:w'
SANCTI_10_21 = 'sancti:10-21:4:w'
SANCTI_10_21PL = 'sancti:10-21pl:3:w'
SANCTI_10_23 = 'sancti:10-23r:3:w'
SANCTI_10_24 = 'sancti:10-24:3:w'
SANCTI_10_25 = 'sancti:10-25:4:r'
SANCTI_10_28 = 'sancti:10-28:2:r'  # SS. Simon and Jude, Apostles

SANCTI_11_01 = 'sancti:11-01:1:w'  # All Saints
SANCTI_11_02_1 = 'sancti:11-02m1:1:b'  # All Souls' Day
SANCTI_11_02_2 = 'sancti:11-02m2:1:b'
SANCTI_11_02_3 = 'sancti:11-02m3:1:b'
SANCTI_11_04 = 'sancti:11-04r:3:w'
SANCTI_11_08 = 'sancti:11-08r:4:r'
SANCTI_11_09 = 'sancti:11-09:2:w'  # Dedication of the Lateran Basilica in Rome
SANCTI_11_10 = 'sancti:11-10:3:w'
SANCTI_11_11 = 'sancti:11-11:3:w'
SANCTI_11_12 = 'sancti:11-12:3:r'
SANCTI_11_12PL = 'sancti:11-12pl:3:r'
SANCTI_11_13 = 'sancti:11-13:4:w'
SANCTI_11_13PL = 'sancti:11-13pl:2:w'
SANCTI_11_14 = 'sancti:11-14:3:w'
SANCTI_11_15 = 'sancti:11-15:3:w'
SANCTI_11_16 = 'sancti:11-16:3:w'
SANCTI_11_17 = 'sancti:11-17:3:w'
SANCTI_11_17PL = 'sancti:11-17pl:3:w'
SANCTI_11_18 = 'sancti:11-18r:3:w'
SANCTI_11_19 = 'sancti:11-19:3:w'
SANCTI_11_20 = 'sancti:11-20:3:w'
SANCTI_11_20PL = 'sancti:11-20pl:3:r'
SANCTI_11_21 = 'sancti:11-21:3:w'
SANCTI_11_22 = 'sancti:11-22:3:r'
SANCTI_11_23 = 'sancti:11-23:3:r'
SANCTI_11_24 = 'sancti:11-24:3:w'
SANCTI_11_25 = 'sancti:11-25:3:r'
SANCTI_11_26 = 'sancti:11-26:3:w'
SANCTI_11_29 = 'sancti:11-29r:4:r'
SANCTI_11_30 = 'sancti:11-30:2:r'  # St. Andrew, Apostle

SANCTI_12_02 = 'sancti:12-02:3:r'
SANCTI_12_02PL = 'sancti:12-02pl:3:w'
SANCTI_12_03 = 'sancti:12-03:3:w'
SANCTI_12_04 = 'sancti:12-04:3:w'
SANCTI_12_04PL = 'sancti:12-04pl:3:r'
SANCTI_12_05 = 'sancti:12-05:4:w'
SANCTI_12_06 = 'sancti:12-06:3:w'
SANCTI_12_07 = 'sancti:12-07:3:w'
SANCTI_12_08 = 'sancti:12-08:1:w'  # Immaculate Conception of the Blessed Virgin Mary
SANCTI_12_10 = 'sancti:12-10:4:r'
SANCTI_12_11 = 'sancti:12-11:3:w'
SANCTI_12_13 = 'sancti:12-13r:3:r'
SANCTI_12_16 = 'sancti:12-16:3:r'
SANCTI_12_21 = 'sancti:12-21:2:r'  # St. Thomas, Apostle
SANCTI_12_24 = 'sancti:12-24:1:v'  # Vigil of the Nativity of the Lord
SANCTI_12_25_1 = 'sancti:12-25m1:1:w'  # Nativity of the Lord
SANCTI_12_25_2 = 'sancti:12-25m2:1:w'
SANCTI_12_25_3 = 'sancti:12-25m3:1:w'
SANCTI_12_26 = 'sancti:12-26:2:r'  # St. Stephen, Protomartyr
SANCTI_12_27 = 'sancti:12-27:2:w'  # St. John, Apostle and Evangelist
SANCTI_12_28 = 'sancti:12-28:2:r'  # Holy Innocents
SANCTI_12_29 = 'sancti:12-29r:4:r'
SANCTI_12_31 = 'sancti:12-31r:4:w'

# COMMUNE / VOTIVE
COMMUNE_C5 = 'commune:C5:0:w'  # Os iusti
COMMUNE_C5B = 'commune:C5b:0:w'  # Iustus ut palma
COMMUNE_C2C = 'commune:C2c:0:r'  # Statuit
COMMUNE_C2B = 'commune:C2b:0:r'  # Sacerdotes Dei
COMMUNE_C_10A = 'commune:C10a:0:w'  # B. V. M. Saturdays in Advent
COMMUNE_C_10B = 'commune:C10b:0:w'  # B. V. M. Saturdays between Nativity and Purification
COMMUNE_C_10C = 'commune:C10c:0:w'  # B. V. M. Saturdays between Feb 2 and Wednesday in Holy Week
COMMUNE_C_10PASC = 'commune:C10Pasc:0:w'  # B. V. M. Saturdays in Easter period
COMMUNE_C_10T = 'commune:C10t:0:w'  # B. V. M. Saturdays between Trinity Sunday and Saturday before 1st Sunday of Advent
VOTIVE_PENT01_0 = 'votive:Pent01-0r:0:w'  # Trinity
VOTIVE_PENT02_5 = 'votive:Pent02-5:0:w'  # Sacred Heart of Jesus
VOTIVE_08_22 = 'votive:08-22r:0:w'  # Immaculate Heart of B. V. M.
VOTIVE_ANGELS = 'votive:Angels:0:w'
VOTIVE_JOSEPH = 'votive:Joseph:0:w'
VOTIVE_PETERPAUL = 'votive:PeterPaul:0:r'
VOTIVE_PETERPAULP = 'votive:PeterPaulP:0:r'
VOTIVE_APOSTLES = 'votive:Apostles:0:r'
VOTIVE_APOSTLESP = 'votive:ApostlesP:0:r'
VOTIVE_HOLYSPIRIT = 'votive:HolySpirit:0:r'
VOTIVE_HOLYSPIRIT2 = 'votive:HolySpirit2:0:r'
VOTIVE_BLESSEDSACRAMENT = 'votive:BlessedSacrament:0:w'
VOTIVE_JESUSETERNALPRIEST = 'votive:JesusEternalPriest:0:w'
VOTIVE_CROSS = 'votive:Cross:0:r'
VOTIVE_PASSION = 'votive:Passion:0:r'
VOTIVE_DEFUNCTORUM = 'votive:Defunctorum:0:b'
VOTIVE_MORTALITATIS = 'votive:TemporeMortalitatis:0:v'
VOTIVE_FIDEI_PROPAGATIONE = 'votive:FideiPropagatione:0:v'
VOTIVE_MATRIMONIUM = 'votive:Matrimonium:0:w'
VOTIVE_TERRIBILIS = 'votive:Terribilis:0:w'

EMBER_DAYS = (
    TEMPORA_QUAD1_3,  # Ember Wednesday of Lent
    TEMPORA_QUAD1_5,  # Ember Friday of Lent
    TEMPORA_QUAD1_6,  # Ember Saturday of Lent
    TEMPORA_PENT_3,  # Ember Wednesday in September
    TEMPORA_PENT_5,  # Ember Friday in September
    TEMPORA_PENT_6,  # Ember Saturday in September
    TEMPORA_ADV3_3,  # Ember Wednesday in Advent
    TEMPORA_ADV3_5,  # Ember Friday in Advent
    TEMPORA_ADV3_6,  # Ember Saturday in Advent
)
TABLE_OF_PRECEDENCE = (
    # 1st class feasts
    SANCTI_12_25_1,  # Nativity
    SANCTI_12_25_2,  # Nativity
    SANCTI_12_25_3,  # Nativity
    TEMPORA_PASC0_0,  # Resurrection Sunday
    TEMPORA_PASC7_0,  # Pentecost
    TEMPORA_QUAD6_4,  # Maundy Thursday
    TEMPORA_QUAD6_5,  # Good Friday
    TEMPORA_QUAD6_6,  # Holy Saturday
    SANCTI_01_06,  # Epiphany
    TEMPORA_PASC5_4,  # Ascension
    TEMPORA_PENT01_0,  # Trinity Sunday
    TEMPORA_PENT01_4,  # Corpus Christi
    TEMPORA_PENT02_5,  # Feast of the Sacred Heart
    SANCTI_10_DU,  # Feast of Christ the King; last Sunday of October
    SANCTI_12_08,  # Immaculate Conception of the Blessed Virgin Mary
    SANCTI_08_15,  # Assumption of Mary
    SANCTI_12_24,  # Vigil of the Nativity of the Lord
    SANCTI_01_01,  # Octave of the Nativity
    PATTERN_ADVENT_SUNDAY,
    PATTERN_LENT_SUNDAY,
    TEMPORA_PASC1_0,  # Low Sunday
    TEMPORA_QUADP3_3,  # Ash Wednesday
    TEMPORA_QUAD6_1,  # Monday of Holy Week
    TEMPORA_QUAD6_2,  # Tuesday of Holy Week
    TEMPORA_QUAD6_3,  # Wednesday of Holy Week
    SANCTI_11_02_1,  # All Souls' Day
    SANCTI_11_02_2,  # All Souls' Day
    SANCTI_11_02_3,  # All Souls' Day
    TEMPORA_PASC6_6,  # Vigil of Pentecost
    TEMPORA_PASC0_1,  # Resurrection Octave
    TEMPORA_PASC0_2,
    TEMPORA_PASC0_3,
    TEMPORA_PASC0_4,
    TEMPORA_PASC0_5,
    TEMPORA_PASC0_6,
    TEMPORA_PASC7_1,  # Pentecost Octave
    TEMPORA_PASC7_2,
    TEMPORA_PASC7_3,
    TEMPORA_PASC7_4,
    TEMPORA_PASC7_5,
    TEMPORA_PASC7_6,
    PATTERN_CLASS_1,
    # 2nd class feasts
    TEMPORA_PASC5_3,  # Vigil of Ascension
    SANCTI_01_13,  # Baptism of the Lord
    SANCTI_08_06, # Transfiguration
    PATTERN_TEMPORA_SUNDAY_CLASS_2,
    PATTERN_CLASS_2,
    SANCTI_12_26,  # Octave of Nativity
    SANCTI_12_27,
    SANCTI_12_28,
    SANCTI_12_29,
    SANCTI_12_31,
    # 3rd class feasts
    TEMPORA_QUAD1_1,  # Feria in Lent (except Ember Days)
    TEMPORA_QUAD1_2,
    TEMPORA_QUAD1_4,
    TEMPORA_QUAD2_1,
    TEMPORA_QUAD2_2,
    TEMPORA_QUAD2_3,
    TEMPORA_QUAD2_4,
    TEMPORA_QUAD2_5,
    TEMPORA_QUAD2_6,
    TEMPORA_QUAD3_1,
    TEMPORA_QUAD3_2,
    TEMPORA_QUAD3_3,
    TEMPORA_QUAD3_4,
    TEMPORA_QUAD3_5,
    TEMPORA_QUAD3_6,
    TEMPORA_QUAD4_1,
    TEMPORA_QUAD4_2,
    TEMPORA_QUAD4_3,
    TEMPORA_QUAD4_4,
    TEMPORA_QUAD4_5,
    TEMPORA_QUAD4_6,
    TEMPORA_QUAD5_1,
    TEMPORA_QUAD5_2,
    TEMPORA_QUAD5_3,
    TEMPORA_QUAD5_4,
    TEMPORA_QUAD5_5,
    TEMPORA_QUAD5_6,
    PATTERN_CLASS_3,
    # 4th class feasts
    '.*'
)

FEASTS_OF_JESUS_CLASS_1_AND_2 = (
    SANCTI_01_06,
    SANCTI_01_13,
    SANCTI_02_02,
    SANCTI_08_06,
)


# Related to propers' printing

COMMEMORATION_SECTIONS = [
    COMMEMORATED_ORATIO,
    COMMEMORATED_SECRETA,
    COMMEMORATED_POSTCOMMUNIO,
]

# This list contains tuples consisting of a proper ID and a list of sections that should be excluded from given proper.
# E.g. some propers contain commemorations in their source, but they should never be exposed as they are not part of
# 1962 issue of the  Missal. Asterisk (*) means that given section should always be excluded.
EXCLUDE_SECTIONS = (
    (SANCTI_06_25, COMMEMORATION_SECTIONS),
    (SANCTI_06_26, COMMEMORATION_SECTIONS),
    (SANCTI_06_30, COMMEMORATION_SECTIONS),
    (SANCTI_07_01, COMMEMORATION_SECTIONS),
    (SANCTI_07_05, COMMEMORATION_SECTIONS),
    (SANCTI_08_06, COMMEMORATION_SECTIONS),
    (SANCTI_08_17, COMMEMORATION_SECTIONS),
    (SANCTI_08_19, COMMEMORATION_SECTIONS),
    (SANCTI_08_20, COMMEMORATION_SECTIONS),
    (SANCTI_08_21, COMMEMORATION_SECTIONS),
    (SANCTI_09_14, COMMEMORATION_SECTIONS),
    (SANCTI_12_07, COMMEMORATION_SECTIONS),
    (SANCTI_12_11, COMMEMORATION_SECTIONS),
    (TEMPORA_EPI1_0, COMMEMORATION_SECTIONS),
    (TEMPORA_PENT02_0, COMMEMORATION_SECTIONS),
    (TEMPORA_PENT03_0, COMMEMORATION_SECTIONS),
    (TEMPORA_PASC5_3, COMMEMORATION_SECTIONS),
    (TEMPORA_PASC6_0, COMMEMORATION_SECTIONS),
    (TEMPORA_PENT02_0, ['Sequentia']),
    (TEMPORA_PENT01_0, COMMEMORATION_SECTIONS)
)

# EXCLUDE_SECTIONS organized by section ID
EXCLUDE_SECTIONS_IDX = defaultdict(set)
for id_, sections in EXCLUDE_SECTIONS:
    for section in sections:
        EXCLUDE_SECTIONS_IDX[section].add(id_)


# Earlier prefaces takes precedence.
CUSTOM_PREFACES = (
    (SANCTI_01_01, PREFATIO_NAT),
    (SANCTI_01_06, PREFATIO_EPI),
    (SANCTI_11_09, PREFATIO_COMMUNIS),  # Consecration of basilica in Lateran
    (SANCTI_11_18, PREFATIO_COMMUNIS),  # Consecration of basilica of Peter and Paul
    (SANCTI_07_25, PREFATIO_APOSTOLIS),  # st. James, the Apostle
    (SANCTI_12_21, PREFATIO_APOSTOLIS),  # st. Thomas, the Apostle
    (SANCTI_05_11, PREFATIO_APOSTOLIS),  # Sts. Philip and James
    (SANCTI_06_24, PREFATIO_COMMUNIS),  # St. John the Baptist
    (PATTERN_ADVENT_FERIA, PREFATIO_COMMUNIS),
    (PATTERN_ADVENT_SUNDAY, PREFATIO_TRINITATE),
    (PATTERN_EASTER_PREFATIO, PREFATIO_PASCHAL),
    (TEMPORA_QUAD6_5, PREFATIO_OMIT),
    (PATTERN_LENT_PREFATIO, PREFATIO_LENT),  # Lent until Saturday before Passion Sunday
    (PATTERN_ASCENSION_PREFATIO, PREFATIO_ASCENSION),  # From Ascension Sunday till Friday before Pentecost Vigil,
    (VOTIVE_TERRIBILIS, PREFATIO_COMMUNIS),
)

CUSTOM_INTER_READING_SECTIONS = {
    SANCTI_04_28: GRADUALE,
    SANCTI_05_02: GRADUALE

}

OBSERVANCES_WITHOUT_OWN_PROPER = (
    # Advent feria except Ember Days
    re.compile(r'tempora:Adv[124]-[1-6]'),
    re.compile(r'tempora:Adv[3]-[124]'),
)

REFERENCE_REGEX = re.compile(r'^@([\w/\-]*):?([^:]*)[: ]*(.*)')
SECTION_REGEX = re.compile(r'^### *([\w\d ]*).*')
