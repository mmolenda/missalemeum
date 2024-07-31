from ..la.translation import *
from .supplements import SUPPLEMENTS
from .pages import PAGES

TITLES = {
    constants.FERIA: "Feria",
    constants.TEMPORA_EPI1_0: "Sanctæ Familiæ Jesu Mariæ Joseph",  # Sagrada Familia de Jesús, María y José
    constants.TEMPORA_EPI1_1: "Feria II infra Hebd I post Epiphaniam",  # Lunes dentro de la Semana I después de la Epifanía
    constants.TEMPORA_EPI1_2: "Feria III infra Hebd I post Epiphaniam",  # Martes dentro de la Semana I después de la Epifanía
    constants.TEMPORA_EPI1_3: "Feria IV infra Hebd I post Epiphaniam",  # Miércoles dentro de la Semana I después de la Epifanía
    constants.TEMPORA_EPI1_4: "Feria V infra Hebd I post Epiphaniam",  # Jueves dentro de la Semana I después de la Epifanía
    constants.TEMPORA_EPI1_5: "Feria VI infra Hebd I post Epiphaniam",  # Viernes dentro de la Semana I después de la Epifanía
    constants.TEMPORA_EPI1_6: "Sabbato infra Hebd I post Epiphaniam",  # Sábado dentro de la Semana I después de la Epifanía
    constants.TEMPORA_EPI2_0: "Dominica II post Epiphaniam",  # Domingo II después de la Epifanía
    constants.TEMPORA_EPI2_1: "Feria II infra Hebd II post Epiphaniam",  # Lunes dentro de la Semana II después de la Epifanía
    constants.TEMPORA_EPI2_2: "Feria III infra Hebd II post Epiphaniam",  # Martes dentro de la Semana II después de la Epifanía
    constants.TEMPORA_EPI2_3: "Feria IV infra Hebd II post Epiphaniam",  # Miércoles dentro de la Semana II después de la Epifanía
    constants.TEMPORA_EPI2_4: "Feria V infra Hebd II post Epiphaniam",  # Jueves dentro de la Semana II después de la Epifanía
    constants.TEMPORA_EPI2_5: "Feria VI infra Hebd II post Epiphaniam",  # Viernes dentro de la Semana II después de la Epifanía
    constants.TEMPORA_EPI2_6: "Sabbato infra Hebd II post Epiphaniam",  # Sábado dentro de la Semana II después de la Epifanía
    constants.TEMPORA_EPI3_0: "Dominica III post Epiphaniam",  # Domingo III después de la Epifanía
    constants.TEMPORA_EPI3_1: "Feria II infra Hebd III post Epiphaniam",  # Lunes dentro de la Semana III después de la Epifanía
    constants.TEMPORA_EPI3_2: "Feria III infra Hebd III post Epiphaniam",  # Martes dentro de la Semana III después de la Epifanía
    constants.TEMPORA_EPI3_3: "Feria IV infra Hebd III post Epiphaniam",  # Miércoles dentro de la Semana III después de la Epifanía
    constants.TEMPORA_EPI3_4: "Feria V infra Hebd III post Epiphaniam",  # Jueves dentro de la Semana III después de la Epifanía
    constants.TEMPORA_EPI3_5: "Feria VI infra Hebd III post Epiphaniam",  # Viernes dentro de la Semana III después de la Epifanía
    constants.TEMPORA_EPI3_6: "Sabbato infra Hebd III post Epiphaniam",  # Sábado dentro de la Semana III después de la Epifanía
    constants.TEMPORA_EPI4_0: "Dominica IV post Epiphaniam",  # Domingo IV después de la Epifanía
    constants.TEMPORA_EPI4_1: "Feria II infra Hebd IV post Epiphaniam",  # Lunes dentro de la Semana IV después de la Epifanía
    constants.TEMPORA_EPI4_2: "Feria III infra Hebd IV post Epiphaniam",  # Martes dentro de la Semana IV después de la Epifanía
    constants.TEMPORA_EPI4_3: "Feria IV infra Hebd IV post Epiphaniam",  # Miércoles dentro de la Semana IV después de la Epifanía
    constants.TEMPORA_EPI4_4: "Feria V infra Hebd IV post Epiphaniam",  # Jueves dentro de la Semana IV después de la Epifanía
    constants.TEMPORA_EPI4_5: "Feria VI infra Hebd IV post Epiphaniam",  # Viernes dentro de la Semana IV después de la Epifanía
    constants.TEMPORA_EPI4_6: "Sabbato infra Hebd IV post Epiphaniam",  # Sábado dentro de la Semana IV después de la Epifanía
    constants.TEMPORA_EPI5_0: "Dominica V post Epiphaniam",  # Domingo V después de la Epifanía
    constants.TEMPORA_EPI5_1: "Feria II infra Hebd V post Epiphaniam",  # Lunes dentro de la Semana V después de la Epifanía
    constants.TEMPORA_EPI5_2: "Feria III infra Hebd V post Epiphaniam",  # Martes dentro de la Semana V después de la Epifanía
    constants.TEMPORA_EPI5_3: "Feria IV infra Hebd V post Epiphaniam",  # Miércoles dentro de la Semana V después de la Epifanía
    constants.TEMPORA_EPI5_4: "Feria V infra Hebd V post Epiphaniam",  # Jueves dentro de la Semana V después de la Epifanía
    constants.TEMPORA_EPI5_5: "Feria VI infra Hebd V post Epiphaniam",  # Viernes dentro de la Semana V después de la Epifanía
    constants.TEMPORA_EPI5_6: "Sabbato infra Hebd V post Epiphaniam",  # Sábado dentro de la Semana V después de la Epifanía
    constants.TEMPORA_EPI6_0: "Dominica VI post Epiphaniam",  # Domingo VI después de la Epifanía
    constants.TEMPORA_EPI6_1: "Feria II infra Hebd VI post Epiphaniam",  # Lunes dentro de la Semana VI después de la Epifanía
    constants.TEMPORA_EPI6_2: "Feria III infra Hebd VI post Epiphaniam",  # Martes dentro de la Semana VI después de la Epifanía
    constants.TEMPORA_EPI6_3: "Feria IV infra Hebd VI post Epiphaniam",  # Miércoles dentro de la Semana VI después de la Epifanía
    constants.TEMPORA_EPI6_4: "Feria V infra Hebd VI post Epiphaniam",  # Jueves dentro de la Semana VI después de la Epifanía
    constants.TEMPORA_EPI6_5: "Feria VI infra Hebd VI post Epiphaniam",  # Viernes dentro de la Semana VI después de la Epifanía
    constants.TEMPORA_EPI6_6: "Sabbato infra Hebd VI post Epiphaniam",  # Sábado dentro de la Semana VI después de la Epifanía
    constants.TEMPORA_QUADP1_0: "Dominica in Septuagesima",  # Domingo en Septuagésima
    constants.TEMPORA_QUADP1_1: "Feria II infra Hebd Septuagesimæ",  # Lunes dentro de la Semana de Septuagésima
    constants.TEMPORA_QUADP1_2: "Feria III infra Hebd Septuagesimæ",  # Martes dentro de la Semana de Septuagésima
    constants.TEMPORA_QUADP1_3: "Feria IV infra Hebd Septuagesimæ",  # Miércoles dentro de la Semana de Septuagésima
    constants.TEMPORA_QUADP1_4: "Feria V infra Hebd Septuagesimæ",  # Jueves dentro de la Semana de Septuagésima
    constants.TEMPORA_QUADP1_5: "Feria VI infra Hebd Septuagesimæ",  # Viernes dentro de la Semana de Septuagésima
    constants.TEMPORA_QUADP1_6: "Sabbato infra Hebd Septuagesimæ",  # Sábado dentro de la Semana de Septuagésima
    constants.TEMPORA_QUADP2_0: "Dominica in Sexagesima",  # Domingo en Sexagésima
    constants.TEMPORA_QUADP2_1: "Feria II infra Hebd Sexagesimæ",  # Lunes dentro de la Semana de Sexagésima
    constants.TEMPORA_QUADP2_2: "Feria III infra Hebd Sexagesimæ",  # Martes dentro de la Semana de Sexagésima
    constants.TEMPORA_QUADP2_3: "Feria IV infra Hebd Sexagesimæ",  # Miércoles dentro de la Semana de Sexagésima
    constants.TEMPORA_QUADP2_4: "Feria V infra Hebd Sexagesimæ",  # Jueves dentro de la Semana de Sexagésima
    constants.TEMPORA_QUADP2_5: "Feria VI infra Hebd Sexagesimæ",  # Viernes dentro de la Semana de Sexagésima
    constants.TEMPORA_QUADP2_6: "Sabbato infra Hebd Sexagesimæ",  # Sábado dentro de la Semana de Sexagésima
    constants.TEMPORA_QUADP3_0: "Dominica in Quinquagesima",  # Domingo en Quincuagésima
    constants.TEMPORA_QUADP3_1: "Feria II infra Hebd Quinquagesimæ",  # Lunes dentro de la Semana de Quincuagésima
    constants.TEMPORA_QUADP3_2: "Feria III infra Hebd Quinquagesimæ",  # Martes dentro de la Semana de Quincuagésima
    constants.TEMPORA_QUADP3_3: "Feria IV Cinerum",  # Miércoles de Ceniza
    constants.TEMPORA_QUADP3_4: "Feria V post Cineres",  # Jueves después de las Cenizas
    constants.TEMPORA_QUADP3_5: "Feria VI post Cineres",  # Viernes después de las Cenizas
    constants.TEMPORA_QUADP3_6: "Sabbato post Cineres",  # Sábado después de las Cenizas
    constants.TEMPORA_QUAD1_0: "Dominica I in Quadragesimæ",  # Domingo I de Cuaresma
    constants.TEMPORA_QUAD1_1: "Feria II infra Hebd I Quadragesimæ",  # Lunes dentro de la Semana I de Cuaresma
    constants.TEMPORA_QUAD1_2: "Feria III infra Hebd I Quadragesimæ",  # Martes dentro de la Semana I de Cuaresma
    constants.TEMPORA_QUAD1_3: "Feria IV Quatuor Temporum Quadragesimæ",  # Miércoles de las Témporas de Cuaresma
    constants.TEMPORA_QUAD1_4: "Feria V infra Hebd I Quadragesimæ",  # Jueves dentro de la Semana I de Cuaresma
    constants.TEMPORA_QUAD1_5: "Feria VI Quattuor Temporum Quadragesimæ",  # Viernes de las Témporas de Cuaresma
    constants.TEMPORA_QUAD1_6: "Sabbato Quattuor Temporum Quadragesimæ",  # Sábado de las Témporas de Cuaresma
    constants.TEMPORA_QUAD2_0: "Dominica II in Quadragesimæ",  # Domingo II de Cuaresma
    constants.TEMPORA_QUAD2_1: "Feria II infra Hebd II Quadragesimæ",  # Lunes dentro de la Semana II de Cuaresma
    constants.TEMPORA_QUAD2_2: "Feria III infra Hebd II Quadragesimæ",  # Martes dentro de la Semana II de Cuaresma
    constants.TEMPORA_QUAD2_3: "Feria IV infra Hebd II Quadragesimæ",  # Miércoles dentro de la Semana II de Cuaresma
    constants.TEMPORA_QUAD2_4: "Feria V infra Hebd II Quadragesimæ",  # Jueves dentro de la Semana II de Cuaresma
    constants.TEMPORA_QUAD2_5: "Feria VI infra Hebd II Quadragesimæ",  # Viernes dentro de la Semana II de Cuaresma
    constants.TEMPORA_QUAD2_6: "Sabbato infra Hebd II Quadragesimæ",  # Sábado dentro de la Semana II de Cuaresma
    constants.TEMPORA_QUAD3_0: "Dominica III in Quadragesimæ",  # Domingo III de Cuaresma
    constants.TEMPORA_QUAD3_1: "Feria II infra Hebd III Quadragesimæ",  # Lunes dentro de la Semana III de Cuaresma
    constants.TEMPORA_QUAD3_2: "Feria III infra Hebd III Quadragesimæ",  # Martes dentro de la Semana III de Cuaresma
    constants.TEMPORA_QUAD3_3: "Feria IV infra Hebd III Quadragesimæ",  # Miércoles dentro de la Semana III de Cuaresma
    constants.TEMPORA_QUAD3_4: "Feria V infra Hebd III Quadragesimæ",  # Jueves dentro de la Semana III de Cuaresma
    constants.TEMPORA_QUAD3_5: "Feria VI infra Hebd III Quadragesimæ",  # Viernes dentro de la Semana III de Cuaresma
    constants.TEMPORA_QUAD3_6: "Sabbato infra Hebd III Quadragesimæ",  # Sábado dentro de la Semana III de Cuaresma
    constants.TEMPORA_QUAD4_0: "Dominica IV in Quadragesimæ",  # Domingo IV de Cuaresma
    constants.TEMPORA_QUAD4_1: "Feria II infra Hebd IV Quadragesimæ",  # Lunes dentro de la Semana IV de Cuaresma
    constants.TEMPORA_QUAD4_2: "Feria III infra Hebd IV Quadragesimæ",  # Martes dentro de la Semana IV de Cuaresma
    constants.TEMPORA_QUAD4_3: "Feria IV infra Hebd IV Quadragesimæ",  # Miércoles dentro de la Semana IV de Cuaresma
    constants.TEMPORA_QUAD4_4: "Feria V infra Hebd IV Quadragesimæ",  # Jueves dentro de la Semana IV de Cuaresma
    constants.TEMPORA_QUAD4_5: "Feria VI infra Hebd IV Quadragesimæ",  # Viernes dentro de la Semana IV de Cuaresma
    constants.TEMPORA_QUAD4_6: "Sabbato infra Hebd IV Quadragesimæ",  # Sábado dentro de la Semana IV de Cuaresma
    constants.TEMPORA_QUAD5_0: "Dominica I Passionis",  # Domingo I de la Pasión
    constants.TEMPORA_QUAD5_1: "Feria II infra Hebd Passionis",  # Lunes dentro de la Semana de la Pasión
    constants.TEMPORA_QUAD5_2: "Feria III infra Hebd Passionis",  # Martes dentro de la Semana de la Pasión
    constants.TEMPORA_QUAD5_3: "Feria IV infra Hebd Passionis",  # Miércoles dentro de la Semana de la Pasión
    constants.TEMPORA_QUAD5_4: "Feria V infra Hebd Passionis",  # Jueves dentro de la Semana de la Pasión
    constants.TEMPORA_QUAD5_5: "Feria VI infra Hebd Passionis",  # Viernes dentro de la Semana de la Pasión
    constants.TEMPORA_QUAD5_6: "Sabbato infra Hebd Passionis",  # Sábado dentro de la Semana de la Pasión
    constants.TEMPORA_QUAD6_0: "Dominica II Passionis seu in Palmis",  # Domingo II de la Pasión o de Ramos
    constants.TEMPORA_QUAD6_1: "Feria II Hebdomadæ Sanctæ",  # Lunes de la Semana Santa
    constants.TEMPORA_QUAD6_2: "Feria III Hebdomadæ Sanctæ",  # Martes de la Semana Santa
    constants.TEMPORA_QUAD6_3: "Feria IV Hebdomadæ Sanctæ",  # Miércoles de la Semana Santa
    constants.TEMPORA_QUAD6_4: "Feria Quinta in Coena Domini",  # Jueves Santo en la Cena del Señor
    constants.TEMPORA_QUAD6_5: "Feria Sexta in Parasceve",  # Viernes Santo en la Pasión del Señor
    constants.TEMPORA_QUAD6_6: "Sabbato Sancto",  # Sábado Santo
    constants.TEMPORA_PASC0_0: "Dominica Resurrectionis",  # Domingo de Resurrección
    constants.TEMPORA_PASC0_1: "Die II infra octavam Paschæ",  # Lunes dentro de la octava de Pascua
    constants.TEMPORA_PASC0_2: "Die III infra octavam Paschæ",  # Martes dentro de la octava de Pascua
    constants.TEMPORA_PASC0_3: "Die VI infra octavam Paschæ",  # Miércoles dentro de la octava de Pascua
    constants.TEMPORA_PASC0_4: "Die V infra octavam Paschæ",  # Jueves dentro de la octava de Pascua
    constants.TEMPORA_PASC0_5: "Die VI infra octavam Paschæ",  # Viernes dentro de la octava de Pascua
    constants.TEMPORA_PASC0_6: "Sabbato in Albis",  # Sábado en Albis
    constants.TEMPORA_PASC1_0: "Dominica in Albis in Octava Paschæ",  # Domingo en Albis en la Octava de Pascua
    constants.TEMPORA_PASC1_1: "Feria II infra Hebd I post Octavam Paschæ",  # Lunes dentro de la Semana I después de la Octava de Pascua
    constants.TEMPORA_PASC1_2: "Feria III infra Hebd I post Octavam Paschæ",  # Martes dentro de la Semana I después de la Octava de Pascua
    constants.TEMPORA_PASC1_3: "Feria IV infra Hebd I post Octavam Paschæ",  # Miércoles dentro de la Semana I después de la Octava de Pascua
    constants.TEMPORA_PASC1_4: "Feria V infra Hebd I post Octavam Paschæ",  # Jueves dentro de la Semana I después de la Octava de Pascua
    constants.TEMPORA_PASC1_5: "Feria VI infra Hebd I post Octavam Paschæ",  # Viernes dentro de la Semana I después de la Octava de Pascua
    constants.TEMPORA_PASC1_6: "Sabbato infra Hebd I post Octavam Paschæ",  # Sábado dentro de la Semana I después de la Octava de Pascua
    constants.TEMPORA_PASC2_0: "Dominica II Post Pascha",  # Domingo II después de Pascua
    constants.TEMPORA_PASC2_1: "Feria II infra Hebd II post Octavam Paschæ",  # Lunes dentro de la Semana II después de la Octava de Pascua
    constants.TEMPORA_PASC2_2: "Feria III infra Hebd II post Octavam Paschæ",  # Martes dentro de la Semana II después de la Octava de Pascua
    constants.TEMPORA_PASC2_3: "Feria IV infra Hebd II post Octavam Paschæ",  # Miércoles dentro de la Semana II después de la Octava de Pascua
    constants.TEMPORA_PASC2_4: "Feria V infra Hebd II post Octavam Paschæ",  # Jueves dentro de la Semana II después de la Octava de Pascua
    constants.TEMPORA_PASC2_5: "Feria VI infra Hebd II post Octavam Paschæ",  # Viernes dentro de la Semana II después de la Octava de Pascua
    constants.TEMPORA_PASC2_6: "Sabbato infra Hebd II post Octavam Paschæ",  # Sábado dentro de la Semana II después de la Octava de Pascua
    constants.TEMPORA_PASC3_0: "Dominica III Post Pascha",  # Domingo III después de Pascua
    constants.TEMPORA_PASC3_1: "Feria II infra Hebd III post Octavam Paschæ",  # Lunes dentro de la Semana III después de la Octava de Pascua
    constants.TEMPORA_PASC3_2: "Feria III infra Hebd III post Octavam Paschæ",  # Martes dentro de la Semana III después de la Octava de Pascua
    constants.TEMPORA_PASC3_3: "Feria IV infra Hebd III post Octavam Paschæ",  # Miércoles dentro de la Semana III después de la Octava de Pascua
    constants.TEMPORA_PASC3_4: "Feria V infra Hebd III post Octavam Paschæ",  # Jueves dentro de la Semana III después de la Octava de Pascua
    constants.TEMPORA_PASC3_5: "Feria VI infra Hebd III post Octavam Paschæ",  # Viernes dentro de la Semana III después de la Octava de Pascua
    constants.TEMPORA_PASC3_6: "Sabbato infra Hebd III post Octavam Paschæ",  # Sábado dentro de la Semana III después de la Octava de Pascua
    constants.TEMPORA_PASC4_0: "Dominica IV Post Pascha",  # Domingo IV después de Pascua
    constants.TEMPORA_PASC4_1: "Feria II infra Hebd IV post Octavam Paschæ",  # Lunes dentro de la Semana IV después de la Octava de Pascua
    constants.TEMPORA_PASC4_2: "Feria III infra Hebd IV post Octavam Paschæ",  # Martes dentro de la Semana IV después de la Octava de Pascua
    constants.TEMPORA_PASC4_3: "Feria IV infra Hebd IV post Octavam Paschæ",  # Miércoles dentro de la Semana IV después de la Octava de Pascua
    constants.TEMPORA_PASC4_4: "Feria V infra Hebd IV post Octavam Paschæ",  # Jueves dentro de la Semana IV después de la Octava de Pascua
    constants.TEMPORA_PASC4_5: "Feria VI infra Hebd IV post Octavam Paschæ",  # Viernes dentro de la Semana IV después de la Octava de Pascua
    constants.TEMPORA_PASC4_6: "Sabbato infra Hebd IV post Octavam Paschæ",  # Sábado dentro de la Semana IV después de la Octava de Pascua
    constants.TEMPORA_PASC5_0: "Dominica V Post Pascha",  # Domingo V después de Pascua
    constants.TEMPORA_PASC5_1: "Feria II in Rogationibus",  # Lunes de Rogaciones
    constants.TEMPORA_PASC5_2: "Feria III in Rogationibus",  # Martes de Rogaciones
    constants.TEMPORA_PASC5_3: "Wigilia Wniebowstąpienia Pańskiego",  # Vigilia de la Ascensión del Señor
    constants.TEMPORA_PASC5_4: "In Ascensione Domini",  # En la Ascensión del Señor
    constants.TEMPORA_PASC5_5: "Feria VI post Ascensionem",  # Viernes después de la Ascensión
    constants.TEMPORA_PASC5_6: "Sabbato post Ascensionem",  # Sábado después de la Ascensión
    constants.TEMPORA_PASC6_0: "Dominica post Ascensionem",  # Domingo después de la Ascensión
    constants.TEMPORA_PASC6_1: "Feria II infra Hebd post Ascensionem",  # Lunes dentro de la Semana después de la Ascensión
    constants.TEMPORA_PASC6_2: "Feria III infra Hebd post Ascensionem",  # Martes dentro de la Semana después de la Ascensión
    constants.TEMPORA_PASC6_3: "Feria IV infra Hebd post Ascensionem",  # Miércoles dentro de la Semana después de la Ascensión
    constants.TEMPORA_PASC6_4: "Feria V infra Hebd post Ascensionem",  # Jueves dentro de la Semana después de la Ascensión
    constants.TEMPORA_PASC6_5: "Feria VI infra Hebd post Ascensionem",  # Viernes dentro de la Semana después de la Ascensión
    constants.TEMPORA_PASC6_6: "Sabbato in Vigilia Pentecostes",  # Sábado en la Vigilia de Pentecostés
    constants.TEMPORA_PASC7_0: "Dominica Pentecostes",  # Domingo de Pentecostés
    constants.TEMPORA_PASC7_1: "Die II infra octavam Pentecostes",  # Lunes dentro de la octava de Pentecostés
    constants.TEMPORA_PASC7_2: "Die III infra octavam Pentecostes",  # Martes dentro de la octava de Pentecostés
    constants.TEMPORA_PASC7_3: "Feria IV Quattuor Temporum Pentecostes",  # Miércoles de las Témporas de Pentecostés
    constants.TEMPORA_PASC7_4: "Die V infra octavam Pentecostes",  # Jueves dentro de la octava de Pentecostés
    constants.TEMPORA_PASC7_5: "Feria VI Quattuor temporum Pentecostes",  # Viernes de las Témporas de Pentecostés
    constants.TEMPORA_PASC7_6: "Sabbato Quattuor Temporum Pentecostes",  # Sábado de las Témporas de Pentecostés
    constants.TEMPORA_PENT01_0: "Dominica Sanctissimæ Trinitatis",  # Domingo de la Santísima Trinidad
    constants.TEMPORA_PENT01_1: "Feria II infra Hebd I post Octavam Pentecostes",  # Lunes dentro de la Semana I después de la Octava de Pentecostés
    constants.TEMPORA_PENT01_2: "Feria III infra Hebd I post Octavam Pentecostes",  # Martes dentro de la Semana I después de la Octava de Pentecostés
    constants.TEMPORA_PENT01_3: "Feria IV infra Hebd I post Octavam Pentecostes",  # Miércoles dentro de la Semana I después de la Octava de Pentecostés
    constants.TEMPORA_PENT01_4: "Festum Sanctissimi Corporis Christi",  # Fiesta del Santísimo Cuerpo de Cristo
    constants.TEMPORA_PENT01_5: "Feria V infra Hebd I post Octavam Pentecostes",  # Jueves dentro de la Semana I después de la Octava de Pentecostés
    constants.TEMPORA_PENT01_6: "Sabbato infra Hebd I post Octavam Pentecostes",  # Sábado dentro de la Semana I después de la Octava de Pentecostés
    constants.TEMPORA_PENT02_0: "Dominica II Post Pentecosten",  # Domingo II después de Pentecostés
    constants.TEMPORA_PENT02_1: "Feria II infra Hebd II post Octavam Pentecostes",  # Lunes dentro de la Semana II después de la Octava de Pentecostés
    constants.TEMPORA_PENT02_2: "Feria III infra Hebd II post Octavam Pentecostes",  # Martes dentro de la Semana II después de la Octava de Pentecostés
    constants.TEMPORA_PENT02_3: "Feria IV infra Hebd II post Octavam Pentecostes",  # Miércoles dentro de la Semana II después de la Octava de Pentecostés
    constants.TEMPORA_PENT02_4: "Feria V infra Hebd II post Octavam Pentecostes",  # Jueves dentro de la Semana II después de la Octava de Pentecostés
    constants.TEMPORA_PENT02_5: "Sanctissimi Cordis Domini Nostri Jesu Christi",  # Santísimo Corazón de Nuestro Señor Jesucristo
    constants.TEMPORA_PENT02_6: "Sabbato infra Hebd II post Octavam Pentecostes",  # Sábado dentro de la Semana II después de la Octava de Pentecostés
    constants.TEMPORA_PENT03_0: "Dominica III Post Pentecosten",  # Domingo III después de Pentecostés
    constants.TEMPORA_PENT03_1: "Feria II infra Hebd III post Octavam Pentecostes",  # Lunes dentro de la Semana III después de la Octava de Pentecostés
    constants.TEMPORA_PENT03_2: "Feria III infra Hebd III post Octavam Pentecostes",  # Martes dentro de la Semana III después de la Octava de Pentecostés
    constants.TEMPORA_PENT03_3: "Feria IV infra Hebd III post Octavam Pentecostes",  # Miércoles dentro de la Semana III después de la Octava de Pentecostés
    constants.TEMPORA_PENT03_4: "Feria V infra Hebd III post Octavam Pentecostes",  # Jueves dentro de la Semana III después de la Octava de Pentecostés
    constants.TEMPORA_PENT03_5: "Feria VI infra Hebd III post Octavam Pentecostes",  # Viernes dentro de la Semana III después de la Octava de Pentecostés
    constants.TEMPORA_PENT03_6: "Sabbato infra Hebd III post Octavam Pentecostes",  # Sábado dentro de la Semana III después de la Octava de Pentecostés
    constants.TEMPORA_PENT04_0: "Dominica IV Post Pentecosten",  # Domingo IV después de Pentecostés
    constants.TEMPORA_PENT04_1: "Feria II infra Hebd IV post Octavam Pentecostes",  # Lunes dentro de la Semana IV después de la Octava de Pentecostés
    constants.TEMPORA_PENT04_2: "Feria III infra Hebd IV post Octavam Pentecostes",  # Martes dentro de la Semana IV después de la Octava de Pentecostés
    constants.TEMPORA_PENT04_3: "Feria IV infra Hebd IV post Octavam Pentecostes",  # Miércoles dentro de la Semana IV después de la Octava de Pentecostés
    constants.TEMPORA_PENT04_4: "Feria V infra Hebd IV post Octavam Pentecostes",  # Jueves dentro de la Semana IV después de la Octava de Pentecostés
    constants.TEMPORA_PENT04_5: "Feria VI infra Hebd IV post Octavam Pentecostes",  # Viernes dentro de la Semana IV después de la Octava de Pentecostés
    constants.TEMPORA_PENT04_6: "Sabbato infra Hebd IV post Octavam Pentecostes",  # Sábado dentro de la Semana IV después de la Octava de Pentecostés
    constants.TEMPORA_PENT05_0: "Dominica V Post Pentecosten",  # Domingo V después de Pentecostés
    constants.TEMPORA_PENT05_1: "Feria II infra Hebd V post Octavam Pentecostes",  # Lunes dentro de la Semana V después de la Octava de Pentecostés
    constants.TEMPORA_PENT05_2: "Feria III infra Hebd V post Octavam Pentecostes",  # Martes dentro de la Semana V después de la Octava de Pentecostés
    constants.TEMPORA_PENT05_3: "Feria IV infra Hebd V post Octavam Pentecostes",  # Miércoles dentro de la Semana V después de la Octava de Pentecostés
    constants.TEMPORA_PENT05_4: "Feria V infra Hebd V post Octavam Pentecostes",  # Jueves dentro de la Semana V después de la Octava de Pentecostés
    constants.TEMPORA_PENT05_5: "Feria VI infra Hebd V post Octavam Pentecostes",  # Viernes dentro de la Semana V después de la Octava de Pentecostés
    constants.TEMPORA_PENT05_6: "Sabbato infra Hebd V post Octavam Pentecostes",  # Sábado dentro de la Semana V después de la Octava de Pentecostés
    constants.TEMPORA_PENT06_0: "Dominica VI Post Pentecosten",  # Domingo VI después de Pentecostés
    constants.TEMPORA_PENT06_1: "Feria II infra Hebd VI post Octavam Pentecostes",  # Lunes dentro de la Semana VI después de la Octava de Pentecostés
    constants.TEMPORA_PENT06_2: "Feria III infra Hebd VI post Octavam Pentecostes",  # Martes dentro de la Semana VI después de la Octava de Pentecostés
    constants.TEMPORA_PENT06_3: "Feria IV infra Hebd VI post Octavam Pentecostes",  # Miércoles dentro de la Semana VI después de la Octava de Pentecostés
    constants.TEMPORA_PENT06_4: "Feria V infra Hebd VI post Octavam Pentecostes",  # Jueves dentro de la Semana VI después de la Octava de Pentecostés
    constants.TEMPORA_PENT06_5: "Feria VI infra Hebd VI post Octavam Pentecostes",  # Viernes dentro de la Semana VI después de la Octava de Pentecostés
    constants.TEMPORA_PENT06_6: "Sabbato infra Hebd VI post Octavam Pentecostes",  # Sábado dentro de la Semana VI después de la Octava de Pentecostés
    constants.TEMPORA_PENT07_0: "Dominica VII Post Pentecosten",  # Domingo VII después de Pentecostés
    constants.TEMPORA_PENT07_1: "Feria II infra Hebd VII post Octavam Pentecostes",  # Lunes dentro de la Semana VII después de la Octava de Pentecostés
    constants.TEMPORA_PENT07_2: "Feria III infra Hebd VII post Octavam Pentecostes",  # Martes dentro de la Semana VII después de la Octava de Pentecostés
    constants.TEMPORA_PENT07_3: "Feria IV infra Hebd VII post Octavam Pentecostes",  # Miércoles dentro de la Semana VII después de la Octava de Pentecostés
    constants.TEMPORA_PENT07_4: "Feria V infra Hebd VII post Octavam Pentecostes",  # Jueves dentro de la Semana VII después de la Octava de Pentecostés
    constants.TEMPORA_PENT07_5: "Feria VI infra Hebd VII post Octavam Pentecostes",  # Viernes dentro de la Semana VII después de la Octava de Pentecostés
    constants.TEMPORA_PENT07_6: "Sabbato infra Hebd VII post Octavam Pentecostes",  # Sábado dentro de la Semana VII después de la Octava de Pentecostés
    constants.TEMPORA_PENT08_0: "Dominica VIII Post Pentecosten",  # Domingo VIII después de Pentecostés
    constants.TEMPORA_PENT08_1: "Feria II infra Hebd VIII post Octavam Pentecostes",  # Lunes dentro de la Semana VIII después de la Octava de Pentecostés
    constants.TEMPORA_PENT08_2: "Feria III infra Hebd VIII post Octavam Pentecostes",  # Martes dentro de la Semana VIII después de la Octava de Pentecostés
    constants.TEMPORA_PENT08_3: "Feria IV infra Hebd VIII post Octavam Pentecostes",  # Miércoles dentro de la Semana VIII después de la Octava de Pentecostés
    constants.TEMPORA_PENT08_4: "Feria V infra Hebd VIII post Octavam Pentecostes",  # Jueves dentro de la Semana VIII después de la Octava de Pentecostés
    constants.TEMPORA_PENT08_5: "Feria VI infra Hebd VIII post Octavam Pentecostes",  # Viernes dentro de la Semana VIII después de la Octava de Pentecostés
    constants.TEMPORA_PENT08_6: "Sabbato infra Hebd VIII post Octavam Pentecostes",  # Sábado dentro de la Semana VIII después de la Octava de Pentecostés
    constants.TEMPORA_PENT09_0: "Dominica IX Post Pentecosten",  # Domingo IX después de Pentecostés
    constants.TEMPORA_PENT09_1: "Feria II infra Hebd IX post Octavam Pentecostes",  # Lunes dentro de la Semana IX después de la Octava de Pentecostés
    constants.TEMPORA_PENT09_2: "Feria III infra Hebd IX post Octavam Pentecostes",  # Martes dentro de la Semana IX después de la Octava de Pentecostés
    constants.TEMPORA_PENT09_3: "Feria IV infra Hebd IX post Octavam Pentecostes",  # Miércoles dentro de la Semana IX después de la Octava de Pentecostés
    constants.TEMPORA_PENT09_4: "Feria V infra Hebd IX post Octavam Pentecostes",  # Jueves dentro de la Semana IX después de la Octava de Pentecostés
    constants.TEMPORA_PENT09_5: "Feria VI infra Hebd IX post Octavam Pentecostes",  # Viernes dentro de la Semana IX después de la Octava de Pentecostés
    constants.TEMPORA_PENT09_6: "Sabbato infra Hebd IX post Octavam Pentecostes",  # Sábado dentro de la Semana IX después de la Octava de Pentecostés
    constants.TEMPORA_PENT10_0: "Dominica X Post Pentecosten",  # Domingo X después de Pentecostés
    constants.TEMPORA_PENT10_1: "Feria II infra Hebd X post Octavam Pentecostes",  # Lunes dentro de la Semana X después de la Octava de Pentecostés
    constants.TEMPORA_PENT10_2: "Feria III infra Hebd X post Octavam Pentecostes",  # Martes dentro de la Semana X después de la Octava de Pentecostés
    constants.TEMPORA_PENT10_3: "Feria IV infra Hebd X post Octavam Pentecostes",  # Miércoles dentro de la Semana X después de la Octava de Pentecostés
    constants.TEMPORA_PENT10_4: "Feria V infra Hebd X post Octavam Pentecostes",  # Jueves dentro de la Semana X después de la Octava de Pentecostés
    constants.TEMPORA_PENT10_5: "Feria VI infra Hebd X post Octavam Pentecostes",  # Viernes dentro de la Semana X después de la Octava de Pentecostés
    constants.TEMPORA_PENT10_6: "Sabbato infra Hebd X post Octavam Pentecostes",  # Sábado dentro de la Semana X después de la Octava de Pentecostés
    constants.TEMPORA_PENT11_0: "Dominica XI Post Pentecosten",  # Domingo XI después de Pentecostés
    constants.TEMPORA_PENT11_1: "Feria II infra Hebd XI post Octavam Pentecostes",  # Lunes dentro de la Semana XI después de la Octava de Pentecostés
    constants.TEMPORA_PENT11_2: "Feria III infra Hebd XI post Octavam Pentecostes",  # Martes dentro de la Semana XI después de la Octava de Pentecostés
    constants.TEMPORA_PENT11_3: "Feria IV infra Hebd XI post Octavam Pentecostes",  # Miércoles dentro de la Semana XI después de la Octava de Pentecostés
    constants.TEMPORA_PENT11_4: "Feria V infra Hebd XI post Octavam Pentecostes",  # Jueves dentro de la Semana XI después de la Octava de Pentecostés
    constants.TEMPORA_PENT11_5: "Feria VI infra Hebd XI post Octavam Pentecostes",  # Viernes dentro de la Semana XI después de la Octava de Pentecostés
    constants.TEMPORA_PENT11_6: "Sabbato infra Hebd XI post Octavam Pentecostes",  # Sábado dentro de la Semana XI después de la Octava de Pentecostés
    constants.TEMPORA_PENT12_0: "Dominica XII Post Pentecosten",  # Domingo XII después de Pentecostés
    constants.TEMPORA_PENT12_1: "Feria II infra Hebd XII post Octavam Pentecostes",  # Lunes dentro de la Semana XII después de la Octava de Pentecostés
    constants.TEMPORA_PENT12_2: "Feria III infra Hebd XII post Octavam Pentecostes",  # Martes dentro de la Semana XII después de la Octava de Pentecostés
    constants.TEMPORA_PENT12_3: "Feria IV infra Hebd XII post Octavam Pentecostes",  # Miércoles dentro de la Semana XII después de la Octava de Pentecostés
    constants.TEMPORA_PENT12_4: "Feria V infra Hebd XII post Octavam Pentecostes",  # Jueves dentro de la Semana XII después de la Octava de Pentecostés
    constants.TEMPORA_PENT12_5: "Feria VI infra Hebd XII post Octavam Pentecostes",  # Viernes dentro de la Semana XII después de la Octava de Pentecostés
    constants.TEMPORA_PENT12_6: "Sabbato infra Hebd XII post Octavam Pentecostes",  # Sábado dentro de la Semana XII después de la Octava de Pentecostés
    constants.TEMPORA_PENT13_0: "Dominica XIII Post Pentecosten",  # Domingo XIII después de Pentecostés
    constants.TEMPORA_PENT13_1: "Feria II infra Hebd XIII post Octavam Pentecostes",  # Lunes dentro de la Semana XIII después de la Octava de Pentecostés
    constants.TEMPORA_PENT13_2: "Feria III infra Hebd XIII post Octavam Pentecostes",  # Martes dentro de la Semana XIII después de la Octava de Pentecostés
    constants.TEMPORA_PENT13_3: "Feria IV infra Hebd XIII post Octavam Pentecostes",  # Miércoles dentro de la Semana XIII después de la Octava de Pentecostés
    constants.TEMPORA_PENT13_4: "Feria V infra Hebd XIII post Octavam Pentecostes",  # Jueves dentro de la Semana XIII después de la Octava de Pentecostés
    constants.TEMPORA_PENT13_5: "Feria VI infra Hebd XIII post Octavam Pentecostes",  # Viernes dentro de la Semana XIII después de la Octava de Pentecostés
    constants.TEMPORA_PENT13_6: "Sabbato infra Hebd XIII post Octavam Pentecostes",  # Sábado dentro de la Semana XIII después de la Octava de Pentecostés
    constants.TEMPORA_PENT14_0: "Dominica XIV Post Pentecosten",  # Domingo XIV después de Pentecostés
    constants.TEMPORA_PENT14_1: "Feria II infra Hebd XIV post Octavam Pentecostes",  # Lunes dentro de la Semana XIV después de la Octava de Pentecostés
    constants.TEMPORA_PENT14_2: "Feria III infra Hebd XIV post Octavam Pentecostes",  # Martes dentro de la Semana XIV después de la Octava de Pentecostés
    constants.TEMPORA_PENT14_3: "Feria IV infra Hebd XIV post Octavam Pentecostes",  # Miércoles dentro de la Semana XIV después de la Octava de Pentecostés
    constants.TEMPORA_PENT14_4: "Feria V infra Hebd XIV post Octavam Pentecostes",  # Jueves dentro de la Semana XIV después de la Octava de Pentecostés
    constants.TEMPORA_PENT14_5: "Feria VI infra Hebd XIV post Octavam Pentecostes",  # Viernes dentro de la Semana XIV después de la Octava de Pentecostés
    constants.TEMPORA_PENT14_6: "Sabbato infra Hebd XIV post Octavam Pentecostes",  # Sábado dentro de la Semana XIV después de la Octava de Pentecostés
    constants.TEMPORA_PENT15_0: "Dominica XV Post Pentecosten",  # Domingo XV después de Pentecostés
    constants.TEMPORA_PENT15_1: "Feria II infra Hebd XV post Octavam Pentecostes",  # Lunes dentro de la Semana XV después de la Octava de Pentecostés
    constants.TEMPORA_PENT15_2: "Feria III infra Hebd XV post Octavam Pentecostes",  # Martes dentro de la Semana XV después de la Octava de Pentecostés
    constants.TEMPORA_PENT15_3: "Feria IV infra Hebd XV post Octavam Pentecostes",  # Miércoles dentro de la Semana XV después de la Octava de Pentecostés
    constants.TEMPORA_PENT15_4: "Feria V infra Hebd XV post Octavam Pentecostes",  # Jueves dentro de la Semana XV después de la Octava de Pentecostés
    constants.TEMPORA_PENT15_5: "Feria VI infra Hebd XV post Octavam Pentecostes",  # Viernes dentro de la Semana XV después de la Octava de Pentecostés
    constants.TEMPORA_PENT15_6: "Sabbato infra Hebd XV post Octavam Pentecostes",  # Sábado dentro de la Semana XV después de la Octava de Pentecostés
    constants.TEMPORA_PENT16_0: "Dominica XVI Post Pentecosten",  # Domingo XVI después de Pentecostés
    constants.TEMPORA_PENT16_1: "Feria II infra Hebd XVI post Octavam Pentecostes",  # Lunes dentro de la Semana XVI después de la Octava de Pentecostés
    constants.TEMPORA_PENT16_2: "Feria III infra Hebd XVI post Octavam Pentecostes",  # Martes dentro de la Semana XVI después de la Octava de Pentecostés
    constants.TEMPORA_PENT16_3: "Feria IV infra Hebd XVI post Octavam Pentecostes",  # Miércoles dentro de la Semana XVI después de la Octava de Pentecostés
    constants.TEMPORA_PENT16_4: "Feria V infra Hebd XVI post Octavam Pentecostes",  # Jueves dentro de la Semana XVI después de la Octava de Pentecostés
    constants.TEMPORA_PENT16_5: "Feria VI infra Hebd XVI post Octavam Pentecostes",  # Viernes dentro de la Semana XVI después de la Octava de Pentecostés
    constants.TEMPORA_PENT16_6: "Sabbato infra Hebd XVI post Octavam Pentecostes",  # Sábado dentro de la Semana XVI después de la Octava de Pentecostés
    constants.TEMPORA_PENT17_0: "Dominica XVII Post Pentecosten",  # Domingo XVII después de Pentecostés
    constants.TEMPORA_PENT17_1: "Feria II infra Hebd XVII post Octavam Pentecostes",  # Lunes dentro de la Semana XVII después de la Octava de Pentecostés
    constants.TEMPORA_PENT17_2: "Feria III infra Hebd XVII post Octavam Pentecostes",  # Martes dentro de la Semana XVII después de la Octava de Pentecostés
    constants.TEMPORA_PENT17_3: "Feria IV infra Hebd XVII post Octavam Pentecostes",  # Miércoles dentro de la Semana XVII después de la Octava de Pentecostés
    constants.TEMPORA_PENT17_4: "Feria V infra Hebd XVII post Octavam Pentecostes",  # Jueves dentro de la Semana XVII después de la Octava de Pentecostés
    constants.TEMPORA_PENT17_5: "Feria VI infra Hebd XVII post Octavam Pentecostes",  # Viernes dentro de la Semana XVII después de la Octava de Pentecostés
    constants.TEMPORA_PENT17_6: "Sabbato infra Hebd XVII post Octavam Pentecostes",  # Sábado dentro de la Semana XVII después de la Octava de Pentecostés
    constants.TEMPORA_PENT18_0: "Dominica XVIII Post Pentecosten",  # Domingo XVIII después de Pentecostés
    constants.TEMPORA_PENT18_1: "Feria II infra Hebd XVIII post Octavam Pentecostes",  # Lunes dentro de la Semana XVIII después de la Octava de Pentecostés
    constants.TEMPORA_PENT18_2: "Feria III infra Hebd XVIII post Octavam Pentecostes",  # Martes dentro de la Semana XVIII después de la Octava de Pentecostés
    constants.TEMPORA_PENT18_3: "Feria IV infra Hebd XVIII post Octavam Pentecostes",  # Miércoles dentro de la Semana XVIII después de la Octava de Pentecostés
    constants.TEMPORA_PENT18_4: "Feria V infra Hebd XVIII post Octavam Pentecostes",  # Jueves dentro de la Semana XVIII después de la Octava de Pentecostés
    constants.TEMPORA_PENT18_5: "Feria VI infra Hebd XVIII post Octavam Pentecostes",  # Viernes dentro de la Semana XVIII después de la Octava de Pentecostés
    constants.TEMPORA_PENT18_6: "Sabbato infra Hebd XVIII post Octavam Pentecostes",  # Sábado dentro de la Semana XVIII después de la Octava de Pentecostés
    constants.TEMPORA_PENT19_0: "Dominica XIX Post Pentecosten",  # Domingo XIX después de Pentecostés
    constants.TEMPORA_PENT19_1: "Feria II infra Hebd XIX post Octavam Pentecostes",  # Lunes dentro de la Semana XIX después de la Octava de Pentecostés
    constants.TEMPORA_PENT19_2: "Feria III infra Hebd XIX post Octavam Pentecostes",  # Martes dentro de la Semana XIX después de la Octava de Pentecostés
    constants.TEMPORA_PENT19_3: "Feria IV infra Hebd XIX post Octavam Pentecostes",  # Miércoles dentro de la Semana XIX después de la Octava de Pentecostés
    constants.TEMPORA_PENT19_4: "Feria V infra Hebd XIX post Octavam Pentecostes",  # Jueves dentro de la Semana XIX después de la Octava de Pentecostés
    constants.TEMPORA_PENT19_5: "Feria VI infra Hebd XIX post Octavam Pentecostes",  # Viernes dentro de la Semana XIX después de la Octava de Pentecostés
    constants.TEMPORA_PENT19_6: "Sabbato infra Hebd XIX post Octavam Pentecostes",  # Sábado dentro de la Semana XIX después de la Octava de Pentecostés
    constants.TEMPORA_PENT20_0: "Dominica XX Post Pentecosten",  # Domingo XX después de Pentecostés
    constants.TEMPORA_PENT20_1: "Feria II infra Hebd XX post Octavam Pentecostes",  # Lunes dentro de la Semana XX después de la Octava de Pentecostés
    constants.TEMPORA_PENT20_2: "Feria III infra Hebd XX post Octavam Pentecostes",  # Martes dentro de la Semana XX después de la Octava de Pentecostés
    constants.TEMPORA_PENT20_3: "Feria IV infra Hebd XX post Octavam Pentecostes",  # Miércoles dentro de la Semana XX después de la Octava de Pentecostés
    constants.TEMPORA_PENT20_4: "Feria V infra Hebd XX post Octavam Pentecostes",  # Jueves dentro de la Semana XX después de la Octava de Pentecostés
    constants.TEMPORA_PENT20_5: "Feria VI infra Hebd XX post Octavam Pentecostes",  # Viernes dentro de la Semana XX después de la Octava de Pentecostés
    constants.TEMPORA_PENT20_6: "Sabbato infra Hebd XX post Octavam Pentecostes",  # Sábado dentro de la Semana XX después de la Octava de Pentecostés
    constants.TEMPORA_PENT21_0: "Dominica XXI Post Pentecosten",  # Domingo XXI después de Pentecostés
    constants.TEMPORA_PENT21_1: "Feria II infra Hebd XXI post Octavam Pentecostes",  # Lunes dentro de la Semana XXI después de la Octava de Pentecostés
    constants.TEMPORA_PENT21_2: "Feria III infra Hebd XXI post Octavam Pentecostes",  # Martes dentro de la Semana XXI después de la Octava de Pentecostés
    constants.TEMPORA_PENT21_3: "Feria IV infra Hebd XXI post Octavam Pentecostes",  # Miércoles dentro de la Semana XXI después de la Octava de Pentecostés
    constants.TEMPORA_PENT21_4: "Feria V infra Hebd XXI post Octavam Pentecostes",  # Jueves dentro de la Semana XXI después de la Octava de Pentecostés
    constants.TEMPORA_PENT21_5: "Feria VI infra Hebd XXI post Octavam Pentecostes",  # Viernes dentro de la Semana XXI después de la Octava de Pentecostés
    constants.TEMPORA_PENT21_6: "Sabbato infra Hebd XXI post Octavam Pentecostes",  # Sábado dentro de la Semana XXI después de la Octava de Pentecostés
    constants.TEMPORA_PENT22_0: "Dominica XXII Post Pentecosten",  # Domingo XXII después de Pentecostés
    constants.TEMPORA_PENT22_1: "Feria II infra Hebd XXII post Octavam Pentecostes",  # Lunes dentro de la Semana XXII después de la Octava de Pentecostés
    constants.TEMPORA_PENT22_2: "Feria III infra Hebd XXII post Octavam Pentecostes",  # Martes dentro de la Semana XXII después de la Octava de Pentecostés
    constants.TEMPORA_PENT22_3: "Feria IV infra Hebd XXII post Octavam Pentecostes",  # Miércoles dentro de la Semana XXII después de la Octava de Pentecostés
    constants.TEMPORA_PENT22_4: "Feria V infra Hebd XXII post Octavam Pentecostes",  # Jueves dentro de la Semana XXII después de la Octava de Pentecostés
    constants.TEMPORA_PENT22_5: "Feria VI infra Hebd XXII post Octavam Pentecostes",  # Viernes dentro de la Semana XXII después de la Octava de Pentecostés
    constants.TEMPORA_PENT22_6: "Sabbato infra Hebd XXII post Octavam Pentecostes",  # Sábado dentro de la Semana XXII después de la Octava de Pentecostés
    constants.TEMPORA_PENT23_0: "Dominica XXIII Post Pentecosten",  # Domingo XXIII después de Pentecostés
    constants.TEMPORA_PENT23_1: "Feria II infra Hebd XXIII post Octavam Pentecostes",  # Lunes dentro de la Semana XXIII después de la Octava de Pentecostés
    constants.TEMPORA_PENT23_2: "Feria III infra Hebd XXIII post Octavam Pentecostes",  # Martes dentro de la Semana XXIII después de la Octava de Pentecostés
    constants.TEMPORA_PENT23_3: "Feria IV infra Hebd XXIII post Octavam Pentecostes",  # Miércoles dentro de la Semana XXIII después de la Octava de Pentecostés
    constants.TEMPORA_PENT23_4: "Feria V infra Hebd XXIII post Octavam Pentecostes",  # Jueves dentro de la Semana XXIII después de la Octava de Pentecostés
    constants.TEMPORA_PENT23_5: "Feria VI infra Hebd XXIII post Octavam Pentecostes",  # Viernes dentro de la Semana XXIII después de la Octava de Pentecostés
    constants.TEMPORA_PENT23_6: "Sabbato infra Hebd XXIII post Octavam Pentecostes",  # Sábado dentro de la Semana XXIII después de la Octava de Pentecostés
    constants.TEMPORA_PENT_3: "Feria IV Quattuor Temporum Septembris",  # Miércoles de las Témporas de Septiembre
    constants.TEMPORA_PENT_5: "Feria VI Quattuor Temporum Septembris",  # Viernes de las Témporas de Septiembre
    constants.TEMPORA_PENT_6: "Sabbato Quattuor Temporum Septembris",  # Sábado de las Témporas de Septiembre
    constants.TEMPORA_PENT24_0: "Dominica XXIV Post Pentecosten",  # Domingo XXIV después de Pentecostés
    constants.TEMPORA_PENT24_1: "Feria II infra Hebd XXIV post Octavam Pentecostes",  # Lunes dentro de la Semana XXIV después de la Octava de Pentecostés
    constants.TEMPORA_PENT24_2: "Feria III infra Hebd XXIV post Octavam Pentecostes",  # Martes dentro de la Semana XXIV después de la Octava de Pentecostés
    constants.TEMPORA_PENT24_3: "Feria IV infra Hebd XXIV post Octavam Pentecostes",  # Miércoles dentro de la Semana XXIV después de la Octava de Pentecostés
    constants.TEMPORA_PENT24_4: "Feria V infra Hebd XXIV post Octavam Pentecostes",  # Jueves dentro de la Semana XXIV después de la Octava de Pentecostés
    constants.TEMPORA_PENT24_5: "Feria VI infra Hebd XXIV post Octavam Pentecostes",  # Viernes dentro de la Semana XXIV después de la Octava de Pentecostés
    constants.TEMPORA_PENT24_6: "Sabbato infra Hebd XXIV post Octavam Pentecostes",  # Sábado dentro de la Semana XXIV después de la Octava de Pentecostés
    constants.TEMPORA_ADV1_0: "Dominica I Adventus",  # Domingo I de Adviento
    constants.TEMPORA_ADV1_1: "Feria II infra Hebd I Adventus",  # Lunes dentro de la Semana I de Adviento
    constants.TEMPORA_ADV1_2: "Feria III infra Hebd I Adventus",  # Martes dentro de la Semana I de Adviento
    constants.TEMPORA_ADV1_3: "Feria IV infra Hebd I Adventus",  # Miércoles dentro de la Semana I de Adviento
    constants.TEMPORA_ADV1_4: "Feria V infra Hebd I Adventus",  # Jueves dentro de la Semana I de Adviento
    constants.TEMPORA_ADV1_5: "Feria VI infra Hebd I Adventus",  # Viernes dentro de la Semana I de Adviento
    constants.TEMPORA_ADV1_6: "Sabbato infra Hebd I Adventus",  # Sábado dentro de la Semana I de Adviento
    constants.TEMPORA_ADV2_0: "Dominica II Adventus",  # Domingo II de Adviento
    constants.TEMPORA_ADV2_1: "Feria II infra Hebd II Adventus",  # Lunes dentro de la Semana II de Adviento
    constants.TEMPORA_ADV2_2: "Feria III infra Hebd II Adventus",  # Martes dentro de la Semana II de Adviento
    constants.TEMPORA_ADV2_3: "Feria IV infra Hebd II Adventus",  # Miércoles dentro de la Semana II de Adviento
    constants.TEMPORA_ADV2_4: "Feria V infra Hebd II Adventus",  # Jueves dentro de la Semana II de Adviento
    constants.TEMPORA_ADV2_5: "Feria VI infra Hebd II Adventus",  # Viernes dentro de la Semana II de Adviento
    constants.TEMPORA_ADV2_6: "Sabbato infra Hebd II Adventus",  # Sábado dentro de la Semana II de Adviento
    constants.TEMPORA_ADV3_0: "Dominica III Adventus",  # Domingo III de Adviento
    constants.TEMPORA_ADV3_1: "Feria II infra Hebd IV Adventus",  # Lunes dentro de la Semana IV de Adviento
    constants.TEMPORA_ADV3_2: "Feria III infra Hebd IV Adventus",  # Martes dentro de la Semana IV de Adviento
    constants.TEMPORA_ADV3_3: "Feria IV Quattuor Temporum Adventus",  # Miércoles de las Témporas de Adviento
    constants.TEMPORA_ADV3_4: "Feria V infra Hebd IV Adventus",  # Jueves dentro de la Semana IV de Adviento
    constants.TEMPORA_ADV3_5: "Feria VI Quattuor Temporum Adventus",  # Viernes de las Témporas de Adviento
    constants.TEMPORA_ADV3_6: "Sabbato Temporum Adventus",  # Sábado de las Témporas de Adviento
    constants.TEMPORA_ADV4_0: "Dominica IV Adventus",  # Domingo IV de Adviento
    constants.TEMPORA_ADV4_1: "Feria II infra Hebd IV Adventus",  # Lunes dentro de la Semana IV de Adviento
    constants.TEMPORA_ADV4_2: "Feria III infra Hebd IV Adventus",  # Martes dentro de la Semana IV de Adviento
    constants.TEMPORA_ADV4_3: "Feria IV infra Hebd IV Adventus",  # Miércoles dentro de la Semana IV de Adviento
    constants.TEMPORA_ADV4_4: "Feria V infra Hebd IV Adventus",  # Jueves dentro de la Semana IV de Adviento
    constants.TEMPORA_ADV4_5: "Feria VI infra Hebd IV Adventus",  # Viernes dentro de la Semana IV de Adviento
    constants.TEMPORA_NAT1_0: "Dominica Infra Octavam Nativitatis",  # Domingo dentro de la Octava de Navidad
    constants.TEMPORA_NAT1_1: "Feria Infra Octavam Nativitatis",  # Día dentro de la Octava de Navidad
    constants.TEMPORA_NAT2_0: "Sanctissimi Nominis Jesu",  # Santísimo Nombre de Jesús
    constants.SANCTI_10_DU: "In festo Domino nostro Jesu Christi Regis",  # En la fiesta de nuestro Señor Jesucristo Rey
    constants.TEMPORA_EPI1_0A: "Dominica post Epiphaniam",  # Domingo después de la Epifanía
    constants.TEMPORA_PENT01_0A: "Dominica Post Pentecosten",  # Domingo después de Pentecostés
    constants.TEMPORA_C_10A: "1 Missa B. V. M. – Rorate",  # 1 Misa de la B. V. M. – Rorate
    constants.COMMUNE_C_10A: "1 Missa B. V. M. – Rorate",  # 1 Misa de la B. V. M. – Rorate
    constants.TEMPORA_C_10B: "2 Missa B. V. M. – Vultum Tuum",  # 2 Misa de la B. V. M. – Vultum Tuum
    constants.COMMUNE_C_10B: "2 Missa B. V. M. – Vultum Tuum",  # 2 Misa de la B. V. M. – Vultum Tuum
    constants.TEMPORA_C_10C: "3 Missa B. V. M. – Salve, Sancta Parens",  # 3 Misa de la B. V. M. – Salve, Sancta Parens
    constants.COMMUNE_C_10C: "3 Missa B. V. M. – Salve, Sancta Parens",  # 3 Misa de la B. V. M. – Salve, Sancta Parens
    constants.TEMPORA_C_10PASC: "4 Missa B. V. M. – Salve, Sancta Parens",  # 4 Misa de la B. V. M. – Salve, Sancta Parens
    constants.COMMUNE_C_10PASC: "4 Missa B. V. M. – Salve, Sancta Parens",  # 4 Misa de la B. V. M. – Salve, Sancta Parens
    constants.TEMPORA_C_10T: "5 Missa B. V. M. – Salve, Sancta Parens",  # 5 Misa de la B. V. M. – Salve, Sancta Parens
    constants.COMMUNE_C_10T: "5 Missa B. V. M. – Salve, Sancta Parens",  # 5 Misa de la B. V. M. – Salve, Sancta Parens
    constants.COMMUNE_C5: "Commune Confessoris non pontificis; Os justi",  # Común del Confesor no Pontífice; Os justi
    constants.COMMUNE_C5B: "Commune Confessoris non pontificis; Iustus ut palma",  # Común del Confesor no Pontífice; Iustus ut palma
    constants.COMMUNE_C2C: "Commune Unius Martyris Pontificis, Statuit",  # Común de un Mártir Pontífice, Statuit
    constants.COMMUNE_C2B: "Commune Unius Martyris Pontificis, Sacerdotes Dei",  # Común de un Mártir Pontífice, Sacerdotes Dei
    constants.SANCTI_01_01: "Die Octavæ Nativitatis Domini",  # Día de la Octava de Navidad del Señor
    constants.SANCTI_01_06: "In Epiphania Domini",  # En la Epifanía del Señor
    constants.SANCTI_01_13: "In Commemoratione Baptismatis Domini Nostri Jesu Christi",  # En la Conmemoración del Bautismo de Nuestro Señor Jesucristo
    constants.SANCTI_01_14: "S. Hilarii Episcopi Confessoris Ecclesiæ Doctoris",  # S. Hilario Obispo Confesor Doctor de la Iglesia
    constants.SANCTI_01_15: "S. Pauli Primi Eremitæ et Confessoris",  # S. Pablo Primer Ermitaño y Confesor
    constants.SANCTI_01_16: "S. Marcelli Papæ et Martyris",  # S. Marcelo Papa y Mártir
    constants.SANCTI_01_17: "S. S. Antonii Abbatis",  # S. Antonio Abad
    constants.SANCTI_01_18: "S. Priscæ Virginis",  # S. Prisca Virgen
    constants.SANCTI_01_19: "S. Marii et Soc. Mart.",  # S. Mario y Compañeros Mártires
    constants.SANCTI_01_20: "Ss. Fabiani et Sebastiani Martyrum",  # Ss. Fabián y Sebastián Mártires
    constants.SANCTI_01_21: "S. Agnetis Virginis et Martyris",  # S. Inés Virgen y Mártir
    constants.SANCTI_01_22: "Ss. Vincentii et Anastasii Martyrum",  # Ss. Vicente y Anastasio Mártires
    constants.SANCTI_01_23: "S. Raymundi de Penafort Confessoris",  # S. Raimundo de Peñafort Confesor
    constants.SANCTI_01_24: "S. Timothei Episcopi et Martyris",  # S. Timoteo Obispo y Mártir
    constants.SANCTI_01_25: "In Conversione S. Pauli Apostoli",  # En la Conversión de S. Pablo Apóstol
    constants.SANCTI_01_26: "S. Polycarpi Episcopi et Martyris",  # S. Policarpo Obispo y Mártir
    constants.SANCTI_01_27: "S. Joannis Chrysostomi Episcopi Confessoris Ecclesiæ Doctoris",  # S. Juan Crisóstomo Obispo Confesor Doctor de la Iglesia
    constants.SANCTI_01_28: "S. Petri Nolasci Confessoris",  # S. Pedro Nolasco Confesor
    constants.SANCTI_01_29: "S. Francisci Salesii Episcopi Confessoris Ecclesiæ Doctoris",  # S. Francisco de Sales Obispo Confesor Doctor de la Iglesia
    constants.SANCTI_01_30: "S. Martinæ Virginis et Martyris",  # S. Martina Virgen y Mártir
    constants.SANCTI_01_31: "S. Joannis Bosco Confessoris",  # S. Juan Bosco Confesor
    constants.SANCTI_02_01: "S. Ignatii Episcopi et Martyris",  # S. Ignacio Obispo y Mártir
    constants.SANCTI_02_02: "In Purificatione Beatæ Mariæ Virginis",  # En la Purificación de la Bienaventurada Virgen María
    constants.SANCTI_02_03: "S. Blasii Episcopi",  # S. Blas Obispo
    constants.SANCTI_02_04: "S. Andreæ Corsini Episcopi et Confessoris",  # S. Andrés Corsini Obispo y Confesor
    constants.SANCTI_02_05: "S. Agathæ Virginis et Martyris",  # S. Águeda Virgen y Mártir
    constants.SANCTI_02_06: "S. Titi Episc. et Confessoris",  # S. Tito Obispo y Confesor
    constants.SANCTI_02_07: "S. Romualdi Abbatis",  # S. Romualdo Abad
    constants.SANCTI_02_08: "S. Joannis de Matha Confessoris",  # S. Juan de Mata Confesor
    constants.SANCTI_02_09: "S. Cyrilli Episc. Alexandrini Confessoris Ecclesiæ Doctoris",  # S. Cirilo Obispo de Alejandría Confesor Doctor de la Iglesia
    constants.SANCTI_02_10: "S. Scholasticæ Virginis",  # S. Escolástica Virgen
    constants.SANCTI_02_11: "In Apparitione Beatæ Mariæ Virginis",  # En la Aparición de la Bienaventurada Virgen María
    constants.SANCTI_02_12: "Ss. Septem Fundat. Ord. Servorum B. M. V.",  # Ss. Siete Fundadores de la Orden de los Siervos de la B. V. M.
    constants.SANCTI_02_14: "S. Valentini",  # S. Valentín
    constants.SANCTI_02_15: "SS. Faustini et Jovitæ",  # SS. Faustino y Jovita
    constants.SANCTI_02_18: "S. Simeonis Faustini Episcopi et Martyris",  # S. Simeón Faustino Obispo y Mártir
    constants.SANCTI_02_22: "In Cathedra S. Petri Ap.",  # En la Cátedra de S. Pedro Apóstol
    constants.SANCTI_02_23: "S. Petri Damiani",  # S. Pedro Damián
    constants.SANCTI_02_24: "S. Matthiæ Apostoli",  # S. Matías Apóstol
    constants.SANCTI_02_27: "S. Gabrielis a Virgine Perdolente Confessoris",  # S. Gabriel de la Virgen Dolorosa Confesor
    constants.SANCTI_03_04: "S. Casimiri Confessoris",  # S. Casimiro Confesor
    constants.SANCTI_03_06: "Ss. Perpetuæ et Felicitatis Martyrum",  # Ss. Perpetua y Felicidad Mártires
    constants.SANCTI_03_07: "S. Thomæ de Aquino Confessoris Ecclesiæ Doctoris",  # S. Tomás de Aquino Confesor Doctor de la Iglesia
    constants.SANCTI_03_08: "S. Joannis de Deo Confessoris",  # S. Juan de Dios Confesor
    constants.SANCTI_03_09: "S. Franciscæ Viduæ Romanæ",  # S. Francisca Viuda Romana
    constants.SANCTI_03_10: "Ss. Quadraginta Martyrum",  # Ss. Cuarenta Mártires
    constants.SANCTI_03_12: "S. Gregorii Papæ Confessoris et Ecclesiæ Doctoris",  # S. Gregorio Papa Confesor Doctor de la Iglesia
    constants.SANCTI_03_15PL: "S. Clementis Hofbauer",  # S. Clemente Hofbauer
    constants.SANCTI_03_17: "S. Patricii Episcopi et Conf.",  # S. Patricio Obispo y Confesor
    constants.SANCTI_03_18: "S. Cyrilli Episcopi Hierosolymitani Ecclesiæ Doctoris",  # S. Cirilo Obispo de Jerusalén Doctor de la Iglesia
    constants.SANCTI_03_19: "S. Joseph Sponsi B.M.V. Confessoris",  # S. José Esposo de la B. M. V. Confesor
    constants.SANCTI_03_21: "S. Benedicti Abbatis",  # S. Benito Abad
    constants.SANCTI_03_24: "S. Gabrielis Archangeli",  # S. Gabriel Arcángel
    constants.SANCTI_03_25: "In Annuntiatione Beate Mariæ Virgine",  # En la Anunciación de la Bienaventurada Virgen María
    constants.SANCTI_03_27: "S. Joannis Damasceni Confessoris",  # S. Juan Damasceno Confesor
    constants.SANCTI_03_28: "S. Joannis a Capistrano Confessoris",  # S. Juan de Capistrano Confesor
    constants.SANCTI_04_02: "S. Francisci de Paula Confessoris",  # S. Francisco de Paula Confesor
    constants.SANCTI_04_04: "S. Isidori Episc. Confessoris et Ecclesiæ Doctoris",  # S. Isidoro Obispo Confesor Doctor de la Iglesia
    constants.SANCTI_04_05: "S. Vincentii Ferrerii Confessoris",  # S. Vicente Ferrer Confesor
    constants.SANCTI_04_11: "S. Leonis I. Papæ Confessoris et Ecclesiæ Doctoris",  # S. León I Papa Confesor Doctor de la Iglesia
    constants.SANCTI_04_13: "S. Hermenegildi Martyris",  # S. Hermenegildo Mártir
    constants.SANCTI_04_14: "S. Justini Martyris",  # S. Justino Mártir
    constants.SANCTI_04_17: "S. Aniceti Papæ et Martyris",  # S. Aniceto Papa y Mártir
    constants.SANCTI_04_21: "S. Anselmi Episcopi Confessoris et Ecclesiæ Doctoris",  # S. Anselmo Obispo Confesor Doctor de la Iglesia
    constants.SANCTI_04_22: "SS. Soteris et Caji Summorum Pontificum et Martyrum",  # SS. Sotero y Cayo Sumos Pontífices y Mártires
    constants.SANCTI_04_23: "S. Georgii Martyris",  # S. Jorge Mártir
    constants.SANCTI_04_23PL: "S. Adalberti, Episcopi et Martyris",  # S. Adalberto, Obispo y Mártir
    constants.SANCTI_04_24: "S. Fidelis de Sigmaringa Martyris",  # S. Fidel de Sigmaringa Mártir
    constants.SANCTI_04_25: "S. Marci Evangelistæ",  # S. Marcos Evangelista
    constants.SANCTI_04_26: "SS. Cleti et Marcellini Summorum Pontificum et Martyrum",  # SS. Cleto y Marcelino Sumos Pontífices y Mártires
    constants.SANCTI_04_27: "S. Petri Canisii Confessoris et Ecclesiæ Doctoris",  # S. Pedro Canisio Confesor Doctor de la Iglesia
    constants.SANCTI_04_28: "S. Pauli a Cruce Confessoris",  # S. Pablo de la Cruz Confesor
    constants.SANCTI_04_29: "S. Petri Martyris",  # S. Pedro Mártir
    constants.SANCTI_04_30: "S. Catharina Senensis Virgine",  # S. Catalina de Siena Virgen
    constants.SANCTI_05_01: "S. Joseph Opificis",  # S. José Obrero
    constants.SANCTI_05_02: "S. Athanasii Confessoris Ecclesiæ Doctoris",  # S. Atanasio Confesor Doctor de la Iglesia
    constants.SANCTI_05_03: "Ss. Alexandri et Sociorum Martyrum",  # Ss. Alejandro y Compañeros Mártires
    constants.SANCTI_05_03PL: "Beatæ Mariæ Virginis Reginæ Poloniæ",  # Beata Virgen María Reina de Polonia
    constants.SANCTI_05_04: "S. Monicæ Viduæ",  # S. Mónica Viuda
    constants.SANCTI_05_04PL: "S. Floriani Martyris",  # S. Floriano Mártir
    constants.SANCTI_05_05: "S. Pii V Papæ Confessoris",  # S. Pío V Papa Confesor
    constants.SANCTI_05_07: "S. Stanislai Episcopi et Martyris",  # S. Estanislao Obispo y Mártir
    constants.SANCTI_05_08PL: "S. Stanislai Episcopi et Martyris",  # S. Estanislao Obispo y Mártir
    constants.SANCTI_05_09: "S. Gregorii Nazianzeni Episcopi Confessoris Ecclesiæ Doctoris",  # S. Gregorio Nacianceno Obispo Confesor Doctor de la Iglesia
    constants.SANCTI_05_10: "S. Antonii Episcopi Confessoris",  # S. Antonio Obispo Confesor
    constants.SANCTI_05_11: "Ss. Philippi et Jacobi Apostolorum",  # Ss. Felipe y Santiago Apóstoles
    constants.SANCTI_05_12: "Ss. Nerei, Achillei et Domitillæ Virginis atque Pancratii Martyrum",  # Ss. Nereo, Aquiles y Domitila Virgen y Pancracio Mártir
    constants.SANCTI_05_13: "S. Roberti Bellarmino Episcopi Confessoris et Ecclesiæ Doctoris",  # S. Roberto Belarmino Obispo Confesor Doctor de la Iglesia
    constants.SANCTI_05_14: "S. Bonifacii Martyris",  # S. Bonifacio Mártir
    constants.SANCTI_05_15: "S. Johanni Baptistæ de la Salle Confessoris",  # S. Juan Bautista de la Salle Confesor
    constants.SANCTI_05_16: "S. Ubaldi Episcopi Confessoris",  # S. Ubaldino Obispo Confesor
    constants.SANCTI_05_16PL: "S. Andreæ Bobolæ Martyrum",  # S. Andrés Bobola Mártir
    constants.SANCTI_05_17: "S. Paschalis Baylon Confessoris",  # S. Pascual Baylón Confesor
    constants.SANCTI_05_18: "S. Venantii Martyris",  # S. Venancio Mártir
    constants.SANCTI_05_19: "S. Petri Celestini Papæ Confessoris",  # S. Pedro Celestino Papa Confesor
    constants.SANCTI_05_20: "S. Bernardini Senensis Confessoris",  # S. Bernardino de Siena Confesor
    constants.SANCTI_05_24PL: "Beatæ Mariæ Virginis Confessoris Auxiliatrix",  # Beata Virgen María Confesora Auxiliadora
    constants.SANCTI_05_25: "S. Gregorii VII Papæ Confessoris",  # S. Gregorio VII Papa Confesor
    constants.SANCTI_05_26: "S. Philippi Neri Confessoris",  # S. Felipe Neri Confesor
    constants.SANCTI_05_27: "S. Bedæ Venerabilis Confessoris et Ecclesiæ Doctoris",  # S. Beda el Venerable Confesor Doctor de la Iglesia
    constants.SANCTI_05_28: "S. Augustini Episcopi Confessoris",  # S. Agustín Obispo Confesor
    constants.SANCTI_05_29: "S. Mariæ Magdalenæ de Pazzis Virginis",  # S. María Magdalena de Pazzi Virgen
    constants.SANCTI_05_30: "S. Felicis Papæ et Martyris",  # S. Félix Papa y Mártir
    constants.SANCTI_05_31: "Beatæ Mariæ Virginis Reginæ",  # Beata Virgen María Reina
    constants.SANCTI_06_01: "S. Angelæ Mericiæ Virginis",  # S. Ángela de Mérici Virgen
    constants.SANCTI_06_02: "Ss. Marcellini, Petri, atque Erasmi Martyrum",  # Ss. Marcelino, Pedro y Erasmo Mártires
    constants.SANCTI_06_04: "S. Francisci Caracciolo Confessoris",  # S. Francisco Caracciolo Confesor
    constants.SANCTI_06_05: "S. Bonifatii Episc. et Mart.",  # S. Bonifacio Obispo y Mártir
    constants.SANCTI_06_06: "S. Norberti Episc. et Confessoris",  # S. Norberto Obispo y Confesor
    constants.SANCTI_06_09: "Ss. Primi et Feliciani Martyrum",  # Ss. Primo y Feliciano Mártires
    constants.SANCTI_06_10: "S. Margaritæ Reginæ viduæ",  # S. Margarita Reina viuda
    constants.SANCTI_06_10PL: "B. Bogumilai Episcopi et Confessoris",  # B. Bogumil Obispo y Confesor
    constants.SANCTI_06_11: "S. Barnabæ Apostoli",  # S. Bernabé Apóstol
    constants.SANCTI_06_12: "S. Joannis a S. Facundo Confessoris",  # S. Juan de San Facundo Confesor
    constants.SANCTI_06_13: "S. Antonii de Padua Confessoris",  # S. Antonio de Padua Confesor
    constants.SANCTI_06_14: "S. Basilii Magni Confessoris et Ecclesiæ Doctoris",  # S. Basilio Magno Confesor Doctor de la Iglesia
    constants.SANCTI_06_15: "Ss. Viti, Modesti atque Crescentiæ Martyrum",  # Ss. Vito, Modesto y Crescencia Mártires
    constants.SANCTI_06_15PL: "b. Jolantae Viduae",  # B. Yolanda Viuda
    constants.SANCTI_06_17: "S. Gregorii Barbadici Episcopi Confessoris",  # S. Gregorio Barbarigo Obispo Confesor
    constants.SANCTI_06_18: "S. Ephræm Syri Confessoris et Ecclesiæ Doctorem",  # S. Efrén el Sirio Confesor Doctor de la Iglesia
    constants.SANCTI_06_19: "S. Julianæ de Falconeriis Virginis",  # S. Juliana de Falconieri Virgen
    constants.SANCTI_06_20: "S. Silverii Papæ et Martyri",  # S. Silverio Papa y Mártir
    constants.SANCTI_06_21: "S. Aloisii Gonzagæ Confessoris",  # S. Luis Gonzaga Confesor
    constants.SANCTI_06_22: "S. Paulini Episcopi et Confessoris",  # S. Paulino Obispo y Confesor
    constants.SANCTI_06_23: "In Vigilia S. Joannis Baptistæ",  # En la Vigilia de S. Juan Bautista
    constants.SANCTI_06_24: "In Nativitate S. Joannis Baptistæ",  # En el Nacimiento de S. Juan Bautista
    constants.SANCTI_06_25: "S. Gulielmi Abbatis",  # S. Guillermo Abad
    constants.SANCTI_06_26: "Ss. Joannis et Pauli Martyrum",  # Ss. Juan y Pablo Mártires
    constants.SANCTI_06_28: "In Vigilia Ss. Petri et Pauli Apostolorum",  # En la Vigilia de los Ss. Pedro y Pablo Apóstoles
    constants.SANCTI_06_29: "SS. Apostolorum Petri et Pauli",  # Ss. Apóstoles Pedro y Pablo
    constants.SANCTI_06_30: "In Commemoratione Sancti Pauli Apostoli",  # En la Conmemoración de San Pablo Apóstol
    constants.SANCTI_07_01: "Pretiosissimi Sanguinis Domini Nostri Jesu Christi",  # Preciosísima Sangre de Nuestro Señor Jesucristo
    constants.SANCTI_07_02: "In Visitatione B. Mariæ Virginis",  # En la Visitación de la Bienaventurada Virgen María
    constants.SANCTI_07_03: "S. Irenæi Episcopi et Martyris",  # S. Ireneo Obispo y Mártir
    constants.SANCTI_07_05: "S. Antonii Mariæ Zaccaria Confessoris",  # S. Antonio María Zacarías Confesor
    constants.SANCTI_07_07: "Ss. Cyrilli et Methodii Pont. et Conf.",  # Ss. Cirilo y Metodio Pontífices y Confesores
    constants.SANCTI_07_08: "S. Elisabeth Reg. Portugaliæ Viduæ",  # S. Isabel Reina de Portugal Viuda
    constants.SANCTI_07_10: "Ss. Septem Fratrum Martyrum, ac Rufinæ et Secundæ Virginum et Martyrum",  # Ss. Siete Hermanos Mártires, y Rufina y Segunda Vírgenes y Mártires
    constants.SANCTI_07_11: "S. Pii I Papæ et Martyris",  # S. Pío I Papa y Mártir
    constants.SANCTI_07_12: "S. Joannis Gualberti Abbatis",  # S. Juan Gualberto Abad
    constants.SANCTI_07_13PL: "Śś. Andreæ et Benedicti",  # Ss. Andrés y Benito
    constants.SANCTI_07_14: "S. Bonaventuræ Episcopi Confessoris et Ecclesiæ Doctoris",  # S. Buenaventura Obispo Confesor Doctor de la Iglesia
    constants.SANCTI_07_15: "S. Henrici Imperatoris Confessoris",  # S. Enrique Emperador Confesor
    constants.SANCTI_07_15PL: "S. Brunonis Episcopi et Martyris",  # S. Bruno Obispo y Mártir
    constants.SANCTI_07_16: "In Commemoratione Beatæ Mariæ Virgine de Monte Carmelo.",  # En la Conmemoración de la Bienaventurada Virgen María del Monte Carmelo
    constants.SANCTI_07_17: "S. Alexii Confessoris",  # S. Alejo Confesor
    constants.SANCTI_07_18: "S. Camilli de Lellis Confessoris",  # S. Camilo de Lelis Confesor
    constants.SANCTI_07_18PL: "B. Simonis Confessoris",  # B. Simón Confesor
    constants.SANCTI_07_19: "S. Vincentii a Paulo Confessoris",  # S. Vicente de Paúl Confesor
    constants.SANCTI_07_20: "S. Hieronymi Emiliani Confessoris",  # S. Jerónimo Emiliani Confesor
    constants.SANCTI_07_20PL: "B. Ceslai Confessoris",  # B. Ceslao Confesor
    constants.SANCTI_07_21: "S. Laurentii a Brundusio Confessoris",  # S. Lorenzo de Brindis Confesor
    constants.SANCTI_07_22: "S. Mariæ Magdalenæ Poenitentis",  # S. María Magdalena Penitente
    constants.SANCTI_07_23: "S. Apollinaris Episcopi et Martyris",  # S. Apolinar Obispo y Mártir
    constants.SANCTI_07_24: "S. Christinæ Virginis et Martyris",  # S. Cristina Virgen y Mártir
    constants.SANCTI_07_24PL: "S. Kingæ Virginis",  # S. Kinga Virgen
    constants.SANCTI_07_25: "S. Jacobi Apostoli",  # S. Santiago Apóstol
    constants.SANCTI_07_26: "S. Annæ Matris B.M.V.",  # S. Ana Madre de la B. V. M.
    constants.SANCTI_07_27: "S. Pantaleonis Martyris",  # S. Pantaleón Mártir
    constants.SANCTI_07_28: "Ss. Nazarii et Celsi Martyrum, Victoris I Papæ et Martyris ac Innocentii I Papæ et Confessoris",  # Ss. Nazario y Celso Mártires, Víctor I Papa y Mártir e Inocencio I Papa y Confesor
    constants.SANCTI_07_29: "S. Marthæ Virginis",  # S. Marta Virgen
    constants.SANCTI_07_30: "S. Abdon et Sennen Martyrum",  # S. Abdón y Senén Mártires
    constants.SANCTI_07_31: "S. Ignatii Confessoris",  # S. Ignacio Confesor
    constants.SANCTI_08_01: "Ss. Martyrum Machabæorum",  # Ss. Mártires Macabeos
    constants.SANCTI_08_02: "S. Alfonsi Mariæ de Ligorio Episcopi Confessoris et Ecclesiæ Doctoris",  # S. Alfonso María de Ligorio Obispo Confesor Doctor de la Iglesia
    constants.SANCTI_08_04: "S. Dominici Confessoris",  # S. Domingo Confesor
    constants.SANCTI_08_05: "S. Mariæ ad Nives",  # S. María de las Nieves
    constants.SANCTI_08_06: "In Transfiguratione Domini Nostri Jesu Christi",  # En la Transfiguración de Nuestro Señor Jesucristo
    constants.SANCTI_08_07: "S. Cajetani Confessoris",  # S. Cayetano Confesor
    constants.SANCTI_08_08: "S. Joannis Mariæ Vianney Confessoris",  # S. Juan María Vianney Confesor
    constants.SANCTI_08_09: "Vigilia S. Laurentii Martyris",  # Vigilia de S. Lorenzo Mártir
    constants.SANCTI_08_10: "S. Laurentii Martyris",  # S. Lorenzo Mártir
    constants.SANCTI_08_11: "Ss. Tiburtii et Susannæ Virginum et Martyrum",  # Ss. Tiburcio y Susana Vírgenes y Mártires
    constants.SANCTI_08_12: "S. Claræ Virginis",  # S. Clara Virgen
    constants.SANCTI_08_13: "Ss. Hippolyti et Cassiani Martyrum",  # Ss. Hipólito y Casiano Mártires
    constants.SANCTI_08_14: "Vigilia Assumptionis B.M.V.",  # Vigilia de la Asunción de la B. V. M.
    constants.SANCTI_08_15: "In Assumptione Beatæ Mariæ Virginis",  # En la Asunción de la Bienaventurada Virgen María
    constants.SANCTI_08_16: "S. Joachim Confessoris, Patris B. Mariæ Virginis",  # S. Joaquín Confesor, Padre de la B. Virgen María
    constants.SANCTI_08_17: "S. Hyacinthi Confessoris",  # S. Jacinto Confesor
    constants.SANCTI_08_18: "S. Agapiti Martyris",  # S. Agapito Mártir
    constants.SANCTI_08_19: "S. Joannis Eudes Confessoris",  # S. Juan Eudes Confesor
    constants.SANCTI_08_20: "S. Bernardi Abbatis et Ecclesiæ Doctoris",  # S. Bernardo Abad Doctor de la Iglesia
    constants.SANCTI_08_21: "S. Joannæ Franciscæ Frémiot de Chantal Viduæ",  # S. Juana Francisca Frémiot de Chantal Viuda
    constants.SANCTI_08_22: "Immaculati Cordis Beatæ Mariæ Virginis",  # Inmaculado Corazón de la Bienaventurada Virgen María
    constants.SANCTI_08_23: "S. Philippi Benitii Confessoris",  # S. Felipe Benicio Confesor
    constants.SANCTI_08_24: "S. Bartholomæi Apostoli",  # S. Bartolomé Apóstol
    constants.SANCTI_08_25: "S. Ludovici Confessoris",  # S. Luis Confesor
    constants.SANCTI_08_26: "S. Zephirini Papæ et Martyris",  # S. Ceferino Papa y Mártir
    constants.SANCTI_08_26PL: "Beate Mariae Virginis Claromontane Czestochoviensis",  # Beata Virgen María de Claro Monte de Czestochova
    constants.SANCTI_08_27: "S. Josephi Calasanctii Confessoris",  # S. José de Calasanz Confesor
    constants.SANCTI_08_28: "S. Augustini Episcopi et Confessoris et Ecclesiæ Doctoris",  # S. Agustín Obispo Confesor Doctor de la Iglesia
    constants.SANCTI_08_29: "Decollatione S. Joannis Baptistæ",  # Degollación de S. Juan Bautista
    constants.SANCTI_08_30: "S. Rosæ a Sancta Maria Limange Virginis",  # S. Rosa de Lima Virgen
    constants.SANCTI_08_31: "S. Raymundi Nonnati Confessoris",  # S. Ramón Nonato Confesor
    constants.SANCTI_09_01: "S. Ægidii Abbatis",  # S. Gil Abad
    constants.SANCTI_09_01PL: "B. Bronislauæ Virginins",  # B. Bronislawa Virgen
    constants.SANCTI_09_02: "S. Stephani Hungariæ Regis Confessoris",  # S. Esteban de Hungría Rey Confesor
    constants.SANCTI_09_03: "S. Pii X Papæ Confessoris",  # S. Pío X Papa Confesor
    constants.SANCTI_09_05: "S. Laurentii Justiniani Episcopi et Confessoris",  # S. Lorenzo Justiniano Obispo y Confesor
    constants.SANCTI_09_07PL: "B. Melchiori Martyrum",  # B. Melchior Mártir
    constants.SANCTI_09_08: "Nativitate Beatæ Mariæ Virginis",  # Natividad de la Bienaventurada Virgen María
    constants.SANCTI_09_09: "S. Gorgonii Martyris",  # S. Gorgonio Mártir
    constants.SANCTI_09_10: "S. Nicolai de Tolentino Confessoris",  # S. Nicolás de Tolentino Confesor
    constants.SANCTI_09_11: "Ss. Proti et Hyacinthi Martyrum",  # Ss. Proto e Jacinto Mártires
    constants.SANCTI_09_12: "S. Nominis Beatæ Mariæ Virginis",  # Santísimo Nombre de la Bienaventurada Virgen María
    constants.SANCTI_09_14: "In Exaltatione Sanctæ crucis",  # En la Exaltación de la Santa Cruz
    constants.SANCTI_09_15: "Septem Dolorum Beatæ Mariæ Virginis",  # Siete Dolores de la Bienaventurada Virgen María
    constants.SANCTI_09_16: "Ss. Cornelii Papæ et Cypriani Episcopi, Martyrum",  # Ss. Cornelio Papa y Cipriano Obispo, Mártires
    constants.SANCTI_09_17: "Impressionis Stigmatum S. Francisci",  # Impresión de los Estigmas de S. Francisco
    constants.SANCTI_09_18: "S. Josephi de Cupertino Confessoris",  # S. José de Cupertino Confesor
    constants.SANCTI_09_19: "S. Januarii Episcopi et Sociorum Martyrum",  # S. Jenaro Obispo y Compañeros Mártires
    constants.SANCTI_09_20: "S. Eustachii et Sociorum Martyrum",  # S. Eustaquio y Compañeros Mártires
    constants.SANCTI_09_21: "S. Matthæi Apostoli et Evangelistæ",  # S. Mateo Apóstol y Evangelista
    constants.SANCTI_09_22: "S. Thomæ de Villanove Episcopi et Confessoris",  # S. Tomás de Villanueva Obispo y Confesor
    constants.SANCTI_09_23: "S. Lini Papæ et Martyris",  # S. Lino Papa y Mártir
    constants.SANCTI_09_24: "Beatæ Mariæ Virginis de Mercede",  # Beata Virgen María de la Merced
    constants.SANCTI_09_25PL: "B. Ladislai Confessoris",  # B. Ladislao Confesor
    constants.SANCTI_09_26: "Ss. Cypriani et Justinæ Martyrum",  # Ss. Cipriano y Justina Mártires
    constants.SANCTI_09_27: "S. Cosmæ et Damiani Martyrum",  # Ss. Cosme y Damián Mártires
    constants.SANCTI_09_28: "S. Wenceslai Ducis et Martyris",  # S. Wenceslao Duque y Mártir
    constants.SANCTI_09_29: "In Dedicatione S. Michælis Archangelis",  # En la Dedicación de S. Miguel Arcángel
    constants.SANCTI_09_30: "S. Hieronymi Presbyteris Confessoris et Ecclesiæ Doctoris",  # S. Jerónimo Presbítero Confesor Doctor de la Iglesia
    constants.SANCTI_10_01: "S. Remigii Episcopi Confessoris",  # S. Remigio Obispo Confesor
    constants.SANCTI_10_01PL: "B. Joannis de Dukla",  # B. Juan de Dukla
    constants.SANCTI_10_02: "Ss. Angelorum Custodum",  # Ss. Ángeles Custodios
    constants.SANCTI_10_03: "S. Theresiæ a Jesu Infante Virginis",  # S. Teresa del Niño Jesús Virgen
    constants.SANCTI_10_04: "S. Francisci Confessoris",  # S. Francisco Confesor
    constants.SANCTI_10_05: "Ss. Placidi et Sociorum Martyrum",  # Ss. Plácido y Compañeros Mártires
    constants.SANCTI_10_06: "S. Brunonis Confessoris",  # S. Bruno Confesor
    constants.SANCTI_10_07: "Festum Beatæ Mariæ Virginis a Rosario",  # Fiesta de la Bienaventurada Virgen María del Rosario
    constants.SANCTI_10_08: "S. Birgittæ Viduæ",  # S. Brígida Viuda
    constants.SANCTI_10_09: "S. Joannis Leonardi Confessoris",  # S. Juan Leonardi Confesor
    constants.SANCTI_10_09PL: "b. Vincenti Episcopi et Confessoris",  # B. Vicente Obispo y Confesor
    constants.SANCTI_10_10: "S. Francisci Borgiæ Confessoris",  # S. Francisco de Borja Confesor
    constants.SANCTI_10_10PL: "Victoriae Chocimensis",  # Victoria de Chocim
    constants.SANCTI_10_11: "Maternitatis Beatæ Mariæ Virginis",  # Maternidad de la Bienaventurada Virgen María
    constants.SANCTI_10_13: "S. Eduardi Regis Confessoris",  # S. Eduardo Rey Confesor
    constants.SANCTI_10_14: "S. Callisti Papæ et Martyris",  # S. Calixto Papa y Mártir
    constants.SANCTI_10_15: "S. Teresiæ Virginis",  # S. Teresa Virgen
    constants.SANCTI_10_16: "S. Hedwigis Viduæ",  # S. Eduvigis Viuda
    constants.SANCTI_10_17: "S. Margaritæ Mariæ Alaquoque Virginis",  # S. Margarita María Alacoque Virgen
    constants.SANCTI_10_18: "S. Lucæ Evangelistæ",  # S. Lucas Evangelista
    constants.SANCTI_10_19: "S. Petri de Alcantara Confessoris",  # S. Pedro de Alcántara Confesor
    constants.SANCTI_10_20: "S. Joannis Cantii Confessoris",  # S. Juan Cancio Confesor
    constants.SANCTI_10_21: "S. Hilarionis Abbatis",  # S. Hilarión Abad
    constants.SANCTI_10_21PL: "B. Jacobi Episcopi et Confessoris",  # B. Jacobo Obispo y Confesor
    constants.SANCTI_10_23: "S. Antonii Mariæ Claret Episcopi Confessoris",  # S. Antonio María Claret Obispo Confesor
    constants.SANCTI_10_24: "S. Raphælis Archangeli",  # S. Rafael Arcángel
    constants.SANCTI_10_25: "Ss. Chrysanthi et Dariæ Martyrum",  # Ss. Crisanto y Daría Mártires
    constants.SANCTI_10_28: "Ss. Simonis et Judæ Apostolorum.",  # Ss. Simón y Judas Apóstoles
    constants.SANCTI_11_01: "Omnium Sanctorum",  # Todos los Santos
    constants.SANCTI_11_02_1: "In Commemoratione Omnium Fidelium Defunctorum Ad primam Missam",  # En la Conmemoración de Todos los Fieles Difuntos en la primera Misa
    constants.SANCTI_11_02_2: "In Commemoratione Omnium Fidelium Defunctorum Ad secundam Missam",  # En la Conmemoración de Todos los Fieles Difuntos en la segunda Misa
    constants.SANCTI_11_02_3: "In Commemoratione Omnium Fidelium Defunctorum Ad tertiam Missam",  # En la Conmemoración de Todos los Fieles Difuntos en la tercera Misa
    constants.SANCTI_11_04: "S. Caroli Episcopi et Confessoris",  # S. Carlos Obispo y Confesor
    constants.SANCTI_11_08: "Ss. Quatuor Coronatorum Martyrum",  # Ss. Cuatro Coronados Mártires
    constants.SANCTI_11_09: "In Dedicatione Basilicæ Ss. Salvatoris",  # En la Dedicación de la Basílica de los Ss. Salvadores
    constants.SANCTI_11_10: "S. Andreæ Avellini Confessoris",  # S. Andrés Avelino Confesor
    constants.SANCTI_11_11: "S. Martini Episcopi et Confessoris",  # S. Martín Obispo y Confesor
    constants.SANCTI_11_12: "S. Martini Papæ et Martyris",  # S. Martín Papa y Mártir
    constants.SANCTI_11_12PL: "Ss. Protomartyrum Poloniae",  # Ss. Protomártires de Polonia
    constants.SANCTI_11_13: "S. Didaci Confessoris",  # S. Diego Confesor
    constants.SANCTI_11_13PL: "S. Stanislai Confessoris",  # S. Estanislao Confesor
    constants.SANCTI_11_14: "S. Josaphat Episcopi et Martyris",  # S. Josafat Obispo y Mártir
    constants.SANCTI_11_15: "S. Alberti Magni Episcopi Confessoris et Ecclesiæ Doctoris",  # S. Alberto Magno Obispo Confesor Doctor de la Iglesia
    constants.SANCTI_11_16: "S. Gertrudis Virginis",  # S. Gertrudis Virgen
    constants.SANCTI_11_17: "S. Gregorii Thaumaturgi Episcopi et Confessoris",  # S. Gregorio Taumaturgo Obispo y Confesor
    constants.SANCTI_11_17PL: "B. Salomea Virginis",  # B. Salomea Virgen
    constants.SANCTI_11_18: "In Dedicatione Basilicarum Ss. Apostolorum Petri et Pauli",  # En la Dedicación de las Basílicas de los Ss. Apóstoles Pedro y Pablo
    constants.SANCTI_11_19: "S. Elisabeth Viduæ",  # S. Isabel Viuda
    constants.SANCTI_11_20: "S. Felicis de Valois Confessoris",  # S. Félix de Valois Confesor
    constants.SANCTI_11_20PL: "S. Martini Papæ et Martyris",  # S. Martín Papa y Mártir (en Polonia, movido del 12.11 con el 1964)
    constants.SANCTI_11_21: "In Presentatione Beatæ Mariæ Virginis",  # En la Presentación de la Bienaventurada Virgen María
    constants.SANCTI_11_22: "S. Cæciliæ Virginis et Martyris",  # S. Cecilia Virgen y Mártir
    constants.SANCTI_11_23: "S. Clementis Papæ et Martyris",  # S. Clemente Papa y Mártir
    constants.SANCTI_11_24: "S. Joannis a Cruce Confessoris et Ecclesiæ Doctoris",  # S. Juan de la Cruz Confesor Doctor de la Iglesia
    constants.SANCTI_11_25: "S. Catharinæ Virginis et Martyris",  # S. Catalina Virgen y Mártir
    constants.SANCTI_11_26: "S. Silvesteri Abbatis et Confessoris",  # S. Silvestre Abad y Confesor
    constants.SANCTI_11_29: "S. Saturnini Martyris",  # S. Saturnino Mártir
    constants.SANCTI_11_30: "S. Andreæ Apostoli",  # S. Andrés Apóstol
    constants.SANCTI_12_02: "S. Bibianæ Virginis et Martyris",  # S. Bibiana Virgen y Mártir
    constants.SANCTI_12_02PL: "S. Petri Chrysologi Episcopi Confessoris et Ecclesiæ Doctoris",  # S. Pedro Crisólogo Obispo Confesor Doctor de la Iglesia
    constants.SANCTI_12_03: "S. Francisci Xaverii Confessoris",  # S. Francisco Javier Confesor
    constants.SANCTI_12_04: "S. Petri Chrysologi Episcopi Confessoris et Ecclesiæ Doctoris",  # S. Pedro Crisólogo Obispo Confesor Doctor de la Iglesia
    constants.SANCTI_12_04PL: "S. Barbaræ Virginis et Martyris",  # S. Bárbara Virgen y Mártir
    constants.SANCTI_12_05: "S. Sabbæ Abbatis",  # S. Sabas Abad
    constants.SANCTI_12_06: "S. Nicolai Episcopi et Confessoris",  # S. Nicolás Obispo y Confesor
    constants.SANCTI_12_07: "S. Ambrosii Episcopi Confessoris et Ecclesiæ Doctoris",  # S. Ambrosio Obispo Confesor Doctor de la Iglesia
    constants.SANCTI_12_08: "In Conceptione Immaculata Beatæ Mariæ Virginis",  # En la Concepción Inmaculada de la Bienaventurada Virgen María
    constants.SANCTI_12_10: "S. Melchiadis Papæ et Mart",  # S. Melquiades Papa y Mártir
    constants.SANCTI_12_11: "S. Damasi Papæ et Confessoris",  # S. Dámaso Papa y Confesor
    constants.SANCTI_12_13: "S. Luciæ Virginis et Martyris",  # S. Lucía Virgen y Mártir
    constants.SANCTI_12_16: "S. Eusebii Episcopi et Martyris",  # S. Eusebio Obispo y Mártir
    constants.SANCTI_12_21: "S. Thomæ Apostoli",  # S. Tomás Apóstol
    constants.SANCTI_12_24: "In Vigilia Nativitatis Domini",  # En la Vigilia de la Navidad del Señor
    constants.SANCTI_12_25_1: "In Nativitate Domini in nocte",  # En la Navidad del Señor en la noche
    constants.SANCTI_12_25_2: "In Nativitatis Domini in aurora",  # En la Navidad del Señor en la aurora
    constants.SANCTI_12_25_3: "In die Nativitatis Domini",  # En el día de la Navidad del Señor
    constants.SANCTI_12_26: "S. Stephani Protomartyris",  # S. Esteban Protomártir
    constants.SANCTI_12_27: "S. Joannis Apostoli et Evangelistæ",  # S. Juan Apóstol y Evangelista
    constants.SANCTI_12_28: "Ss. Innocentium",  # Ss. Inocentes
    constants.SANCTI_12_29: "S. Thomæ M.",  # S. Tomás Mártir
    constants.SANCTI_12_31: "S. Silvestri",  # S. Silvestre
    constants.VOTIVE_ANGELS: "Missa de Angelis",  # Misa de los Ángeles
    constants.VOTIVE_JOSEPH: "Missa de S. Ioseph",  # Misa de S. José
    constants.VOTIVE_PETERPAUL: "Missa de Ss. Petro et Paulo App.",  # Misa de Ss. Pedro y Pablo Apóstoles
    constants.VOTIVE_PETERPAULP: "Missa de Ss. Petro et Paulo App.",  # Misa de Ss. Pedro y Pablo Apóstoles
    constants.VOTIVE_APOSTLES: "Missa de omnibus Ss. Apostolis",  # Misa de todos los Ss. Apóstoles
    constants.VOTIVE_APOSTLESP: "Missa de omnibus Ss. Apostolis",  # Misa de todos los Ss. Apóstoles
    constants.VOTIVE_HOLYSPIRIT: "Missa de Spiritu Sancto",  # Misa del Espíritu Santo
    constants.VOTIVE_HOLYSPIRIT2: "Missa ad postulandam gratiam Spiritus Sancti",  # Misa para pedir la gracia del Espíritu Santo
    constants.VOTIVE_BLESSEDSACRAMENT: "Missa de sanctissimo Eucharistiae Sacramento",  # Misa del Santísimo Sacramento de la Eucaristía
    constants.VOTIVE_JESUSETERNALPRIEST: "Missa de D. N. Iesu Christo summo et aeterno Sacerdote",  # Misa de Nuestro Señor Jesucristo sumo y eterno Sacerdote
    constants.VOTIVE_CROSS: "Missa de sancta Cruce",  # Misa de la Santa Cruz
    constants.VOTIVE_PASSION: "Missa de Passione Domini",  # Misa de la Pasión del Señor
    constants.VOTIVE_PENT01_0: "Sanctissimæ Trinitatis",  # Santísima Trinidad
    constants.VOTIVE_PENT02_5: "Sanctissimi Cordis Domini Nostri Jesu Christi",  # Sacratísimo Corazón de Nuestro Señor Jesucristo
    constants.VOTIVE_08_22: "Immaculati Cordis Beatæ Mariæ Virginis",  # Inmaculado Corazón de la Bienaventurada Virgen María
    constants.VOTIVE_DEFUNCTORUM: "Missa Defunctorum Quotidianis",  # Misa de Difuntos Diaria
    constants.VOTIVE_MORTALITATIS: "Missa Tempore Mortalitatis",  # Misa en Tiempo de Mortalidad
    constants.VOTIVE_FIDEI_PROPAGATIONE: "Missa pro Fidei Propagatione",  # Misa por la Propagación de la Fe
    constants.VOTIVE_TERRIBILIS: "Missa de Communi Dedicationis Ecclesiae.",  # Misa del Común de la Dedicación de la Iglesia
}

VOTIVE_MASSES = [
    {
        "ref": "rorate",
        "id": constants.COMMUNE_C_10A,
        "title": TITLES[constants.COMMUNE_C_10A],
        "tags": ["Advent"],
    },
    {
        "ref": "vultum-tuum",
        "id": constants.COMMUNE_C_10B,
        "title": TITLES[constants.COMMUNE_C_10B],
        "tags": ["From Nativity util Purification"],
    },
    {
        "ref": "salve-sancta-parens-3",
        "id": constants.COMMUNE_C_10C,
        "title": TITLES[constants.COMMUNE_C_10C],
        "tags": ["From Feb 3 until Holy Wednesday"],
    },
    {
        "ref": "salve-sancta-parens-4",
        "id": constants.COMMUNE_C_10PASC,
        "title": TITLES[constants.COMMUNE_C_10PASC],
        "tags": ["Eastertide"],
    },
    {
        "ref": "salve-sancta-parens-5",
        "id": constants.COMMUNE_C_10T,
        "title": TITLES[constants.COMMUNE_C_10T],
        "tags": ["From Trinity Sunday until Advent"],
    },
    {
        "ref": "trinitas",
        "id": constants.VOTIVE_PENT01_0,
        "title": TITLES[constants.VOTIVE_PENT01_0],
        "tags": ["Votive", "Monday"],
    },
    {
        "ref": "angelis",
        "id": constants.VOTIVE_ANGELS,
        "title": TITLES[constants.VOTIVE_ANGELS],
        "tags": ["Votive", "Tuesday"],
    },
    {
        "ref": "joseph",
        "id": constants.VOTIVE_JOSEPH,
        "title": TITLES[constants.VOTIVE_JOSEPH],
        "tags": ["Votive", "Wednesday"],
    },
    {
        "ref": "aeterno-sacerdote",
        "id": constants.VOTIVE_JESUSETERNALPRIEST,
        "title": TITLES[constants.VOTIVE_JESUSETERNALPRIEST],
        "tags": ["Votive", "Thursday"],
    },
    {
        "ref": "cordis-jesu",
        "id": constants.VOTIVE_PENT02_5,
        "title": TITLES[constants.VOTIVE_PENT02_5],
        "tags": ["Votive", "Friday"],
    },
    {
        "ref": "cordis-mariae",
        "id": constants.VOTIVE_08_22,
        "title": TITLES[constants.VOTIVE_08_22],
        "tags": ["Votive", "First Saturday"],
    },
    {
        "ref": "tempore-mortalitatis",
        "id": constants.VOTIVE_MORTALITATIS,
        "title": TITLES[constants.VOTIVE_MORTALITATIS],
        "tags": ["For the deliverance from death in time of pestilence"],
    },
]

SECTION_LABELS = {
    "Communicantes": "Communicantes",
    "CommunioP": "Communion",
    "Communio": "Communion",
    "Evangelium": "Gospel",
    "GradualeP": "Gradual",
    "Graduale": "Gradual",
    "Introitus": "Introit",
    "Lectio": "Epistle",
    "OffertoriumP": "Offertory",
    "Offertorium": "Offertory",
    "Oratio": "Collect",
    "Commemoratio Oratio": "Commemoration Collect",
    "Postcommunio": "Postcommunion",
    "Commemoratio Postcommunio": "Commemoration Postcommunion",
    "Secreta": "Secret",
    "Commemoratio Secreta": "Commemoration Secret",
    "Sequentia": "Sequence",
    "Super populum": "Prayer over the people",
    "Prefatio": "Preface",
    "Tractus": "Gradual",
    # 02-02, feast of the Purification of the B.V.M.
    "De Benedictione Candelarum": "The Blessing of Candles",
    "De Distributione Candelarum": "The Distribution of Candles",
    "De Processione": "The Procession",
    # Quad6-0r, Dominica II Passionis seu in Palmis
    "Benedictio Palmorum": "The Blessing of the Palms",
    "De distributione ramorum": "Distribution of the branches",
    "De lectione Evangelica": "Gospel",
    "De processione cum ramis benedictis": "The Procession of Palms",
    "Hymnus ad Christum Regem": "Hymn to Christ the King",
    # Quad6-4r, Feria Quinta in Coena Domini
    "Maundi": "Washing of the feet",
    "Post Missam": "After the Mass",
    "Denudatione altaris": "Stripping the altar",
    # Quad6-5r, Feria Sexta in Parasceve
    "Lectiones": "Part one: Readings from Scripture",
    "Passio": "Passion",
    "Oratio Fidelium": "Part two: The Great Intercessions",
    "Crucis Adoratione": "Part three: Adoration of the Cross",
    "CommunioQ": "Part four: Communion",
    # Quad6-5r, Sabbato Sancto
    "Benedictio ignis": "The Blessing of the New Fire",
    "De benedictione cerei Paschalis": "The Blessing of the Paschal Candle",
    "De solemni processione": "The Procession with the Paschal Candle",
    "De praeconio paschali": "The Singing of the Paschal Proclamation",
    "De lectionibus": "The Readings",
    "De prima parte Litaniarum": "The First Part of the Litany",
    "De benedictione aquae baptismalis": "The Blessing of the Baptismal Water",
    "De renovatione promissionum baptismatis": "The Renewal of Baptismal Promises",
    "De altera parte Litaniarum": "The Second Part of the Litany",
    "De Missa solemni Vigiliae paschalis": "Holy Mass",
    "Pro Laudibus": "Solemn Lauds of Easter Day",
    "Conclusio": "Dismissal",
    "Benedictio cinerum": "Blessing of the Ashes",
}

SECTION_LABELS_MULTI = {
    "GradualeL1": "Gradual",
    "GradualeL2": "Gradual",
    "GradualeL3": "Gradual",
    "GradualeL4": "Gradual",
    "GradualeL5": "Gradual",
    "Graduale": "Gradual",
    "LectioL1": "Epistle",
    "LectioL2": "Epistle",
    "LectioL3": "Epistle",
    "LectioL4": "Epistle",
    "LectioL5": "Epistle",
    "Lectio": "Epistle",
    "OratioL1": "Collect",
    "OratioL2": "Collect",
    "OratioL3": "Collect",
    "OratioL4": "Collect",
    "OratioL5": "Collect",
    "Oratio": "Collect",
}

PATERNOSTER = (
    "Our Father, who art in heaven,\n"
    "hallowed be Thy Name;\n"
    "Thy kingdom come;\n"
    "Thy will be done on earth as it is in heaven.\n"
    "Give us this day our daily bread.\n"
    "And forgive us our trespasses, as we forgive those who trespass against us.\n"
    "And lead us not into temptation.\n"
    "But deliver us from evil. Amen."
)

TRANSFORMATIONS = (
    (re.compile(r"\+\+"), "☩"),
    (re.compile(r"\+"), "☩"),
    (re.compile(r"V\."), "℣."),
    (re.compile(r"R\."), "℟."),
    (re.compile(r"^#"), "##"),
    (re.compile(r"^!x!"), "!"),
    (re.compile(r"^!! *(.*)"), "### \\1"),
    (re.compile(r"^\[([^\]^]*)\]"), "### \\1"),
    (re.compile(r"^! *(.*)"), "*\\1*"),
    (re.compile(r"^v\. *"), ""),
    (re.compile(r"^_"), ""),
    (re.compile(r"\(\("), "("),
    (re.compile(r"\)\)"), ")"),
    (re.compile(r"\["), "("),
    (re.compile(r"\]"), ")"),
    (re.compile(r"\((\^\d+)\)"), "[\\1]"),  # preserving footnotes, like [^1], [^1]:
    (re.compile(r"^.*`.*$"), ""),
    (re.compile(r"^[&$]Gloria\.*"), "Glory Be to the Father…"),
    (re.compile(r"^\$Oremus\.*"), "Let us pray."),
    (re.compile(r"^\$Per D[oó]minum eiusdem\.*"), "Through our Lord…"),
    (re.compile(r"^\$Per D[oó]minum\.*"), "Through our Lord…"),
    (re.compile(r"^\$Per eu[mn]dem\.*"), "Through the same Christ our Lord…"),
    (
        re.compile(r"^\$Qui tecum eiusdem\.*"),
        "Who livest and reignest with God the Father…",
    ),
    (re.compile(r"^\$Qui tecum\.*"), "Who livest and reignest with God the Father…"),
    (re.compile(r"^\$Qui vivis\.*"), "Who livest…"),
    (re.compile(r"^\$Deo [Gg]ratias\.*"), "Thanks be to God."),
    (
        re.compile(r"^[&$]Dominus *[Vv]obiscum\.*"),
        "℣. The Lord be with you. \n\r℟. And with thy spirit.",
    ),
    (re.compile(r"^\*Modlitwa nad ludem\*.*"), ""),
    (re.compile(r"^\$Pater noster.*"), PATERNOSTER),
    (re.compile(r"\(rubrica 1955 aut rubrica 1960 dicitur\)"), ""),
    (re.compile(r"\(deinde dicuntur semper\)"), ""),
)

COMMEMORATIONS = {
    constants.COMMEMORATION: "Commemoration",
    constants.COMMEMORATED_ORATIO: "Commemoration Collect",
    constants.COMMEMORATED_SECRETA: "Commemoration Secret",
    constants.COMMEMORATED_POSTCOMMUNIO: "Commemoration Postcommunion",
}
