from constants import common

from ..Latin.translation import paternoster, titles, transformations

titles[common.SANCTI_03_15PL] = 'Św. Klemensa Marii Dworzaka (Hofbauera)'
titles[common.SANCTI_04_23PL] = 'Św. Wojciecha, Biskupa i Męczennika'
titles[common.SANCTI_05_03PL] = 'N. M. P., Królowej Polski, Głównej Patronki Polski'
titles[common.SANCTI_05_08PL] = 'Św. Stanisława, Biskupa i Męczennika'
titles[common.SANCTI_05_16PL] = 'Św. Andrzeja Boboli, Męczennika'
titles[common.SANCTI_05_24PL] = 'N. M. P. Wspomożycielki Wiernych'
titles[common.SANCTI_06_01PL] = 'Bł. Jakuba Strzemię, Biskupa i Wyznawcy'
titles[common.SANCTI_06_10PL] = 'Bł. Bogumiła, Biskupa i Wyznawcy'
titles[common.SANCTI_07_18PL] = 'Bł. Szymona z Lipnicy, Wyznawcy'
titles[common.SANCTI_07_20PL] = 'Bł. Czesława, Wyznawcy'
titles[common.SANCTI_07_24PL] = 'Bł. Kingi, Dziewicy'
titles[common.SANCTI_08_26PL] = 'N. M. P. Jasnogórskiej czyli Częstochowskiej'
titles[common.SANCTI_09_01PL] = 'Bł. Bronisławy, Dziewicy'
titles[common.SANCTI_09_07PL] = 'Bł. Melchiora Grodzieckiego, Męczennika'
titles[common.SANCTI_09_25PL] = 'Bł. Władysława z Gielniowa, Wyznawcy'
titles[common.SANCTI_10_01PL] = 'Bł. Jana z Dukli'
titles[common.SANCTI_11_13PL] = 'Św. Stanisława Kostki, Wyznawcy'

section_labels = {
    'Communicantes': 'Communicantes',
    'CommunioP': 'Antyfona na Komunię (Okres Wielkanocny)',
    'Communio': 'Antyfona na Komunię',
    'Evangelium': 'Ewangelia',
    'GradualeP': 'Graduał',
    'Graduale': 'Graduał',
    'Introitus': 'Introit',
    'Lectio': 'Lekcja',
    'OffertoriumP': 'Antyfona na Ofiarowanie (Okres Wielkanocny)',
    'Offertorium': 'Antyfona na Ofiarowanie',
    'Oratio': 'Kolekta',
    'Commemoratio Oratio': 'Kolekta Wspomnienia',
    'Postcommunio': 'Pokomunia',
    'Commemoratio Postcommunio': 'Pokomunia Wspomnienia',
    'Secreta': 'Sekreta',
    'Commemoratio Secreta': 'Sekreta Wspomnienia',
    'Sequentia': 'Sekwencja',
    'Super populum': 'Modlitwa nad ludem',
    'Prefatio': 'Prefacja',
    'Tractus': 'Graduał',
    # 02-02, feast of the Purification of the B.V.M.
    'De Benedictione Candelarum': 'Poświęcenie Świec',
    'De Distributione Candelarum': 'Rozdawanie Świec',
    'De Processione': 'Procesja',
    # Quad6-0r, Dominica II Passionis seu in Palmis
    'Benedictio Palmorum': 'Poświęcenie Palm',
    'De distributione ramorum': 'Rozdawanie Gałązek',
    'De lectione Evangelica': 'Czytanie Ewangelii',
    'De processione cum ramis benedictis': 'Procesja z Poświęconymi Palmami',
    'Hymnus ad Christum Regem': 'Hymn ku Czci Chrystusa Króla',
    # Quad6-4r, Feria Quinta in Coena Domini
    'Maundi': 'Mandatum, czyli Umywanie Nóg',
    'Post Missam': 'Uroczyste Przeniesienie i Złożenie Najświętszego Sakramentu',
    'Denudatione altaris': 'Obnażenie Ołtarzy',
    # Quad6-5r, Feria Sexta in Parasceve
    'Lectiones': 'Część Pierwsza: Czytania',
    'Passio': 'Pasja',
    'Oratio Fidelium': 'Część Druga: Uroczyste Modły zwane «Modlitwą Wiernych»',
    'Crucis Adoratione': 'Część Trzecia: Uroczysta Adoracja Krzyża',
    'CommunioQ': 'Część Czwarta: Komunia Święta',
    # Quad6-5r, Sabbato Sancto
    'Benedictio ignis': 'Poświęcenie nowego ognia',
    'De benedictione cerei Paschalis': 'Poświęcenie Paschału',
    'De solemni processione': 'Uroczysta Procesja',
    'De praeconio paschali': 'Orędzie Wielkanocne',
    'De lectionibus': 'Czytania',
    'De prima parte Litaniarum': 'Pierwsza Część Litanii',
    'De benedictione aquae baptismalis': 'Poświęcenie Wody Chrzcielnej',
    'De renovatione promissionum baptismatis': 'Odnowienie Przyrzeczeń Chrztu Świętego',
    'De altera parte Litaniarum': 'Druga Część Litanii',
    'De Missa solemni Vigiliae paschalis': 'Uroczysta Msza Rezurekcyjna',
    'Pro Laudibus': 'Laudes',
    'Conclusio': 'Zakończenie',
    'Benedictio cinerum': 'Poświęcenie Popiołu'

}

section_labels_multi = {
    'GradualeL1': 'Graduał',
    'GradualeL2': 'Graduał',
    'GradualeL3': 'Graduał',
    'GradualeL4': 'Graduał',
    'GradualeL5': 'Graduał',
    'Graduale': 'Graduał',
    'LectioL1': 'Lekcja',
    'LectioL2': 'Lekcja',
    'LectioL3': 'Lekcja',
    'LectioL4': 'Lekcja',
    'LectioL5': 'Lekcja',
    'Lectio': 'Lekcja',
    'OratioL1': 'Kolekta',
    'OratioL2': 'Kolekta',
    'OratioL3': 'Kolekta',
    'OratioL4': 'Kolekta',
    'OratioL5': 'Kolekta',
    'Oratio': 'Kolekta'
}
