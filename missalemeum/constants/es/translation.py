from ..la.translation import *
from .supplements import SUPPLEMENTS
from .pages import PAGES

TITLES = {
    constants.FERIA: "Feria",
    constants.TEMPORA_EPI1_0: "Sagrada Familia de Jesús, María y José",  # Sanctæ Familiæ Jesu Mariæ Joseph
    constants.TEMPORA_EPI1_1: "Lunes dentro de la Semana I después de la Epifanía",  # Feria II infra Hebd I post Epiphaniam
    constants.TEMPORA_EPI1_2: "Martes dentro de la Semana I después de la Epifanía",  # Feria III infra Hebd I post Epiphaniam
    constants.TEMPORA_EPI1_3: "Miércoles dentro de la Semana I después de la Epifanía",  # Feria IV infra Hebd I post Epiphaniam
    constants.TEMPORA_EPI1_4: "Jueves dentro de la Semana I después de la Epifanía",  # Feria V infra Hebd I post Epiphaniam
    constants.TEMPORA_EPI1_5: "Viernes dentro de la Semana I después de la Epifanía",  # Feria VI infra Hebd I post Epiphaniam
    constants.TEMPORA_EPI1_6: "Sábado dentro de la Semana I después de la Epifanía",  # Sabbato infra Hebd I post Epiphaniam
    constants.TEMPORA_EPI2_0: "Domingo II después de la Epifanía",  # Dominica II post Epiphaniam
    constants.TEMPORA_EPI2_1: "Lunes dentro de la Semana II después de la Epifanía",  # Feria II infra Hebd II post Epiphaniam
    constants.TEMPORA_EPI2_2: "Martes dentro de la Semana II después de la Epifanía",  # Feria III infra Hebd II post Epiphaniam
    constants.TEMPORA_EPI2_3: "Miércoles dentro de la Semana II después de la Epifanía",  # Feria IV infra Hebd II post Epiphaniam
    constants.TEMPORA_EPI2_4: "Jueves dentro de la Semana II después de la Epifanía",  # Feria V infra Hebd II post Epiphaniam
    constants.TEMPORA_EPI2_5: "Viernes dentro de la Semana II después de la Epifanía",  # Feria VI infra Hebd II post Epiphaniam
    constants.TEMPORA_EPI2_6: "Sábado dentro de la Semana II después de la Epifanía",  # Sabbato infra Hebd II post Epiphaniam
    constants.TEMPORA_EPI3_0: "Domingo III después de la Epifanía",  # Dominica III post Epiphaniam
    constants.TEMPORA_EPI3_1: "Lunes dentro de la Semana III después de la Epifanía",  # Feria II infra Hebd III post Epiphaniam
    constants.TEMPORA_EPI3_2: "Martes dentro de la Semana III después de la Epifanía",  # Feria III infra Hebd III post Epiphaniam
    constants.TEMPORA_EPI3_3: "Miércoles dentro de la Semana III después de la Epifanía",  # Feria IV infra Hebd III post Epiphaniam
    constants.TEMPORA_EPI3_4: "Jueves dentro de la Semana III después de la Epifanía",  # Feria V infra Hebd III post Epiphaniam
    constants.TEMPORA_EPI3_5: "Viernes dentro de la Semana III después de la Epifanía",  # Feria VI infra Hebd III post Epiphaniam
    constants.TEMPORA_EPI3_6: "Sábado dentro de la Semana III después de la Epifanía",  # Sabbato infra Hebd III post Epiphaniam
    constants.TEMPORA_EPI4_0: "Domingo IV después de la Epifanía",  # Dominica IV post Epiphaniam
    constants.TEMPORA_EPI4_1: "Lunes dentro de la Semana IV después de la Epifanía",  # Feria II infra Hebd IV post Epiphaniam
    constants.TEMPORA_EPI4_2: "Martes dentro de la Semana IV después de la Epifanía",  # Feria III infra Hebd IV post Epiphaniam
    constants.TEMPORA_EPI4_3: "Miércoles dentro de la Semana IV después de la Epifanía",  # Feria IV infra Hebd IV post Epiphaniam
    constants.TEMPORA_EPI4_4: "Jueves dentro de la Semana IV después de la Epifanía",  # Feria V infra Hebd IV post Epiphaniam
    constants.TEMPORA_EPI4_5: "Viernes dentro de la Semana IV después de la Epifanía",  # Feria VI infra Hebd IV post Epiphaniam
    constants.TEMPORA_EPI4_6: "Sábado dentro de la Semana IV después de la Epifanía",  # Sabbato infra Hebd IV post Epiphaniam
    constants.TEMPORA_EPI5_0: "Domingo V después de la Epifanía",  # Dominica V post Epiphaniam
    constants.TEMPORA_EPI5_1: "Lunes dentro de la Semana V después de la Epifanía",  # Feria II infra Hebd V post Epiphaniam
    constants.TEMPORA_EPI5_2: "Martes dentro de la Semana V después de la Epifanía",  # Feria III infra Hebd V post Epiphaniam
    constants.TEMPORA_EPI5_3: "Miércoles dentro de la Semana V después de la Epifanía",  # Feria IV infra Hebd V post Epiphaniam
    constants.TEMPORA_EPI5_4: "Jueves dentro de la Semana V después de la Epifanía",  # Feria V infra Hebd V post Epiphaniam
    constants.TEMPORA_EPI5_5: "Viernes dentro de la Semana V después de la Epifanía",  # Feria VI infra Hebd V post Epiphaniam
    constants.TEMPORA_EPI5_6: "Sábado dentro de la Semana V después de la Epifanía",  # Sabbato infra Hebd V post Epiphaniam
    constants.TEMPORA_EPI6_0: "Domingo VI después de la Epifanía",  # Dominica VI post Epiphaniam
    constants.TEMPORA_EPI6_1: "Lunes dentro de la Semana VI después de la Epifanía",  # Feria II infra Hebd VI post Epiphaniam
    constants.TEMPORA_EPI6_2: "Martes dentro de la Semana VI después de la Epifanía",  # Feria III infra Hebd VI post Epiphaniam
    constants.TEMPORA_EPI6_3: "Miércoles dentro de la Semana VI después de la Epifanía",  # Feria IV infra Hebd VI post Epiphaniam
    constants.TEMPORA_EPI6_4: "Jueves dentro de la Semana VI después de la Epifanía",  # Feria V infra Hebd VI post Epiphaniam
    constants.TEMPORA_EPI6_5: "Viernes dentro de la Semana VI después de la Epifanía",  # Feria VI infra Hebd VI post Epiphaniam
    constants.TEMPORA_EPI6_6: "Sábado dentro de la Semana VI después de la Epifanía",  # Sabbato infra Hebd VI post Epiphaniam
    constants.TEMPORA_QUADP1_0: "Domingo en Septuagésima",  # Dominica in Septuagesima
    constants.TEMPORA_QUADP1_1: "Lunes dentro de la Semana de Septuagésima",  # Feria II infra Hebd Septuagesimæ
    constants.TEMPORA_QUADP1_2: "Martes dentro de la Semana de Septuagésima",  # Feria III infra Hebd Septuagesimæ
    constants.TEMPORA_QUADP1_3: "Miércoles dentro de la Semana de Septuagésima",  # Feria IV infra Hebd Septuagesimæ
    constants.TEMPORA_QUADP1_4: "Jueves dentro de la Semana de Septuagésima",  # Feria V infra Hebd Septuagesimæ
    constants.TEMPORA_QUADP1_5: "Viernes dentro de la Semana de Septuagésima",  # Feria VI infra Hebd Septuagesimæ
    constants.TEMPORA_QUADP1_6: "Sábado dentro de la Semana de Septuagésima",  # Sabbato infra Hebd Septuagesimæ
    constants.TEMPORA_QUADP2_0: "Domingo en Sexagésima",  # Dominica in Sexagesima
    constants.TEMPORA_QUADP2_1: "Lunes dentro de la Semana de Sexagésima",  # Feria II infra Hebd Sexagesimæ
    constants.TEMPORA_QUADP2_2: "Martes dentro de la Semana de Sexagésima",  # Feria III infra Hebd Sexagesimæ
    constants.TEMPORA_QUADP2_3: "Miércoles dentro de la Semana de Sexagésima",  # Feria IV infra Hebd Sexagesimæ
    constants.TEMPORA_QUADP2_4: "Jueves dentro de la Semana de Sexagésima",  # Feria V infra Hebd Sexagesimæ
    constants.TEMPORA_QUADP2_5: "Viernes dentro de la Semana de Sexagésima",  # Feria VI infra Hebd Sexagesimæ
    constants.TEMPORA_QUADP2_6: "Sábado dentro de la Semana de Sexagésima",  # Sabbato infra Hebd Sexagesimæ
    constants.TEMPORA_QUADP3_0: "Domingo en Quincuagésima",  # Dominica in Quinquagesima
    constants.TEMPORA_QUADP3_1: "Lunes dentro de la Semana de Quincuagésima",  # Feria II infra Hebd Quinquagesimæ
    constants.TEMPORA_QUADP3_2: "Martes dentro de la Semana de Quincuagésima",  # Feria III infra Hebd Quinquagesimæ
    constants.TEMPORA_QUADP3_3: "Miércoles de Ceniza",  # Feria IV Cinerum
    constants.TEMPORA_QUADP3_4: "Jueves después de las Cenizas",  # Feria V post Cineres
    constants.TEMPORA_QUADP3_5: "Viernes después de las Cenizas",  # Feria VI post Cineres
    constants.TEMPORA_QUADP3_6: "Sábado después de las Cenizas",  # Sabbato post Cineres
    constants.TEMPORA_QUAD1_0: "Domingo I de Cuaresma",  # Dominica I in Quadragesimæ
    constants.TEMPORA_QUAD1_1: "Lunes dentro de la Semana I de Cuaresma",  # Feria II infra Hebd I Quadragesimæ
    constants.TEMPORA_QUAD1_2: "Martes dentro de la Semana I de Cuaresma",  # Feria III infra Hebd I Quadragesimæ
    constants.TEMPORA_QUAD1_3: "Miércoles de las Témporas de Cuaresma",  # Feria IV Quatuor Temporum Quadragesimæ
    constants.TEMPORA_QUAD1_4: "Jueves dentro de la Semana I de Cuaresma",  # Feria V infra Hebd I Quadragesimæ
    constants.TEMPORA_QUAD1_5: "Viernes de las Témporas de Cuaresma",  # Feria VI Quattuor Temporum Quadragesimæ
    constants.TEMPORA_QUAD1_6: "Sábado de las Témporas de Cuaresma",  # Sabbato Quattuor Temporum Quadragesimæ
    constants.TEMPORA_QUAD2_0: "Domingo II de Cuaresma",  # Dominica II in Quadragesimæ
    constants.TEMPORA_QUAD2_1: "Lunes dentro de la Semana II de Cuaresma",  # Feria II infra Hebd II Quadragesimæ
    constants.TEMPORA_QUAD2_2: "Martes dentro de la Semana II de Cuaresma",  # Feria III infra Hebd II Quadragesimæ
    constants.TEMPORA_QUAD2_3: "Miércoles dentro de la Semana II de Cuaresma",  # Feria IV infra Hebd II Quadragesimæ
    constants.TEMPORA_QUAD2_4: "Jueves dentro de la Semana II de Cuaresma",  # Feria V infra Hebd II Quadragesimæ
    constants.TEMPORA_QUAD2_5: "Viernes dentro de la Semana II de Cuaresma",  # Feria VI infra Hebd II Quadragesimæ
    constants.TEMPORA_QUAD2_6: "Sábado dentro de la Semana II de Cuaresma",  # Sabbato infra Hebd II Quadragesimæ
    constants.TEMPORA_QUAD3_0: "Domingo III de Cuaresma",  # Dominica III in Quadragesimæ
    constants.TEMPORA_QUAD3_1: "Lunes dentro de la Semana III de Cuaresma",  # Feria II infra Hebd III Quadragesimæ
    constants.TEMPORA_QUAD3_2: "Martes dentro de la Semana III de Cuaresma",  # Feria III infra Hebd III Quadragesimæ
    constants.TEMPORA_QUAD3_3: "Miércoles dentro de la Semana III de Cuaresma",  # Feria IV infra Hebd III Quadragesimæ
    constants.TEMPORA_QUAD3_4: "Jueves dentro de la Semana III de Cuaresma",  # Feria V infra Hebd III Quadragesimæ
    constants.TEMPORA_QUAD3_5: "Viernes dentro de la Semana III de Cuaresma",  # Feria VI infra Hebd III Quadragesimæ
    constants.TEMPORA_QUAD3_6: "Sábado dentro de la Semana III de Cuaresma",  # Sabbato infra Hebd III Quadragesimæ
    constants.TEMPORA_QUAD4_0: "Domingo IV de Cuaresma",  # Dominica IV in Quadragesimæ
    constants.TEMPORA_QUAD4_1: "Lunes dentro de la Semana IV de Cuaresma",  # Feria II infra Hebd IV Quadragesimæ
    constants.TEMPORA_QUAD4_2: "Martes dentro de la Semana IV de Cuaresma",  # Feria III infra Hebd IV Quadragesimæ
    constants.TEMPORA_QUAD4_3: "Miércoles dentro de la Semana IV de Cuaresma",  # Feria IV infra Hebd IV Quadragesimæ
    constants.TEMPORA_QUAD4_4: "Jueves dentro de la Semana IV de Cuaresma",  # Feria V infra Hebd IV Quadragesimæ
    constants.TEMPORA_QUAD4_5: "Viernes dentro de la Semana IV de Cuaresma",  # Feria VI infra Hebd IV Quadragesimæ
    constants.TEMPORA_QUAD4_6: "Sábado dentro de la Semana IV de Cuaresma",  # Sabbato infra Hebd IV Quadragesimæ
    constants.TEMPORA_QUAD5_0: "Domingo I de la Pasión",  # Dominica I Passionis
    constants.TEMPORA_QUAD5_1: "Lunes dentro de la Semana de la Pasión",  # Feria II infra Hebd Passionis
    constants.TEMPORA_QUAD5_2: "Martes dentro de la Semana de la Pasión",  # Feria III infra Hebd Passionis
    constants.TEMPORA_QUAD5_3: "Miércoles dentro de la Semana de la Pasión",  # Feria IV infra Hebd Passionis
    constants.TEMPORA_QUAD5_4: "Jueves dentro de la Semana de la Pasión",  # Feria V infra Hebd Passionis
    constants.TEMPORA_QUAD5_5: "Viernes dentro de la Semana de la Pasión",  # Feria VI infra Hebd Passionis
    constants.TEMPORA_QUAD5_6: "Sábado dentro de la Semana de la Pasión",  # Sabbato infra Hebd Passionis
    constants.TEMPORA_QUAD6_0: "Domingo II de la Pasión o de Ramos",  # Dominica II Passionis seu in Palmis
    constants.TEMPORA_QUAD6_1: "Lunes de la Semana Santa",  # Feria II Hebdomadæ Sanctæ
    constants.TEMPORA_QUAD6_2: "Martes de la Semana Santa",  # Feria III Hebdomadæ Sanctæ
    constants.TEMPORA_QUAD6_3: "Miércoles de la Semana Santa",  # Feria IV Hebdomadæ Sanctæ
    constants.TEMPORA_QUAD6_4: "Jueves Santo en la Cena del Señor",  # Feria Quinta in Coena Domini
    constants.TEMPORA_QUAD6_5: "Viernes Santo en la Pasión del Señor",  # Feria Sexta in Parasceve
    constants.TEMPORA_QUAD6_6: "Sábado Santo",  # Sabbato Sancto
    constants.TEMPORA_PASC0_0: "Domingo de Resurrección",  # Dominica Resurrectionis
    constants.TEMPORA_PASC0_1: "Lunes dentro de la octava de Pascua",  # Die II infra octavam Paschæ
    constants.TEMPORA_PASC0_2: "Martes dentro de la octava de Pascua",  # Die III infra octavam Paschæ
    constants.TEMPORA_PASC0_3: "Miércoles dentro de la octava de Pascua",  # Die VI infra octavam Paschæ
    constants.TEMPORA_PASC0_4: "Jueves dentro de la octava de Pascua",  # Die V infra octavam Paschæ
    constants.TEMPORA_PASC0_5: "Viernes dentro de la octava de Pascua",  # Die VI infra octavam Paschæ
    constants.TEMPORA_PASC0_6: "Sábado en Albis",  # Sabbato in Albis
    constants.TEMPORA_PASC1_0: "Domingo en Albis en la Octava de Pascua",  # Dominica in Albis in Octava Paschæ
    constants.TEMPORA_PASC1_1: "Lunes dentro de la Semana I después de la Octava de Pascua",  # Feria II infra Hebd I post Octavam Paschæ
    constants.TEMPORA_PASC1_2: "Martes dentro de la Semana I después de la Octava de Pascua",  # Feria III infra Hebd I post Octavam Paschæ
    constants.TEMPORA_PASC1_3: "Miércoles dentro de la Semana I después de la Octava de Pascua",  # Feria IV infra Hebd I post Octavam Paschæ
    constants.TEMPORA_PASC1_4: "Jueves dentro de la Semana I después de la Octava de Pascua",  # Feria V infra Hebd I post Octavam Paschæ
    constants.TEMPORA_PASC1_5: "Viernes dentro de la Semana I después de la Octava de Pascua",  # Feria VI infra Hebd I post Octavam Paschæ
    constants.TEMPORA_PASC1_6: "Sábado dentro de la Semana I después de la Octava de Pascua",  # Sabbato infra Hebd I post Octavam Paschæ
    constants.TEMPORA_PASC2_0: "Domingo II después de Pascua",  # Dominica II Post Pascha
    constants.TEMPORA_PASC2_1: "Lunes dentro de la Semana II después de la Octava de Pascua",  # Feria II infra Hebd II post Octavam Paschæ
    constants.TEMPORA_PASC2_2: "Martes dentro de la Semana II después de la Octava de Pascua",  # Feria III infra Hebd II post Octavam Paschæ
    constants.TEMPORA_PASC2_3: "Miércoles dentro de la Semana II después de la Octava de Pascua",  # Feria IV infra Hebd II post Octavam Paschæ
    constants.TEMPORA_PASC2_4: "Jueves dentro de la Semana II después de la Octava de Pascua",  # Feria V infra Hebd II post Octavam Paschæ
    constants.TEMPORA_PASC2_5: "Viernes dentro de la Semana II después de la Octava de Pascua",  # Feria VI infra Hebd II post Octavam Paschæ
    constants.TEMPORA_PASC2_6: "Sábado dentro de la Semana II después de la Octava de Pascua",  # Sabbato infra Hebd II post Octavam Paschæ
    constants.TEMPORA_PASC3_0: "Domingo III después de Pascua",  # Dominica III Post Pascha
    constants.TEMPORA_PASC3_1: "Lunes dentro de la Semana III después de la Octava de Pascua",  # Feria II infra Hebd III post Octavam Paschæ
    constants.TEMPORA_PASC3_2: "Martes dentro de la Semana III después de la Octava de Pascua",  # Feria III infra Hebd III post Octavam Paschæ
    constants.TEMPORA_PASC3_3: "Miércoles dentro de la Semana III después de la Octava de Pascua",  # Feria IV infra Hebd III post Octavam Paschæ
    constants.TEMPORA_PASC3_4: "Jueves dentro de la Semana III después de la Octava de Pascua",  # Feria V infra Hebd III post Octavam Paschæ
    constants.TEMPORA_PASC3_5: "Viernes dentro de la Semana III después de la Octava de Pascua",  # Feria VI infra Hebd III post Octavam Paschæ
    constants.TEMPORA_PASC3_6: "Sábado dentro de la Semana III después de la Octava de Pascua",  # Sabbato infra Hebd III post Octavam Paschæ
    constants.TEMPORA_PASC4_0: "Domingo IV después de Pascua",  # Dominica IV Post Pascha
    constants.TEMPORA_PASC4_1: "Lunes dentro de la Semana IV después de la Octava de Pascua",  # Feria II infra Hebd IV post Octavam Paschæ
    constants.TEMPORA_PASC4_2: "Martes dentro de la Semana IV después de la Octava de Pascua",  # Feria III infra Hebd IV post Octavam Paschæ
    constants.TEMPORA_PASC4_3: "Miércoles dentro de la Semana IV después de la Octava de Pascua",  # Feria IV infra Hebd IV post Octavam Paschæ
    constants.TEMPORA_PASC4_4: "Jueves dentro de la Semana IV después de la Octava de Pascua",  # Feria V infra Hebd IV post Octavam Paschæ
    constants.TEMPORA_PASC4_5: "Viernes dentro de la Semana IV después de la Octava de Pascua",  # Feria VI infra Hebd IV post Octavam Paschæ
    constants.TEMPORA_PASC4_6: "Sábado dentro de la Semana IV después de la Octava de Pascua",  # Sabbato infra Hebd IV post Octavam Paschæ
    constants.TEMPORA_PASC5_0: "Domingo V después de Pascua",  # Dominica V Post Pascha
    constants.TEMPORA_PASC5_1: "Lunes de Rogaciones",  # Feria II in Rogationibus
    constants.TEMPORA_PASC5_2: "Martes de Rogaciones",  # Feria III in Rogationibus
    constants.TEMPORA_PASC5_3: "Vigilia de la Ascensión del Señor",  # Wigilia Wniebowstąpienia Pańskiego
    constants.TEMPORA_PASC5_4: "En la Ascensión del Señor",  # In Ascensione Domini
    constants.TEMPORA_PASC5_5: "Viernes después de la Ascensión",  # Feria VI post Ascensionem
    constants.TEMPORA_PASC5_6: "Sábado después de la Ascensión",  # Sabbato post Ascensionem
    constants.TEMPORA_PASC6_0: "Domingo después de la Ascensión",  # Dominica post Ascensionem
    constants.TEMPORA_PASC6_1: "Lunes dentro de la Semana después de la Ascensión",  # Feria II infra Hebd post Ascensionem
    constants.TEMPORA_PASC6_2: "Martes dentro de la Semana después de la Ascensión",  # Feria III infra Hebd post Ascensionem
    constants.TEMPORA_PASC6_3: "Miércoles dentro de la Semana después de la Ascensión",  # Feria IV infra Hebd post Ascensionem
    constants.TEMPORA_PASC6_4: "Jueves dentro de la Semana después de la Ascensión",  # Feria V infra Hebd post Ascensionem
    constants.TEMPORA_PASC6_5: "Viernes dentro de la Semana después de la Ascensión",  # Feria VI infra Hebd post Ascensionem
    constants.TEMPORA_PASC6_6: "Sábado en la Vigilia de Pentecostés",  # Sabbato in Vigilia Pentecostes
    constants.TEMPORA_PASC7_0: "Domingo de Pentecostés",  # Dominica Pentecostes
    constants.TEMPORA_PASC7_1: "Lunes dentro de la octava de Pentecostés",  # Die II infra octavam Pentecostes
    constants.TEMPORA_PASC7_2: "Martes dentro de la octava de Pentecostés",  # Die III infra octavam Pentecostes
    constants.TEMPORA_PASC7_3: "Miércoles de las Témporas de Pentecostés",  # Feria IV Quattuor Temporum Pentecostes
    constants.TEMPORA_PASC7_4: "Jueves dentro de la octava de Pentecostés",  # Die V infra octavam Pentecostes
    constants.TEMPORA_PASC7_5: "Viernes de las Témporas de Pentecostés",  # Feria VI Quattuor temporum Pentecostes
    constants.TEMPORA_PASC7_6: "Sábado de las Témporas de Pentecostés",  # Sabbato Quattuor Temporum Pentecostes
    constants.TEMPORA_PENT01_0: "Domingo de la Santísima Trinidad",  # Dominica Sanctissimæ Trinitatis
    constants.TEMPORA_PENT01_1: "Lunes dentro de la Semana I después de la Octava de Pentecostés",  # Feria II infra Hebd I post Octavam Pentecostes
    constants.TEMPORA_PENT01_2: "Martes dentro de la Semana I después de la Octava de Pentecostés",  # Feria III infra Hebd I post Octavam Pentecostes
    constants.TEMPORA_PENT01_3: "Miércoles dentro de la Semana I después de la Octava de Pentecostés",  # Feria IV infra Hebd I post Octavam Pentecostes
    constants.TEMPORA_PENT01_4: "Fiesta del Santísimo Cuerpo de Cristo",  # Festum Sanctissimi Corporis Christi
    constants.TEMPORA_PENT01_5: "Jueves dentro de la Semana I después de la Octava de Pentecostés",  # Feria V infra Hebd I post Octavam Pentecostes
    constants.TEMPORA_PENT01_6: "Sábado dentro de la Semana I después de la Octava de Pentecostés",  # Sabbato infra Hebd I post Octavam Pentecostes
    constants.TEMPORA_PENT02_0: "Domingo II después de Pentecostés",  # Dominica II Post Pentecosten
    constants.TEMPORA_PENT02_1: "Lunes dentro de la Semana II después de la Octava de Pentecostés",  # Feria II infra Hebd II post Octavam Pentecostes
    constants.TEMPORA_PENT02_2: "Martes dentro de la Semana II después de la Octava de Pentecostés",  # Feria III infra Hebd II post Octavam Pentecostes
    constants.TEMPORA_PENT02_3: "Miércoles dentro de la Semana II después de la Octava de Pentecostés",  # Feria IV infra Hebd II post Octavam Pentecostes
    constants.TEMPORA_PENT02_4: "Jueves dentro de la Semana II después de la Octava de Pentecostés",  # Feria V infra Hebd II post Octavam Pentecostes
    constants.TEMPORA_PENT02_5: "Santísimo Corazón de Nuestro Señor Jesucristo",  # Sanctissimi Cordis Domini Nostri Jesu Christi
    constants.TEMPORA_PENT02_6: "Sábado dentro de la Semana II después de la Octava de Pentecostés",  # Sabbato infra Hebd II post Octavam Pentecostes
    constants.TEMPORA_PENT03_0: "Domingo III después de Pentecostés",  # Dominica III Post Pentecosten
    constants.TEMPORA_PENT03_1: "Lunes dentro de la Semana III después de la Octava de Pentecostés",  # Feria II infra Hebd III post Octavam Pentecostes
    constants.TEMPORA_PENT03_2: "Martes dentro de la Semana III después de la Octava de Pentecostés",  # Feria III infra Hebd III post Octavam Pentecostes
    constants.TEMPORA_PENT03_3: "Miércoles dentro de la Semana III después de la Octava de Pentecostés",  # Feria IV infra Hebd III post Octavam Pentecostes
    constants.TEMPORA_PENT03_4: "Jueves dentro de la Semana III después de la Octava de Pentecostés",  # Feria V infra Hebd III post Octavam Pentecostes
    constants.TEMPORA_PENT03_5: "Viernes dentro de la Semana III después de la Octava de Pentecostés",  # Feria VI infra Hebd III post Octavam Pentecostes
    constants.TEMPORA_PENT03_6: "Sábado dentro de la Semana III después de la Octava de Pentecostés",  # Sabbato infra Hebd III post Octavam Pentecostes
    constants.TEMPORA_PENT04_0: "Domingo IV después de Pentecostés",  # Dominica IV Post Pentecosten
    constants.TEMPORA_PENT04_1: "Lunes dentro de la Semana IV después de la Octava de Pentecostés",  # Feria II infra Hebd IV post Octavam Pentecostes
    constants.TEMPORA_PENT04_2: "Martes dentro de la Semana IV después de la Octava de Pentecostés",  # Feria III infra Hebd IV post Octavam Pentecostes
    constants.TEMPORA_PENT04_3: "Miércoles dentro de la Semana IV después de la Octava de Pentecostés",  # Feria IV infra Hebd IV post Octavam Pentecostes
    constants.TEMPORA_PENT04_4: "Jueves dentro de la Semana IV después de la Octava de Pentecostés",  # Feria V infra Hebd IV post Octavam Pentecostes
    constants.TEMPORA_PENT04_5: "Viernes dentro de la Semana IV después de la Octava de Pentecostés",  # Feria VI infra Hebd IV post Octavam Pentecostes
    constants.TEMPORA_PENT04_6: "Sábado dentro de la Semana IV después de la Octava de Pentecostés",  # Sabbato infra Hebd IV post Octavam Pentecostes
    constants.TEMPORA_PENT05_0: "Domingo V después de Pentecostés",  # Dominica V Post Pentecosten
    constants.TEMPORA_PENT05_1: "Lunes dentro de la Semana V después de la Octava de Pentecostés",  # Feria II infra Hebd V post Octavam Pentecostes
    constants.TEMPORA_PENT05_2: "Martes dentro de la Semana V después de la Octava de Pentecostés",  # Feria III infra Hebd V post Octavam Pentecostes
    constants.TEMPORA_PENT05_3: "Miércoles dentro de la Semana V después de la Octava de Pentecostés",  # Feria IV infra Hebd V post Octavam Pentecostes
    constants.TEMPORA_PENT05_4: "Jueves dentro de la Semana V después de la Octava de Pentecostés",  # Feria V infra Hebd V post Octavam Pentecostes
    constants.TEMPORA_PENT05_5: "Viernes dentro de la Semana V después de la Octava de Pentecostés",  # Feria VI infra Hebd V post Octavam Pentecostes
    constants.TEMPORA_PENT05_6: "Sábado dentro de la Semana V después de la Octava de Pentecostés",  # Sabbato infra Hebd V post Octavam Pentecostes
    constants.TEMPORA_PENT06_0: "Domingo VI después de Pentecostés",  # Dominica VI Post Pentecosten
    constants.TEMPORA_PENT06_1: "Lunes dentro de la Semana VI después de la Octava de Pentecostés",  # Feria II infra Hebd VI post Octavam Pentecostes
    constants.TEMPORA_PENT06_2: "Martes dentro de la Semana VI después de la Octava de Pentecostés",  # Feria III infra Hebd VI post Octavam Pentecostes
    constants.TEMPORA_PENT06_3: "Miércoles dentro de la Semana VI después de la Octava de Pentecostés",  # Feria IV infra Hebd VI post Octavam Pentecostes
    constants.TEMPORA_PENT06_4: "Jueves dentro de la Semana VI después de la Octava de Pentecostés",  # Feria V infra Hebd VI post Octavam Pentecostes
    constants.TEMPORA_PENT06_5: "Viernes dentro de la Semana VI después de la Octava de Pentecostés",  # Feria VI infra Hebd VI post Octavam Pentecostes
    constants.TEMPORA_PENT06_6: "Sábado dentro de la Semana VI después de la Octava de Pentecostés",  # Sabbato infra Hebd VI post Octavam Pentecostes
    constants.TEMPORA_PENT07_0: "Domingo VII después de Pentecostés",  # Dominica VII Post Pentecosten
    constants.TEMPORA_PENT07_1: "Lunes dentro de la Semana VII después de la Octava de Pentecostés",  # Feria II infra Hebd VII post Octavam Pentecostes
    constants.TEMPORA_PENT07_2: "Martes dentro de la Semana VII después de la Octava de Pentecostés",  # Feria III infra Hebd VII post Octavam Pentecostes
    constants.TEMPORA_PENT07_3: "Miércoles dentro de la Semana VII después de la Octava de Pentecostés",  # Feria IV infra Hebd VII post Octavam Pentecostes
    constants.TEMPORA_PENT07_4: "Jueves dentro de la Semana VII después de la Octava de Pentecostés",  # Feria V infra Hebd VII post Octavam Pentecostes
    constants.TEMPORA_PENT07_5: "Viernes dentro de la Semana VII después de la Octava de Pentecostés",  # Feria VI infra Hebd VII post Octavam Pentecostes
    constants.TEMPORA_PENT07_6: "Sábado dentro de la Semana VII después de la Octava de Pentecostés",  # Sabbato infra Hebd VII post Octavam Pentecostes
    constants.TEMPORA_PENT08_0: "Domingo VIII después de Pentecostés",  # Dominica VIII Post Pentecosten
    constants.TEMPORA_PENT08_1: "Lunes dentro de la Semana VIII después de la Octava de Pentecostés",  # Feria II infra Hebd VIII post Octavam Pentecostes
    constants.TEMPORA_PENT08_2: "Martes dentro de la Semana VIII después de la Octava de Pentecostés",  # Feria III infra Hebd VIII post Octavam Pentecostes
    constants.TEMPORA_PENT08_3: "Miércoles dentro de la Semana VIII después de la Octava de Pentecostés",  # Feria IV infra Hebd VIII post Octavam Pentecostes
    constants.TEMPORA_PENT08_4: "Jueves dentro de la Semana VIII después de la Octava de Pentecostés",  # Feria V infra Hebd VIII post Octavam Pentecostes
    constants.TEMPORA_PENT08_5: "Viernes dentro de la Semana VIII después de la Octava de Pentecostés",  # Feria VI infra Hebd VIII post Octavam Pentecostes
    constants.TEMPORA_PENT08_6: "Sábado dentro de la Semana VIII después de la Octava de Pentecostés",  # Sabbato infra Hebd VIII post Octavam Pentecostes
    constants.TEMPORA_PENT09_0: "Domingo IX después de Pentecostés",  # Dominica IX Post Pentecosten
    constants.TEMPORA_PENT09_1: "Lunes dentro de la Semana IX después de la Octava de Pentecostés",  # Feria II infra Hebd IX post Octavam Pentecostes
    constants.TEMPORA_PENT09_2: "Martes dentro de la Semana IX después de la Octava de Pentecostés",  # Feria III infra Hebd IX post Octavam Pentecostes
    constants.TEMPORA_PENT09_3: "Miércoles dentro de la Semana IX después de la Octava de Pentecostés",  # Feria IV infra Hebd IX post Octavam Pentecostes
    constants.TEMPORA_PENT09_4: "Jueves dentro de la Semana IX después de la Octava de Pentecostés",  # Feria V infra Hebd IX post Octavam Pentecostes
    constants.TEMPORA_PENT09_5: "Viernes dentro de la Semana IX después de la Octava de Pentecostés",  # Feria VI infra Hebd IX post Octavam Pentecostes
    constants.TEMPORA_PENT09_6: "Sábado dentro de la Semana IX después de la Octava de Pentecostés",  # Sabbato infra Hebd IX post Octavam Pentecostes
    constants.TEMPORA_PENT10_0: "Domingo X después de Pentecostés",  # Dominica X Post Pentecosten
    constants.TEMPORA_PENT10_1: "Lunes dentro de la Semana X después de la Octava de Pentecostés",  # Feria II infra Hebd X post Octavam Pentecostes
    constants.TEMPORA_PENT10_2: "Martes dentro de la Semana X después de la Octava de Pentecostés",  # Feria III infra Hebd X post Octavam Pentecostes
    constants.TEMPORA_PENT10_3: "Miércoles dentro de la Semana X después de la Octava de Pentecostés",  # Feria IV infra Hebd X post Octavam Pentecostes
    constants.TEMPORA_PENT10_4: "Jueves dentro de la Semana X después de la Octava de Pentecostés",  # Feria V infra Hebd X post Octavam Pentecostes
    constants.TEMPORA_PENT10_5: "Viernes dentro de la Semana X después de la Octava de Pentecostés",  # Feria VI infra Hebd X post Octavam Pentecostes
    constants.TEMPORA_PENT10_6: "Sábado dentro de la Semana X después de la Octava de Pentecostés",  # Sabbato infra Hebd X post Octavam Pentecostes
    constants.TEMPORA_PENT11_0: "Domingo XI después de Pentecostés",  # Dominica XI Post Pentecosten
    constants.TEMPORA_PENT11_1: "Lunes dentro de la Semana XI después de la Octava de Pentecostés",  # Feria II infra Hebd XI post Octavam Pentecostes
    constants.TEMPORA_PENT11_2: "Martes dentro de la Semana XI después de la Octava de Pentecostés",  # Feria III infra Hebd XI post Octavam Pentecostes
    constants.TEMPORA_PENT11_3: "Miércoles dentro de la Semana XI después de la Octava de Pentecostés",  # Feria IV infra Hebd XI post Octavam Pentecostes
    constants.TEMPORA_PENT11_4: "Jueves dentro de la Semana XI después de la Octava de Pentecostés",  # Feria V infra Hebd XI post Octavam Pentecostes
    constants.TEMPORA_PENT11_5: "Viernes dentro de la Semana XI después de la Octava de Pentecostés",  # Feria VI infra Hebd XI post Octavam Pentecostes
    constants.TEMPORA_PENT11_6: "Sábado dentro de la Semana XI después de la Octava de Pentecostés",  # Sabbato infra Hebd XI post Octavam Pentecostes
    constants.TEMPORA_PENT12_0: "Domingo XII después de Pentecostés",  # Dominica XII Post Pentecosten
    constants.TEMPORA_PENT12_1: "Lunes dentro de la Semana XII después de la Octava de Pentecostés",  # Feria II infra Hebd XII post Octavam Pentecostes
    constants.TEMPORA_PENT12_2: "Martes dentro de la Semana XII después de la Octava de Pentecostés",  # Feria III infra Hebd XII post Octavam Pentecostes
    constants.TEMPORA_PENT12_3: "Miércoles dentro de la Semana XII después de la Octava de Pentecostés",  # Feria IV infra Hebd XII post Octavam Pentecostes
    constants.TEMPORA_PENT12_4: "Jueves dentro de la Semana XII después de la Octava de Pentecostés",  # Feria V infra Hebd XII post Octavam Pentecostes
    constants.TEMPORA_PENT12_5: "Viernes dentro de la Semana XII después de la Octava de Pentecostés",  # Feria VI infra Hebd XII post Octavam Pentecostes
    constants.TEMPORA_PENT12_6: "Sábado dentro de la Semana XII después de la Octava de Pentecostés",  # Sabbato infra Hebd XII post Octavam Pentecostes
    constants.TEMPORA_PENT13_0: "Domingo XIII después de Pentecostés",  # Dominica XIII Post Pentecosten
    constants.TEMPORA_PENT13_1: "Lunes dentro de la Semana XIII después de la Octava de Pentecostés",  # Feria II infra Hebd XIII post Octavam Pentecostes
    constants.TEMPORA_PENT13_2: "Martes dentro de la Semana XIII después de la Octava de Pentecostés",  # Feria III infra Hebd XIII post Octavam Pentecostes
    constants.TEMPORA_PENT13_3: "Miércoles dentro de la Semana XIII después de la Octava de Pentecostés",  # Feria IV infra Hebd XIII post Octavam Pentecostes
    constants.TEMPORA_PENT13_4: "Jueves dentro de la Semana XIII después de la Octava de Pentecostés",  # Feria V infra Hebd XIII post Octavam Pentecostes
    constants.TEMPORA_PENT13_5: "Viernes dentro de la Semana XIII después de la Octava de Pentecostés",  # Feria VI infra Hebd XIII post Octavam Pentecostes
    constants.TEMPORA_PENT13_6: "Sábado dentro de la Semana XIII después de la Octava de Pentecostés",  # Sabbato infra Hebd XIII post Octavam Pentecostes
    constants.TEMPORA_PENT14_0: "Domingo XIV después de Pentecostés",  # Dominica XIV Post Pentecosten
    constants.TEMPORA_PENT14_1: "Lunes dentro de la Semana XIV después de la Octava de Pentecostés",  # Feria II infra Hebd XIV post Octavam Pentecostes
    constants.TEMPORA_PENT14_2: "Martes dentro de la Semana XIV después de la Octava de Pentecostés",  # Feria III infra Hebd XIV post Octavam Pentecostes
    constants.TEMPORA_PENT14_3: "Miércoles dentro de la Semana XIV después de la Octava de Pentecostés",  # Feria IV infra Hebd XIV post Octavam Pentecostes
    constants.TEMPORA_PENT14_4: "Jueves dentro de la Semana XIV después de la Octava de Pentecostés",  # Feria V infra Hebd XIV post Octavam Pentecostes
    constants.TEMPORA_PENT14_5: "Viernes dentro de la Semana XIV después de la Octava de Pentecostés",  # Feria VI infra Hebd XIV post Octavam Pentecostes
    constants.TEMPORA_PENT14_6: "Sábado dentro de la Semana XIV después de la Octava de Pentecostés",  # Sabbato infra Hebd XIV post Octavam Pentecostes
    constants.TEMPORA_PENT15_0: "Domingo XV después de Pentecostés",  # Dominica XV Post Pentecosten
    constants.TEMPORA_PENT15_1: "Lunes dentro de la Semana XV después de la Octava de Pentecostés",  # Feria II infra Hebd XV post Octavam Pentecostes
    constants.TEMPORA_PENT15_2: "Martes dentro de la Semana XV después de la Octava de Pentecostés",  # Feria III infra Hebd XV post Octavam Pentecostes
    constants.TEMPORA_PENT15_3: "Miércoles dentro de la Semana XV después de la Octava de Pentecostés",  # Feria IV infra Hebd XV post Octavam Pentecostes
    constants.TEMPORA_PENT15_4: "Jueves dentro de la Semana XV después de la Octava de Pentecostés",  # Feria V infra Hebd XV post Octavam Pentecostes
    constants.TEMPORA_PENT15_5: "Viernes dentro de la Semana XV después de la Octava de Pentecostés",  # Feria VI infra Hebd XV post Octavam Pentecostes
    constants.TEMPORA_PENT15_6: "Sábado dentro de la Semana XV después de la Octava de Pentecostés",  # Sabbato infra Hebd XV post Octavam Pentecostes
    constants.TEMPORA_PENT16_0: "Domingo XVI después de Pentecostés",  # Dominica XVI Post Pentecosten
    constants.TEMPORA_PENT16_1: "Lunes dentro de la Semana XVI después de la Octava de Pentecostés",  # Feria II infra Hebd XVI post Octavam Pentecostes
    constants.TEMPORA_PENT16_2: "Martes dentro de la Semana XVI después de la Octava de Pentecostés",  # Feria III infra Hebd XVI post Octavam Pentecostes
    constants.TEMPORA_PENT16_3: "Miércoles dentro de la Semana XVI después de la Octava de Pentecostés",  # Feria IV infra Hebd XVI post Octavam Pentecostes
    constants.TEMPORA_PENT16_4: "Jueves dentro de la Semana XVI después de la Octava de Pentecostés",  # Feria V infra Hebd XVI post Octavam Pentecostes
    constants.TEMPORA_PENT16_5: "Viernes dentro de la Semana XVI después de la Octava de Pentecostés",  # Feria VI infra Hebd XVI post Octavam Pentecostes
    constants.TEMPORA_PENT16_6: "Sábado dentro de la Semana XVI después de la Octava de Pentecostés",  # Sabbato infra Hebd XVI post Octavam Pentecostes
    constants.TEMPORA_PENT17_0: "Domingo XVII después de Pentecostés",  # Dominica XVII Post Pentecosten
    constants.TEMPORA_PENT17_1: "Lunes dentro de la Semana XVII después de la Octava de Pentecostés",  # Feria II infra Hebd XVII post Octavam Pentecostes
    constants.TEMPORA_PENT17_2: "Martes dentro de la Semana XVII después de la Octava de Pentecostés",  # Feria III infra Hebd XVII post Octavam Pentecostes
    constants.TEMPORA_PENT17_3: "Miércoles dentro de la Semana XVII después de la Octava de Pentecostés",  # Feria IV infra Hebd XVII post Octavam Pentecostes
    constants.TEMPORA_PENT17_4: "Jueves dentro de la Semana XVII después de la Octava de Pentecostés",  # Feria V infra Hebd XVII post Octavam Pentecostes
    constants.TEMPORA_PENT17_5: "Viernes dentro de la Semana XVII después de la Octava de Pentecostés",  # Feria VI infra Hebd XVII post Octavam Pentecostes
    constants.TEMPORA_PENT17_6: "Sábado dentro de la Semana XVII después de la Octava de Pentecostés",  # Sabbato infra Hebd XVII post Octavam Pentecostes
    constants.TEMPORA_PENT18_0: "Domingo XVIII después de Pentecostés",  # Dominica XVIII Post Pentecosten
    constants.TEMPORA_PENT18_1: "Lunes dentro de la Semana XVIII después de la Octava de Pentecostés",  # Feria II infra Hebd XVIII post Octavam Pentecostes
    constants.TEMPORA_PENT18_2: "Martes dentro de la Semana XVIII después de la Octava de Pentecostés",  # Feria III infra Hebd XVIII post Octavam Pentecostes
    constants.TEMPORA_PENT18_3: "Miércoles dentro de la Semana XVIII después de la Octava de Pentecostés",  # Feria IV infra Hebd XVIII post Octavam Pentecostes
    constants.TEMPORA_PENT18_4: "Jueves dentro de la Semana XVIII después de la Octava de Pentecostés",  # Feria V infra Hebd XVIII post Octavam Pentecostes
    constants.TEMPORA_PENT18_5: "Viernes dentro de la Semana XVIII después de la Octava de Pentecostés",  # Feria VI infra Hebd XVIII post Octavam Pentecostes
    constants.TEMPORA_PENT18_6: "Sábado dentro de la Semana XVIII después de la Octava de Pentecostés",  # Sabbato infra Hebd XVIII post Octavam Pentecostes
    constants.TEMPORA_PENT19_0: "Domingo XIX después de Pentecostés",  # Dominica XIX Post Pentecosten
    constants.TEMPORA_PENT19_1: "Lunes dentro de la Semana XIX después de la Octava de Pentecostés",  # Feria II infra Hebd XIX post Octavam Pentecostes
    constants.TEMPORA_PENT19_2: "Martes dentro de la Semana XIX después de la Octava de Pentecostés",  # Feria III infra Hebd XIX post Octavam Pentecostes
    constants.TEMPORA_PENT19_3: "Miércoles dentro de la Semana XIX después de la Octava de Pentecostés",  # Feria IV infra Hebd XIX post Octavam Pentecostes
    constants.TEMPORA_PENT19_4: "Jueves dentro de la Semana XIX después de la Octava de Pentecostés",  # Feria V infra Hebd XIX post Octavam Pentecostes
    constants.TEMPORA_PENT19_5: "Viernes dentro de la Semana XIX después de la Octava de Pentecostés",  # Feria VI infra Hebd XIX post Octavam Pentecostes
    constants.TEMPORA_PENT19_6: "Sábado dentro de la Semana XIX después de la Octava de Pentecostés",  # Sabbato infra Hebd XIX post Octavam Pentecostes
    constants.TEMPORA_PENT20_0: "Domingo XX después de Pentecostés",  # Dominica XX Post Pentecosten
    constants.TEMPORA_PENT20_1: "Lunes dentro de la Semana XX después de la Octava de Pentecostés",  # Feria II infra Hebd XX post Octavam Pentecostes
    constants.TEMPORA_PENT20_2: "Martes dentro de la Semana XX después de la Octava de Pentecostés",  # Feria III infra Hebd XX post Octavam Pentecostes
    constants.TEMPORA_PENT20_3: "Miércoles dentro de la Semana XX después de la Octava de Pentecostés",  # Feria IV infra Hebd XX post Octavam Pentecostes
    constants.TEMPORA_PENT20_4: "Jueves dentro de la Semana XX después de la Octava de Pentecostés",  # Feria V infra Hebd XX post Octavam Pentecostes
    constants.TEMPORA_PENT20_5: "Viernes dentro de la Semana XX después de la Octava de Pentecostés",  # Feria VI infra Hebd XX post Octavam Pentecostes
    constants.TEMPORA_PENT20_6: "Sábado dentro de la Semana XX después de la Octava de Pentecostés",  # Sabbato infra Hebd XX post Octavam Pentecostes
    constants.TEMPORA_PENT21_0: "Domingo XXI después de Pentecostés",  # Dominica XXI Post Pentecosten
    constants.TEMPORA_PENT21_1: "Lunes dentro de la Semana XXI después de la Octava de Pentecostés",  # Feria II infra Hebd XXI post Octavam Pentecostes
    constants.TEMPORA_PENT21_2: "Martes dentro de la Semana XXI después de la Octava de Pentecostés",  # Feria III infra Hebd XXI post Octavam Pentecostes
    constants.TEMPORA_PENT21_3: "Miércoles dentro de la Semana XXI después de la Octava de Pentecostés",  # Feria IV infra Hebd XXI post Octavam Pentecostes
    constants.TEMPORA_PENT21_4: "Jueves dentro de la Semana XXI después de la Octava de Pentecostés",  # Feria V infra Hebd XXI post Octavam Pentecostes
    constants.TEMPORA_PENT21_5: "Viernes dentro de la Semana XXI después de la Octava de Pentecostés",  # Feria VI infra Hebd XXI post Octavam Pentecostes
    constants.TEMPORA_PENT21_6: "Sábado dentro de la Semana XXI después de la Octava de Pentecostés",  # Sabbato infra Hebd XXI post Octavam Pentecostes
    constants.TEMPORA_PENT22_0: "Domingo XXII después de Pentecostés",  # Dominica XXII Post Pentecosten
    constants.TEMPORA_PENT22_1: "Lunes dentro de la Semana XXII después de la Octava de Pentecostés",  # Feria II infra Hebd XXII post Octavam Pentecostes
    constants.TEMPORA_PENT22_2: "Martes dentro de la Semana XXII después de la Octava de Pentecostés",  # Feria III infra Hebd XXII post Octavam Pentecostes
    constants.TEMPORA_PENT22_3: "Miércoles dentro de la Semana XXII después de la Octava de Pentecostés",  # Feria IV infra Hebd XXII post Octavam Pentecostes
    constants.TEMPORA_PENT22_4: "Jueves dentro de la Semana XXII después de la Octava de Pentecostés",  # Feria V infra Hebd XXII post Octavam Pentecostes
    constants.TEMPORA_PENT22_5: "Viernes dentro de la Semana XXII después de la Octava de Pentecostés",  # Feria VI infra Hebd XXII post Octavam Pentecostes
    constants.TEMPORA_PENT22_6: "Sábado dentro de la Semana XXII después de la Octava de Pentecostés",  # Sabbato infra Hebd XXII post Octavam Pentecostes
    constants.TEMPORA_PENT23_0: "Domingo XXIII después de Pentecostés",  # Dominica XXIII Post Pentecosten
    constants.TEMPORA_PENT23_1: "Lunes dentro de la Semana XXIII después de la Octava de Pentecostés",  # Feria II infra Hebd XXIII post Octavam Pentecostes
    constants.TEMPORA_PENT23_2: "Martes dentro de la Semana XXIII después de la Octava de Pentecostés",  # Feria III infra Hebd XXIII post Octavam Pentecostes
    constants.TEMPORA_PENT23_3: "Miércoles dentro de la Semana XXIII después de la Octava de Pentecostés",  # Feria IV infra Hebd XXIII post Octavam Pentecostes
    constants.TEMPORA_PENT23_4: "Jueves dentro de la Semana XXIII después de la Octava de Pentecostés",  # Feria V infra Hebd XXIII post Octavam Pentecostes
    constants.TEMPORA_PENT23_5: "Viernes dentro de la Semana XXIII después de la Octava de Pentecostés",  # Feria VI infra Hebd XXIII post Octavam Pentecostes
    constants.TEMPORA_PENT23_6: "Sábado dentro de la Semana XXIII después de la Octava de Pentecostés",  # Sabbato infra Hebd XXIII post Octavam Pentecostes
    constants.TEMPORA_PENT_3: "Miércoles de las Témporas de Septiembre",  # Feria IV Quattuor Temporum Septembris
    constants.TEMPORA_PENT_5: "Viernes de las Témporas de Septiembre",  # Feria VI Quattuor Temporum Septembris
    constants.TEMPORA_PENT_6: "Sábado de las Témporas de Septiembre",  # Sabbato Quattuor Temporum Septembris
    constants.TEMPORA_PENT24_0: "Domingo XXIV después de Pentecostés",  # Dominica XXIV Post Pentecosten
    constants.TEMPORA_PENT24_1: "Lunes dentro de la Semana XXIV después de la Octava de Pentecostés",  # Feria II infra Hebd XXIV post Octavam Pentecostes
    constants.TEMPORA_PENT24_2: "Martes dentro de la Semana XXIV después de la Octava de Pentecostés",  # Feria III infra Hebd XXIV post Octavam Pentecostes
    constants.TEMPORA_PENT24_3: "Miércoles dentro de la Semana XXIV después de la Octava de Pentecostés",  # Feria IV infra Hebd XXIV post Octavam Pentecostes
    constants.TEMPORA_PENT24_4: "Jueves dentro de la Semana XXIV después de la Octava de Pentecostés",  # Feria V infra Hebd XXIV post Octavam Pentecostes
    constants.TEMPORA_PENT24_5: "Viernes dentro de la Semana XXIV después de la Octava de Pentecostés",  # Feria VI infra Hebd XXIV post Octavam Pentecostes
    constants.TEMPORA_PENT24_6: "Sábado dentro de la Semana XXIV después de la Octava de Pentecostés",  # Sabbato infra Hebd XXIV post Octavam Pentecostes
    constants.TEMPORA_ADV1_0: "Domingo I de Adviento",  # Dominica I Adventus
    constants.TEMPORA_ADV1_1: "Lunes dentro de la Semana I de Adviento",  # Feria II infra Hebd I Adventus
    constants.TEMPORA_ADV1_2: "Martes dentro de la Semana I de Adviento",  # Feria III infra Hebd I Adventus
    constants.TEMPORA_ADV1_3: "Miércoles dentro de la Semana I de Adviento",  # Feria IV infra Hebd I Adventus
    constants.TEMPORA_ADV1_4: "Jueves dentro de la Semana I de Adviento",  # Feria V infra Hebd I Adventus
    constants.TEMPORA_ADV1_5: "Viernes dentro de la Semana I de Adviento",  # Feria VI infra Hebd I Adventus
    constants.TEMPORA_ADV1_6: "Sábado dentro de la Semana I de Adviento",  # Sabbato infra Hebd I Adventus
    constants.TEMPORA_ADV2_0: "Domingo II de Adviento",  # Dominica II Adventus
    constants.TEMPORA_ADV2_1: "Lunes dentro de la Semana II de Adviento",  # Feria II infra Hebd II Adventus
    constants.TEMPORA_ADV2_2: "Martes dentro de la Semana II de Adviento",  # Feria III infra Hebd II Adventus
    constants.TEMPORA_ADV2_3: "Miércoles dentro de la Semana II de Adviento",  # Feria IV infra Hebd II Adventus
    constants.TEMPORA_ADV2_4: "Jueves dentro de la Semana II de Adviento",  # Feria V infra Hebd II Adventus
    constants.TEMPORA_ADV2_5: "Viernes dentro de la Semana II de Adviento",  # Feria VI infra Hebd II Adventus
    constants.TEMPORA_ADV2_6: "Sábado dentro de la Semana II de Adviento",  # Sabbato infra Hebd II Adventus
    constants.TEMPORA_ADV3_0: "Domingo III de Adviento",  # Dominica III Adventus
    constants.TEMPORA_ADV3_1: "Lunes dentro de la Semana IV de Adviento",  # Feria II infra Hebd IV Adventus
    constants.TEMPORA_ADV3_2: "Martes dentro de la Semana IV de Adviento",  # Feria III infra Hebd IV Adventus
    constants.TEMPORA_ADV3_3: "Miércoles de las Témporas de Adviento",  # Feria IV Quattuor Temporum Adventus
    constants.TEMPORA_ADV3_4: "Jueves dentro de la Semana IV de Adviento",  # Feria V infra Hebd IV Adventus
    constants.TEMPORA_ADV3_5: "Viernes de las Témporas de Adviento",  # Feria VI Quattuor Temporum Adventus
    constants.TEMPORA_ADV3_6: "Sábado de las Témporas de Adviento",  # Sabbato Temporum Adventus
    constants.TEMPORA_ADV4_0: "Domingo IV de Adviento",  # Dominica IV Adventus
    constants.TEMPORA_ADV4_1: "Lunes dentro de la Semana IV de Adviento",  # Feria II infra Hebd IV Adventus
    constants.TEMPORA_ADV4_2: "Martes dentro de la Semana IV de Adviento",  # Feria III infra Hebd IV Adventus
    constants.TEMPORA_ADV4_3: "Miércoles dentro de la Semana IV de Adviento",  # Feria IV infra Hebd IV Adventus
    constants.TEMPORA_ADV4_4: "Jueves dentro de la Semana IV de Adviento",  # Feria V infra Hebd IV Adventus
    constants.TEMPORA_ADV4_5: "Viernes dentro de la Semana IV de Adviento",  # Feria VI infra Hebd IV Adventus
    constants.TEMPORA_NAT1_0: "Domingo dentro de la Octava de Navidad",  # Dominica Infra Octavam Nativitatis
    constants.TEMPORA_NAT1_1: "Día dentro de la Octava de Navidad",  # Feria Infra Octavam Nativitatis
    constants.TEMPORA_NAT2_0: "Santísimo Nombre de Jesús",  # Sanctissimi Nominis Jesu
    constants.SANCTI_10_DU: "En la fiesta de nuestro Señor Jesucristo Rey",  # In festo Domino nostro Jesu Christi Regis
    constants.TEMPORA_EPI1_0A: "Domingo después de la Epifanía",  # Dominica post Epiphaniam
    constants.TEMPORA_PENT01_0A: "Domingo después de Pentecostés",  # Dominica Post Pentecosten
    constants.TEMPORA_C_10A: "1 Misa de la B. V. M. – Rorate",  # 1 Missa B. V. M. – Rorate
    constants.COMMUNE_C_10A: "1 Misa de la B. V. M. – Rorate",  # 1 Missa B. V. M. – Rorate
    constants.TEMPORA_C_10B: "2 Misa de la B. V. M. – Vultum Tuum",  # 2 Missa B. V. M. – Vultum Tuum
    constants.COMMUNE_C_10B: "2 Misa de la B. V. M. – Vultum Tuum",  # 2 Missa B. V. M. – Vultum Tuum
    constants.TEMPORA_C_10C: "3 Misa de la B. V. M. – Salve, Sancta Parens",  # 3 Missa B. V. M. – Salve, Sancta Parens
    constants.COMMUNE_C_10C: "3 Misa de la B. V. M. – Salve, Sancta Parens",  # 3 Missa B. V. M. – Salve, Sancta Parens
    constants.TEMPORA_C_10PASC: "4 Misa de la B. V. M. – Salve, Sancta Parens",  # 4 Missa B. V. M. – Salve, Sancta Parens
    constants.COMMUNE_C_10PASC: "4 Misa de la B. V. M. – Salve, Sancta Parens",  # 4 Missa B. V. M. – Salve, Sancta Parens
    constants.TEMPORA_C_10T: "5 Misa de la B. V. M. – Salve, Sancta Parens",  # 5 Missa B. V. M. – Salve, Sancta Parens
    constants.COMMUNE_C_10T: "5 Misa de la B. V. M. – Salve, Sancta Parens",  # 5 Missa B. V. M. – Salve, Sancta Parens
    constants.COMMUNE_C5: "Común del Confesor no Pontífice; Os justi",  # Commune Confessoris non pontificis; Os justi
    constants.COMMUNE_C5B: "Común del Confesor no Pontífice; Iustus ut palma",  # Commune Confessoris non pontificis; Iustus ut palma
    constants.COMMUNE_C2C: "Común de un Mártir Pontífice, Statuit",  # Commune Unius Martyris Pontificis, Statuit
    constants.COMMUNE_C2B: "Común de un Mártir Pontífice, Sacerdotes Dei",  # Commune Unius Martyris Pontificis, Sacerdotes Dei
    constants.SANCTI_01_01: "Día de la Octava de Navidad del Señor",  # Die Octavæ Nativitatis Domini
    constants.SANCTI_01_06: "En la Epifanía del Señor",  # In Epiphania Domini
    constants.SANCTI_01_13: "En la Conmemoración del Bautismo de Nuestro Señor Jesucristo",  # In Commemoratione Baptismatis Domini Nostri Jesu Christi
    constants.SANCTI_01_14: "S. Hilario Obispo Confesor Doctor de la Iglesia",  # S. Hilarii Episcopi Confessoris Ecclesiæ Doctoris
    constants.SANCTI_01_15: "S. Pablo Primer Ermitaño y Confesor",  # S. Pauli Primi Eremitæ et Confessoris
    constants.SANCTI_01_16: "S. Marcelo Papa y Mártir",  # S. Marcelli Papæ et Martyris
    constants.SANCTI_01_17: "S. Antonio Abad",  # S. S. Antonii Abbatis
    constants.SANCTI_01_18: "S. Prisca Virgen",  # S. Priscæ Virginis
    constants.SANCTI_01_19: "S. Mario y Compañeros Mártires",  # S. Marii et Soc. Mart.
    constants.SANCTI_01_20: "Ss. Fabián y Sebastián Mártires",  # Ss. Fabiani et Sebastiani Martyrum
    constants.SANCTI_01_21: "S. Inés Virgen y Mártir",  # S. Agnetis Virginis et Martyris
    constants.SANCTI_01_22: "Ss. Vicente y Anastasio Mártires",  # Ss. Vincentii et Anastasii Martyrum
    constants.SANCTI_01_23: "S. Raimundo de Peñafort Confesor",  # S. Raymundi de Penafort Confessoris
    constants.SANCTI_01_24: "S. Timoteo Obispo y Mártir",  # S. Timothei Episcopi et Martyris
    constants.SANCTI_01_25: "En la Conversión de S. Pablo Apóstol",  # In Conversione S. Pauli Apostoli
    constants.SANCTI_01_26: "S. Policarpo Obispo y Mártir",  # S. Polycarpi Episcopi et Martyris
    constants.SANCTI_01_27: "S. Juan Crisóstomo Obispo Confesor Doctor de la Iglesia",  # S. Joannis Chrysostomi Episcopi Confessoris Ecclesiæ Doctoris
    constants.SANCTI_01_28: "S. Pedro Nolasco Confesor",  # S. Petri Nolasci Confessoris
    constants.SANCTI_01_29: "S. Francisco de Sales Obispo Confesor Doctor de la Iglesia",  # S. Francisci Salesii Episcopi Confessoris Ecclesiæ Doctoris
    constants.SANCTI_01_30: "S. Martina Virgen y Mártir",  # S. Martinæ Virginis et Martyris
    constants.SANCTI_01_31: "S. Juan Bosco Confesor",  # S. Joannis Bosco Confessoris
    constants.SANCTI_02_01: "S. Ignacio Obispo y Mártir",  # S. Ignatii Episcopi et Martyris
    constants.SANCTI_02_02: "En la Purificación de la Bienaventurada Virgen María",  # In Purificatione Beatæ Mariæ Virginis
    constants.SANCTI_02_03: "S. Blas Obispo",  # S. Blasii Episcopi
    constants.SANCTI_02_04: "S. Andrés Corsini Obispo y Confesor",  # S. Andreæ Corsini Episcopi et Confessoris
    constants.SANCTI_02_05: "S. Águeda Virgen y Mártir",  # S. Agathæ Virginis et Martyris
    constants.SANCTI_02_06: "S. Tito Obispo y Confesor",  # S. Titi Episc. et Confessoris
    constants.SANCTI_02_07: "S. Romualdo Abad",  # S. Romualdi Abbatis
    constants.SANCTI_02_08: "S. Juan de Mata Confesor",  # S. Joannis de Matha Confessoris
    constants.SANCTI_02_09: "S. Cirilo Obispo de Alejandría Confesor Doctor de la Iglesia",  # S. Cyrilli Episc. Alexandrini Confessoris Ecclesiæ Doctoris
    constants.SANCTI_02_10: "S. Escolástica Virgen",  # S. Scholasticæ Virginis
    constants.SANCTI_02_11: "En la Aparición de la Bienaventurada Virgen María",  # In Apparitione Beatæ Mariæ Virginis
    constants.SANCTI_02_12: "Ss. Siete Fundadores de la Orden de los Siervos de la B. V. M.",  # Ss. Septem Fundat. Ord. Servorum B. M. V.
    constants.SANCTI_02_14: "S. Valentín",  # S. Valentini
    constants.SANCTI_02_15: "SS. Faustino y Jovita",  # SS. Faustini et Jovitæ
    constants.SANCTI_02_18: "S. Simeón Faustino Obispo y Mártir",  # S. Simeonis Faustini Episcopi et Martyris
    constants.SANCTI_02_22: "En la Cátedra de S. Pedro Apóstol",  # In Cathedra S. Petri Ap.
    constants.SANCTI_02_23: "S. Pedro Damián",  # S. Petri Damiani
    constants.SANCTI_02_24: "S. Matías Apóstol",  # S. Matthiæ Apostoli
    constants.SANCTI_02_27: "S. Gabriel de la Virgen Dolorosa Confesor",  # S. Gabrielis a Virgine Perdolente Confessoris
    constants.SANCTI_03_04: "S. Casimiro Confesor",  # S. Casimiri Confessoris
    constants.SANCTI_03_06: "Ss. Perpetua y Felicidad Mártires",  # Ss. Perpetuæ et Felicitatis Martyrum
    constants.SANCTI_03_07: "S. Tomás de Aquino Confesor Doctor de la Iglesia",  # S. Thomæ de Aquino Confessoris Ecclesiæ Doctoris
    constants.SANCTI_03_08: "S. Juan de Dios Confesor",  # S. Joannis de Deo Confessoris
    constants.SANCTI_03_09: "S. Francisca Viuda Romana",  # S. Franciscæ Viduæ Romanæ
    constants.SANCTI_03_10: "Ss. Cuarenta Mártires",  # Ss. Quadraginta Martyrum
    constants.SANCTI_03_12: "S. Gregorio Papa Confesor Doctor de la Iglesia",  # S. Gregorii Papæ Confessoris et Ecclesiæ Doctoris
    constants.SANCTI_03_15PL: "S. Clemente Hofbauer",  # S. Clementis Hofbauer
    constants.SANCTI_03_17: "S. Patricio Obispo y Confesor",  # S. Patricii Episcopi et Conf.
    constants.SANCTI_03_18: "S. Cirilo Obispo de Jerusalén Doctor de la Iglesia",  # S. Cyrilli Episcopi Hierosolymitani Ecclesiæ Doctoris
    constants.SANCTI_03_19: "S. José Esposo de la B. M. V. Confesor",  # S. Joseph Sponsi B.M.V. Confessoris
    constants.SANCTI_03_21: "S. Benito Abad",  # S. Benedicti Abbatis
    constants.SANCTI_03_24: "S. Gabriel Arcángel",  # S. Gabrielis Archangeli
    constants.SANCTI_03_25: "En la Anunciación de la Bienaventurada Virgen María",  # In Annuntiatione Beate Mariæ Virgine
    constants.SANCTI_03_27: "S. Juan Damasceno Confesor",  # S. Joannis Damasceni Confessoris
    constants.SANCTI_03_28: "S. Juan de Capistrano Confesor",  # S. Joannis a Capistrano Confessoris
    constants.SANCTI_04_02: "S. Francisco de Paula Confesor",  # S. Francisci de Paula Confessoris
    constants.SANCTI_04_04: "S. Isidoro Obispo Confesor Doctor de la Iglesia",  # S. Isidori Episc. Confessoris et Ecclesiæ Doctoris
    constants.SANCTI_04_05: "S. Vicente Ferrer Confesor",  # S. Vincentii Ferrerii Confessoris
    constants.SANCTI_04_11: "S. León I Papa Confesor Doctor de la Iglesia",  # S. Leonis I. Papæ Confessoris et Ecclesiæ Doctoris
    constants.SANCTI_04_13: "S. Hermenegildo Mártir",  # S. Hermenegildi Martyris
    constants.SANCTI_04_14: "S. Justino Mártir",  # S. Justini Martyris
    constants.SANCTI_04_17: "S. Aniceto Papa y Mártir",  # S. Aniceti Papæ et Martyris
    constants.SANCTI_04_21: "S. Anselmo Obispo Confesor Doctor de la Iglesia",  # S. Anselmi Episcopi Confessoris et Ecclesiæ Doctoris
    constants.SANCTI_04_22: "SS. Sotero y Cayo Sumos Pontífices y Mártires",  # SS. Soteris et Caji Summorum Pontificum et Martyrum
    constants.SANCTI_04_23: "S. Jorge Mártir",  # S. Georgii Martyris
    constants.SANCTI_04_23PL: "S. Adalberto, Obispo y Mártir",  # S. Adalberti, Episcopi et Martyris
    constants.SANCTI_04_24: "S. Fidel de Sigmaringa Mártir",  # S. Fidelis de Sigmaringa Martyris
    constants.SANCTI_04_25: "S. Marcos Evangelista",  # S. Marci Evangelistæ
    constants.SANCTI_04_26: "SS. Cleto y Marcelino Sumos Pontífices y Mártires",  # SS. Cleti et Marcellini Summorum Pontificum et Martyrum
    constants.SANCTI_04_27: "S. Pedro Canisio Confesor Doctor de la Iglesia",  # S. Petri Canisii Confessoris et Ecclesiæ Doctoris
    constants.SANCTI_04_28: "S. Pablo de la Cruz Confesor",  # S. Pauli a Cruce Confessoris
    constants.SANCTI_04_29: "S. Pedro Mártir",  # S. Petri Martyris
    constants.SANCTI_04_30: "S. Catalina de Siena Virgen",  # S. Catharina Senensis Virgine
    constants.SANCTI_05_01: "S. José Obrero",  # S. Joseph Opificis
    constants.SANCTI_05_02: "S. Atanasio Confesor Doctor de la Iglesia",  # S. Athanasii Confessoris Ecclesiæ Doctoris
    constants.SANCTI_05_03: "Ss. Alejandro y Compañeros Mártires",  # Ss. Alexandri et Sociorum Martyrum
    constants.SANCTI_05_03PL: "Beata Virgen María Reina de Polonia",  # Beatæ Mariæ Virginis Reginæ Poloniæ
    constants.SANCTI_05_04: "S. Mónica Viuda",  # S. Monicæ Viduæ
    constants.SANCTI_05_04PL: "S. Floriano Mártir",  # S. Floriani Martyris
    constants.SANCTI_05_05: "S. Pío V Papa Confesor",  # S. Pii V Papæ Confessoris
    constants.SANCTI_05_07: "S. Estanislao Obispo y Mártir",  # S. Stanislai Episcopi et Martyris
    constants.SANCTI_05_08PL: "S. Estanislao Obispo y Mártir",  # S. Stanislai Episcopi et Martyris
    constants.SANCTI_05_09: "S. Gregorio Nacianceno Obispo Confesor Doctor de la Iglesia",  # S. Gregorii Nazianzeni Episcopi Confessoris Ecclesiæ Doctoris
    constants.SANCTI_05_10: "S. Antonio Obispo Confesor",  # S. Antonii Episcopi Confessoris
    constants.SANCTI_05_11: "Ss. Felipe y Santiago Apóstoles",  # Ss. Philippi et Jacobi Apostolorum
    constants.SANCTI_05_12: "Ss. Nereo, Aquiles y Domitila Virgen y Pancracio Mártir",  # Ss. Nerei, Achillei et Domitillæ Virginis atque Pancratii Martyrum
    constants.SANCTI_05_13: "S. Roberto Belarmino Obispo Confesor Doctor de la Iglesia",  # S. Roberti Bellarmino Episcopi Confessoris et Ecclesiæ Doctoris
    constants.SANCTI_05_14: "S. Bonifacio Mártir",  # S. Bonifacii Martyris
    constants.SANCTI_05_15: "S. Juan Bautista de la Salle Confesor",  # S. Johanni Baptistæ de la Salle Confessoris
    constants.SANCTI_05_16: "S. Ubaldino Obispo Confesor",  # S. Ubaldi Episcopi Confessoris
    constants.SANCTI_05_16PL: "S. Andrés Bobola Mártir",  # S. Andreæ Bobolæ Martyrum
    constants.SANCTI_05_17: "S. Pascual Baylón Confesor",  # S. Paschalis Baylon Confessoris
    constants.SANCTI_05_18: "S. Venancio Mártir",  # S. Venantii Martyris
    constants.SANCTI_05_19: "S. Pedro Celestino Papa Confesor",  # S. Petri Celestini Papæ Confessoris
    constants.SANCTI_05_20: "S. Bernardino de Siena Confesor",  # S. Bernardini Senensis Confessoris
    constants.SANCTI_05_24PL: "Beata Virgen María Confesora Auxiliadora",  # Beatæ Mariæ Virginis Confessoris Auxiliatrix
    constants.SANCTI_05_25: "S. Gregorio VII Papa Confesor",  # S. Gregorii VII Papæ Confessoris
    constants.SANCTI_05_26: "S. Felipe Neri Confesor",  # S. Philippi Neri Confessoris
    constants.SANCTI_05_27: "S. Beda el Venerable Confesor Doctor de la Iglesia",  # S. Bedæ Venerabilis Confessoris et Ecclesiæ Doctoris
    constants.SANCTI_05_28: "S. Agustín Obispo Confesor",  # S. Augustini Episcopi Confessoris
    constants.SANCTI_05_29: "S. María Magdalena de Pazzi Virgen",  # S. Mariæ Magdalenæ de Pazzis Virginis
    constants.SANCTI_05_30: "S. Félix Papa y Mártir",  # S. Felicis Papæ et Martyris
    constants.SANCTI_05_31: "Beata Virgen María Reina",  # Beatæ Mariæ Virginis Reginæ
    constants.SANCTI_06_01: "S. Ángela de Mérici Virgen",  # S. Angelæ Mericiæ Virginis
    constants.SANCTI_06_02: "Ss. Marcelino, Pedro y Erasmo Mártires",  # Ss. Marcellini, Petri, atque Erasmi Martyrum
    constants.SANCTI_06_04: "S. Francisco Caracciolo Confesor",  # S. Francisci Caracciolo Confessoris
    constants.SANCTI_06_05: "S. Bonifacio Obispo y Mártir",  # S. Bonifatii Episc. et Mart.
    constants.SANCTI_06_06: "S. Norberto Obispo y Confesor",  # S. Norberti Episc. et Confessoris
    constants.SANCTI_06_09: "Ss. Primo y Feliciano Mártires",  # Ss. Primi et Feliciani Martyrum
    constants.SANCTI_06_10: "S. Margarita Reina viuda",  # S. Margaritæ Reginæ viduæ
    constants.SANCTI_06_10PL: "B. Bogumil Obispo y Confesor",  # B. Bogumilai Episcopi et Confessoris
    constants.SANCTI_06_11: "S. Bernabé Apóstol",  # S. Barnabæ Apostoli
    constants.SANCTI_06_12: "S. Juan de San Facundo Confesor",  # S. Joannis a S. Facundo Confessoris
    constants.SANCTI_06_13: "S. Antonio de Padua Confesor",  # S. Antonii de Padua Confessoris
    constants.SANCTI_06_14: "S. Basilio Magno Confesor Doctor de la Iglesia",  # S. Basilii Magni Confessoris et Ecclesiæ Doctoris
    constants.SANCTI_06_15: "Ss. Vito, Modesto y Crescencia Mártires",  # Ss. Viti, Modesti atque Crescentiæ Martyrum
    constants.SANCTI_06_15PL: "B. Yolanda Viuda",  # b. Jolantae Viduae
    constants.SANCTI_06_17: "S. Gregorio Barbarigo Obispo Confesor",  # S. Gregorii Barbadici Episcopi Confessoris
    constants.SANCTI_06_18: "S. Efrén el Sirio Confesor Doctor de la Iglesia",  # S. Ephræm Syri Confessoris et Ecclesiæ Doctorem
    constants.SANCTI_06_19: "S. Juliana de Falconieri Virgen",  # S. Julianæ de Falconeriis Virginis
    constants.SANCTI_06_20: "S. Silverio Papa y Mártir",  # S. Silverii Papæ et Martyri
    constants.SANCTI_06_21: "S. Luis Gonzaga Confesor",  # S. Aloisii Gonzagæ Confessoris
    constants.SANCTI_06_22: "S. Paulino Obispo y Confesor",  # S. Paulini Episcopi et Confessoris
    constants.SANCTI_06_23: "En la Vigilia de S. Juan Bautista",  # In Vigilia S. Joannis Baptistæ
    constants.SANCTI_06_24: "En el Nacimiento de S. Juan Bautista",  # In Nativitate S. Joannis Baptistæ
    constants.SANCTI_06_25: "S. Guillermo Abad",  # S. Gulielmi Abbatis
    constants.SANCTI_06_26: "Ss. Juan y Pablo Mártires",  # Ss. Joannis et Pauli Martyrum
    constants.SANCTI_06_28: "En la Vigilia de los Ss. Pedro y Pablo Apóstoles",  # In Vigilia Ss. Petri et Pauli Apostolorum
    constants.SANCTI_06_29: "Ss. Apóstoles Pedro y Pablo",  # SS. Apostolorum Petri et Pauli
    constants.SANCTI_06_30: "En la Conmemoración de San Pablo Apóstol",  # In Commemoratione Sancti Pauli Apostoli
    constants.SANCTI_07_01: "Preciosísima Sangre de Nuestro Señor Jesucristo",  # Pretiosissimi Sanguinis Domini Nostri Jesu Christi
    constants.SANCTI_07_02: "En la Visitación de la Bienaventurada Virgen María",  # In Visitatione B. Mariæ Virginis
    constants.SANCTI_07_03: "S. Ireneo Obispo y Mártir",  # S. Irenæi Episcopi et Martyris
    constants.SANCTI_07_05: "S. Antonio María Zacarías Confesor",  # S. Antonii Mariæ Zaccaria Confessoris
    constants.SANCTI_07_07: "Ss. Cirilo y Metodio Pontífices y Confesores",  # Ss. Cyrilli et Methodii Pont. et Conf.
    constants.SANCTI_07_08: "S. Isabel Reina de Portugal Viuda",  # S. Elisabeth Reg. Portugaliæ Viduæ
    constants.SANCTI_07_10: "Ss. Siete Hermanos Mártires, y Rufina y Segunda Vírgenes y Mártires",  # Ss. Septem Fratrum Martyrum, ac Rufinæ et Secundæ Virginum et Martyrum
    constants.SANCTI_07_11: "S. Pío I Papa y Mártir",  # S. Pii I Papæ et Martyris
    constants.SANCTI_07_12: "S. Juan Gualberto Abad",  # S. Joannis Gualberti Abbatis
    constants.SANCTI_07_13PL: "Ss. Andrés y Benito",  # Śś. Andreæ et Benedicti
    constants.SANCTI_07_14: "S. Buenaventura Obispo Confesor Doctor de la Iglesia",  # S. Bonaventuræ Episcopi Confessoris et Ecclesiæ Doctoris
    constants.SANCTI_07_15: "S. Enrique Emperador Confesor",  # S. Henrici Imperatoris Confessoris
    constants.SANCTI_07_15PL: "S. Bruno Obispo y Mártir",  # S. Brunonis Episcopi et Martyris
    constants.SANCTI_07_16: "En la Conmemoración de la Bienaventurada Virgen María del Monte Carmelo",  # In Commemoratione Beatæ Mariæ Virgine de Monte Carmelo.
    constants.SANCTI_07_17: "S. Alejo Confesor",  # S. Alexii Confessoris
    constants.SANCTI_07_18: "S. Camilo de Lelis Confesor",  # S. Camilli de Lellis Confessoris
    constants.SANCTI_07_18PL: "B. Simón Confesor",  # B. Simonis Confessoris
    constants.SANCTI_07_19: "S. Vicente de Paúl Confesor",  # S. Vincentii a Paulo Confessoris
    constants.SANCTI_07_20: "S. Jerónimo Emiliani Confesor",  # S. Hieronymi Emiliani Confessoris
    constants.SANCTI_07_20PL: "B. Ceslao Confesor",  # B. Ceslai Confessoris
    constants.SANCTI_07_21: "S. Lorenzo de Brindis Confesor",  # S. Laurentii a Brundusio Confessoris
    constants.SANCTI_07_22: "S. María Magdalena Penitente",  # S. Mariæ Magdalenæ Poenitentis
    constants.SANCTI_07_23: "S. Apolinar Obispo y Mártir",  # S. Apollinaris Episcopi et Martyris
    constants.SANCTI_07_24: "S. Cristina Virgen y Mártir",  # S. Christinæ Virginis et Martyris
    constants.SANCTI_07_24PL: "S. Kinga Virgen",  # S. Kingæ Virginis
    constants.SANCTI_07_25: "S. Santiago Apóstol",  # S. Jacobi Apostoli
    constants.SANCTI_07_26: "S. Ana Madre de la B. V. M.",  # S. Annæ Matris B.M.V.
    constants.SANCTI_07_27: "S. Pantaleón Mártir",  # S. Pantaleonis Martyris
    constants.SANCTI_07_28: "Ss. Nazario y Celso Mártires, Víctor I Papa y Mártir e Inocencio I Papa y Confesor",  # Ss. Nazarii et Celsi Martyrum, Victoris I Papæ et Martyris ac Innocentii I Papæ et Confessoris
    constants.SANCTI_07_29: "S. Marta Virgen",  # S. Marthæ Virginis
    constants.SANCTI_07_30: "S. Abdón y Senén Mártires",  # S. Abdon et Sennen Martyrum
    constants.SANCTI_07_31: "S. Ignacio Confesor",  # S. Ignatii Confessoris
    constants.SANCTI_08_01: "Ss. Mártires Macabeos",  # Ss. Martyrum Machabæorum
    constants.SANCTI_08_02: "S. Alfonso María de Ligorio Obispo Confesor Doctor de la Iglesia",  # S. Alfonsi Mariæ de Ligorio Episcopi Confessoris et Ecclesiæ Doctoris
    constants.SANCTI_08_04: "S. Domingo Confesor",  # S. Dominici Confessoris
    constants.SANCTI_08_05: "S. María de las Nieves",  # S. Mariæ ad Nives
    constants.SANCTI_08_06: "En la Transfiguración de Nuestro Señor Jesucristo",  # In Transfiguratione Domini Nostri Jesu Christi
    constants.SANCTI_08_07: "S. Cayetano Confesor",  # S. Cajetani Confessoris
    constants.SANCTI_08_08: "S. Juan María Vianney Confesor",  # S. Joannis Mariæ Vianney Confessoris
    constants.SANCTI_08_09: "Vigilia de S. Lorenzo Mártir",  # Vigilia S. Laurentii Martyris
    constants.SANCTI_08_10: "S. Lorenzo Mártir",  # S. Laurentii Martyris
    constants.SANCTI_08_11: "Ss. Tiburcio y Susana Vírgenes y Mártires",  # Ss. Tiburtii et Susannæ Virginum et Martyrum
    constants.SANCTI_08_12: "S. Clara Virgen",  # S. Claræ Virginis
    constants.SANCTI_08_13: "Ss. Hipólito y Casiano Mártires",  # Ss. Hippolyti et Cassiani Martyrum
    constants.SANCTI_08_14: "Vigilia de la Asunción de la B. V. M.",  # Vigilia Assumptionis B.M.V.
    constants.SANCTI_08_15: "En la Asunción de la Bienaventurada Virgen María",  # In Assumptione Beatæ Mariæ Virginis
    constants.SANCTI_08_16: "S. Joaquín Confesor, Padre de la B. Virgen María",  # S. Joachim Confessoris, Patris B. Mariæ Virginis
    constants.SANCTI_08_17: "S. Jacinto Confesor",  # S. Hyacinthi Confessoris
    constants.SANCTI_08_18: "S. Agapito Mártir",  # S. Agapiti Martyris
    constants.SANCTI_08_19: "S. Juan Eudes Confesor",  # S. Joannis Eudes Confessoris
    constants.SANCTI_08_20: "S. Bernardo Abad Doctor de la Iglesia",  # S. Bernardi Abbatis et Ecclesiæ Doctoris
    constants.SANCTI_08_21: "S. Juana Francisca Frémiot de Chantal Viuda",  # S. Joannæ Franciscæ Frémiot de Chantal Viduæ
    constants.SANCTI_08_22: "Inmaculado Corazón de la Bienaventurada Virgen María",  # Immaculati Cordis Beatæ Mariæ Virginis
    constants.SANCTI_08_23: "S. Felipe Benicio Confesor",  # S. Philippi Benitii Confessoris
    constants.SANCTI_08_24: "S. Bartolomé Apóstol",  # S. Bartholomæi Apostoli
    constants.SANCTI_08_25: "S. Luis Confesor",  # S. Ludovici Confessoris
    constants.SANCTI_08_26: "S. Ceferino Papa y Mártir",  # S. Zephirini Papæ et Martyris
    constants.SANCTI_08_26PL: "Beata Virgen María de Claro Monte de Czestochova",  # Beate Mariae Virginis Claromontane Czestochoviensis
    constants.SANCTI_08_27: "S. José de Calasanz Confesor",  # S. Josephi Calasanctii Confessoris
    constants.SANCTI_08_28: "S. Agustín Obispo Confesor Doctor de la Iglesia",  # S. Augustini Episcopi et Confessoris et Ecclesiæ Doctoris
    constants.SANCTI_08_29: "Degollación de S. Juan Bautista",  # Decollatione S. Joannis Baptistæ
    constants.SANCTI_08_30: "S. Rosa de Lima Virgen",  # S. Rosæ a Sancta Maria Limange Virginis
    constants.SANCTI_08_31: "S. Ramón Nonato Confesor",  # S. Raymundi Nonnati Confessoris
    constants.SANCTI_09_01: "S. Gil Abad",  # S. Ægidii Abbatis
    constants.SANCTI_09_01PL: "B. Bronislawa Virgen",  # B. Bronislauæ Virginins
    constants.SANCTI_09_02: "S. Esteban de Hungría Rey Confesor",  # S. Stephani Hungariæ Regis Confessoris
    constants.SANCTI_09_03: "S. Pío X Papa Confesor",  # S. Pii X Papæ Confessoris
    constants.SANCTI_09_05: "S. Lorenzo Justiniano Obispo y Confesor",  # S. Laurentii Justiniani Episcopi et Confessoris
    constants.SANCTI_09_07PL: "B. Melchior Mártir",  # B. Melchiori Martyrum
    constants.SANCTI_09_08: "Natividad de la Bienaventurada Virgen María",  # Nativitate Beatæ Mariæ Virginis
    constants.SANCTI_09_09: "S. Gorgonio Mártir",  # S. Gorgonii Martyris
    constants.SANCTI_09_10: "S. Nicolás de Tolentino Confesor",  # S. Nicolai de Tolentino Confessoris
    constants.SANCTI_09_11: "Ss. Proto e Jacinto Mártires",  # Ss. Proti et Hyacinthi Martyrum
    constants.SANCTI_09_12: "Santísimo Nombre de la Bienaventurada Virgen María",  # S. Nominis Beatæ Mariæ Virginis
    constants.SANCTI_09_14: "En la Exaltación de la Santa Cruz",  # In Exaltatione Sanctæ crucis
    constants.SANCTI_09_15: "Siete Dolores de la Bienaventurada Virgen María",  # Septem Dolorum Beatæ Mariæ Virginis
    constants.SANCTI_09_16: "Ss. Cornelio Papa y Cipriano Obispo, Mártires",  # Ss. Cornelii Papæ et Cypriani Episcopi, Martyrum
    constants.SANCTI_09_17: "Impresión de los Estigmas de S. Francisco",  # Impressionis Stigmatum S. Francisci
    constants.SANCTI_09_18: "S. José de Cupertino Confesor",  # S. Josephi de Cupertino Confessoris
    constants.SANCTI_09_19: "S. Jenaro Obispo y Compañeros Mártires",  # S. Januarii Episcopi et Sociorum Martyrum
    constants.SANCTI_09_20: "S. Eustaquio y Compañeros Mártires",  # S. Eustachii et Sociorum Martyrum
    constants.SANCTI_09_21: "S. Mateo Apóstol y Evangelista",  # S. Matthæi Apostoli et Evangelistæ
    constants.SANCTI_09_22: "S. Tomás de Villanueva Obispo y Confesor",  # S. Thomæ de Villanove Episcopi et Confessoris
    constants.SANCTI_09_23: "S. Lino Papa y Mártir",  # S. Lini Papæ et Martyris
    constants.SANCTI_09_24: "Beata Virgen María de la Merced",  # Beatæ Mariæ Virginis de Mercede
    constants.SANCTI_09_25PL: "B. Ladislao Confesor",  # B. Ladislai Confessoris
    constants.SANCTI_09_26: "Ss. Cipriano y Justina Mártires",  # Ss. Cypriani et Justinæ Martyrum
    constants.SANCTI_09_27: "Ss. Cosme y Damián Mártires",  # S. Cosmæ et Damiani Martyrum
    constants.SANCTI_09_28: "S. Wenceslao Duque y Mártir",  # S. Wenceslai Ducis et Martyris
    constants.SANCTI_09_29: "En la Dedicación de S. Miguel Arcángel",  # In Dedicatione S. Michælis Archangelis
    constants.SANCTI_09_30: "S. Jerónimo Presbítero Confesor Doctor de la Iglesia",  # S. Hieronymi Presbyteris Confessoris et Ecclesiæ Doctoris
    constants.SANCTI_10_01: "S. Remigio Obispo Confesor",  # S. Remigii Episcopi Confessoris
    constants.SANCTI_10_01PL: "B. Juan de Dukla",  # B. Joannis de Dukla
    constants.SANCTI_10_02: "Ss. Ángeles Custodios",  # Ss. Angelorum Custodum
    constants.SANCTI_10_03: "S. Teresa del Niño Jesús Virgen",  # S. Theresiæ a Jesu Infante Virginis
    constants.SANCTI_10_04: "S. Francisco Confesor",  # S. Francisci Confessoris
    constants.SANCTI_10_05: "Ss. Plácido y Compañeros Mártires",  # Ss. Placidi et Sociorum Martyrum
    constants.SANCTI_10_06: "S. Bruno Confesor",  # S. Brunonis Confessoris
    constants.SANCTI_10_07: "Fiesta de la Bienaventurada Virgen María del Rosario",  # Festum Beatæ Mariæ Virginis a Rosario
    constants.SANCTI_10_08: "S. Brígida Viuda",  # S. Birgittæ Viduæ
    constants.SANCTI_10_09: "S. Juan Leonardi Confesor",  # S. Joannis Leonardi Confessoris
    constants.SANCTI_10_09PL: "B. Vicente Obispo y Confesor",  # b. Vincenti Episcopi et Confessoris
    constants.SANCTI_10_10: "S. Francisco de Borja Confesor",  # S. Francisci Borgiæ Confessoris
    constants.SANCTI_10_10PL: "Victoria de Chocim",  # Victoriae Chocimensis
    constants.SANCTI_10_11: "Maternidad de la Bienaventurada Virgen María",  # Maternitatis Beatæ Mariæ Virginis
    constants.SANCTI_10_13: "S. Eduardo Rey Confesor",  # S. Eduardi Regis Confessoris
    constants.SANCTI_10_14: "S. Calixto Papa y Mártir",  # S. Callisti Papæ et Martyris
    constants.SANCTI_10_15: "S. Teresa Virgen",  # S. Teresiæ Virginis
    constants.SANCTI_10_16: "S. Eduvigis Viuda",  # S. Hedwigis Viduæ
    constants.SANCTI_10_17: "S. Margarita María Alacoque Virgen",  # S. Margaritæ Mariæ Alaquoque Virginis
    constants.SANCTI_10_18: "S. Lucas Evangelista",  # S. Lucæ Evangelistæ
    constants.SANCTI_10_19: "S. Pedro de Alcántara Confesor",  # S. Petri de Alcantara Confessoris
    constants.SANCTI_10_20: "S. Juan Cancio Confesor",  # S. Joannis Cantii Confessoris
    constants.SANCTI_10_21: "S. Hilarión Abad",  # S. Hilarionis Abbatis
    constants.SANCTI_10_21PL: "B. Jacobo Obispo y Confesor",  # B. Jacobi Episcopi et Confessoris
    constants.SANCTI_10_23: "S. Antonio María Claret Obispo Confesor",  # S. Antonii Mariæ Claret Episcopi Confessoris
    constants.SANCTI_10_24: "S. Rafael Arcángel",  # S. Raphælis Archangeli
    constants.SANCTI_10_25: "Ss. Crisanto y Daría Mártires",  # Ss. Chrysanthi et Dariæ Martyrum
    constants.SANCTI_10_28: "Ss. Simón y Judas Apóstoles",  # Ss. Simonis et Judæ Apostolorum.
    constants.SANCTI_11_01: "Todos los Santos",  # Omnium Sanctorum
    constants.SANCTI_11_02_1: "En la Conmemoración de Todos los Fieles Difuntos en la primera Misa",  # In Commemoratione Omnium Fidelium Defunctorum Ad primam Missam
    constants.SANCTI_11_02_2: "En la Conmemoración de Todos los Fieles Difuntos en la segunda Misa",  # In Commemoratione Omnium Fidelium Defunctorum Ad secundam Missam
    constants.SANCTI_11_02_3: "En la Conmemoración de Todos los Fieles Difuntos en la tercera Misa",  # In Commemoratione Omnium Fidelium Defunctorum Ad tertiam Missam
    constants.SANCTI_11_04: "S. Carlos Obispo y Confesor",  # S. Caroli Episcopi et Confessoris
    constants.SANCTI_11_08: "Ss. Cuatro Coronados Mártires",  # Ss. Quatuor Coronatorum Martyrum
    constants.SANCTI_11_09: "En la Dedicación de la Basílica de los Ss. Salvadores",  # In Dedicatione Basilicæ Ss. Salvatoris
    constants.SANCTI_11_10: "S. Andrés Avelino Confesor",  # S. Andreæ Avellini Confessoris
    constants.SANCTI_11_11: "S. Martín Obispo y Confesor",  # S. Martini Episcopi et Confessoris
    constants.SANCTI_11_12: "S. Martín Papa y Mártir",  # S. Martini Papæ et Martyris
    constants.SANCTI_11_12PL: "Ss. Protomártires de Polonia",  # Ss. Protomartyrum Poloniae
    constants.SANCTI_11_13: "S. Diego Confesor",  # S. Didaci Confessoris
    constants.SANCTI_11_13PL: "S. Estanislao Confesor",  # S. Stanislai Confessoris
    constants.SANCTI_11_14: "S. Josafat Obispo y Mártir",  # S. Josaphat Episcopi et Martyris
    constants.SANCTI_11_15: "S. Alberto Magno Obispo Confesor Doctor de la Iglesia",  # S. Alberti Magni Episcopi Confessoris et Ecclesiæ Doctoris
    constants.SANCTI_11_16: "S. Gertrudis Virgen",  # S. Gertrudis Virginis
    constants.SANCTI_11_17: "S. Gregorio Taumaturgo Obispo y Confesor",  # S. Gregorii Thaumaturgi Episcopi et Confessoris
    constants.SANCTI_11_17PL: "B. Salomea Virgen",  # B. Salomea Virginis
    constants.SANCTI_11_18: "En la Dedicación de las Basílicas de los Ss. Apóstoles Pedro y Pablo",  # In Dedicatione Basilicarum Ss. Apostolorum Petri et Pauli
    constants.SANCTI_11_19: "S. Isabel Viuda",  # S. Elisabeth Viduæ
    constants.SANCTI_11_20: "S. Félix de Valois Confesor",  # S. Felicis de Valois Confessoris
    constants.SANCTI_11_20PL: "S. Martín Papa y Mártir (en Polonia, movido del 12.11 con el 1964)",  # S. Martini Papæ et Martyris
    constants.SANCTI_11_21: "En la Presentación de la Bienaventurada Virgen María",  # In Presentatione Beatæ Mariæ Virginis
    constants.SANCTI_11_22: "S. Cecilia Virgen y Mártir",  # S. Cæciliæ Virginis et Martyris
    constants.SANCTI_11_23: "S. Clemente Papa y Mártir",  # S. Clementis Papæ et Martyris
    constants.SANCTI_11_24: "S. Juan de la Cruz Confesor Doctor de la Iglesia",  # S. Joannis a Cruce Confessoris et Ecclesiæ Doctoris
    constants.SANCTI_11_25: "S. Catalina Virgen y Mártir",  # S. Catharinæ Virginis et Martyris
    constants.SANCTI_11_26: "S. Silvestre Abad y Confesor",  # S. Silvesteri Abbatis et Confessoris
    constants.SANCTI_11_29: "S. Saturnino Mártir",  # S. Saturnini Martyris
    constants.SANCTI_11_30: "S. Andrés Apóstol",  # S. Andreæ Apostoli
    constants.SANCTI_12_02: "S. Bibiana Virgen y Mártir",  # S. Bibianæ Virginis et Martyris
    constants.SANCTI_12_02PL: "S. Pedro Crisólogo Obispo Confesor Doctor de la Iglesia",  # S. Petri Chrysologi Episcopi Confessoris et Ecclesiæ Doctoris
    constants.SANCTI_12_03: "S. Francisco Javier Confesor",  # S. Francisci Xaverii Confessoris
    constants.SANCTI_12_04: "S. Pedro Crisólogo Obispo Confesor Doctor de la Iglesia",  # S. Petri Chrysologi Episcopi Confessoris et Ecclesiæ Doctoris
    constants.SANCTI_12_04PL: "S. Bárbara Virgen y Mártir",  # S. Barbaræ Virginis et Martyris
    constants.SANCTI_12_05: "S. Sabas Abad",  # S. Sabbæ Abbatis
    constants.SANCTI_12_06: "S. Nicolás Obispo y Confesor",  # S. Nicolai Episcopi et Confessoris
    constants.SANCTI_12_07: "S. Ambrosio Obispo Confesor Doctor de la Iglesia",  # S. Ambrosii Episcopi Confessoris et Ecclesiæ Doctoris
    constants.SANCTI_12_08: "En la Concepción Inmaculada de la Bienaventurada Virgen María",  # In Conceptione Immaculata Beatæ Mariæ Virginis
    constants.SANCTI_12_10: "S. Melquiades Papa y Mártir",  # S. Melchiadis Papæ et Mart
    constants.SANCTI_12_11: "S. Dámaso Papa y Confesor",  # S. Damasi Papæ et Confessoris
    constants.SANCTI_12_13: "S. Lucía Virgen y Mártir",  # S. Luciæ Virginis et Martyris
    constants.SANCTI_12_16: "S. Eusebio Obispo y Mártir",  # S. Eusebii Episcopi et Martyris
    constants.SANCTI_12_21: "S. Tomás Apóstol",  # S. Thomæ Apostoli
    constants.SANCTI_12_24: "En la Vigilia de la Navidad del Señor",  # In Vigilia Nativitatis Domini
    constants.SANCTI_12_25_1: "En la Navidad del Señor en la noche",  # In Nativitate Domini in nocte
    constants.SANCTI_12_25_2: "En la Navidad del Señor en la aurora",  # In Nativitatis Domini in aurora
    constants.SANCTI_12_25_3: "En el día de la Navidad del Señor",  # In die Nativitatis Domini
    constants.SANCTI_12_26: "S. Esteban Protomártir",  # S. Stephani Protomartyris
    constants.SANCTI_12_27: "S. Juan Apóstol y Evangelista",  # S. Joannis Apostoli et Evangelistæ
    constants.SANCTI_12_28: "Ss. Inocentes",  # Ss. Innocentium
    constants.SANCTI_12_29: "S. Tomás Mártir",  # S. Thomæ M.
    constants.SANCTI_12_31: "S. Silvestre",  # S. Silvestri
    constants.VOTIVE_ANGELS: "Misa de los Ángeles",  # Missa de Angelis
    constants.VOTIVE_JOSEPH: "Misa de S. José",  # Missa de S. Ioseph
    constants.VOTIVE_PETERPAUL: "Misa de Ss. Pedro y Pablo Apóstoles",  # Missa de Ss. Petro et Paulo App.
    constants.VOTIVE_PETERPAULP: "Misa de Ss. Pedro y Pablo Apóstoles",  # Missa de Ss. Petro et Paulo App.
    constants.VOTIVE_APOSTLES: "Misa de todos los Ss. Apóstoles",  # Missa de omnibus Ss. Apostolis
    constants.VOTIVE_APOSTLESP: "Misa de todos los Ss. Apóstoles",  # Missa de omnibus Ss. Apostolis
    constants.VOTIVE_HOLYSPIRIT: "Misa del Espíritu Santo",  # Missa de Spiritu Sancto
    constants.VOTIVE_HOLYSPIRIT2: "Misa para pedir la gracia del Espíritu Santo",  # Missa ad postulandam gratiam Spiritus Sancti
    constants.VOTIVE_BLESSEDSACRAMENT: "Misa del Santísimo Sacramento de la Eucaristía",  # Missa de sanctissimo Eucharistiae Sacramento
    constants.VOTIVE_JESUSETERNALPRIEST: "Misa de Nuestro Señor Jesucristo sumo y eterno Sacerdote",  # Missa de D. N. Iesu Christo summo et aeterno Sacerdote
    constants.VOTIVE_CROSS: "Misa de la Santa Cruz",  # Missa de sancta Cruce
    constants.VOTIVE_PASSION: "Misa de la Pasión del Señor",  # Missa de Passione Domini
    constants.VOTIVE_PENT01_0: "Santísima Trinidad",  # Sanctissimæ Trinitatis
    constants.VOTIVE_PENT02_5: "Sacratísimo Corazón de Nuestro Señor Jesucristo",  # Sanctissimi Cordis Domini Nostri Jesu Christi
    constants.VOTIVE_08_22: "Inmaculado Corazón de la Bienaventurada Virgen María",  # Immaculati Cordis Beatæ Mariæ Virginis
    constants.VOTIVE_DEFUNCTORUM: "Misa de Difuntos Diaria",  # Missa Defunctorum Quotidianis
    constants.VOTIVE_MORTALITATIS: "Misa en Tiempo de Mortalidad",  # Missa Tempore Mortalitatis
    constants.VOTIVE_FIDEI_PROPAGATIONE: "Misa por la Propagación de la Fe",  # Missa pro Fidei Propagatione
    constants.VOTIVE_TERRIBILIS: "Misa del Común de la Dedicación de la Iglesia",  # Missa de Communi Dedicationis Ecclesiae.
}

VOTIVE_MASSES = [
    {
        "ref": "rorate",
        "id": constants.COMMUNE_C_10A,
        "title": TITLES[constants.COMMUNE_C_10A],
        "tags": ["Adviento"],
    },
    {
        "ref": "vultum-tuum",
        "id": constants.COMMUNE_C_10B,
        "title": TITLES[constants.COMMUNE_C_10B],
        "tags": ["Desde la Natividad hasta la Purificación"],
    },
    {
        "ref": "salve-sancta-parens-3",
        "id": constants.COMMUNE_C_10C,
        "title": TITLES[constants.COMMUNE_C_10C],
        "tags": ["Desde el 3 de Febrero hasta Miercoles Santo"],
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
