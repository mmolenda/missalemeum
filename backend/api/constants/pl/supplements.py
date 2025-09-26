from api.constants import common as constants

KDE = "Komentarz do Ewangelii"
SUPPLEMENTS_V4 = {
    constants.TEMPORA_ADV1_0: [
        {"label": "Adwent", "path": "/pl/supplement/2-adwent"},
        {"label": f"{KDE} na 1 Niedzielę Adwentu", "path": "http://vetusordo.pl/objasnienia1na/"}
    ],
    constants.TEMPORA_ADV2_0: [
        {"label": f"{KDE} na 2 Niedzielę Adwentu", "path": "http://vetusordo.pl/objasnienia2na/"}
    ],
    constants.TEMPORA_ADV3_0: [
        {"label": f"{KDE} na 3 Niedzielę Adwentu", "path": "http://vetusordo.pl/objasnienia3na/"}
    ],
    constants.TEMPORA_ADV4_0: [
        {"label": f"{KDE} na 4 Niedzielę Adwentu", "path": "http://vetusordo.pl/objasnienia4na/"}
    ],
    constants.SANCTI_12_24: [
        {"label": "Boże Narodzenie", "path": "/pl/supplement/3-boze-narodzenie"}
        ],
    constants.SANCTI_12_25_1: [
        {"label": "Boże Narodzenie", "path": "/pl/supplement/3-boze-narodzenie"},
        {"label": f"{KDE} pierwszej na uroczystość Bożego Narodzenia", "path": "http://vetusordo.pl/objasnieniaenubn/"}
    ],
    constants.SANCTI_12_25_2: [
        {"label": f"{KDE} drugiej na uroczystość Bożego Narodzenia", "path": "http://vetusordo.pl/objasnieniaenubn2/"}
    ],
    constants.SANCTI_12_25_3: [
        {"label": f"{KDE} trzeciej na uroczystość Bożego Narodzenia", "path": "http://vetusordo.pl/objasnieniaenubn3/"}
    ],
    constants.SANCTI_12_26: [
        {"label": f"{KDE} na uroczystość pierwszego męczennika św. Szczepana", "path": "http://vetusordo.pl/objasnieniaupmss/"}
    ],
    constants.TEMPORA_NAT1_0: [
        {"label": f"{KDE} na niedzielę po Bożym Narodzeniu", "path": "http://vetusordo.pl/objasnieniaennpbn/"}
    ],
    constants.SANCTI_01_01: [
        {"label": f"{KDE} na Oktawę Bożego Narodzenia", "path": "http://vetusordo.pl/objasnieniaenunr/"}
    ],
    constants.SANCTI_01_06: [
        {"label": f"{KDE} na Objawienia Pańskie", "path": "http://vetusordo.pl/objasnieniaenustk/"}
    ],
    constants.TEMPORA_EPI1_0: [
        {"label": "Okres po Objawieniu", "path": "/pl/supplement/4-okres-po-objawieniu"}
    ],
    constants.TEMPORA_EPI2_0: [
        {"label": f"{KDE} na 2 niedzielę po Objawieniu", "path": "http://vetusordo.pl/objasnieniaenndpstk/"}
    ],
    constants.TEMPORA_EPI3_0: [
        {"label": f"{KDE} na 3 niedzielę po Objawieniu", "path": "http://vetusordo.pl/objasnieniaenntpstk/"}
    ],
    constants.TEMPORA_EPI4_0: [
        {"label": f"{KDE} na 4 niedzielę po Objawieniu", "path": "http://vetusordo.pl/objasnieniaenncpstk/"}
    ],
    constants.TEMPORA_EPI5_0: [
        {"label": f"{KDE} na 5 niedzielę po Objawieniu", "path": "http://vetusordo.pl/objasnieniaennppstk-2/"}
    ],
    constants.TEMPORA_QUADP1_0: [
        {"label": "Przedpoście", "path": "/pl/supplement/5-przedposcie"},
        {"label": f"{KDE} na niedzielę Siedemdziesiątnicy", "path": "http://vetusordo.pl/oenns/"}
    ],
    constants.TEMPORA_QUADP2_0: [
        {"label": f"{KDE} na niedzielę Sześćdziesiątnicy", "path": "http://vetusordo.pl/objasnieniaennmpna/"}
    ],
    constants.TEMPORA_QUADP3_0: [
        {"label": f"{KDE} na niedzielę Pięćdziesiątnicy", "path": "http://vetusordo.pl/objasnieniannzpna/"}
    ],
    constants.TEMPORA_QUADP3_3: [
        {"label": "Wielki Post", "path": "/pl/supplement/6-wielki-post"}
    ],
    constants.TEMPORA_QUAD1_0: [
        {"label": f"{KDE} na 1 niedzielę Wielkiego Postu", "path": "http://vetusordo.pl/objasnieniann1p/"}
    ],
    constants.TEMPORA_QUAD2_0: [
        {"label": f"{KDE} na 2 niedzielę Wielkiego Postu", "path": "http://vetusordo.pl/2019oenndp/"}
    ],
    constants.TEMPORA_QUAD3_0: [
        {"label": f"{KDE} na 3 niedzielę Wielkiego Postu", "path": "http://vetusordo.pl/2019oenntp/"}
    ],
    constants.TEMPORA_QUAD4_0: [
        {"label": f"{KDE} na 4 niedzielę Wielkiego Postu", "path": "http://vetusordo.pl/2019oenncp/"}
    ],
    constants.TEMPORA_QUAD5_0: [
        {"label": "Okres Męki Pańskiej", "path": "/pl/supplement/8-okres-meki-panskiej"},
        {"label": f"{KDE} na 1 niedzielę Męki Pańskiej", "path": "http://vetusordo.pl/objasnieniaennpp/"}
    ],
    constants.TEMPORA_QUAD6_0: [
        {"label": "Wielki Tydzień", "path": "/pl/supplement/7-wielki-tydzien"},
        {"label": f"{KDE} na 2 niedzielę Męki Pańskiej (Palmową)", "path": "http://vetusordo.pl/objasnieniaennk/"}
    ],
    constants.TEMPORA_QUAD6_6: [
        {"label": "Okres Wielkanocny", "path": "/pl/supplement/9-okres-wielkanocny"}
    ],
    constants.TEMPORA_PASC0_0: [
        {"label": f"{KDE} na Wielkanoc", "path": "http://vetusordo.pl/objasnieniaenw/"}
    ],
    constants.TEMPORA_PASC0_1: [
        {"label": f"{KDE} na poniedziałek Wielkanocny", "path": "http://vetusordo.pl/2019oenpw/"}
    ],
    constants.TEMPORA_PASC1_0: [
        {"label": f"{KDE} na niedzielę Białą", "path": "http://vetusordo.pl/2019oennp/"}
    ],
    constants.TEMPORA_PASC2_0: [
        {"label": f"{KDE} na 2 niedzielę po Wielkanocy", "path": "http://vetusordo.pl/2019oenn2pw/"}
    ],
    constants.TEMPORA_PASC3_0: [
        {"label": f"{KDE} na 3 niedzielę po Wielkanocy", "path": "http://vetusordo.pl/2019oenn3pw/"}
    ],
    constants.TEMPORA_PASC4_0: [
        {"label": f"{KDE} na 4 niedzielę po Wielkanocy", "path": "http://vetusordo.pl/2019oenn4pw/"}
    ],
    constants.TEMPORA_PASC5_0: [
        {"label": f"{KDE} na 5 niedzielę po Wielkanocy", "path": "http://vetusordo.pl/2019oenn5pw/"}
    ],
    constants.TEMPORA_PASC5_4: [
        {"label": f"{KDE} na Wniebowstąpienie Pańskie", "path": "http://vetusordo.pl/2019oenwp/"}
    ],
    constants.TEMPORA_PASC6_0: [
        {"label": f"{KDE} na niedzielę po Wniebostąpieniu", "path": "http://vetusordo.pl/objasnieniaenn6pw/"}
    ],
    constants.TEMPORA_PASC6_6: [
        {"label": "Zesłanie Ducha św.", "path": "/pl/supplement/10-zeslanie-ducha-sw"}
    ],
    constants.TEMPORA_PASC7_0: [
        {"label": f"{KDE} na niedzielę Zesłania Ducha św.", "path": "http://vetusordo.pl/objasnieniaenuzds/"}
    ],
    constants.TEMPORA_PASC7_1: [
        {"label": f"{KDE} na poniedzialek w Oktawie Zesłania Ducha św.", "path": "/pl/supplement/commentary/poniedzialek-po-zeslaniu"}
    ],
    constants.TEMPORA_PENT01_0: [
        {"label": "Okres po Zesłaniu Ducha św.", "path": "/pl/supplement/11-okres-po-zeslaniu-ducha-sw"},
        {"label": f"{KDE} na uroczystość Trójcy Przenajświętszej", "path": "http://vetusordo.pl/objasnienia2019enuts/"}
    ],
    constants.TEMPORA_PENT01_4: [
        {"label": f"{KDE} na uroczystość Bożego Ciała", "path": "http://vetusordo.pl/objasnienia2019enubc/"}
    ],
    constants.TEMPORA_PENT02_0: [
        {"label": f"{KDE} na 2 niedzielę po Zesłaniu Ducha św.", "path": "http://vetusordo.pl/objasnienia2019enndps/"}
    ],
    constants.TEMPORA_PENT03_0: [
        {"label": f"{KDE} na 3 niedzielę po Zesłaniu Ducha św.", "path": "http://vetusordo.pl/objasnienia2019enntps/"}
    ],
    constants.TEMPORA_PENT04_0: [
        {"label": f"{KDE} na 4 niedzielę po Zesłaniu Ducha św.", "path": "http://vetusordo.pl/objasnienie2019enn4ps/"}
    ],
    constants.TEMPORA_PENT05_0: [
        {"label": f"{KDE} na 5 niedzielę po Zesłaniu Ducha św.", "path": "http://vetusordo.pl/objasnienia2019enn5ps/"}
    ],
    constants.TEMPORA_PENT06_0: [
        {"label": f"{KDE} na 6 niedzielę po Zesłaniu Ducha św.", "path": "http://vetusordo.pl/objasnienie2019enn6ps/"}
    ],
    constants.TEMPORA_PENT07_0: [
        {"label": f"{KDE} na 7 niedzielę po Zesłaniu Ducha św.", "path": "http://vetusordo.pl/objasnienia2019nn7ps/"}
    ],
    constants.TEMPORA_PENT08_0: [
        {"label": f"{KDE} na 8 niedzielę po Zesłaniu Ducha św.", "path": "http://vetusordo.pl/objasnienia2019nn8ps/"}
    ],
    constants.TEMPORA_PENT09_0: [
        {"label": f"{KDE} na 9 niedzielę po Zesłaniu Ducha św.", "path": "http://vetusordo.pl/objasnienia2019nn9ps/"}
    ],
    constants.TEMPORA_PENT10_0: [
        {"label": f"{KDE} na 10 niedzielę po Zesłaniu Ducha św.", "path": "http://vetusordo.pl/objasnienia2019nn10ps/"}
    ],
    constants.TEMPORA_PENT11_0: [
        {"label": f"{KDE} na 11 niedzielę po Zesłaniu Ducha św.", "path": "http://vetusordo.pl/objasnienie2019nn11ps/"}
    ],
    constants.TEMPORA_PENT12_0: [
        {"label": f"{KDE} na 12 niedzielę po Zesłaniu Ducha św.", "path": "http://vetusordo.pl/objasnienie2019nn12ps/"}
    ],
    constants.TEMPORA_PENT13_0: [
        {"label": f"{KDE} na 13 niedzielę po Zesłaniu Ducha św.", "path": "http://vetusordo.pl/objasnienie2019nn13ps/"}
    ],
    constants.TEMPORA_PENT14_0: [
        {"label": f"{KDE} na 14 niedzielę po Zesłaniu Ducha św.", "path": "http://vetusordo.pl/objasnienie2019nn14ps/"}
    ],
    constants.TEMPORA_PENT15_0: [
        {"label": f"{KDE} na 15 niedzielę po Zesłaniu Ducha św.", "path": "http://vetusordo.pl/objasnienie2019nn15ps/"}
    ],
    constants.TEMPORA_PENT16_0: [
        {"label": f"{KDE} na 16 niedzielę po Zesłaniu Ducha św.", "path": "/pl/supplement/commentary/16-niedziela-po-zeslaniu"}
    ],
    constants.TEMPORA_PENT17_0: [
        {"label": f"{KDE} na 17 niedzielę po Zesłaniu Ducha św.", "path": "http://vetusordo.pl/objasnieniaenn17ps/"}
    ],
    constants.TEMPORA_PENT18_0: [
        {"label": f"{KDE} na 18 niedzielę po Zesłaniu Ducha św.", "path": "http://vetusordo.pl/objasnieniaenn18ps/"}
    ],
    constants.TEMPORA_PENT19_0: [
        {"label": f"{KDE} na 19 niedzielę po Zesłaniu Ducha św.", "path": "http://vetusordo.pl/objasnieniaenn19ps/"}
    ],
    constants.TEMPORA_PENT20_0: [
        {"label": f"{KDE} na 20 niedzielę po Zesłaniu Ducha św.", "path": "/pl/supplement/commentary/20-niedziela-po-zeslaniu"}
    ],
    constants.TEMPORA_PENT21_0: [
        {"label": f"{KDE} na 21 niedzielę po Zesłaniu Ducha św.", "path": "http://vetusordo.pl/2019oenn21ps/"}
    ],
    constants.TEMPORA_PENT22_0: [
        {"label": f"{KDE} na 22 niedzielę po Zesłaniu Ducha św.", "path": "http://vetusordo.pl/2019oenn22ps/"}
    ],
    constants.TEMPORA_PENT23_0: [
        {"label": f"{KDE} na 23 niedzielę po Zesłaniu Ducha św.", "path": "http://vetusordo.pl/2019oenn23ps/"}
    ],
    constants.TEMPORA_PENT24_0: [
        {"label": f"{KDE} na 24 niedzielę po Zesłaniu Ducha św.", "path": "/pl/supplement/commentary/24-niedziela-po-zeslaniu"}
    ],
    constants.SANCTI_12_08: [
        {"label": f"{KDE} na uroczystość Niepokalanego Poczęcia N. M. P.", "path": "http://vetusordo.pl/oenunmp/"}
    ],
    constants.SANCTI_02_02: [
        {"label": f"{KDE} na uroczystość Oczyszczenia N. M. P.", "path": "http://vetusordo.pl/2019uroczystosconmp/"}
    ],
    constants.SANCTI_03_25: [
        {"label": f"{KDE} na uroczystość Zwiastowania N. M. P.", "path": "http://vetusordo.pl/2019oenuznmp/"}
    ],
    constants.SANCTI_06_29: [
        {"label": f"{KDE} na uroczystość śś. Apostołów Piotra i Pawła", "path": "http://vetusordo.pl/objasnienia2019enussapip/"}
    ],
    constants.SANCTI_08_15: [
        {"label": f"{KDE} na Wniebowzięcie N. M. P.", "path": "/pl/supplement/commentary/wniebowziecie-nmp"}
    ],
    constants.SANCTI_09_08: [
        {"label": f"{KDE} na Narodzenie N. M. P.", "path": "/pl/supplement/commentary/narodzenie-nmp"}
    ],
    constants.SANCTI_11_01: [
        {"label": f"{KDE} na uroczystość Wszystkich Świętych", "path": "http://vetusordo.pl/2019oenuws/"}
    ]
}


OE = "Objaśnienia Ewangelii"
DIOECESIUM_POLONIAE_1964 = {"label": "Msze dla diecezji polskich wg kalendarza z 1964 r.", "path": "/pl/supplement/dioecesium-poloniae-1964"}
SUPPLEMENTS = {
    constants.TEMPORA_ADV1_0: [
        {"label": "Adwent", "path": "/pl/supplement/2-adwent"},
        {"label": OE, "path": "/pl/supplement/objasnienia-Adv1-0"}
    ],
    constants.TEMPORA_ADV2_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Adv2-0"}
    ],
    constants.TEMPORA_ADV3_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Adv3-0"}
    ],
    constants.TEMPORA_ADV4_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Adv4-0"}
    ],
    constants.SANCTI_12_24: [
        {"label": "Boże Narodzenie", "path": "/pl/supplement/3-boze-narodzenie"}
        ],
    constants.SANCTI_12_25_1: [
        {"label": "Boże Narodzenie", "path": "/pl/supplement/3-boze-narodzenie"},
        {"label": OE, "path": "/pl/supplement/objasnienia-12-25m1"}
    ],
    constants.SANCTI_12_25_2: [
        {"label": OE, "path": "/pl/supplement/objasnienia-12-25m2"}
    ],
    constants.SANCTI_12_25_3: [
        {"label": OE, "path": "/pl/supplement/objasnienia-"}
    ],
    constants.SANCTI_12_26: [
        {"label": OE, "path": "/pl/supplement/objasnienia-12-25m3"}
    ],
    constants.TEMPORA_NAT1_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Nat1-0"}
    ],
    constants.SANCTI_01_01: [
        {"label": OE, "path": "/pl/supplement/objasnienia-01-01"}
    ],
    constants.SANCTI_01_06: [
        {"label": OE, "path": "/pl/supplement/objasnienia-01-06"}
    ],
    constants.TEMPORA_EPI1_0: [
        {"label": "Okres po Objawieniu", "path": "/pl/supplement/4-okres-po-objawieniu"}
    ],
    constants.TEMPORA_EPI2_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Epi2-0"}
    ],
    constants.TEMPORA_EPI3_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Epi3-0"}
    ],
    constants.TEMPORA_EPI4_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Epi4-0"}
    ],
    constants.TEMPORA_EPI5_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Epi5-0"}
    ],
    constants.TEMPORA_QUADP1_0: [
        {"label": "Przedpoście", "path": "/pl/supplement/5-przedposcie"},
        {"label": OE, "path": "/pl/supplement/objasnienia-Quadp1-0"}
    ],
    constants.TEMPORA_QUADP2_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Quadp2-0"}
    ],
    constants.TEMPORA_QUADP3_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Quadp3-0"}
    ],
    constants.TEMPORA_QUADP3_3: [
        {"label": "Wielki Post", "path": "/pl/supplement/6-wielki-post"}
    ],
    constants.TEMPORA_QUAD1_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Quad1-0"}
    ],
    constants.TEMPORA_QUAD2_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Quad2-0"}
    ],
    constants.TEMPORA_QUAD3_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Quad3-0"}
    ],
    constants.TEMPORA_QUAD4_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Quad4-0"}
    ],
    constants.TEMPORA_QUAD5_0: [
        {"label": "Okres Męki Pańskiej", "path": "/pl/supplement/8-okres-meki-panskiej"},
        {"label": OE, "path": "/pl/supplement/objasnienia-Quad5-0"}
    ],
    constants.TEMPORA_QUAD6_0: [
        {"label": "Wielki Tydzień", "path": "/pl/supplement/7-wielki-tydzien"},
        {"label": OE, "path": "/pl/supplement/objasnienia-Quad6-0r"}
    ],
    constants.TEMPORA_QUAD6_6: [
        {"label": "Okres Wielkanocny", "path": "/pl/supplement/9-okres-wielkanocny"}
    ],
    constants.TEMPORA_PASC0_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pasc0-0"}
    ],
    constants.TEMPORA_PASC0_1: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pasc0-1"}
    ],
    constants.TEMPORA_PASC1_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pasc1-0"}
    ],
    constants.TEMPORA_PASC2_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pasc2-0"}
    ],
    constants.TEMPORA_PASC3_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pasc3-0r"}
    ],
    constants.TEMPORA_PASC4_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pasc4-0"}
    ],
    constants.TEMPORA_PASC5_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pasc5-0"}
    ],
    constants.TEMPORA_PASC5_4: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pasc5-4"}
    ],
    constants.TEMPORA_PASC6_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pasc6-0"}
    ],
    constants.TEMPORA_PASC6_6: [
        {"label": "Zesłanie Ducha św.", "path": "/pl/supplement/10-zeslanie-ducha-sw"}
    ],
    constants.TEMPORA_PASC7_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pasc7-0"}
    ],
    constants.TEMPORA_PASC7_1: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pasc7-1"}
    ],
    constants.TEMPORA_PENT01_0: [
        {"label": "Okres po Zesłaniu Ducha św.", "path": "/pl/supplement/11-okres-po-zeslaniu-ducha-sw"},
        {"label": OE, "path": "/pl/supplement/objasnienia-Pent01-0r"}
    ],
    constants.TEMPORA_PENT01_4: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pent01-4"}
    ],
    constants.TEMPORA_PENT02_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pent02-0r"}
    ],
    constants.TEMPORA_PENT03_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pent03-0r"}
    ],
    constants.TEMPORA_PENT04_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pent04-0"}
    ],
    constants.TEMPORA_PENT05_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pent05-0"}
    ],
    constants.TEMPORA_PENT06_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pent06-0"}
    ],
    constants.TEMPORA_PENT07_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pent07-0"}
    ],
    constants.TEMPORA_PENT08_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pent08-0"}
    ],
    constants.TEMPORA_PENT09_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pent09-0"}
    ],
    constants.TEMPORA_PENT10_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pent10-0"}
    ],
    constants.TEMPORA_PENT11_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pent11-0"}
    ],
    constants.TEMPORA_PENT12_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pent12-0"}
    ],
    constants.TEMPORA_PENT13_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pent13-0"}
    ],
    constants.TEMPORA_PENT14_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pent14-0"}
    ],
    constants.TEMPORA_PENT15_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pent15-0"}
    ],
    constants.TEMPORA_PENT16_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pent16-0"}
    ],
    constants.TEMPORA_PENT17_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pent17-0"}
    ],
    constants.TEMPORA_PENT18_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pent18-0"}
    ],
    constants.TEMPORA_PENT19_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pent19-0"}
    ],
    constants.TEMPORA_PENT20_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pent20-0"}
    ],
    constants.TEMPORA_PENT21_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pent21-0"}
    ],
    constants.TEMPORA_PENT22_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pent22-0"}
    ],
    constants.TEMPORA_PENT23_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pent23-0"}
    ],
    constants.TEMPORA_PENT24_0: [
        {"label": OE, "path": "/pl/supplement/objasnienia-Pent24-0"}
    ],
    constants.SANCTI_12_08: [
        {"label": OE, "path": "/pl/supplement/objasnienia-12-08"}
    ],
    constants.SANCTI_02_02: [
        {"label": OE, "path": "/pl/supplement/objasnienia-02-02"}
    ],
    constants.SANCTI_03_25: [
        {"label": OE, "path": "/pl/supplement/objasnienia-03-25"}
    ],
    constants.SANCTI_06_29: [
        {"label": OE, "path": "/pl/supplement/objasnienia-06-29"}
    ],
    constants.SANCTI_08_15: [
        {"label": OE, "path": "/pl/supplement/objasnienia-08-15r"}
    ],
    constants.SANCTI_09_08: [
        {"label": OE, "path": "/pl/supplement/objasnienia-09-08"}
    ],
    constants.SANCTI_11_01: [
        {"label": OE, "path": "/pl/supplement/objasnienia-11-01"}
    ],
    constants.VOTIVE_MATRIMONIUM: [
        {"label": "Obrzędy sakramentu małżeństwa", "path": "/pl/supplement/22-malzenstwo"}
    ],
    constants.SANCTI_05_04PL: [DIOECESIUM_POLONIAE_1964],
    constants.SANCTI_10_09PL: [DIOECESIUM_POLONIAE_1964],
    constants.SANCTI_10_21PL: [DIOECESIUM_POLONIAE_1964],
    constants.SANCTI_11_20PL: [DIOECESIUM_POLONIAE_1964],
    constants.SANCTI_12_02PL: [DIOECESIUM_POLONIAE_1964],
    constants.SANCTI_12_04PL: [DIOECESIUM_POLONIAE_1964],
    constants.SANCTI_07_13PL: [
        DIOECESIUM_POLONIAE_1964,
        {"label": "1 Msza o Wyznawcy – Os iusti", "path": "/pl/commune:C5:0:w"},
        {"label": "2 Msza o Wyznawcy – Iustus ut palma", "path": "/pl/commune:C5b:0:w"}
    ],
    constants.SANCTI_07_15PL: [
        DIOECESIUM_POLONIAE_1964,
        {"label": "1 Msza o Męczenniku Biskupie – Statuit", "path": "/pl/commune:C2c:0:r"},
        {"label": "2 Msza o Męczenniku Biskupie – Sacerdotes Dei", "path": "/pl/commune:C2b:0:r"}
    ]
}
