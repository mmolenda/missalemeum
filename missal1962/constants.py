import os
import re

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

LANGUAGE_LATIN = 'Latin'
TYPE_TEMPORA = 'tempora'
TYPE_SANCTI = 'sancti'

PATTERN_TEMPORA = re.compile(r'^tempora:.*')
PATTERN_ADVENT = re.compile(r'^tempora:Adv\d')
PATTERN_EASTER = re.compile(r'^tempora:Pasc\d')
PATTERN_ADVENT_SUNDAY = re.compile(r'^tempora:Adv\d-0')
PATTERN_ADVENT_FERIA = re.compile('tempora:Adv\d-[1-6]')
PATTERN_ADVENT_FERIA_BETWEEN_17_AND_23 = re.compile('tempora:Adv\d-[1-6]:2')
PATTERN_ADVENT_FERIA_BEFORE_17 = re.compile('tempora:Adv\d-[1-6]:3')
PATTERN_LENT_SUNDAY = re.compile(r'^tempora:Quad\d-0.*')
PATTERN_TEMPORA_SUNDAY = re.compile(r'^tempora:.*-0r*:\d$')
PATTERN_TEMPORA_SUNDAY_CLASS_1 = re.compile(r'^tempora:.*-0r*:1$')
PATTERN_TEMPORA_SUNDAY_CLASS_2 = re.compile(r'^tempora:.*-0r*:2$')
PATTERN_TEMPORA_CLASS_1 = re.compile(r'^tempora:.*:1$')
PATTERN_TEMPORA_CLASS_2 = re.compile(r'^tempora:.*:2$')
PATTERN_TEMPORA_CLASS_3 = re.compile(r'^tempora:.*:3$')
PATTERN_SANCTI_CLASS_1 = re.compile(r'^sancti:.*:1$')
PATTERN_SANCTI_CLASS_2 = re.compile(r'^sancti:.*:2$')
PATTERN_SANCTI_CLASS_3 = re.compile(r'^sancti:.*:3$')
PATTERN_SANCTI_CLASS_1_OR_2 = re.compile(r'^sancti:.*:[12]$')
PATTERN_CLASS_1 = re.compile(r'^[a-z]+:.*:1$')
PATTERN_CLASS_2 = re.compile(r'^[a-z]+:.*:2$')
PATTERN_CLASS_3 = re.compile(r'^[a-z]+:.*:3$')
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
    '10-DUr': 6  # The Feast of Christ the King, last Sunday of October.
}

VISIBLE_SECTIONS = [
    'Comment',
    'De Benedictione Candelarum',  # 02-02, feast of the Purification of the B.V.M.
    'De Distributione Candelarum',  # 02-02, feast of the Purification of the B.V.M.
    'De Processione',  # 02-02, feast of the Purification of the B.V.M.
    'Prelude',
    'Introitus',
    'Oratio',
    'OratioL1',
    'OratioL2',
    'OratioL3',
    'OratioL4',
    'OratioL5',
    'Commemoratio Oratio',
    'Lectio',
    'LectioL1',
    'LectioL2',
    'LectioL3',
    'LectioL4',
    'LectioL5',
    'Graduale',
    'GradualeP',
    'GradualeL1',
    'GradualeL2',
    'GradualeL3',
    'GradualeL4',
    'GradualeL5',
    'Tractus',
    'Sequentia',
    'Evangelium',
    'Offertorium',
    'OffertoriumP',
    'Secreta',
    'Commemoratio Secreta',
    'Prefatio',
    'Communicantes',
    'Communio',
    'CommunioP',
    'Postcommunio',
    'Commemoratio Postcommunio',
    'Super populum'
]

# TEMPORA - days whose dates are not fixed, but are calculated (in most cases depending on Easter Sunday)

TEMPORA_EPI1_0 = 'tempora:Epi1-0:2'    # Feast of the Holy Family
TEMPORA_EPI1_0A = 'tempora:Epi1-0a:2'  # First Sunday after Epiphany
TEMPORA_EPI1_1 = 'tempora:Epi1-1:4'    # Monday after 1st week of Epiphany
TEMPORA_EPI1_2 = 'tempora:Epi1-2:4'    # Tuesday after 1st week of Epiphany
TEMPORA_EPI1_3 = 'tempora:Epi1-3:4'    # Wednesday after 1st week of Epiphany
TEMPORA_EPI1_4 = 'tempora:Epi1-4:4'    # Thursday after 1st week of Epiphany
TEMPORA_EPI1_5 = 'tempora:Epi1-5:4'    # Friday after 1st week of Epiphany
TEMPORA_EPI1_6 = 'tempora:Epi1-6:4'    # Saturday after 1st week of Epiphany
TEMPORA_EPI2_0 = 'tempora:Epi2-0:2'    # Sunday after 2nd week of Epiphany
TEMPORA_EPI2_1 = 'tempora:Epi2-1:4'    # Monday after 2nd week of Epiphany
TEMPORA_EPI2_2 = 'tempora:Epi2-2:4'
TEMPORA_EPI2_3 = 'tempora:Epi2-3:4'
TEMPORA_EPI2_4 = 'tempora:Epi2-4:4'
TEMPORA_EPI2_5 = 'tempora:Epi2-5:4'
TEMPORA_EPI2_6 = 'tempora:Epi2-6:4'
TEMPORA_EPI3_0 = 'tempora:Epi3-0:2'
TEMPORA_EPI3_1 = 'tempora:Epi3-1:4'
TEMPORA_EPI3_2 = 'tempora:Epi3-2:4'
TEMPORA_EPI3_3 = 'tempora:Epi3-3:4'
TEMPORA_EPI3_4 = 'tempora:Epi3-4:4'
TEMPORA_EPI3_5 = 'tempora:Epi3-5:4'
TEMPORA_EPI3_6 = 'tempora:Epi3-6:4'
TEMPORA_EPI4_0 = 'tempora:Epi4-0:2'
TEMPORA_EPI4_1 = 'tempora:Epi4-1:4'
TEMPORA_EPI4_2 = 'tempora:Epi4-2:4'
TEMPORA_EPI4_3 = 'tempora:Epi4-3:4'
TEMPORA_EPI4_4 = 'tempora:Epi4-4:4'
TEMPORA_EPI4_5 = 'tempora:Epi4-5:4'
TEMPORA_EPI4_6 = 'tempora:Epi4-6:4'
TEMPORA_EPI5_0 = 'tempora:Epi5-0:2'
TEMPORA_EPI5_1 = 'tempora:Epi5-1:4'
TEMPORA_EPI5_2 = 'tempora:Epi5-2:4'
TEMPORA_EPI5_3 = 'tempora:Epi5-3:4'
TEMPORA_EPI5_4 = 'tempora:Epi5-4:4'
TEMPORA_EPI5_5 = 'tempora:Epi5-5:4'
TEMPORA_EPI5_6 = 'tempora:Epi5-6:4'
TEMPORA_EPI6_0 = 'tempora:Epi6-0:2'
TEMPORA_EPI6_1 = 'tempora:Epi6-1:4'
TEMPORA_EPI6_2 = 'tempora:Epi6-2:4'
TEMPORA_EPI6_3 = 'tempora:Epi6-3:4'
TEMPORA_EPI6_4 = 'tempora:Epi6-4:4'
TEMPORA_EPI6_5 = 'tempora:Epi6-5:4'
TEMPORA_EPI6_6 = 'tempora:Epi6-6:4'

TEMPORA_QUADP1_0 = 'tempora:Quadp1-0:2'  # Septuagesima Sunday
TEMPORA_QUADP1_1 = 'tempora:Quadp1-1:4'
TEMPORA_QUADP1_2 = 'tempora:Quadp1-2:4'
TEMPORA_QUADP1_3 = 'tempora:Quadp1-3:4'
TEMPORA_QUADP1_4 = 'tempora:Quadp1-4:4'
TEMPORA_QUADP1_5 = 'tempora:Quadp1-5:4'
TEMPORA_QUADP1_6 = 'tempora:Quadp1-6:4'
TEMPORA_QUADP2_0 = 'tempora:Quadp2-0:2'  # Sexagesima Sunday
TEMPORA_QUADP2_1 = 'tempora:Quadp2-1:4'
TEMPORA_QUADP2_2 = 'tempora:Quadp2-2:4'
TEMPORA_QUADP2_3 = 'tempora:Quadp2-3:4'
TEMPORA_QUADP2_4 = 'tempora:Quadp2-4:4'
TEMPORA_QUADP2_5 = 'tempora:Quadp2-5:4'
TEMPORA_QUADP2_6 = 'tempora:Quadp2-6:4'
TEMPORA_QUADP3_0 = 'tempora:Quadp3-0:2'  # Quinquagesima Sunday
TEMPORA_QUADP3_1 = 'tempora:Quadp3-1:4'
TEMPORA_QUADP3_2 = 'tempora:Quadp3-2:4'

TEMPORA_QUADP3_3 = 'tempora:Quadp3-3:1'  # Ash Wednesday
TEMPORA_QUADP3_4 = 'tempora:Quadp3-4:3'
TEMPORA_QUADP3_5 = 'tempora:Quadp3-5:3'
TEMPORA_QUADP3_6 = 'tempora:Quadp3-6:3'
TEMPORA_QUAD1_0 = 'tempora:Quad1-0:1'  # Sunday in 1st week of Lent
TEMPORA_QUAD1_1 = 'tempora:Quad1-1:3'  # Monday in 1st week of Lent
TEMPORA_QUAD1_2 = 'tempora:Quad1-2:3'  # Tuesday in 1st week of Lent
TEMPORA_QUAD1_3 = 'tempora:Quad1-3:2'  # Ember Wednesday of Lent
TEMPORA_QUAD1_4 = 'tempora:Quad1-4:3'  # Thursday in 1st week of Lent
TEMPORA_QUAD1_5 = 'tempora:Quad1-5:2'  # Ember Friday of Lent
TEMPORA_QUAD1_6 = 'tempora:Quad1-6:2'  # Ember Saturday of Lent
TEMPORA_QUAD2_0 = 'tempora:Quad2-0:1'  # Sunday in 2nd week of Lent
TEMPORA_QUAD2_1 = 'tempora:Quad2-1:3'  # Monday in 2nd week of Lent
TEMPORA_QUAD2_2 = 'tempora:Quad2-2:3'
TEMPORA_QUAD2_3 = 'tempora:Quad2-3:3'
TEMPORA_QUAD2_4 = 'tempora:Quad2-4:3'
TEMPORA_QUAD2_5 = 'tempora:Quad2-5:3'
TEMPORA_QUAD2_6 = 'tempora:Quad2-6:3'
TEMPORA_QUAD3_0 = 'tempora:Quad3-0:1'
TEMPORA_QUAD3_1 = 'tempora:Quad3-1:3'
TEMPORA_QUAD3_2 = 'tempora:Quad3-2:3'
TEMPORA_QUAD3_3 = 'tempora:Quad3-3:3'
TEMPORA_QUAD3_4 = 'tempora:Quad3-4:3'
TEMPORA_QUAD3_5 = 'tempora:Quad3-5:3'
TEMPORA_QUAD3_6 = 'tempora:Quad3-6:3'
TEMPORA_QUAD4_0 = 'tempora:Quad4-0:1'
TEMPORA_QUAD4_1 = 'tempora:Quad4-1:3'
TEMPORA_QUAD4_2 = 'tempora:Quad4-2:3'
TEMPORA_QUAD4_3 = 'tempora:Quad4-3:3'
TEMPORA_QUAD4_4 = 'tempora:Quad4-4:3'
TEMPORA_QUAD4_5 = 'tempora:Quad4-5:3'
TEMPORA_QUAD4_6 = 'tempora:Quad4-6:3'
TEMPORA_QUAD5_0 = 'tempora:Quad5-0:1'  # 1st Passion Sunday
TEMPORA_QUAD5_1 = 'tempora:Quad5-1:3'
TEMPORA_QUAD5_2 = 'tempora:Quad5-2:3'
TEMPORA_QUAD5_3 = 'tempora:Quad5-3:3'
TEMPORA_QUAD5_4 = 'tempora:Quad5-4:3'
TEMPORA_QUAD5_5 = 'tempora:Quad5-5Feria:3'
TEMPORA_QUAD5_6 = 'tempora:Quad5-6:3'
TEMPORA_QUAD6_0 = 'tempora:Quad6-0r:1'  # 2nd Passion Sunday (Palm Sunday)
TEMPORA_QUAD6_1 = 'tempora:Quad6-1:1'
TEMPORA_QUAD6_2 = 'tempora:Quad6-2:1'
TEMPORA_QUAD6_3 = 'tempora:Quad6-3:1'
TEMPORA_QUAD6_4 = 'tempora:Quad6-4r:1'  # Maundy Thursday
TEMPORA_QUAD6_5 = 'tempora:Quad6-5r:1'  # Good Friday
TEMPORA_QUAD6_6 = 'tempora:Quad6-6r:1'  # Holy Saturday
#
TEMPORA_PASC0_0 = 'tempora:Pasc0-0:1'  # Resurrection Sunday
TEMPORA_PASC0_1 = 'tempora:Pasc0-1:1'
TEMPORA_PASC0_2 = 'tempora:Pasc0-2:1'
TEMPORA_PASC0_3 = 'tempora:Pasc0-3:1'
TEMPORA_PASC0_4 = 'tempora:Pasc0-4:1'
TEMPORA_PASC0_5 = 'tempora:Pasc0-5:1'
TEMPORA_PASC0_6 = 'tempora:Pasc0-6:1'
TEMPORA_PASC1_0 = 'tempora:Pasc1-0:1'  # Low Sunday
TEMPORA_PASC1_1 = 'tempora:Pasc1-1:4'
TEMPORA_PASC1_2 = 'tempora:Pasc1-2:4'
TEMPORA_PASC1_3 = 'tempora:Pasc1-3:4'
TEMPORA_PASC1_4 = 'tempora:Pasc1-4:4'
TEMPORA_PASC1_5 = 'tempora:Pasc1-5:4'
TEMPORA_PASC1_6 = 'tempora:Pasc1-6:4'
TEMPORA_PASC2_0 = 'tempora:Pasc2-0:2'
TEMPORA_PASC2_1 = 'tempora:Pasc2-1:4'
TEMPORA_PASC2_2 = 'tempora:Pasc2-2:4'
TEMPORA_PASC2_3 = 'tempora:Pasc2-3Feria:4'
TEMPORA_PASC2_4 = 'tempora:Pasc2-4Feria:4'
TEMPORA_PASC2_5 = 'tempora:Pasc2-5Feria:4'
TEMPORA_PASC2_6 = 'tempora:Pasc2-6Feria:4'
TEMPORA_PASC3_0 = 'tempora:Pasc3-0r:2'
TEMPORA_PASC3_1 = 'tempora:Pasc3-1Feria:4'
TEMPORA_PASC3_2 = 'tempora:Pasc3-2Feria:4'
TEMPORA_PASC3_3 = 'tempora:Pasc3-3Feria:4'
TEMPORA_PASC3_4 = 'tempora:Pasc3-4:4'
TEMPORA_PASC3_5 = 'tempora:Pasc3-5:4'
TEMPORA_PASC3_6 = 'tempora:Pasc3-6:4'
TEMPORA_PASC4_0 = 'tempora:Pasc4-0:2'
TEMPORA_PASC4_1 = 'tempora:Pasc4-1:4'
TEMPORA_PASC4_2 = 'tempora:Pasc4-2:4'
TEMPORA_PASC4_3 = 'tempora:Pasc4-3:4'
TEMPORA_PASC4_4 = 'tempora:Pasc4-4:4'
TEMPORA_PASC4_5 = 'tempora:Pasc4-5:4'
TEMPORA_PASC4_6 = 'tempora:Pasc4-6:4'
TEMPORA_PASC5_0 = 'tempora:Pasc5-0:2'
TEMPORA_PASC5_1 = 'tempora:Pasc5-1:4'
TEMPORA_PASC5_2 = 'tempora:Pasc5-2:4'
TEMPORA_PASC5_3 = 'tempora:Pasc5-3:2'  # Vigil of Ascension
#
TEMPORA_PASC5_4 = 'tempora:Pasc5-4:1'  # Ascension
TEMPORA_PASC5_5 = 'tempora:Pasc5-5:4'
TEMPORA_PASC5_6 = 'tempora:Pasc5-6:4'
TEMPORA_PASC6_0 = 'tempora:Pasc6-0:2'
TEMPORA_PASC6_1 = 'tempora:Pasc6-1:4'
TEMPORA_PASC6_2 = 'tempora:Pasc6-2:4'
TEMPORA_PASC6_3 = 'tempora:Pasc6-3:4'
TEMPORA_PASC6_4 = 'tempora:Pasc6-4r:4'
TEMPORA_PASC6_5 = 'tempora:Pasc6-5:4'
TEMPORA_PASC6_6 = 'tempora:Pasc6-6:1'  # Vigil of Pentecost
#
TEMPORA_PASC7_0 = 'tempora:Pasc7-0:1'  # Pentecost
TEMPORA_PASC7_1 = 'tempora:Pasc7-1:1'  # Whit Monday
TEMPORA_PASC7_2 = 'tempora:Pasc7-2:1'
TEMPORA_PASC7_3 = 'tempora:Pasc7-3:1'  # Ember Wednesday in Octave of Pentecost
TEMPORA_PASC7_4 = 'tempora:Pasc7-4:1'
TEMPORA_PASC7_5 = 'tempora:Pasc7-5:1'  # Ember Friday in Octave of Pentecost
TEMPORA_PASC7_6 = 'tempora:Pasc7-6:1'  # Ember Saturday in Octave of Pentecost
TEMPORA_PENT01_0 = 'tempora:Pent01-0r:1'  # Trinity Sunday
TEMPORA_PENT01_1 = 'tempora:Pent01-1:4'
TEMPORA_PENT01_2 = 'tempora:Pent01-2:4'
TEMPORA_PENT01_3 = 'tempora:Pent01-3:4'
TEMPORA_PENT01_4 = 'tempora:Pent01-4:1'  # Corpus Christi
TEMPORA_PENT01_5 = 'tempora:Pent01-5:4'
TEMPORA_PENT01_6 = 'tempora:Pent01-6:4'
TEMPORA_PENT02_0 = 'tempora:Pent02-0r:2'  # Sunday in 2nd week after Pentecost
TEMPORA_PENT02_1 = 'tempora:Pent02-1:4'  # Monday in 2nd week after Pentecost
TEMPORA_PENT02_2 = 'tempora:Pent02-2:4'  # Tuesday in 2nd week after Pentecost
TEMPORA_PENT02_3 = 'tempora:Pent02-3:4'  # Wednesday in 2nd week after Pentecost
TEMPORA_PENT02_4 = 'tempora:Pent02-4:4'  # Thursday in 2nd week after Pentecost
TEMPORA_PENT02_5 = 'tempora:Pent02-5:1'  # Feast of the Sacred Heart
TEMPORA_PENT02_6 = 'tempora:Pent02-6Feria:4'  # Saturday in 2nd week after Pentecost
TEMPORA_PENT03_0 = 'tempora:Pent03-0r:2'  # Sunday in 3rd week after Pentecost
TEMPORA_PENT03_1 = 'tempora:Pent03-1Feria:4'
TEMPORA_PENT03_2 = 'tempora:Pent03-2Feria:4'
TEMPORA_PENT03_3 = 'tempora:Pent03-3Feria:4'
TEMPORA_PENT03_4 = 'tempora:Pent03-4Feria:4'
TEMPORA_PENT03_5 = 'tempora:Pent03-5Feria:4'
TEMPORA_PENT03_6 = 'tempora:Pent03-6:4'
TEMPORA_PENT04_0 = 'tempora:Pent04-0:2'
TEMPORA_PENT04_1 = 'tempora:Pent04-1:4'
TEMPORA_PENT04_2 = 'tempora:Pent04-2:4'
TEMPORA_PENT04_3 = 'tempora:Pent04-3:4'
TEMPORA_PENT04_4 = 'tempora:Pent04-4:4'
TEMPORA_PENT04_5 = 'tempora:Pent04-5:4'
TEMPORA_PENT04_6 = 'tempora:Pent04-6:4'
TEMPORA_PENT05_0 = 'tempora:Pent05-0:2'
TEMPORA_PENT05_1 = 'tempora:Pent05-1:4'
TEMPORA_PENT05_2 = 'tempora:Pent05-2:4'
TEMPORA_PENT05_3 = 'tempora:Pent05-3:4'
TEMPORA_PENT05_4 = 'tempora:Pent05-4:4'
TEMPORA_PENT05_5 = 'tempora:Pent05-5:4'
TEMPORA_PENT05_6 = 'tempora:Pent05-6:4'
TEMPORA_PENT06_0 = 'tempora:Pent06-0:2'
TEMPORA_PENT06_1 = 'tempora:Pent06-1:4'
TEMPORA_PENT06_2 = 'tempora:Pent06-2:4'
TEMPORA_PENT06_3 = 'tempora:Pent06-3:4'
TEMPORA_PENT06_4 = 'tempora:Pent06-4:4'
TEMPORA_PENT06_5 = 'tempora:Pent06-5:4'
TEMPORA_PENT06_6 = 'tempora:Pent06-6:4'
TEMPORA_PENT07_0 = 'tempora:Pent07-0:2'
TEMPORA_PENT07_1 = 'tempora:Pent07-1:4'
TEMPORA_PENT07_2 = 'tempora:Pent07-2:4'
TEMPORA_PENT07_3 = 'tempora:Pent07-3:4'
TEMPORA_PENT07_4 = 'tempora:Pent07-4:4'
TEMPORA_PENT07_5 = 'tempora:Pent07-5:4'
TEMPORA_PENT07_6 = 'tempora:Pent07-6:4'
TEMPORA_PENT08_0 = 'tempora:Pent08-0:2'
TEMPORA_PENT08_1 = 'tempora:Pent08-1:4'
TEMPORA_PENT08_2 = 'tempora:Pent08-2:4'
TEMPORA_PENT08_3 = 'tempora:Pent08-3:4'
TEMPORA_PENT08_4 = 'tempora:Pent08-4:4'
TEMPORA_PENT08_5 = 'tempora:Pent08-5:4'
TEMPORA_PENT08_6 = 'tempora:Pent08-6:4'
TEMPORA_PENT09_0 = 'tempora:Pent09-0:2'
TEMPORA_PENT09_1 = 'tempora:Pent09-1:4'
TEMPORA_PENT09_2 = 'tempora:Pent09-2:4'
TEMPORA_PENT09_3 = 'tempora:Pent09-3:4'
TEMPORA_PENT09_4 = 'tempora:Pent09-4:4'
TEMPORA_PENT09_5 = 'tempora:Pent09-5:4'
TEMPORA_PENT09_6 = 'tempora:Pent09-6:4'
TEMPORA_PENT10_0 = 'tempora:Pent10-0:2'
TEMPORA_PENT10_1 = 'tempora:Pent10-1:4'
TEMPORA_PENT10_2 = 'tempora:Pent10-2:4'
TEMPORA_PENT10_3 = 'tempora:Pent10-3:4'
TEMPORA_PENT10_4 = 'tempora:Pent10-4:4'
TEMPORA_PENT10_5 = 'tempora:Pent10-5:4'
TEMPORA_PENT10_6 = 'tempora:Pent10-6:4'
TEMPORA_PENT11_0 = 'tempora:Pent11-0:2'
TEMPORA_PENT11_1 = 'tempora:Pent11-1:4'
TEMPORA_PENT11_2 = 'tempora:Pent11-2:4'
TEMPORA_PENT11_3 = 'tempora:Pent11-3:4'
TEMPORA_PENT11_4 = 'tempora:Pent11-4:4'
TEMPORA_PENT11_5 = 'tempora:Pent11-5:4'
TEMPORA_PENT11_6 = 'tempora:Pent11-6:4'
TEMPORA_PENT12_0 = 'tempora:Pent12-0:2'
TEMPORA_PENT12_1 = 'tempora:Pent12-1:4'
TEMPORA_PENT12_2 = 'tempora:Pent12-2:4'
TEMPORA_PENT12_3 = 'tempora:Pent12-3:4'
TEMPORA_PENT12_4 = 'tempora:Pent12-4:4'
TEMPORA_PENT12_5 = 'tempora:Pent12-5:4'
TEMPORA_PENT12_6 = 'tempora:Pent12-6:4'
TEMPORA_PENT13_0 = 'tempora:Pent13-0:2'
TEMPORA_PENT13_1 = 'tempora:Pent13-1:4'
TEMPORA_PENT13_2 = 'tempora:Pent13-2:4'
TEMPORA_PENT13_3 = 'tempora:Pent13-3:4'
TEMPORA_PENT13_4 = 'tempora:Pent13-4:4'
TEMPORA_PENT13_5 = 'tempora:Pent13-5:4'
TEMPORA_PENT13_6 = 'tempora:Pent13-6:4'
TEMPORA_PENT14_0 = 'tempora:Pent14-0:2'
TEMPORA_PENT14_1 = 'tempora:Pent14-1:4'
TEMPORA_PENT14_2 = 'tempora:Pent14-2:4'
TEMPORA_PENT14_3 = 'tempora:Pent14-3:4'
TEMPORA_PENT14_4 = 'tempora:Pent14-4:4'
TEMPORA_PENT14_5 = 'tempora:Pent14-5:4'
TEMPORA_PENT14_6 = 'tempora:Pent14-6:4'
TEMPORA_PENT15_0 = 'tempora:Pent15-0:2'
TEMPORA_PENT15_1 = 'tempora:Pent15-1:4'
TEMPORA_PENT15_2 = 'tempora:Pent15-2:4'
TEMPORA_PENT15_3 = 'tempora:Pent15-3:4'
TEMPORA_PENT15_4 = 'tempora:Pent15-4:4'
TEMPORA_PENT15_5 = 'tempora:Pent15-5:4'
TEMPORA_PENT15_6 = 'tempora:Pent15-6:4'
TEMPORA_PENT16_0 = 'tempora:Pent16-0:2'
TEMPORA_PENT16_1 = 'tempora:Pent16-1:4'
TEMPORA_PENT16_2 = 'tempora:Pent16-2:4'
TEMPORA_PENT16_3 = 'tempora:Pent16-3:4'
TEMPORA_PENT16_4 = 'tempora:Pent16-4:4'
TEMPORA_PENT16_5 = 'tempora:Pent16-5:4'
TEMPORA_PENT16_6 = 'tempora:Pent16-6:4'
TEMPORA_PENT17_0 = 'tempora:Pent17-0:2'
TEMPORA_PENT17_1 = 'tempora:Pent17-1:4'
TEMPORA_PENT17_2 = 'tempora:Pent17-2:4'
TEMPORA_PENT17_3 = 'tempora:Pent17-3:4'
TEMPORA_PENT17_4 = 'tempora:Pent17-4:4'
TEMPORA_PENT17_5 = 'tempora:Pent17-5:4'
TEMPORA_PENT17_6 = 'tempora:Pent17-6:4'
TEMPORA_PENT18_0 = 'tempora:Pent18-0:2'
TEMPORA_PENT18_1 = 'tempora:Pent18-1:4'
TEMPORA_PENT18_2 = 'tempora:Pent18-2:4'
TEMPORA_PENT18_3 = 'tempora:Pent18-3:4'
TEMPORA_PENT18_4 = 'tempora:Pent18-4:4'
TEMPORA_PENT18_5 = 'tempora:Pent18-5:4'
TEMPORA_PENT18_6 = 'tempora:Pent18-6:4'
TEMPORA_PENT19_0 = 'tempora:Pent19-0:2'
TEMPORA_PENT19_1 = 'tempora:Pent19-1:4'
TEMPORA_PENT19_2 = 'tempora:Pent19-2:4'
TEMPORA_PENT19_3 = 'tempora:Pent19-3:4'
TEMPORA_PENT19_4 = 'tempora:Pent19-4:4'
TEMPORA_PENT19_5 = 'tempora:Pent19-5:4'
TEMPORA_PENT19_6 = 'tempora:Pent19-6:4'
TEMPORA_PENT20_0 = 'tempora:Pent20-0:2'
TEMPORA_PENT20_1 = 'tempora:Pent20-1:4'
TEMPORA_PENT20_2 = 'tempora:Pent20-2:4'
TEMPORA_PENT20_3 = 'tempora:Pent20-3:4'
TEMPORA_PENT20_4 = 'tempora:Pent20-4:4'
TEMPORA_PENT20_5 = 'tempora:Pent20-5:4'
TEMPORA_PENT20_6 = 'tempora:Pent20-6:4'
TEMPORA_PENT21_0 = 'tempora:Pent21-0:2'
TEMPORA_PENT21_1 = 'tempora:Pent21-1:4'
TEMPORA_PENT21_2 = 'tempora:Pent21-2:4'
TEMPORA_PENT21_3 = 'tempora:Pent21-3:4'
TEMPORA_PENT21_4 = 'tempora:Pent21-4:4'
TEMPORA_PENT21_5 = 'tempora:Pent21-5:4'
TEMPORA_PENT21_6 = 'tempora:Pent21-6:4'
TEMPORA_PENT22_0 = 'tempora:Pent22-0:2'
TEMPORA_PENT22_1 = 'tempora:Pent22-1:4'
TEMPORA_PENT22_2 = 'tempora:Pent22-2:4'
TEMPORA_PENT22_3 = 'tempora:Pent22-3:4'
TEMPORA_PENT22_4 = 'tempora:Pent22-4:4'
TEMPORA_PENT22_5 = 'tempora:Pent22-5:4'
TEMPORA_PENT22_6 = 'tempora:Pent22-6:4'
TEMPORA_PENT23_0 = 'tempora:Pent23-0:2'
TEMPORA_PENT23_1 = 'tempora:Pent23-1:4'
TEMPORA_PENT23_2 = 'tempora:Pent23-2:4'
TEMPORA_PENT23_3 = 'tempora:Pent23-3:4'
TEMPORA_PENT23_4 = 'tempora:Pent23-4:4'
TEMPORA_PENT23_5 = 'tempora:Pent23-5:4'
TEMPORA_PENT23_6 = 'tempora:Pent23-6:4'

TEMPORA_PENT_3 = 'tempora:093-3:2'  # Ember Wednesday in September
TEMPORA_PENT_5 = 'tempora:093-5:2'  # Ember Friday in September
TEMPORA_PENT_6 = 'tempora:093-6:2'  # Ember Saturday in September

TEMPORA_PENT24_0 = 'tempora:Pent24-0:2'
TEMPORA_PENT24_1 = 'tempora:Pent24-1:4'
TEMPORA_PENT24_2 = 'tempora:Pent24-2:4'
TEMPORA_PENT24_3 = 'tempora:Pent24-3:4'
TEMPORA_PENT24_4 = 'tempora:Pent24-4:4'
TEMPORA_PENT24_5 = 'tempora:Pent24-5:4'
TEMPORA_PENT24_6 = 'tempora:Pent24-6:4'

TEMPORA_ADV1_0 = 'tempora:Adv1-0:1'  # Sunday in 1st week of Advent
TEMPORA_ADV1_1 = 'tempora:Adv1-1:3'  # Monday in 1st week of Advent
TEMPORA_ADV1_2 = 'tempora:Adv1-2:3'  # Tuesday in 1st week of Advent
TEMPORA_ADV1_3 = 'tempora:Adv1-3:3'  # Wednesday in 1st week of Advent
TEMPORA_ADV1_4 = 'tempora:Adv1-4:3'  # Thursday in 1st week of Advent
TEMPORA_ADV1_5 = 'tempora:Adv1-5:3'  # Friday in 1st week of Advent
TEMPORA_ADV1_6 = 'tempora:Adv1-6:3'  # Saturday in 1st week of Advent
TEMPORA_ADV2_0 = 'tempora:Adv2-0:1'
TEMPORA_ADV2_1 = 'tempora:Adv2-1:3'
TEMPORA_ADV2_2 = 'tempora:Adv2-2:3'
TEMPORA_ADV2_3 = 'tempora:Adv2-3:3'
TEMPORA_ADV2_4 = 'tempora:Adv2-4:3'
TEMPORA_ADV2_5 = 'tempora:Adv2-5:3'
TEMPORA_ADV2_6 = 'tempora:Adv2-6:3'
TEMPORA_ADV3_0 = 'tempora:Adv3-0:1'
TEMPORA_ADV3_1 = 'tempora:Adv3-1:3'
TEMPORA_ADV3_2 = 'tempora:Adv3-2:3'
TEMPORA_ADV3_3 = 'tempora:Adv3-3:2'  # Ember Wednesday in Advent
TEMPORA_ADV3_4 = 'tempora:Adv3-4:3'
TEMPORA_ADV3_5 = 'tempora:Adv3-5:2'  # Ember Friday in Advent
TEMPORA_ADV3_6 = 'tempora:Adv3-6:2'  # Ember Saturday in Advent
TEMPORA_ADV4_0 = 'tempora:Adv4-0:1'
TEMPORA_ADV4_1 = 'tempora:Adv4-1:3'
TEMPORA_ADV4_2 = 'tempora:Adv4-2:3'
TEMPORA_ADV4_3 = 'tempora:Adv4-3:3'
TEMPORA_ADV4_4 = 'tempora:Adv4-4:3'
TEMPORA_ADV4_5 = 'tempora:Adv4-5:3'

NAT1_0 = 'tempora:Nat1-0:2'  # Sunday in the Octave of Nativity
NAT2_0 = 'tempora:Nat2-0:2'  # Feast of the Holy Name of Jesus
SANCTI_10_DUr = 'sancti:10-DUr:1'  # Feast of Christ the King; last Sunday of October
EPI1_0A = 'tempora:Epi1-0a:2'  # 1st Sunday after Epiphany
PENT01_0A = 'tempora:Pent01-0a:2'  # 1st Sunday after Pentecost
C_10A = 'tempora:C10a:4'  # B. M. V. Saturdays in Advent
C_10B = 'tempora:C10b:4'  # B. M. V. Saturdays between Nativity and Purification
C_10C = 'tempora:C10c:4'  # B. M. V. Saturdays between Feb 2 and Wednesday in Holy Week
C_10PASC = 'tempora:C10Pasc:4'  # B. M. V. Saturdays in Easter period
C_10T = 'tempora:C10t:4'  # B. M. V. Saturdays between Trinity Sunday and Saturday before 1st Sunday of Advent


# SANCTI - days which have fixed date

SANCTI_01_01 = 'sancti:01-01:1'  # Octave of the Nativity
SANCTI_01_06 = 'sancti:01-06:1'  # Epiphany
SANCTI_01_13 = 'sancti:01-13:2'  # Baptism of the Lord
SANCTI_01_14 = 'sancti:01-14:3'
SANCTI_01_15 = 'sancti:01-15:3'
SANCTI_01_16 = 'sancti:01-16:3'
SANCTI_01_17 = 'sancti:01-17:3'
SANCTI_01_18 = 'sancti:01-18r:4'
SANCTI_01_19 = 'sancti:01-19:4'
SANCTI_01_20 = 'sancti:01-20:3'
SANCTI_01_21 = 'sancti:01-21:3'
SANCTI_01_22 = 'sancti:01-22:3'
SANCTI_01_23 = 'sancti:01-23:3'
SANCTI_01_24 = 'sancti:01-24:3'
SANCTI_01_25 = 'sancti:01-25r:3'
SANCTI_01_26 = 'sancti:01-26:3'
SANCTI_01_27 = 'sancti:01-27:3'
SANCTI_01_28 = 'sancti:01-28:3'
SANCTI_01_29 = 'sancti:01-29:3'
SANCTI_01_30 = 'sancti:01-30:3'
SANCTI_01_31 = 'sancti:01-31:3'

SANCTI_02_01 = 'sancti:02-01:3'
SANCTI_02_02 = 'sancti:02-02:2'  # Feast of the Purification of the Blessed Virgin Mary
SANCTI_02_03 = 'sancti:02-03:4'
SANCTI_02_04 = 'sancti:02-04:3'
SANCTI_02_05 = 'sancti:02-05:3'
SANCTI_02_06 = 'sancti:02-06:3'
SANCTI_02_07 = 'sancti:02-07:3'
SANCTI_02_08 = 'sancti:02-08:3'
SANCTI_02_09 = 'sancti:02-09:3'
SANCTI_02_10 = 'sancti:02-10:3'
SANCTI_02_11 = 'sancti:02-11:3'
SANCTI_02_12 = 'sancti:02-12:3'
SANCTI_02_14 = 'sancti:02-14:4'
SANCTI_02_15 = 'sancti:02-15:4'
SANCTI_02_18 = 'sancti:02-18:4'
SANCTI_02_22 = 'sancti:02-22:2'  # Feast of the Chair of Saint Peter
SANCTI_02_23 = 'sancti:02-23:3'
SANCTI_02_24 = 'sancti:02-24:2'  # St. Matthias, Apostle
SANCTI_02_27 = 'sancti:02-27:3'

SANCTI_03_04 = 'sancti:03-04:3'
SANCTI_03_06 = 'sancti:03-06:3'
SANCTI_03_07 = 'sancti:03-07:3'
SANCTI_03_08 = 'sancti:03-08:3'
SANCTI_03_08PL = 'sancti:03-08pl:3'
SANCTI_03_09 = 'sancti:03-09:3'
SANCTI_03_10 = 'sancti:03-10:3'
SANCTI_03_12 = 'sancti:03-12:3'
SANCTI_03_15PL = 'sancti:03-15pl:3'
SANCTI_03_17 = 'sancti:03-17:3'
SANCTI_03_17PL = 'sancti:03-17pl:3'
SANCTI_03_18 = 'sancti:03-18:3'
SANCTI_03_19 = 'sancti:03-19:1'  # Saint Joseph's Day
SANCTI_03_21 = 'sancti:03-21:3'
SANCTI_03_24 = 'sancti:03-24:3'
SANCTI_03_25 = 'sancti:03-25:1'  # Annunciation
SANCTI_03_27 = 'sancti:03-27:3'
SANCTI_03_28 = 'sancti:03-28:3'

SANCTI_04_02 = 'sancti:04-02:3'
SANCTI_04_04 = 'sancti:04-04:3'
SANCTI_04_05 = 'sancti:04-05:3'
SANCTI_04_11 = 'sancti:04-11:3'
SANCTI_04_13 = 'sancti:04-13:3'
SANCTI_04_14 = 'sancti:04-14:3'
SANCTI_04_17 = 'sancti:04-17:4'
SANCTI_04_21 = 'sancti:04-21:3'
SANCTI_04_22 = 'sancti:04-22:3'
SANCTI_04_23 = 'sancti:04-23:4'
SANCTI_04_23PL = 'sancti:04-23pl:1'
SANCTI_04_24 = 'sancti:04-24:3'
SANCTI_04_25 = 'sancti:04-25:2'  # St. Mark, Evangelist
SANCTI_04_26 = 'sancti:04-26:3'
SANCTI_04_27 = 'sancti:04-27:3'
SANCTI_04_28 = 'sancti:04-28:3'
SANCTI_04_29 = 'sancti:04-29:3'
SANCTI_04_30 = 'sancti:04-30:3'

SANCTI_05_01 = 'sancti:05-01r:1'  # St. Joseph the Worker
SANCTI_05_02 = 'sancti:05-02:3'
SANCTI_05_03 = 'sancti:05-03:4'
SANCTI_05_03PL = 'sancti:05-03pl:1'
SANCTI_05_04 = 'sancti:05-04:3'
SANCTI_05_05 = 'sancti:05-05:3'
SANCTI_05_07 = 'sancti:05-07:3'
SANCTI_05_08PL = 'sancti:05-08pl:1'
SANCTI_05_09 = 'sancti:05-09:3'
SANCTI_05_10 = 'sancti:05-10:3'
SANCTI_05_11 = 'sancti:05-11r:2'  # SS. Philip and James, Apostles
SANCTI_05_12 = 'sancti:05-12:3'
SANCTI_05_13 = 'sancti:05-13:3'
SANCTI_05_14 = 'sancti:05-14:4'
SANCTI_05_15 = 'sancti:05-15:3'
SANCTI_05_16 = 'sancti:05-16:4'
SANCTI_05_16PL = 'sancti:05-16pl:3'
SANCTI_05_17 = 'sancti:05-17:3'
SANCTI_05_18 = 'sancti:05-18:3'
SANCTI_05_19 = 'sancti:05-19:3'
SANCTI_05_20 = 'sancti:05-20:3'
SANCTI_05_24PL = 'sancti:05-24pl:2'
SANCTI_05_25 = 'sancti:05-25:3'
SANCTI_05_26 = 'sancti:05-26:3'
SANCTI_05_27 = 'sancti:05-27:3'
SANCTI_05_28 = 'sancti:05-28:3'
SANCTI_05_29 = 'sancti:05-29:3'
SANCTI_05_30 = 'sancti:05-30:4'
SANCTI_05_31 = 'sancti:05-31:2'  # Mary the Queen

SANCTI_06_01 = 'sancti:06-01:3'
SANCTI_06_01PL = 'sancti:06-01pl:3'
SANCTI_06_02 = 'sancti:06-02:4'
SANCTI_06_04 = 'sancti:06-04:3'
SANCTI_06_05 = 'sancti:06-05:3'
SANCTI_06_06 = 'sancti:06-06:3'
SANCTI_06_09 = 'sancti:06-09:4'
SANCTI_06_10 = 'sancti:06-10:3'
SANCTI_06_10PL = 'sancti:06-10pl:3'
SANCTI_06_11 = 'sancti:06-11:3'
SANCTI_06_12 = 'sancti:06-12:3'
SANCTI_06_13 = 'sancti:06-13:3'
SANCTI_06_14 = 'sancti:06-14:3'
SANCTI_06_15 = 'sancti:06-15:3'
SANCTI_06_17 = 'sancti:06-17r:3'
SANCTI_06_18 = 'sancti:06-18:3'
SANCTI_06_19 = 'sancti:06-19:3'
SANCTI_06_20 = 'sancti:06-20:4'
SANCTI_06_21 = 'sancti:06-21:3'
SANCTI_06_22 = 'sancti:06-22:3'
SANCTI_06_23 = 'sancti:06-23:2'  # Vigil of st. John Baptist
SANCTI_06_24 = 'sancti:06-24:1'  # St. John Baptist
SANCTI_06_25 = 'sancti:06-25:3'
SANCTI_06_26 = 'sancti:06-26r:3'
SANCTI_06_28 = 'sancti:06-28r:2'  # Vigil of ss. Peter and Paul
SANCTI_06_29 = 'sancti:06-29:1'  # Ss. Peter and Paul
SANCTI_06_30 = 'sancti:06-30:3'

SANCTI_07_01 = 'sancti:07-01:1'  # Feast of the Most Precious Blood
SANCTI_07_02 = 'sancti:07-02:2'  # Feast of the Visitation of the Blessed Virgin Mary
SANCTI_07_03 = 'sancti:07-03r:3'
SANCTI_07_05 = 'sancti:07-05:3'
SANCTI_07_07 = 'sancti:07-07:3'
SANCTI_07_08 = 'sancti:07-08:3'
SANCTI_07_10 = 'sancti:07-10:3'
SANCTI_07_11 = 'sancti:07-11:4'
SANCTI_07_12 = 'sancti:07-12:3'
SANCTI_07_14 = 'sancti:07-14:3'
SANCTI_07_15 = 'sancti:07-15:3'
SANCTI_07_16 = 'sancti:07-16:4'
SANCTI_07_17 = 'sancti:07-17:4'
SANCTI_07_18 = 'sancti:07-18:3'
SANCTI_07_18PL = 'sancti:07-18pl:3'
SANCTI_07_19 = 'sancti:07-19:3'
SANCTI_07_20 = 'sancti:07-20:3'
SANCTI_07_20PL = 'sancti:07-20pl:3'
SANCTI_07_21 = 'sancti:07-21r:3'
SANCTI_07_22 = 'sancti:07-22:3'
SANCTI_07_23 = 'sancti:07-23:3'
SANCTI_07_24 = 'sancti:07-24r:4'
SANCTI_07_24PL = 'sancti:07-24pl:3'
SANCTI_07_25 = 'sancti:07-25:2'  # St. James, Apostle
SANCTI_07_26 = 'sancti:07-26:2'  # St. Anna, Mary's Mother
SANCTI_07_27 = 'sancti:07-27:4'
SANCTI_07_28 = 'sancti:07-28:3'
SANCTI_07_29 = 'sancti:07-29:3'
SANCTI_07_30 = 'sancti:07-30:4'
SANCTI_07_31 = 'sancti:07-31:3'

SANCTI_08_01 = 'sancti:08-01r:4'
SANCTI_08_02 = 'sancti:08-02:3'
SANCTI_08_04 = 'sancti:08-04:3'
SANCTI_08_05 = 'sancti:08-05:3'
SANCTI_08_06 = 'sancti:08-06:2'  # Transfiguration
SANCTI_08_07 = 'sancti:08-07:3'
SANCTI_08_08 = 'sancti:08-08r:3'
SANCTI_08_09 = 'sancti:08-09t:3'  # Vigil of st. Laurent
SANCTI_08_10 = 'sancti:08-10:2'  # St. Laurent
SANCTI_08_11 = 'sancti:08-11:4'
SANCTI_08_12 = 'sancti:08-12:3'
SANCTI_08_13 = 'sancti:08-13:4'
SANCTI_08_14 = 'sancti:08-14:2'  # Vigil of Assumption of Mary
SANCTI_08_15 = 'sancti:08-15r:1'  # Assumption of Mary
SANCTI_08_16 = 'sancti:08-16:2'  # St. Joachim
SANCTI_08_17 = 'sancti:08-17:3'
SANCTI_08_18 = 'sancti:08-18r:4'
SANCTI_08_19 = 'sancti:08-19:3'
SANCTI_08_20 = 'sancti:08-20:3'
SANCTI_08_21 = 'sancti:08-21:3'
SANCTI_08_22 = 'sancti:08-22r:2'  # Immaculate Heart of Mary
SANCTI_08_23 = 'sancti:08-23:3'
SANCTI_08_24 = 'sancti:08-24:2'  # St. Bartholomew, Apostle
SANCTI_08_25 = 'sancti:08-25:3'
SANCTI_08_26 = 'sancti:08-26:4'
SANCTI_08_26PL = 'sancti:08-26pl:1'
SANCTI_08_27 = 'sancti:08-27:3'
SANCTI_08_28 = 'sancti:08-28:3'
SANCTI_08_29 = 'sancti:08-29:3'
SANCTI_08_30 = 'sancti:08-30:3'
SANCTI_08_31 = 'sancti:08-31:3'

SANCTI_09_01 = 'sancti:09-01:4'
SANCTI_09_01PL = 'sancti:09-01pl:3'
SANCTI_09_02 = 'sancti:09-02:3'
SANCTI_09_03 = 'sancti:09-03r:3'
SANCTI_09_05 = 'sancti:09-05:3'
SANCTI_09_07PL = 'sancti:09-07pl:3'
SANCTI_09_08 = 'sancti:09-08:2'  # Nativity of Mary
SANCTI_09_09 = 'sancti:09-09:4'
SANCTI_09_10 = 'sancti:09-10:3'
SANCTI_09_11 = 'sancti:09-11:4'
SANCTI_09_12 = 'sancti:09-12:3'
SANCTI_09_14 = 'sancti:09-14:2'  # Exaltation of the Cross
SANCTI_09_15 = 'sancti:09-15:2'  # The Seven Dolors of the Blessed Virgin Mary
SANCTI_09_16 = 'sancti:09-16:3'
SANCTI_09_17 = 'sancti:09-17:4'
SANCTI_09_18 = 'sancti:09-18r:3'
SANCTI_09_19 = 'sancti:09-19:3'
SANCTI_09_20 = 'sancti:09-20:4'
SANCTI_09_21 = 'sancti:09-21:2'  # St. Matthew, Apostle and Evangelist
SANCTI_09_22 = 'sancti:09-22:3'
SANCTI_09_23 = 'sancti:09-23:3'
SANCTI_09_24 = 'sancti:09-24:4'
SANCTI_09_25PL = 'sancti:09-25pl:3'
SANCTI_09_26 = 'sancti:09-26:4'
SANCTI_09_27 = 'sancti:09-27:3'
SANCTI_09_28 = 'sancti:09-28:3'
SANCTI_09_29 = 'sancti:09-29:1'  # St. Michael the Archangel
SANCTI_09_30 = 'sancti:09-30r:3'

SANCTI_10_01 = 'sancti:10-01:4'
SANCTI_10_01PL = 'sancti:10-01pl:3'
SANCTI_10_02 = 'sancti:10-02:3'
SANCTI_10_03 = 'sancti:10-03:3'
SANCTI_10_04 = 'sancti:10-04:3'
SANCTI_10_05 = 'sancti:10-05:4'
SANCTI_10_06 = 'sancti:10-06:3'
SANCTI_10_07 = 'sancti:10-07r:2'  # Our Lady of the Rosary
SANCTI_10_08 = 'sancti:10-08r:3'
SANCTI_10_09 = 'sancti:10-09:3'
SANCTI_10_10 = 'sancti:10-10:3'
SANCTI_10_11 = 'sancti:10-11:2'  # Maternity of the Blessed Virgin Mary
SANCTI_10_13 = 'sancti:10-13:3'
SANCTI_10_14 = 'sancti:10-14:3'
SANCTI_10_15 = 'sancti:10-15:3'
SANCTI_10_16 = 'sancti:10-16:3'
SANCTI_10_17 = 'sancti:10-17:3'
SANCTI_10_18 = 'sancti:10-18:2'  # St. Luke, Evangelist
SANCTI_10_19 = 'sancti:10-19:3'
SANCTI_10_20 = 'sancti:10-20:3'
SANCTI_10_21 = 'sancti:10-21:3'
SANCTI_10_23 = 'sancti:10-23r:3'
SANCTI_10_24 = 'sancti:10-24:3'
SANCTI_10_25 = 'sancti:10-25:4'
SANCTI_10_28 = 'sancti:10-28:2'  # SS. Simon and Jude, Apostles

SANCTI_11_01 = 'sancti:11-01:1'  # All Saints
SANCTI_11_02_1 = 'sancti:11-02m1:1'  # All Souls' Day
SANCTI_11_02_2 = 'sancti:11-02m2:1'
SANCTI_11_02_3 = 'sancti:11-02m3:1'
SANCTI_11_04 = 'sancti:11-04r:3'
SANCTI_11_08 = 'sancti:11-08r:4'
SANCTI_11_09 = 'sancti:11-09:2'  # Dedication of the Lateran Basilica in Rome
SANCTI_11_10 = 'sancti:11-10:3'
SANCTI_11_11 = 'sancti:11-11:3'
SANCTI_11_12 = 'sancti:11-12:3'
SANCTI_11_13 = 'sancti:11-13:4'
SANCTI_11_13PL = 'sancti:11-13pl:2'
SANCTI_11_14 = 'sancti:11-14:3'
SANCTI_11_15 = 'sancti:11-15:3'
SANCTI_11_16 = 'sancti:11-16:3'
SANCTI_11_17 = 'sancti:11-17:3'
SANCTI_11_18 = 'sancti:11-18r:3'
SANCTI_11_19 = 'sancti:11-19:3'
SANCTI_11_20 = 'sancti:11-20:3'
SANCTI_11_21 = 'sancti:11-21:3'
SANCTI_11_22 = 'sancti:11-22:3'
SANCTI_11_23 = 'sancti:11-23:3'
SANCTI_11_24 = 'sancti:11-24:3'
SANCTI_11_25 = 'sancti:11-25:3'
SANCTI_11_26 = 'sancti:11-26:3'
SANCTI_11_29 = 'sancti:11-29r:4'
SANCTI_11_30 = 'sancti:11-30:2'  # St. Andrew, Apostle

SANCTI_12_02 = 'sancti:12-02:3'
SANCTI_12_03 = 'sancti:12-03:3'
SANCTI_12_04 = 'sancti:12-04:3'
SANCTI_12_05 = 'sancti:12-05:4'
SANCTI_12_06 = 'sancti:12-06:3'
SANCTI_12_07 = 'sancti:12-07:3'
SANCTI_12_08 = 'sancti:12-08:1'  # Immaculate Conception of the Blessed Virgin Mary
SANCTI_12_10 = 'sancti:12-10:4'
SANCTI_12_11 = 'sancti:12-11:3'
SANCTI_12_13 = 'sancti:12-13r:3'
SANCTI_12_16 = 'sancti:12-16:3'
SANCTI_12_21 = 'sancti:12-21:2'  # St. Thomas, Apostle
SANCTI_12_24 = 'sancti:12-24:1'  # Vigil of the Nativity of the Lord
SANCTI_12_25_1 = 'sancti:12-25m1:1'  # Nativity of the Lord
SANCTI_12_25_2 = 'sancti:12-25m2:1'
SANCTI_12_25_3 = 'sancti:12-25m3:1'
SANCTI_12_26 = 'sancti:12-26:2'  # St. Stephen, Protomartyr
SANCTI_12_27 = 'sancti:12-27:2'  # St. John, Apostle and Evangelist
SANCTI_12_28 = 'sancti:12-28:2'  # Holy Innocents
SANCTI_12_29 = 'sancti:12-29r:2'
SANCTI_12_30 = 'sancti:12-30:2'
SANCTI_12_31 = 'sancti:12-31r:2'

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
    SANCTI_10_DUr,  # Feast of Christ the King; last Sunday of October
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
    SANCTI_12_30,
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
    SANCTI_08_06,
)


# Related to propers' printing

DIVOFF_DIR = os.path.join(THIS_DIR, 'resources', 'divinum-officium')
CUSTOM_DIVOFF_DIR = os.path.join(THIS_DIR, 'resources', 'divinum-officium-custom')

EXCLUDE_SECTIONS = (
    'Evangelium1',
    'Evangelium2',
    'Evangelium3',
    'Evangelium4',
    'Lectio1',
    'Prelude(rubrica 1570)',
    'Rank1570',
    'Rank1960',
    'RankNewcal',
    'RankTrident',
    'Rank',
    'Rank (rubrica 1955 aut rubrica 1960)',
    'Rank (rubrica 1960)',
    'Rank (rubrica innovata)',
    'Rank (si rubrica 1960)',
    'Rank (si rubrica innovata)',
    'Rule',
    'Tractus1',
    'Munda Cor Passionis',
    'GradualeF',
    'Footnotes',
    'Name'
)
EXCLUDE_SECTIONS_TITLES = (
    'Commemoratio Oratio',
    'Commemoratio Postcommunio',
    'Commemoratio Secreta',
    'Comment',
    'Prelude',
    'Prelude(rubrica 1960)',
    'Maundi',
    'Post Missam'
)

REFERENCE_REGEX = re.compile('^@([\w/\-]*):?([^:]*)[: ]*(.*)')
SECTION_REGEX = re.compile(r'^### *(.*)')
