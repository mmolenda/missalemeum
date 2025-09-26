"""Example payloads for FastAPI documentation."""

CALENDAR_ITEMS_EXAMPLE = [
    {
        "id": "2023-11-11",
        "title": "St. Martin of Tours",
        "rank": 3,
        "tags": ["Saturday after XXIII Sunday after Pentecost"],
        "colors": ["w"],
        "commemorations": ["St. Menna"],
    }
]

PROPER_EXAMPLE = [
    {
        "info": {
            "colors": ["w"],
            "date": "2023-03-25",
            "description": "Commemoration Saturday after the IV Sunday of Lent.",
            "id": "sancti:03-25:1:w",
            "rank": 1,
            "supplements": [
                {
                    "label": "Commentary on the propers of the Mass from Sermonry",
                    "path": "https://sermonry.com/propers/annunciation-blessed-virgin-mary",
                }
            ],
            "tags": ["White vestments"],
            "tempora": "Saturday after the IV Sunday of Lent",
            "title": "Annunciation of the Blessed Virgin Mary",
            "commemorations": ["Saturday after the IV Sunday of Lent"],
        },
        "sections": [
            {
                "id": "Introitus",
                "label": "Introit",
                "body": [
                    [
                        "All the rich among the people seek Your face...",
                        "Vultum tuum deprecabúntur omnes dívites plebis...",
                    ]
                ],
            }
        ],
    }
]

ORDO_EXAMPLE = [
    {
        "info": {"title": "Order of Mass"},
        "sections": [
            {
                "id": None,
                "label": "Asperges",
                "body": [
                    [
                        "On Sundays, especially in Eastertide, the blessing of holy water and sprinkling with it may be carried out in memory of baptism.",
                    ],
                    [
                        "Thou shalt sprinkle me, O Lord, with hyssop...",
                        "Aspérges me, Dómine, hyssópo, et mundábor...",
                    ],
                ],
            }
        ],
    }
]

SUPPLEMENT_LIST_EXAMPLE = [
    {
        "id": "regina-caeli",
        "title": "Regina Caeli",
        "tags": ["Queen of Heaven", "Easter"],
    }
]

VOTIVE_LIST_EXAMPLE = [
    {
        "id": "salve-sancta-parens-3",
        "title": "III Mass of the B. V. M. – Salve, Sancta Parens",
        "tags": [
            "From Feb 3 until Holy Wednesday"
        ]
    }
]

SUPPLEMENT_CONTENT_EXAMPLE = [
    {
        "info": {
            "title": "Regina Caeli",
            "tags": ["Queen of Heaven", "Easter"],
        },
        "sections": [
            {
                "id": None,
                "label": None,
                "body": [
                    [
                        "QUEEN OF HEAVEN, rejoice, alleluia. ...",
                        "REGINA CAELI, laetare, alleluia...",
                    ]
                ],
            }
        ],
    }
]

ICALENDAR_EXAMPLE = (
    "BEGIN:VEVENT\n"
    "SUMMARY:Vigil of Christmas\n"
    "DTSTART;VALUE=DATE:20221224\n"
    "DTSTAMP;VALUE=DATE-TIME:20220307T140546Z\n"
    "UID:20221224@missalemeum.comDESCRIPTION:https://www.missalemeum.com/en/2022-12-24\n"
    "END:VEVENT"
)


def get_json_response(example):
    return {
        200: {
            "content": {
                "application/json": {
                    "example": example
                }
            }
        }
    }


def get_text_response(example: str, media_type: str = "text/plain"):
    return {
        200: {
            "content": {
                media_type: {
                    "schema": {
                        "type": "string",
                        "example": example
                    }
                }
            }
        }
    }
